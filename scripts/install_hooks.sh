#!/usr/bin/env bash
# Active les hooks versionnés de .githooks/ (à lancer une fois après chaque clone).
set -euo pipefail
cd "$(dirname "$0")/.."
git config core.hooksPath .githooks
chmod +x .githooks/* scripts/*.sh scripts/check_staged.py
echo "Hooks activés : $(git config core.hooksPath)"
