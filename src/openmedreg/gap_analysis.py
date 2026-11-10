"""Analyse d'écarts : confronte un document à chaque unité d'un périmètre du règlement.

Le jugement est délégué à un « juge » interchangeable (modèle distant ou
local). Ce module ne dépend d'aucun fournisseur : il choisit les unités,
donne leur contexte au juge, puis applique la règle du projet, à savoir
qu'un verdict sans citation vérifiée mot pour mot devient ``non_trouve``.

Usage :
    python -m openmedreg.gap_analysis eval/cases/fictif-therm-t1/dossier.md \\
        --scope anx_II --lang fr --out build/predictions.jsonl
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path
from typing import Callable, Protocol

from openmedreg.citations import contains_quote
from openmedreg.corpus.eurlex import parse

VERDICTS = ("conforme", "non_conforme", "non_trouve", "non_applicable")
DEFAULT_VERDICT = "non_trouve"
REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_CELEX = "02017R0745-20261109"


class Judge(Protocol):
    """Rend un jugement brut pour une unité. Aucune vérification n'est attendue de lui."""

    def judge(self, requirement: dict, document: str) -> dict:
        """Retourne {"verdict", "requirement_quote", "evidence", "rationale"}."""


def load_units(celex: str = DEFAULT_CELEX, lang: str = "fr") -> dict[str, dict]:
    source = REPO_ROOT / "corpus" / "public" / "mdr" / f"{celex}.{lang}.xhtml"
    units, _ = parse(source)
    return {u["id"]: u for u in units}


def requirements_in_scope(units: dict[str, dict], scope: str) -> list[dict]:
    """Unités feuilles du périmètre, chacune avec le texte introductif de ses parents.

    Le contexte compte : « la stabilité, y compris la durée de conservation »
    ne se comprend qu'avec la phrase du point b) qui l'introduit.
    """
    out = []
    for ident, unit in units.items():
        if unit["children"] or not (ident == scope or ident.startswith(scope + "/")):
            continue
        context = []
        parent = unit["parent"]
        while parent:
            node = units[parent]
            head = " ".join(x for x in (node["marker"], node["title"]) if x)
            context.append("\n".join(x for x in (head, node["text"]) if x))
            parent = node["parent"]
        out.append(
            {
                "unit": ident,
                "text": unit["full_text"],
                "context": list(reversed(context)),
            }
        )
    return out


def verify(requirement: dict, document: str, raw: dict) -> dict:
    """Applique la règle de citation à un jugement brut et retourne la prédiction finale."""
    verdict = raw.get("verdict")
    notes = []
    if verdict not in VERDICTS:
        notes.append(f"verdict inconnu : {verdict!r}")
        verdict = DEFAULT_VERDICT
    evidence = [q for q in (raw.get("evidence") or []) if isinstance(q, str)]
    valid_evidence = [q for q in evidence if contains_quote(document, q)]
    requirement_quote = raw.get("requirement_quote") or ""
    requirement_ok = contains_quote(requirement["text"], requirement_quote)

    retained = verdict
    if verdict != DEFAULT_VERDICT:
        if not requirement_ok:
            notes.append("passage du règlement introuvable dans l'unité")
            retained = DEFAULT_VERDICT
        if not evidence:
            notes.append("aucun passage du document cité")
            retained = DEFAULT_VERDICT
        elif len(valid_evidence) < len(evidence):
            notes.append(
                f"{len(evidence) - len(valid_evidence)} passage(s) du document introuvable(s)"
            )
            retained = DEFAULT_VERDICT
    return {
        "unit": requirement["unit"],
        "verdict": retained,
        "model_verdict": raw.get("verdict"),
        "requirement_quote": requirement_quote if requirement_ok else None,
        "evidence": valid_evidence if retained != DEFAULT_VERDICT else [],
        "rejected_evidence": [q for q in evidence if q not in valid_evidence],
        "rationale": raw.get("rationale", ""),
        "verification_notes": notes,
    }


def analyse(
    document: str,
    requirements: list[dict],
    judge: Judge,
    on_result: Callable[[dict], None] | None = None,
) -> list[dict]:
    results = []
    for requirement in requirements:
        try:
            raw = judge.judge(requirement, document)
        except Exception as error:  # un échec isolé ne doit pas perdre les autres verdicts
            raw = {"verdict": DEFAULT_VERDICT, "rationale": f"échec du juge : {error}"}
        result = verify(requirement, document, raw)
        results.append(result)
        if on_result:
            on_result(result)
    return results


def load_dotenv(path: Path) -> None:
    """Charge les variables d'un fichier .env sans écraser l'environnement existant."""
    if not path.exists():
        return
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            key, value = line.split("=", 1)
            os.environ.setdefault(key.strip(), value.strip().strip("\"'"))


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("document", type=Path, help="document à analyser (texte ou Markdown)")
    parser.add_argument("--scope", default="anx_II", help="unité racine du périmètre")
    parser.add_argument("--lang", default="fr")
    parser.add_argument("--celex", default=DEFAULT_CELEX)
    parser.add_argument("--out", type=Path, required=True, help="prédictions JSONL")
    parser.add_argument("--model", default="claude-opus-5-5")
    parser.add_argument("--effort", default="medium")
    parser.add_argument("--limit", type=int, help="ne traiter que les N premières unités")
    args = parser.parse_args(argv)

    load_dotenv(REPO_ROOT / ".env")
    from openmedreg.engines.claude import ClaudeJudge

    document = args.document.read_text(encoding="utf-8")
    requirements = requirements_in_scope(load_units(args.celex, args.lang), args.scope)
    if args.limit:
        requirements = requirements[: args.limit]
    judge = ClaudeJudge(model=args.model, effort=args.effort)

    args.out.parent.mkdir(parents=True, exist_ok=True)
    with args.out.open("w", encoding="utf-8") as handle:
        def write(result: dict) -> None:
            handle.write(json.dumps(result, ensure_ascii=False) + "\n")
            handle.flush()
            flag = "" if result["verdict"] == result["model_verdict"] else "  (rétrogradé)"
            print(f"{result['unit']:<22} {result['verdict']}{flag}", file=sys.stderr)

        analyse(document, requirements, judge, write)
    print(json.dumps(judge.usage, ensure_ascii=False), file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
