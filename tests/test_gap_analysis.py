"""Moteur d'analyse d'écarts, testé sans aucun appel réseau."""
import json
from pathlib import Path
from types import SimpleNamespace

import pytest

from openmedreg.engines.claude import FALLBACK_BETA, ClaudeJudge
from openmedreg.engines.ollama import OllamaJudge
from openmedreg.engines.prompt import INSTRUCTIONS, OUTPUT_SCHEMA, build_user_message
from openmedreg.evaluation import load_case, score
from openmedreg.gap_analysis import analyse, load_units, requirements_in_scope, verify

CASE_DIR = Path(__file__).resolve().parents[1] / "eval" / "cases" / "fictif-therm-t1"


@pytest.fixture(scope="module")
def case():
    return load_case(CASE_DIR)


@pytest.fixture(scope="module")
def requirements():
    return requirements_in_scope(load_units(lang="fr"), "anx_II")


class OracleJudge:
    """Répond avec la vérité terrain : sert à vérifier la tuyauterie de bout en bout."""

    def __init__(self, case):
        self.case = case

    def judge(self, requirement, document):
        entry = self.case.truth[requirement["unit"]]
        return {
            "verdict": entry["expected"],
            "requirement_quote": requirement["text"][:40],
            "evidence": list(entry["evidence"]),
            "rationale": entry["rationale"],
        }


def test_scope_is_the_44_leaves_with_parent_context(requirements):
    assert len(requirements) == 44
    by_unit = {r["unit"]: r for r in requirements}
    stability = by_unit["anx_II/6.1/b/t5"]
    assert "stabilité" in stability["text"]
    # la phrase introductive du point b) accompagne le tiret
    assert any("protocoles d'essai" in part for part in stability["context"])
    assert stability["context"][0].startswith("ANNEXE II")


def test_end_to_end_with_oracle_judge(case, requirements):
    predictions = analyse(case.document, requirements, OracleJudge(case))
    result = score(case, predictions)
    assert result["accuracy"] == 1.0
    assert result["verdicts_downgraded_for_citation"] == 0


def test_invented_document_quote_is_rejected(requirements):
    requirement = requirements[0]
    out = verify(
        requirement,
        "Le dispositif est un capteur.",
        {
            "verdict": "conforme",
            "requirement_quote": requirement["text"][:30],
            "evidence": ["Le dispositif est un thermomètre."],
            "rationale": "x",
        },
    )
    assert out["verdict"] == "non_trouve"
    assert out["model_verdict"] == "conforme"
    assert out["rejected_evidence"] == ["Le dispositif est un thermomètre."]
    assert out["evidence"] == []


def test_invented_requirement_quote_is_rejected(requirements):
    out = verify(
        requirements[0],
        "Le dispositif est un capteur.",
        {
            "verdict": "conforme",
            "requirement_quote": "phrase absente du règlement",
            "evidence": ["Le dispositif est un capteur."],
            "rationale": "x",
        },
    )
    assert out["verdict"] == "non_trouve"
    assert out["requirement_quote"] is None


def test_verdict_without_evidence_is_rejected(requirements):
    out = verify(
        requirements[0],
        "texte",
        {"verdict": "non_applicable", "requirement_quote": requirements[0]["text"][:30],
         "evidence": [], "rationale": "x"},
    )
    assert out["verdict"] == "non_trouve"


def test_unknown_verdict_becomes_not_found(requirements):
    out = verify(requirements[0], "texte", {"verdict": "peut-être"})
    assert out["verdict"] == "non_trouve"


def test_judge_failure_does_not_stop_the_run(requirements):
    class Failing:
        def judge(self, requirement, document):
            raise RuntimeError("panne")

    results = analyse("texte", requirements[:3], Failing())
    assert [r["verdict"] for r in results] == ["non_trouve"] * 3
    assert "panne" in results[0]["rationale"]


# --- Juge Claude : forme de la requête, sans réseau ---------------------------

class FakeMessages:
    def __init__(self, response):
        self.response = response
        self.calls = []

    def create(self, **kwargs):
        self.calls.append(kwargs)
        return self.response


def fake_client(payload=None, stop_reason="end_turn"):
    content = [SimpleNamespace(type="thinking", thinking="")]
    if payload is not None:
        content.append(SimpleNamespace(type="text", text=json.dumps(payload)))
    response = SimpleNamespace(
        content=content,
        stop_reason=stop_reason,
        usage=SimpleNamespace(input_tokens=100, output_tokens=20,
                              cache_read_input_tokens=80, cache_creation_input_tokens=0),
    )
    plain, beta = FakeMessages(response), FakeMessages(response)
    client = SimpleNamespace(messages=plain, beta=SimpleNamespace(messages=beta))
    return client, plain, beta


PAYLOAD = {"verdict": "conforme", "requirement_quote": "q", "evidence": ["e"], "rationale": "r"}


def test_claude_judge_request_shape(requirements):
    client, plain, beta = fake_client(PAYLOAD)
    judge = ClaudeJudge(client=client)
    assert judge.judge(requirements[0], "DOC") == PAYLOAD
    assert plain.calls == []
    call = beta.calls[0]
    assert call["model"] == "claude-opus-5-5"
    assert call["betas"] == [FALLBACK_BETA] and call["fallbacks"] == "default"
    assert call["output_config"]["effort"] == "medium"
    assert call["output_config"]["format"]["type"] == "json_schema"
    assert "thinking" not in call and "temperature" not in call
    # préfixe stable : consignes puis document, le document porte le point de cache
    assert "DOC" in call["system"][1]["text"]
    assert call["system"][1]["cache_control"] == {"type": "ephemeral"}
    assert requirements[0]["unit"] in call["messages"][0]["content"]
    assert judge.usage["requests"] == 1 and judge.usage["cache_read_input_tokens"] == 80


def test_claude_judge_without_fallback_uses_plain_endpoint(requirements):
    client, plain, beta = fake_client(PAYLOAD)
    ClaudeJudge(client=client, refusal_fallback=False).judge(requirements[0], "DOC")
    assert beta.calls == [] and "fallbacks" not in plain.calls[0]


def test_claude_judge_refusal_becomes_not_found(requirements):
    client, _, _ = fake_client(None, stop_reason="refusal")
    assert ClaudeJudge(client=client).judge(requirements[0], "DOC")["verdict"] == "non_trouve"


def test_user_message_separates_context_from_requirement(requirements):
    message = build_user_message(requirements[-1])
    assert message.index("<contexte>") < message.index("<exigence id=")


# --- Juge Ollama : forme de la requête, sans réseau ----------------------------

def test_ollama_judge_request_shape(requirements):
    calls = []

    def post(url, payload, timeout):
        calls.append((url, payload))
        return {"message": {"content": json.dumps(PAYLOAD)}, "prompt_eval_count": 900, "eval_count": 50}

    judge = OllamaJudge(model="modele-local", host="localhost:11434", post=post)
    assert judge.judge(requirements[0], "DOC") == PAYLOAD
    url, payload = calls[0]
    assert url == "http://localhost:11434/api/chat"
    assert payload["format"] == OUTPUT_SCHEMA and payload["stream"] is False
    assert payload["options"] == {"temperature": 0, "num_ctx": 16384}
    system, user = payload["messages"]
    # mêmes consignes que le juge Claude : les mesures restent comparables
    assert system["content"].startswith(INSTRUCTIONS) and "DOC" in system["content"]
    assert requirements[0]["unit"] in user["content"]
    assert judge.usage == {"requests": 1, "input_tokens": 900, "output_tokens": 50}


def test_ollama_judge_flags_truncated_context(requirements):
    def post(url, payload, timeout):
        return {"message": {"content": json.dumps(PAYLOAD)}, "prompt_eval_count": 2048}

    out = OllamaJudge(model="m", num_ctx=2048, post=post).judge(requirements[0], "DOC")
    assert out["verdict"] == "non_trouve" and "contexte" in out["rationale"]
