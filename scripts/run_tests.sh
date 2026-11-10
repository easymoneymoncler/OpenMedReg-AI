#!/usr/bin/env bash
# Lance les tests unitaires puis le contrôle des fichiers interdits sur tout
# le dépôt, et affiche un résumé pass/fail.
#
# Usage : ./scripts/run_tests.sh

set -uo pipefail
cd "$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

if [ ! -x ".venv/bin/python" ]; then
  echo "Environnement virtuel introuvable (.venv/bin/python) — lancer d'abord :"
  echo "  python3 -m venv .venv && .venv/bin/pip install -r requirements-dev.txt"
  exit 1
fi

echo "== 1/2 : tests unitaires (pytest) =="
.venv/bin/python -m pytest tests/ -q
PYTEST_STATUS=$?
echo

echo "== 2/2 : contrôle des fichiers interdits (tout le dépôt) =="
.venv/bin/python scripts/check_staged.py --all
GUARD_STATUS=$?
echo

echo "== Résumé =="
[ $PYTEST_STATUS -eq 0 ] && echo "  Tests unitaires    : OK" || echo "  Tests unitaires    : ÉCHEC"
[ $GUARD_STATUS -eq 0 ] && echo "  Fichiers interdits : OK" || echo "  Fichiers interdits : ÉCHEC"

[ $PYTEST_STATUS -eq 0 ] && [ $GUARD_STATUS -eq 0 ]
