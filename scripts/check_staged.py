#!/usr/bin/env python3
"""Bloque les fichiers interdits avant commit ou push.

Sans argument : contrôle les fichiers indexés (usage pre-commit).
Avec --all    : contrôle tous les fichiers suivis par git (usage pre-push).

Interdits : dossiers privés, documents bureautiques hors des dossiers
autorisés, texte portant une mention de copyright d'organisme de
normalisation, secrets, fichiers trop volumineux.
N'utilise que la bibliothèque standard.
"""
import re
import subprocess
import sys
from pathlib import PurePosixPath

MAX_BYTES = 5 * 1024 * 1024

PRIVATE_DIRS = ("corpus/private/", "data/client/")
PRIVATE_DIR_ALLOWED_NAMES = {".gitkeep", "README.md"}

DOC_EXTENSIONS = {".pdf", ".doc", ".docx", ".xls", ".xlsx", ".ppt", ".pptx", ".odt", ".epub"}
DOC_ALLOWED_DIRS = ("corpus/public/", "eval/fixtures/")

SECRET_FILE_NAMES = {".env", "secrets.yaml", "secrets.yml", "id_rsa", "id_ed25519"}

# Fichiers qui contiennent les motifs ci-dessous par construction.
CONTENT_SCAN_EXEMPT = {"scripts/check_staged.py", "tests/test_check_staged.py"}

COPYRIGHT_MARKERS = [
    re.compile(p, re.IGNORECASE)
    for p in (
        r"copyright protected document",
        r"iso copyright office",
        r"©\s*(iso|iec|cen|cenelec|afnor|bsi|din)\b",
        r"\(c\)\s*(iso|iec|cen|cenelec|afnor)\b",
        r"single[- ]user licen[cs]e",
        r"licensed to .{0,80}(iso|iec|afnor|bsi) store",
        r"droits de reproduction réservés.{0,80}(iso|iec|afnor)",
    )
]

SECRET_PATTERNS = [
    re.compile(p)
    for p in (
        r"sk-ant-[A-Za-z0-9_\-]{20,}",
        r"sk-[A-Za-z0-9]{32,}",
        r"gh[pousr]_[A-Za-z0-9]{30,}",
        r"github_pat_[A-Za-z0-9_]{30,}",
        r"AKIA[0-9A-Z]{16}",
        r"hf_[A-Za-z0-9]{30,}",
        r"-----BEGIN [A-Z ]*PRIVATE KEY-----",
    )
]


def violations(path: str, content: bytes) -> list[str]:
    """Retourne la liste des raisons de blocage pour un fichier."""
    found = []
    p = PurePosixPath(path)

    for private in PRIVATE_DIRS:
        if path.startswith(private) and p.name not in PRIVATE_DIR_ALLOWED_NAMES:
            found.append(f"fichier dans le dossier privé {private}")

    if p.suffix.lower() in DOC_EXTENSIONS and not path.startswith(DOC_ALLOWED_DIRS):
        found.append(
            f"document {p.suffix.lower()} hors de {' ou '.join(DOC_ALLOWED_DIRS)}"
        )

    if p.name in SECRET_FILE_NAMES:
        found.append("fichier de secrets")

    if len(content) > MAX_BYTES:
        found.append(f"fichier de plus de {MAX_BYTES // (1024 * 1024)} Mo")

    if path not in CONTENT_SCAN_EXEMPT:
        text = content.decode("utf-8", errors="ignore")
        for marker in COPYRIGHT_MARKERS:
            if marker.search(text):
                found.append(f"mention de copyright de norme ({marker.pattern})")
                break
        for secret in SECRET_PATTERNS:
            if secret.search(text):
                found.append("secret probable (clé ou jeton)")
                break

    return found


def _git(*args: str) -> bytes:
    return subprocess.run(["git", *args], check=True, capture_output=True).stdout


def _paths(check_all: bool) -> list[str]:
    if check_all:
        raw = _git("ls-files", "-z")
    else:
        raw = _git("diff", "--cached", "--name-only", "--diff-filter=ACMR", "-z")
    return [p for p in raw.decode("utf-8").split("\0") if p]


def _content(path: str, check_all: bool) -> bytes:
    if check_all:
        try:
            with open(path, "rb") as handle:
                return handle.read()
        except OSError:
            return b""
    return _git("show", f":{path}")


def main() -> int:
    check_all = "--all" in sys.argv[1:]
    failures = []
    for path in _paths(check_all):
        for reason in violations(path, _content(path, check_all)):
            failures.append(f"  {path} : {reason}")
    if failures:
        print("Fichiers interdits détectés, opération bloquée :", file=sys.stderr)
        print("\n".join(failures), file=sys.stderr)
        print(
            "Voir CLAUDE.md (règles du domaine réglementaire). "
            "Ne pas contourner avec --no-verify.",
            file=sys.stderr,
        )
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
