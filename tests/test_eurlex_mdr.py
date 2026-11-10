"""Tests du découpage sur le texte consolidé réel du MDR (corpus public)."""
import re
from pathlib import Path

import pytest

from openmedreg.corpus.eurlex import (
    RANK_DASH,
    RANK_DIGIT_PAREN,
    RANK_LETTER,
    RANK_NUMBER,
    RANK_OTHER,
    RANK_ROMAN,
    classify_marker,
    parse,
    raw_container_texts,
)

CORPUS = Path(__file__).resolve().parents[1] / "corpus" / "public" / "mdr"
VERSION = "02017R0745-20261109"
ROMAN = ["I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X",
         "XI", "XII", "XIII", "XIV", "XV", "XVI", "XVII"]


def _path(lang):
    return CORPUS / f"{VERSION}.{lang}.xhtml"


@pytest.fixture(scope="module")
def parsed():
    return {lang: parse(_path(lang)) for lang in ("fr", "en")}


@pytest.fixture(scope="module")
def fr(parsed):
    return {u["id"]: u for u in parsed["fr"][0]}


@pytest.mark.parametrize("lang", ["fr", "en"])
def test_metadata(parsed, lang):
    unit = parsed[lang][0][0]
    assert (unit["celex"], unit["version"], unit["lang"]) == ("02017R0745", "2026-11-09", lang)


@pytest.mark.parametrize("lang", ["fr", "en"])
def test_no_warnings_and_unique_ids(parsed, lang):
    units, warnings = parsed[lang]
    assert warnings == []
    ids = [u["id"] for u in units]
    assert len(ids) == len(set(ids))


def test_ids_are_language_independent(parsed):
    assert {u["id"] for u in parsed["fr"][0]} == {u["id"] for u in parsed["en"][0]}


def test_all_articles_and_annexes_present(fr):
    for n in range(1, 124):
        assert f"art_{n}" in fr
    for r in ROMAN:
        assert f"anx_{r}" in fr


@pytest.mark.parametrize("lang", ["fr", "en"])
def test_no_text_is_lost(parsed, lang):
    """Le texte de chaque article et annexe est repris intégralement."""
    units = {u["id"]: u for u in parsed[lang][0]}
    raw = raw_container_texts(_path(lang))
    for ident, text in raw.items():
        if "#" in ident:
            continue
        expected = len(re.sub(r"\s", "", text)) - int(raw[ident + "#modref"])
        got = len(re.sub(r"\s", "", units[ident]["full_text"]))
        assert got >= expected, ident


def test_article_paragraph_with_subparagraph(fr):
    unit = fr["art_10/4"]
    assert unit["marker"] == "4."
    assert unit["kind"] == "article"
    assert unit["breadcrumb"] == ["Obligations générales des fabricants"]
    assert "annexes II et III" in unit["text"]
    # le second alinéa, non numéroté, reste rattaché au paragraphe 4
    assert "article 115" in unit["text"]


def test_annex_item_under_numbered_headings(fr):
    unit = fr["anx_II/1.1/a"]
    assert unit["kind"] == "annex"
    assert unit["parent"] == "anx_II/1.1"
    assert unit["breadcrumb"][0] == "DOCUMENTATION TECHNIQUE"
    assert "dénomination commerciale" in unit["full_text"]


def test_annex_chapters_and_nested_numbers(fr):
    assert fr["anx_I/chap_I"]["title"] == "EXIGENCES GÉNÉRALES"
    assert fr["anx_I/chap_II/10.4.1"]["parent"] == "anx_I/chap_II/10.4"
    # numérotation qui recommence dans chaque partie de l'annexe VI
    assert "anx_VI/part_A/1.1" in fr and "anx_VI/part_B/1" in fr


def test_definitions_are_units(fr):
    assert fr["art_2/1"]["full_text"].startswith("1) «dispositif médical»")


def test_latin_suffixes_match_article_ids(fr):
    assert "art_10a" in fr
    assert {"art_123/3/ea", "art_123/3/eb", "art_123/3/ec"} <= set(fr)


def test_letter_i_after_deleted_point_is_not_roman(fr):
    assert "art_123/3/i" in fr
    assert set(fr["art_123/3/g"]["children"]) == {
        "art_123/3/g/i", "art_123/3/g/ii", "art_123/3/g/iii"
    }


def test_parent_child_links_are_consistent(fr):
    for unit in fr.values():
        for child in unit["children"]:
            assert fr[child]["parent"] == unit["id"]


@pytest.mark.parametrize(
    "marker, open_letter, expected",
    [
        ("1.", None, (RANK_NUMBER + 1, "1")),
        ("10.4.1.", None, (RANK_NUMBER + 3, "10.4.1")),
        ("1 bis.", None, (RANK_NUMBER + 1, "1a")),
        ("1a.", None, (RANK_NUMBER + 1, "1a")),
        ("‘4.", None, (RANK_NUMBER + 1, "4")),
        ("1)", None, (RANK_DIGIT_PAREN, "1")),
        ("(1)", None, (RANK_DIGIT_PAREN, "1")),
        ("a)", None, (RANK_LETTER, "a")),
        ("(a)", None, (RANK_LETTER, "a")),
        ("e bis)", None, (RANK_LETTER, "ea")),
        ("(ea)", None, (RANK_LETTER, "ea")),
        ("i)", None, (RANK_ROMAN, "i")),
        ("i)", "h", (RANK_LETTER, "i")),
        ("ii)", "h", (RANK_ROMAN, "ii")),
        ("—", None, (RANK_DASH, None)),
        ("???", None, (RANK_OTHER, None)),
    ],
)
def test_classify_marker(marker, open_letter, expected):
    assert classify_marker(marker, open_letter) == expected
