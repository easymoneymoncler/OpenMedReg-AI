"""Consigne une demande utilisateur, sous le verrou de scripts/with_ai_lock.sh."""
import argparse
from datetime import datetime, timezone
import os
from pathlib import Path
import uuid

import yaml

AGENTS = ("CLAUDE", "CHATGPT", "GEMINI")
ROOT = Path(__file__).resolve().parents[1]

p = argparse.ArgumentParser(description=__doc__)
p.add_argument("--id", default=None)
p.add_argument("--summary", required=True)
p.add_argument("--authorization", required=True)
p.add_argument("--next-action", required=True)
p.add_argument("--status", choices=["open", "done", "awaiting_user", "blocked"], default="open")
p.add_argument("--outcome", default="")
a = p.parse_args()

agent = os.environ.get("AI_AGENT")
owner = ROOT / ".ai/LOCKDIR/owner"
if agent not in AGENTS or not owner.exists() or f"agent={agent}" not in owner.read_text().splitlines():
    p.error("Utiliser : AI_AGENT=<AGENT> bash scripts/with_ai_lock.sh .venv/bin/python scripts/record_prompt.py ...")

path = ROOT / ".ai/PROMPT_LOG.yaml"
data = yaml.safe_load(path.read_text()) if path.exists() else None
data = data or {"schema": 1, "entries": []}
now = datetime.now(timezone.utc)
identity = a.id or f"{now:%Y%m%dT%H%M%SZ}-{agent}-{uuid.uuid4().hex[:8]}"
entry = dict(
    id=identity,
    at=now.isoformat(),
    receiver=agent,
    summary=a.summary,
    authorization=a.authorization,
    status=a.status,
    outcome=a.outcome,
    next_action=a.next_action,
)
old = next((e for e in data["entries"] if e["id"] == identity), None)
if old:
    if old["receiver"] != agent:
        p.error("Impossible de remplacer l'entrée d'un autre agent")
    entry["at"] = old["at"]
    old.update(entry)
else:
    data["entries"].append(entry)

temp = path.with_suffix(".yaml.tmp")
try:
    temp.write_text(yaml.safe_dump(data, allow_unicode=True, sort_keys=False))
    yaml.safe_load(temp.read_text())
    os.replace(temp, path)
    yaml.safe_load(path.read_text())
finally:
    temp.unlink(missing_ok=True)
print(identity)
