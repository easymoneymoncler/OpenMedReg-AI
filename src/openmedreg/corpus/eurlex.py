"""Découpe un texte consolidé EUR-Lex (XHTML) en unités citables.

Chaque article, paragraphe, point d'annexe et élément de liste devient une
unité dotée d'un identifiant stable et indépendant de la langue, par exemple
``art_10/4`` ou ``anx_II/1.1/a``. Ces identifiants servent de cible aux
citations ; le texte de l'unité sert à vérifier une citation mot pour mot.

Bibliothèque standard uniquement.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import xml.etree.ElementTree as ET
from dataclasses import dataclass, field
from pathlib import Path

XHTML = "{http://www.w3.org/1999/xhtml}"
INLINE_TAGS = {"span", "a", "br", "sup", "sub", "i", "b", "em", "strong", "img"}
SKIPPED_P_CLASSES = {"modref", "title-annex-1", "title-article-norm", "arrow"}

# Rang d'un élément : plus il est petit, plus l'élément est haut dans la hiérarchie.
RANK_ROOT = 0
RANK_NUMBER = 10  # + nombre de composantes : « 10.4.1 » -> 13
RANK_UPPER = 20  # « A. »
RANK_DIGIT_PAREN = 30  # « 1) »
RANK_LETTER = 40  # « a) »
RANK_ROMAN = 50  # « i) »
RANK_OTHER = 55
RANK_DASH = 60  # « — »
RANK_LIST_MIN = RANK_DIGIT_PAREN  # à partir de ce rang : élément de liste

LATIN_SUFFIX = {
    "bis": "a", "ter": "b", "quater": "c", "quinquies": "d",
    "sexies": "e", "septies": "f", "octies": "g", "nonies": "h", "decies": "i",
}
DIVISION_WORDS = {
    "chapitre": "chap", "chapter": "chap",
    "partie": "part", "part": "part",
    "section": "sect",
    "titre": "tit", "title": "tit",
}

_NUMBER_RE = re.compile(
    r"^(\d+(?:\.\d+)*)\s*(?:(" + "|".join(LATIN_SUFFIX) + r")|([a-z]))?\s*\.?$"
)
_HEADING_NUMBER_RE = re.compile(r"^(\d+(?:\.\d+)*)\.?\s+(.*)$", re.S)
_DIVISION_RE = re.compile(
    r"^(" + "|".join(DIVISION_WORDS) + r")\s+([IVXLC]+|[A-Z]|\d+)$", re.I
)
_AMENDMENT_RE = re.compile(r"[►▼][A-Z]\d*\s*|◄\s*")
_ROMAN_RE = re.compile(r"^[ivxl]+$")


def _clean(text: str) -> str:
    text = _AMENDMENT_RE.sub("", text.replace(" ", " "))
    return re.sub(r"\s+", " ", text).strip()


def _text(el: ET.Element) -> str:
    return _clean("".join(el.itertext()))


def _tag(el: ET.Element) -> str:
    return el.tag.replace(XHTML, "")


@dataclass
class Node:
    label: str
    marker: str = ""
    rank: int = RANK_ROOT
    title: str = ""
    parts: list = field(default_factory=list)  # str | Node, dans l'ordre du texte
    parent: "Node | None" = None
    id: str = ""

    @property
    def children(self) -> list["Node"]:
        return [p for p in self.parts if isinstance(p, Node)]

    def own_text(self) -> str:
        return "\n".join(p for p in self.parts if isinstance(p, str))

    def head(self) -> str:
        return " ".join(x for x in (self.marker, self.title) if x)

    def full_text(self) -> str:
        lines = [self.head()] if self.head() else []
        for part in self.parts:
            lines.append(part if isinstance(part, str) else part.full_text())
        if len(lines) > 1 and self.marker and not self.title and isinstance(self.parts[0], str):
            lines[0:2] = [f"{lines[0]} {lines[1]}"]
        return "\n".join(line for line in lines if line)


def classify_marker(raw: str, open_letter: str | None) -> tuple[int, str | None]:
    """Retourne (rang, composant d'identifiant) pour un marqueur de liste.

    ``open_letter`` est la lettre du dernier élément « a) » ouvert au même
    niveau ; elle sert à distinguer la lettre « i) » du chiffre romain « i) ».
    """
    m = raw.strip().strip("«»\"“”‘’'").strip()
    if m in {"—", "–", "-", "•", "·"}:
        return RANK_DASH, None
    num = _NUMBER_RE.match(m)
    if num and (m.endswith(".") or "." in num.group(1)):
        suffix = LATIN_SUFFIX.get(num.group(2) or "", num.group(3) or "")
        return RANK_NUMBER + num.group(1).count(".") + 1, num.group(1) + suffix
    latin = re.match(r"^\(?([a-z])\s+(" + "|".join(LATIN_SUFFIX) + r")\)$", m)
    if latin:  # « e bis) » en français, « (ea) » en anglais
        return RANK_LETTER, latin.group(1) + LATIN_SUFFIX[latin.group(2)]
    paren = re.match(r"^\(?([0-9]+|[a-z]+|[A-Z]+)\)$", m)
    if paren:
        body = paren.group(1)
        if body.isdigit():
            return RANK_DIGIT_PAREN, body
        if body.isupper():
            return RANK_UPPER, body
        if _ROMAN_RE.match(body):
            continues_letters = (
                len(body) == 1
                and open_letter is not None
                and len(open_letter) == 1
                and ord(body) == ord(open_letter) + 1
            )
            if not continues_letters:
                return RANK_ROMAN, body
        return RANK_LETTER, body
    upper = re.match(r"^([A-Z])\.$", m)
    if upper:
        return RANK_UPPER, upper.group(1)
    return RANK_OTHER, None


class _Walker:
    """Reconstruit la hiérarchie d'une suite d'éléments frères."""

    def __init__(self, base: Node, warnings: list[str]):
        self.stack = [base]
        self.warnings = warnings
        self._pending_division: Node | None = None

    # -- construction de l'arbre ------------------------------------------
    def _open(self, rank: int, label: str | None, marker: str, title: str = "") -> Node:
        while len(self.stack) > 1 and self.stack[-1].rank >= rank:
            self.stack.pop()
        parent = self.stack[-1]
        siblings = parent.children
        if label is None:
            prefix = {RANK_DASH: "t"}.get(rank, "h" if rank < RANK_NUMBER else "n")
            count = sum(1 for s in siblings if re.fullmatch(prefix + r"\d+", s.label))
            label = f"{prefix}{count + 1}"
            if prefix == "n":
                self.warnings.append(f"marqueur non reconnu : {marker!r}")
        taken = {s.label for s in siblings}
        if label in taken:
            n = 2
            while f"{label}~{n}" in taken:
                n += 1
            self.warnings.append(f"étiquette en double : {label!r} sous {parent.label!r}")
            label = f"{label}~{n}"
        node = Node(label=label, marker=marker, rank=rank, title=title, parent=parent)
        parent.parts.append(node)
        self.stack.append(node)
        return node

    def _add_text(self, text: str) -> None:
        if not text:
            return
        # Un texte libre entre frères n'appartient pas au dernier élément de
        # liste : il se rattache au paragraphe ou au titre qui porte la liste.
        while len(self.stack) > 1 and self.stack[-1].rank >= RANK_LIST_MIN:
            self.stack.pop()
        self.stack[-1].parts.append(text)

    def _open_letter(self) -> str | None:
        top = self.stack[-1]
        return top.label if len(self.stack) > 1 and top.rank == RANK_LETTER else None

    def _item(self, marker_raw: str, content: list[ET.Element]) -> None:
        marker = _clean(marker_raw)
        rank, label = classify_marker(marker, self._open_letter())
        if rank == RANK_ROMAN and len(label) == 1:
            depth = len(self.stack) - 1
            while depth > 0 and self.stack[depth].rank >= RANK_ROMAN:
                depth -= 1
            if any(s.label == label for s in self.stack[depth].children):
                # « i) » alors que la liste romaine visée contient déjà « i) » :
                # c'est la lettre i de la liste alphabétique englobante
                # (cas d'un point « h) » supprimé par un acte modificatif).
                rank = RANK_LETTER
        node = self._open(rank, label, marker)
        inner = _Walker(node, self.warnings)
        for el in content:
            inner.walk(el)

    # -- parcours ----------------------------------------------------------
    def walk(self, container: ET.Element) -> None:
        """Parcourt le contenu mixte (texte et blocs) d'un conteneur."""
        buffer = [container.text or ""]
        for child in container:
            if _tag(child) in INLINE_TAGS:
                buffer.append("".join(child.itertext()))
                buffer.append(child.tail or "")
                continue
            self._add_text(_clean("".join(buffer)))
            buffer = [child.tail or ""]
            self.element(child)
        self._add_text(_clean("".join(buffer)))

    def element(self, el: ET.Element) -> None:
        tag, cls = _tag(el), el.get("class") or ""
        division_follow, self._pending_division = self._pending_division, None
        if tag == "p":
            if cls in SKIPPED_P_CLASSES:
                self._pending_division = division_follow
            elif cls.startswith("title-gr-seq-level-"):
                self._heading(el, int(cls.rsplit("-", 1)[1]), division_follow)
            else:
                self._add_text(_text(el))
        elif tag == "table":
            self._table(el)
        elif tag == "div":
            children = list(el)
            if cls == "eli-title":
                self.stack[0].title = self.stack[0].title or _text(el)
            elif "grid-container" in cls and len(children) == 2:
                self._item("".join(children[0].itertext()), [children[1]])
            elif children and (children[0].get("class") or "") == "no-parag":
                self._paragraph(el, children)
            else:
                self.walk(el)
        elif tag == "hr":
            self._pending_division = division_follow
        else:
            self._add_text(_text(el))

    def _paragraph(self, el: ET.Element, children: list[ET.Element]) -> None:
        marker = _clean("".join(children[0].itertext()))
        rank, label = classify_marker(marker, None)
        node = self._open(rank, label, marker)
        inner = _Walker(node, self.warnings)
        inner._add_text(_clean(children[0].tail or ""))
        for child in children[1:]:
            if _tag(child) in INLINE_TAGS:
                inner._add_text(_clean("".join(child.itertext()) + (child.tail or "")))
            else:
                inner.element(child)
                inner._add_text(_clean(child.tail or ""))

    def _heading(self, el: ET.Element, level: int, division: Node | None) -> None:
        text = _text(el)
        if not text:
            return
        base = self.stack[0]
        if level == 1 and base.rank == RANK_ROOT and not base.title and not base.parts:
            base.title = text
            return
        if division is not None and division.rank == level and not division.title:
            if not _DIVISION_RE.match(text) and not _HEADING_NUMBER_RE.match(text):
                division.title = text
                return
        numbered = _HEADING_NUMBER_RE.match(text)
        named = _DIVISION_RE.match(text)
        if numbered:
            self._open(level, numbered.group(1), numbered.group(1) + ".", numbered.group(2))
        elif named:
            label = f"{DIVISION_WORDS[named.group(1).lower()]}_{named.group(2).upper()}"
            self._pending_division = self._open(level, label, text)
        else:
            self._open(level, None, "", text)

    def _table(self, el: ET.Element) -> None:
        rows = [r for r in el.iter(f"{XHTML}tr") if self._owns_row(el, r)]
        cells = [[c for c in r if _tag(c) in ("td", "th")] for r in rows]
        is_marker_table = bool(cells) and all(
            len(c) == 2 and classify_marker(_text(c[0]), None)[0] != RANK_OTHER for c in cells
        )
        if is_marker_table:
            for marker_cell, content_cell in cells:
                self._item("".join(marker_cell.itertext()), [content_cell])
        else:
            for row in cells:
                self._add_text(" | ".join(t for t in (_text(c) for c in row) if t))

    @staticmethod
    def _owns_row(table: ET.Element, row: ET.Element) -> bool:
        """Vrai si la ligne appartient à ce tableau et non à un tableau imbriqué."""
        for nested in table.iter(f"{XHTML}table"):
            if nested is not table and row in list(nested.iter(f"{XHTML}tr")):
                return False
        return True


def _assign_ids(node: Node, path: list[str]) -> None:
    node.id = "/".join(path)
    for child in node.children:
        kept = [
            p for i, p in enumerate(path)
            if i == 0 or not (
                re.fullmatch(r"\d+(\.\d+)*[a-z]?", p) and child.label.startswith(p + ".")
            )
        ]
        _assign_ids(child, kept + [child.label])


def _units(node: Node, meta: dict, container: Node) -> list[dict]:
    breadcrumb = []
    current = node.parent
    while current is not None:
        if current.title:
            breadcrumb.append(current.title)
        current = current.parent
    unit = {
        **meta,
        "id": node.id,
        "container": container.id,
        "kind": "article" if container.id.startswith("art_") else "annex",
        "marker": node.marker,
        "title": node.title,
        "breadcrumb": list(reversed(breadcrumb)),
        "parent": node.parent.id if node.parent else None,
        "children": [c.id for c in node.children],
        "text": node.own_text(),
        "full_text": node.full_text(),
    }
    out = [unit]
    for child in node.children:
        out.extend(_units(child, meta, container))
    return out


_CONTAINER_RE = re.compile(r"^(art_\d+[a-z]*|anx_[IVXLC]+)$")
_REFERENCE_RE = re.compile(r"^(\S+) — (\w+) — (\d{2})\.(\d{2})\.(\d{4})")


def parse(path: str | Path) -> tuple[list[dict], list[str]]:
    """Retourne (unités, avertissements) pour un fichier XHTML consolidé."""
    root = ET.parse(path).getroot()
    meta = {"celex": "", "version": "", "lang": ""}
    for el in root.iter(f"{XHTML}p"):
        if el.get("class") == "reference":
            ref = _REFERENCE_RE.match(_text(el))
            if ref:
                meta = {
                    "celex": ref.group(1),
                    "version": f"{ref.group(5)}-{ref.group(4)}-{ref.group(3)}",
                    "lang": ref.group(2).lower(),
                }
            break
    units, warnings = [], []
    for el in root.iter(f"{XHTML}div"):
        ident = el.get("id") or ""
        if not _CONTAINER_RE.match(ident):
            continue
        local: list[str] = []
        base = Node(label=ident)
        for title in el.findall(f"{XHTML}p"):
            if title.get("class") in ("title-article-norm", "title-annex-1"):
                base.marker = _text(title)
                break
        _Walker(base, local).walk(el)
        _assign_ids(base, [ident])
        units.extend(_units(base, meta, base))
        warnings.extend(f"{ident} : {w}" for w in local)
    return units, warnings


def raw_container_texts(path: str | Path) -> dict[str, str]:
    """Texte brut de chaque article et annexe, pour mesurer la couverture."""
    root = ET.parse(path).getroot()
    out = {}
    for el in root.iter(f"{XHTML}div"):
        ident = el.get("id") or ""
        if _CONTAINER_RE.match(ident):
            skipped = sum(
                len(_text(p)) for p in el.iter(f"{XHTML}p") if p.get("class") == "modref"
            )
            out[ident] = _text(el)
            out[ident + "#modref"] = str(skipped)
    return out


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("xhtml", type=Path)
    parser.add_argument("--out", type=Path, required=True, help="fichier JSONL de sortie")
    args = parser.parse_args(argv)
    units, warnings = parse(args.xhtml)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    with args.out.open("w", encoding="utf-8") as handle:
        for unit in units:
            handle.write(json.dumps(unit, ensure_ascii=False) + "\n")
    print(f"{len(units)} unités écrites dans {args.out} ; {len(warnings)} avertissements")
    for warning in warnings:
        print("  " + warning, file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
