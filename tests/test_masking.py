"""Masquage réversible : retour exact, citations rétablies, aucun effet sans --mask."""
import json
from pathlib import Path

import pytest

from openmedreg import gap_analysis
from openmedreg.evaluation import load_case, score
from openmedreg.gap_analysis import analyse, load_units, requirements_in_scope
from openmedreg.masking import Masker, MaskingError, compare_predictions, load_rules

CASE_DIR = Path(__file__).resolve().parents[1] / "eval" / "cases" / "fictif-therm-t1"
CASE_RULES = Path(__file__).resolve().parent / "fixtures" / "masquage_fictif-therm-t1.yaml"
RULES = {
    "termes": {
        "FABRICANT": [["Exemplia Dispositifs SAS", "Exemplia Dispositifs"]],
        "PRODUIT": ["FICTIF-Therm T1"],
    },
    "motifs": {"COURRIEL": r"[\w.+-]+@[\w-]+\.[\w.-]+"},
}


@pytest.fixture(scope="module")
def case():
    return load_case(CASE_DIR)


@pytest.fixture(scope="module")
def requirements():
    return requirements_in_scope(load_units(lang="fr"), "anx_II")


@pytest.fixture(scope="module")
def case_rules():
    return load_rules(CASE_RULES)


def test_round_trip_is_exact_and_terms_are_gone():
    text = (
        "Fabricant : Exemplia Dispositifs SAS.\nLe FICTIF-Therm T1 d'Exemplia\n"
        "Dispositifs, écrire à qualite@exemplia.example ou QUALITE@exemplia.example."
    )
    masker = Masker(RULES)
    masked = masker.mask(text)
    assert "Exemplia" not in masked and "Therm" not in masked and "@" not in masked
    assert masker.unmask(masked) == text
    # deux formes de la même entité : même numéro, suffixe pour la seconde
    assert "[FABRICANT_1]" in masked and "[FABRICANT_1~2]" in masked
    # deux adresses distinctes par la casse : deux entités du motif
    assert "[COURRIEL_1]" in masked and "[COURRIEL_2]" in masked


def test_longest_term_wins_and_word_boundaries_hold():
    masker = Masker({"termes": {"NOM": [["Exemplia Dispositifs", "Exemplia"]], "SIGLE": ["SAS"]}})
    masked = masker.mask("Exemplia Dispositifs, puis Exemplia seule. Un SASSAFRAS, une SAS.")
    assert masked == "[NOM_1], puis [NOM_1~2] seule. Un SASSAFRAS, une [SIGLE_1]."


def test_same_entity_keeps_its_label_across_documents():
    masker = Masker(RULES)
    first = masker.mask("FICTIF-Therm T1 en service.")
    second = masker.mask("Notice du FICTIF-Therm T1.")
    assert first.startswith("[PRODUIT_1]") and second.endswith("[PRODUIT_1].")


def test_existing_label_in_document_is_refused():
    with pytest.raises(MaskingError):
        Masker(RULES).mask("Voir [PRODUIT_1] dans le plan.")
    # une étiquette d'une autre catégorie ne gêne pas le retour
    text = "Voir [FIGURE_2] pour le FICTIF-Therm T1."
    masker = Masker(RULES)
    assert masker.unmask(masker.mask(text)) == text


def test_invalid_rules_are_refused():
    with pytest.raises(MaskingError):
        Masker({"termes": {"fabricant": ["x"]}})
    with pytest.raises(MaskingError):
        Masker({"motifs": {"CODE": "("}})


def test_saved_table_restores_text(tmp_path):
    masker = Masker(RULES)
    masked = masker.mask("Exemplia Dispositifs SAS fabrique le FICTIF-Therm T1.")
    masker.save(tmp_path / "t.masking.json")
    assert (
        Masker.load(tmp_path / "t.masking.json").unmask(masked)
        == "Exemplia Dispositifs SAS fabrique le FICTIF-Therm T1."
    )


def test_case_rules_mask_every_fictional_name(case, case_rules):
    masker = Masker(case_rules)
    masked = masker.mask(case.document)
    assert "Exemplia" not in masked and "FICTIF-Therm" not in masked
    assert "rue des Exemples" not in masked
    assert masker.unmask(masked) == case.document


class MaskedOracle:
    """Juge qui ne connaît que le document masqué et cite ses étiquettes."""

    def __init__(self, case, rules):
        self.case, self.masker, self.seen = case, Masker(rules), []
        self.masker.mask(case.document)

    def judge(self, requirement, document):
        self.seen.append(document)
        entry = self.case.truth[requirement["unit"]]
        return {
            "verdict": entry["expected"],
            "requirement_quote": requirement["text"][:40],
            "evidence": [self.masker.mask(q) for q in entry["evidence"]],
            "rationale": self.masker.mask(entry["rationale"]),
        }


def test_end_to_end_masked_run_scores_like_the_plain_one(case, requirements, case_rules):
    judge = MaskedOracle(case, case_rules)
    predictions = analyse(case.document, requirements, judge, masker=Masker(case_rules))
    assert all("Exemplia" not in doc and "FICTIF-Therm" not in doc for doc in judge.seen)
    result = score(case, predictions)
    assert result["accuracy"] == 1.0
    assert result["verdicts_downgraded_for_citation"] == 0
    assert all(p["masked"] for p in predictions)
    # les prédictions écrites ne contiennent plus aucune étiquette
    assert "[PRODUIT_" not in json.dumps(predictions, ensure_ascii=False)
    quoted = [q for p in predictions for q in p["evidence"]]
    assert any("FICTIF-Therm T1" in q for q in quoted)


def test_evidence_that_cuts_a_label_is_downgraded(requirements):
    document = "Le fabricant est Exemplia Dispositifs SAS, établi en France."

    class Cutter:
        def judge(self, requirement, masked):
            return {
                "verdict": "conforme",
                "requirement_quote": requirement["text"][:30],
                "evidence": ["Le fabricant est [FABRICANT_"],
                "rationale": "x",
            }

    (prediction,) = analyse(document, requirements[:1], Cutter(), masker=Masker(RULES))
    assert prediction["verdict"] == "non_trouve"
    assert prediction["evidence"] == []
    assert any("démasquage" in note for note in prediction["verification_notes"])


def test_without_masker_the_judge_sees_the_original(case, requirements):
    seen = []

    class Recorder:
        def judge(self, requirement, document):
            seen.append(document)
            return {"verdict": "non_trouve", "rationale": ""}

    (prediction,) = analyse(case.document, requirements[:1], Recorder())
    assert seen == [case.document]
    assert prediction["masked"] is False


def test_compare_predictions_lists_only_differences():
    first = [{"unit": "a", "verdict": "conforme"}, {"unit": "b", "verdict": "non_trouve"}]
    second = [{"unit": "a", "verdict": "non_conforme"}, {"unit": "b", "verdict": "non_trouve"}]
    assert compare_predictions(first, second) == [
        {"unit": "a", "first": "conforme", "second": "non_conforme"}
    ]


def test_mask_table_is_refused_in_a_published_path(tmp_path):
    repo = gap_analysis.REPO_ROOT
    assert gap_analysis.is_published_path(repo / "eval" / "table.json")
    assert not gap_analysis.is_published_path(repo / "build" / "runs" / "p.jsonl.masking.json")
    assert not gap_analysis.is_published_path(repo / "eval" / "p.jsonl.masking.json")
    assert not gap_analysis.is_published_path(tmp_path / "table.json")
