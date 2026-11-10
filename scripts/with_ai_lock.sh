#!/usr/bin/env bash
# Exécute une commande sous le verrou atomique du dépôt (un seul agent écrivain).
set -euo pipefail
cd "$(dirname "$0")/.."
case "${AI_AGENT:-}" in CLAUDE|CHATGPT|GEMINI) ;; *) echo 'Définir AI_AGENT=CLAUDE, CHATGPT ou GEMINI' >&2; exit 64;; esac
mkdir -p .ai
if ! mkdir .ai/LOCKDIR 2>/dev/null; then
  echo 'Dépôt déjà verrouillé ; aucune modification faite.' >&2
  cat .ai/LOCKDIR/owner >&2 || true
  exit 73
fi
trap 'rm -f .ai/LOCKDIR/owner; rmdir .ai/LOCKDIR' EXIT
trap 'exit 130' INT
trap 'exit 143' TERM HUP
{ printf 'agent=%s\npid=%s\n' "$AI_AGENT" "$$"; date -u '+time=%Y-%m-%dT%H:%M:%SZ'; git rev-parse HEAD 2>/dev/null || echo 'head=aucun-commit'; } > .ai/LOCKDIR/owner
"$@"
