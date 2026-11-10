"""Cohérence du cas d'évaluation fictif et comportement du banc d'évaluation."""
from pathlib import Path

import pytest

from openmedreg.citations import contains_quote, normalize
from openmedreg.evaluation import GAP_VERDICTS, VERDICTS, baseline, load_case, score

CASE_DIR = Path(__file__).resolve().parents[1] / "eval" / "cases" / "fictif-therm-t1"


@pytest.fixture(scope="module")
def case():
    return load_case(CASE_DIR)


def test_truth_covers_every_leaf_unit_of_annex_ii(case):
    leaves = {
        ident for ident, unit in case.units.items()
        if unit["container"] == "anx_II" and not unit["children"]
    }
    assert set(case.truth) == leaves
    assert len(leaves) == 44


def test_annotations_are_well_formed(case):
    for unit, entry in case.truth.items():
        assert entry["expected"] in VERDICTS, unit
        assert entry["review_status"] in ("non_relu", "relu"), unit
        assert entry["rationale"].strip(), unit
        assert entry["injected_gap"] == (entry["expected"] in GAP_VERDICTS), unit
        if entry["expected"] == "non_trouve":
            assert entry["evidence"] == [], unit
        else:
            assert entry["evidence"], unit


def test_every_evidence_quote_exists_in_the_document(case):
    for unit, entry in case.truth.items():
        for quote in entry["evidence"]:
            assert contains_quote(case.document, quote), (unit, quote)


def test_document_is_marked_fictional(case):
    assert "DOCUMENT FICTIF" in case.document


def test_expected_distribution(case):
    counts = {v: sum(e["expected"] == v for e in case.truth.values()) for v in VERDICTS}
    assert counts == {"conforme": 23, "non_conforme": 6, "non_trouve": 7, "non_applicable": 8}


def test_oracle_scores_perfectly(case):
    result = score(case, baseline(case, "oracle"))
    assert result["accuracy"] == 1.0
    assert result["false_conforme_rate"] == 0.0
    assert result["gap_recall"] == 1.0
    assert result["citation_validity"] == 1.0
    assert result["errors"] == []


def test_always_not_found_baseline(case):
    result = score(case, baseline(case, "non_trouve"))
    assert result["accuracy"] == pytest.approx(7 / 44)
    assert result["false_conforme_rate"] == 0.0
    assert result["gap_recall"] == 1.0


def test_missing_predictions_count_as_not_found(case):
    assert score(case, [])["confusion"] == score(case, baseline(case, "non_trouve"))["confusion"]


def test_verdict_with_invented_quote_is_downgraded(case):
    predictions = [
        {"unit": "anx_II/1.1/b", "verdict": "conforme", "evidence": ["IUD-ID de base : 0000"]}
    ]
    result = score(case, predictions)
    assert result["verdicts_downgraded_for_citation"] == 1
    assert result["false_conforme_rate"] == 0.0
    assert result["citation_validity"] == 0.0


def test_verdict_without_evidence_is_downgraded(case):
    result = score(case, [{"unit": "anx_II/1.1/a", "verdict": "conforme"}])
    assert result["confusion"]["conforme"]["non_trouve"] == 23


def test_false_conforme_with_real_quote_is_counted(case):
    predictions = [
        {
            "unit": "anx_II/1.1/f",
            "verdict": "conforme",
            "requirement_quote": "La classe de risque du dispositif",
            "evidence": ["Le dispositif relève de la classe IIa."],
        }
    ]
    result = score(case, predictions)
    assert result["false_conforme_rate"] == pytest.approx(1 / 13)
    assert result["citation_validity"] == 1.0


def test_wrong_requirement_quote_downgrades(case):
    predictions = [
        {
            "unit": "anx_II/1.1/a",
            "verdict": "conforme",
            "requirement_quote": "texte absent du règlement",
            "evidence": ["Les utilisateurs prévus sont les infirmiers"],
        }
    ]
    assert score(case, predictions)["verdicts_downgraded_for_citation"] == 1


def test_quote_matching_is_exact_but_whitespace_tolerant():
    source = "Le dispositif relève\nde la  classe IIa. L’étiquette est jointe."
    assert contains_quote(source, "relève de la classe IIa")
    assert contains_quote(source, "L'étiquette")
    assert not contains_quote(source, "relève de la classe IIb")
    assert not contains_quote(source, "le dispositif relève")  # casse conservée
    assert not contains_quote(source, "")
    assert normalize("a b") == "a b"
