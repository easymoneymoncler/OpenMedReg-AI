"""Masquage réversible des termes sensibles avant l'envoi d'un document à un juge.

Chaque terme déclaré (fabricant, produit, personne, adresse…) est remplacé
par une étiquette neutre, par exemple ``[FABRICANT_1]``. La table
étiquette → texte d'origine permet de revenir exactement au document de
départ et de rétablir les citations rendues par le juge.

Ce module ne devine rien : seuls les termes et motifs listés par
l'utilisateur sont masqués. Ce n'est pas une anonymisation automatique, et
un terme oublié dans les règles part tel quel chez le juge.

La table contient les termes d'origine : elle se range dans un dossier
ignoré par git (``build/``, ``data/client/``), jamais dans le dépôt.

Règles (YAML) :

    termes:
      FABRICANT:
        - [Exemplia Dispositifs SAS, Exemplia Dispositifs]  # variantes d'une même entité
      PRODUIT:
        - FICTIF-Therm T1
    motifs:
      COURRIEL: '[\\w.+-]+@[\\w-]+\\.[\\w.-]+'

Usage :
    python -m openmedreg.masking mask dossier.md --rules regles.yaml \\
        --out build/dossier.masque.md --map build/dossier.masking.json
    python -m openmedreg.masking unmask build/dossier.masque.md --map build/dossier.masking.json
    python -m openmedreg.masking compare build/sans.jsonl build/avec.jsonl
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

import yaml

SCHEMA = 1
CATEGORY_RE = re.compile(r"[A-Z][A-Z_]*\Z")
LABEL_RE = re.compile(r"\[([A-Z][A-Z_]*)_(\d+)(?:~(\d+))?\]")


class MaskingError(ValueError):
    """Règles invalides ou masquage qui ne serait pas réversible."""


def load_rules(path: str | Path) -> dict:
    return yaml.safe_load(Path(path).read_text(encoding="utf-8")) or {}


def _term_pattern(term: str) -> str:
    """Le terme entier, espaces et sauts de ligne confondus, pas un morceau de mot."""
    words = term.split()
    if not words:
        raise MaskingError("terme vide dans les règles de masquage")
    return r"(?<!\w)" + r"\s+".join(re.escape(w) for w in words) + r"(?!\w)"


class Masker:
    """Remplace les termes sensibles par des étiquettes et sait revenir en arrière.

    Une entité garde le même numéro d'un document à l'autre (ordre des
    règles). Quand une même entité apparaît sous plusieurs formes exactes
    (variante, casse), la première forme rencontrée reçoit ``[CAT_1]`` et les
    suivantes ``[CAT_1~2]``, ``[CAT_1~3]`` : c'est ce qui rend le retour
    exact, caractère pour caractère.
    """

    def __init__(self, rules: dict | None = None):
        rules = rules or {}
        self.labels: dict[str, str] = {}  # étiquette -> texte d'origine
        self._by_surface: dict[tuple[str, int, str], str] = {}
        self._forms: dict[tuple[str, int], int] = {}  # entité -> nombre de formes vues
        self._pattern_entities: dict[tuple[str, str], int] = {}
        self._next_entity: dict[str, int] = {}
        self._alternatives: list[tuple[str, int | None]] = []  # (catégorie, entité ou None)
        parts: list[tuple[int, str, str, int | None]] = []

        for category, entities in (rules.get("termes") or {}).items():
            self._check_category(category)
            for number, entity in enumerate(entities or [], start=1):
                variants = [entity] if isinstance(entity, str) else list(entity)
                for variant in variants:
                    if not isinstance(variant, str):
                        raise MaskingError(f"terme non textuel dans {category}")
                    parts.append((len(variant), _term_pattern(variant), category, number))
            self._next_entity[category] = len(entities or []) + 1
        # les termes les plus longs d'abord : « Exemplia Dispositifs SAS » avant « Exemplia »
        parts.sort(key=lambda part: -part[0])
        for category, pattern in (rules.get("motifs") or {}).items():
            self._check_category(category)
            try:
                re.compile(pattern)
            except re.error as error:
                raise MaskingError(f"motif invalide pour {category} : {error}") from error
            parts.append((0, pattern, category, None))
            self._next_entity.setdefault(category, 1)

        groups = []
        for index, (_, pattern, category, number) in enumerate(parts):
            groups.append(f"(?P<m{index}>{pattern})")
            self._alternatives.append((category, number))
        self._regex = re.compile("|".join(groups), re.IGNORECASE) if groups else None

    @staticmethod
    def _check_category(category: str) -> None:
        if not isinstance(category, str) or not CATEGORY_RE.match(category):
            raise MaskingError(
                f"catégorie invalide : {category!r} (majuscules sans accent et « _ » uniquement)"
            )

    @property
    def categories(self) -> set[str]:
        return {category for category, _ in self._alternatives} | {
            LABEL_RE.match(label).group(1) for label in self.labels
        }

    def _label_for(self, category: str, entity: int | None, surface: str) -> str:
        if entity is None:  # motif : chaque texte distinct est une entité
            key = (category, surface)
            if key not in self._pattern_entities:
                self._pattern_entities[key] = self._next_entity[category]
                self._next_entity[category] += 1
            entity = self._pattern_entities[key]
        known = self._by_surface.get((category, entity, surface))
        if known:
            return known
        form = self._forms.get((category, entity), 0) + 1
        self._forms[(category, entity)] = form
        label = f"[{category}_{entity}]" if form == 1 else f"[{category}_{entity}~{form}]"
        self._by_surface[(category, entity, surface)] = label
        self.labels[label] = surface
        return label

    def mask(self, text: str) -> str:
        """Retourne le texte masqué ; lève MaskingError si le retour ne serait pas exact."""
        for match in LABEL_RE.finditer(text):
            if match.group(1) in self.categories:
                raise MaskingError(
                    f"le texte contient déjà « {match.group(0)} » : renommer la catégorie "
                    f"{match.group(1)} dans les règles pour garder un masquage réversible"
                )
        if self._regex is None:
            return text

        def replace(match: re.Match) -> str:
            category, entity = self._alternatives[int(match.lastgroup[1:])]
            return self._label_for(category, entity, match.group(0))

        masked = self._regex.sub(replace, text)
        if self.unmask(masked) != text:
            raise MaskingError("masquage non réversible : le texte rétabli diffère de l'original")
        return masked

    def unmask(self, text: str) -> str:
        """Remet les textes d'origine à la place des étiquettes connues."""
        return LABEL_RE.sub(lambda m: self.labels.get(m.group(0), m.group(0)), text)

    def counts(self, masked: str) -> dict[str, int]:
        """Nombre d'occurrences de chaque étiquette dans un texte masqué."""
        out: dict[str, int] = {}
        for match in LABEL_RE.finditer(masked):
            if match.group(0) in self.labels:
                out[match.group(0)] = out.get(match.group(0), 0) + 1
        return out

    def save(self, path: str | Path) -> None:
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        payload = {"schema": SCHEMA, "labels": self.labels}
        path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    @classmethod
    def load(cls, path: str | Path) -> "Masker":
        """Recharge une table enregistrée : suffit pour ``unmask``, pas pour ``mask``."""
        payload = json.loads(Path(path).read_text(encoding="utf-8"))
        if payload.get("schema") != SCHEMA:
            raise MaskingError(f"table de masquage de schéma inconnu : {payload.get('schema')!r}")
        masker = cls()
        masker.labels = dict(payload["labels"])
        return masker


def compare_predictions(first: list[dict], second: list[dict]) -> list[dict]:
    """Unités dont le verdict retenu diffère entre deux séries de prédictions."""
    left = {p["unit"]: p.get("verdict") for p in first}
    right = {p["unit"]: p.get("verdict") for p in second}
    return [
        {"unit": unit, "first": left.get(unit), "second": right.get(unit)}
        for unit in sorted(set(left) | set(right))
        if left.get(unit) != right.get(unit)
    ]


def _read_jsonl(path: Path) -> list[dict]:
    lines = path.read_text(encoding="utf-8").splitlines()
    return [json.loads(line) for line in lines if line.strip()]


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    commands = parser.add_subparsers(dest="command", required=True)
    mask = commands.add_parser("mask", help="masquer un document et enregistrer la table")
    mask.add_argument("document", type=Path)
    mask.add_argument("--rules", type=Path, required=True)
    mask.add_argument("--out", type=Path, required=True, help="document masqué")
    mask.add_argument("--map", type=Path, required=True, help="table étiquette -> original (privée)")
    unmask = commands.add_parser("unmask", help="rétablir un texte masqué (texte brut)")
    unmask.add_argument("document", type=Path)
    unmask.add_argument("--map", type=Path, required=True)
    compare = commands.add_parser("compare", help="verdicts qui diffèrent entre deux séries")
    compare.add_argument("first", type=Path)
    compare.add_argument("second", type=Path)
    args = parser.parse_args(argv)

    if args.command == "mask":
        masker = Masker(load_rules(args.rules))
        masked = masker.mask(args.document.read_text(encoding="utf-8"))
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(masked, encoding="utf-8")
        masker.save(args.map)
        # les étiquettes seules : les termes d'origine ne sont pas affichés
        print(json.dumps(masker.counts(masked), ensure_ascii=False, indent=2), file=sys.stderr)
    elif args.command == "unmask":
        masker = Masker.load(args.map)
        sys.stdout.write(masker.unmask(args.document.read_text(encoding="utf-8")))
    else:
        differences = compare_predictions(_read_jsonl(args.first), _read_jsonl(args.second))
        json.dump(differences, sys.stdout, ensure_ascii=False, indent=2)
        print()
    return 0


if __name__ == "__main__":
    sys.exit(main())
