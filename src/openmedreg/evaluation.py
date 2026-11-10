"""Banc d'évaluation : compare des verdicts prédits à la vérité terrain d'un cas.

Format d'une prédiction (une par ligne, JSONL) :
    {"unit": "anx_II/1.1/f", "verdict": "non_conforme",
     "requirement_quote": "passage de l'unité du règlement",
     "evidence": ["passage du document analysé", ...]}

Usage :
    python -m openmedreg.evaluation eval/cases/fictif-therm-t1 --predictions preds.jsonl
    python -m openmedreg.evaluation eval/cases/fictif-therm-t1 --baseline non_trouve
"""
from __future__ import annotations

import argparse
import json
import math
import sys
from dataclasses import dataclass
from pathlib import Path

import yaml

from openmedreg.citations import contains_quote
from openmedreg.corpus.eurlex import parse

def wilson_interval(successes: int, n: int, z: float = 1.96) -> list[float] | None:
    """Intervalle de confiance à 95 % d'une proportion (méthode de Wilson)."""
    if n == 0:
        return None
    p = successes / n
    denom = 1 + z * z / n
    centre = (p + z * z / (2 * n)) / denom
    half = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / denom
    return [round(max(0.0, centre - half), 4), round(min(1.0, centre + half), 4)]


VERDICTS = ("conforme", "non_conforme", "non_trouve", "non_applicable")
GAP_VERDICTS = ("non_conforme", "non_trouve")
DEFAULT_VERDICT = "non_trouve"
REPO_ROOT = Path(__file__).resolve().parents[2]


@dataclass
class Case:
    name: str
    document: str
    truth: dict[str, dict]  # identifiant d'unité -> annotation
    units: dict[str, dict]  # identifiant d'unité -> unité du corpus


def load_case(case_dir: str | Path, corpus_root: Path | None = None) -> Case:
    case_dir = Path(case_dir)
    spec = yaml.safe_load((case_dir / "ground_truth.yaml").read_text(encoding="utf-8"))
    corpus_root = corpus_root or REPO_ROOT / "corpus" / "public" / "mdr"
    source = corpus_root / f"{spec['corpus']['celex']}.{spec['lang']}.xhtml"
    units, _ = parse(source)
    return Case(
        name=spec["case"],
        document=(case_dir / spec["document"]).read_text(encoding="utf-8"),
        truth={entry["unit"]: entry for entry in spec["units"]},
        units={u["id"]: u for u in units},
    )


def apply_citation_rule(case: Case, prediction: dict) -> tuple[str, int, int]:
    """Applique la règle du projet : pas de verdict sans citation vérifiée.

    Retourne (verdict retenu, citations valides, citations totales). Un
    verdict autre que ``non_trouve`` est ramené à ``non_trouve`` s'il ne
    s'appuie sur aucun passage réel du document, ou si le passage cité du
    règlement n'existe pas dans l'unité visée.
    """
    verdict = prediction.get("verdict", DEFAULT_VERDICT)
    if verdict not in VERDICTS:
        verdict = DEFAULT_VERDICT
    evidence = prediction.get("evidence") or []
    valid = sum(contains_quote(case.document, quote) for quote in evidence)
    total = len(evidence)
    requirement = prediction.get("requirement_quote")
    requirement_ok = True
    if requirement is not None:
        total += 1
        unit = case.units.get(prediction.get("unit", ""), {})
        requirement_ok = contains_quote(unit.get("full_text", ""), requirement)
        valid += requirement_ok
    if verdict != "non_trouve" and (valid < total or not evidence or not requirement_ok):
        verdict = DEFAULT_VERDICT
    return verdict, valid, total


def score(case: Case, predictions: list[dict]) -> dict:
    by_unit = {p["unit"]: p for p in predictions if p.get("unit") in case.truth}
    confusion = {t: {p: 0 for p in VERDICTS} for t in VERDICTS}
    valid_quotes = total_quotes = downgraded = 0
    errors = []
    for unit, entry in case.truth.items():
        prediction = by_unit.get(unit, {"unit": unit, "verdict": DEFAULT_VERDICT})
        verdict, valid, total = apply_citation_rule(case, prediction)
        valid_quotes += valid
        total_quotes += total
        downgraded += verdict != prediction.get("verdict", DEFAULT_VERDICT)
        confusion[entry["expected"]][verdict] += 1
        if verdict != entry["expected"]:
            errors.append({"unit": unit, "expected": entry["expected"], "got": verdict})

    n = len(case.truth)
    correct = sum(confusion[v][v] for v in VERDICTS)
    gaps = sum(sum(confusion[t].values()) for t in GAP_VERDICTS)
    gaps_flagged = sum(confusion[t][p] for t in GAP_VERDICTS for p in GAP_VERDICTS)
    false_conforme = sum(confusion[t]["conforme"] for t in GAP_VERDICTS)
    per_verdict = {}
    for v in VERDICTS:
        predicted = sum(confusion[t][v] for t in VERDICTS)
        actual = sum(confusion[v].values())
        per_verdict[v] = {
            "precision": confusion[v][v] / predicted if predicted else None,
            "recall": confusion[v][v] / actual if actual else None,
            "support": actual,
        }
    return {
        "case": case.name,
        "units": n,
        "accuracy": correct / n,
        # Part des écarts réels déclarés « conforme » : l'erreur la plus grave.
        "false_conforme_rate": false_conforme / gaps if gaps else None,
        "false_conforme_count": f"{false_conforme}/{gaps}",
        # Sur peu d'unités, l'intervalle est large : deux moteurs dont les
        # intervalles se recouvrent ne sont pas départagés par ce cas.
        "false_conforme_ci95": wilson_interval(false_conforme, gaps),
        "accuracy_ci95": wilson_interval(correct, n),
        # Part des écarts réels signalés comme écart (non_conforme ou non_trouve).
        "gap_recall": gaps_flagged / gaps if gaps else None,
        "citation_validity": valid_quotes / total_quotes if total_quotes else None,
        "verdicts_downgraded_for_citation": downgraded,
        "unknown_units_ignored": sum(1 for p in predictions if p.get("unit") not in case.truth),
        "per_verdict": per_verdict,
        "confusion": confusion,
        "errors": errors,
    }


def baseline(case: Case, name: str) -> list[dict]:
    if name == "non_trouve":
        return [{"unit": u, "verdict": "non_trouve"} for u in case.truth]
    if name == "oracle":
        return [
            {"unit": u, "verdict": e["expected"], "evidence": list(e["evidence"])}
            for u, e in case.truth.items()
        ]
    raise ValueError(f"baseline inconnue : {name}")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("case_dir", type=Path)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--predictions", type=Path, help="fichier JSONL de prédictions")
    group.add_argument("--baseline", choices=["non_trouve", "oracle"])
    args = parser.parse_args(argv)
    case = load_case(args.case_dir)
    if args.baseline:
        predictions = baseline(case, args.baseline)
    else:
        lines = args.predictions.read_text(encoding="utf-8").splitlines()
        predictions = [json.loads(line) for line in lines if line.strip()]
    json.dump(score(case, predictions), sys.stdout, ensure_ascii=False, indent=2)
    print()
    return 0


if __name__ == "__main__":
    sys.exit(main())
