#!/usr/bin/env python3
"""Télécharge un texte consolidé depuis le dépôt de l'Office des publications de l'UE.

Exemple :
    python3 scripts/fetch_eurlex.py 02017R0745-20261109 --lang fr en --out corpus/public/mdr

Affiche l'empreinte SHA-256 de chaque fichier, à reporter dans SOURCE.yaml.
Bibliothèque standard uniquement.
"""
import argparse
import hashlib
import sys
import urllib.request
from pathlib import Path

BASE = "http://publications.europa.eu/resource/celex/"


def fetch(celex: str, lang: str) -> bytes:
    request = urllib.request.Request(
        BASE + celex,
        headers={
            "Accept": "application/xhtml+xml",
            "Accept-Language": lang,
            "User-Agent": "openmedreg-fetch",
        },
    )
    with urllib.request.urlopen(request, timeout=120) as response:
        return response.read()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("celex", help="identifiant CELEX, ex. 02017R0745-20261109")
    parser.add_argument("--lang", nargs="+", default=["fr", "en"])
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)
    for lang in args.lang:
        data = fetch(args.celex, lang)
        target = args.out / f"{args.celex}.{lang}.xhtml"
        target.write_bytes(data)
        print(f"{hashlib.sha256(data).hexdigest()}  {target}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
