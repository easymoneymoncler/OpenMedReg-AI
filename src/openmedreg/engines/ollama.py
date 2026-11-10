"""Juge reposant sur un modèle local servi par Ollama. Rien ne quitte la machine.

Bibliothèque standard uniquement. Le schéma JSON est passé à Ollama, qui
contraint la génération : la réponse est toujours un JSON valide.
"""
from __future__ import annotations

import json
import os
import urllib.request

from openmedreg.engines.prompt import INSTRUCTIONS, OUTPUT_SCHEMA, build_user_message

DEFAULT_HOST = "http://localhost:11434"


def _post(url: str, payload: dict, timeout: float) -> dict:
    request = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
    )
    with urllib.request.urlopen(request, timeout=timeout) as response:
        return json.loads(response.read())


class OllamaJudge:
    def __init__(
        self,
        model: str,
        host: str | None = None,
        num_ctx: int = 16384,
        timeout: float = 600.0,
        post=_post,
    ):
        self.model = model
        self.host = (host or os.environ.get("OLLAMA_HOST") or DEFAULT_HOST).rstrip("/")
        if not self.host.startswith("http"):
            self.host = "http://" + self.host
        # Sans num_ctx explicite, Ollama tronque en silence un document long.
        self.num_ctx = num_ctx
        self.timeout = timeout
        self._post = post
        self.usage = {"requests": 0, "input_tokens": 0, "output_tokens": 0}

    def judge(self, requirement: dict, document: str) -> dict:
        response = self._post(
            f"{self.host}/api/chat",
            {
                "model": self.model,
                "stream": False,
                "format": OUTPUT_SCHEMA,
                "options": {"temperature": 0, "num_ctx": self.num_ctx},
                "messages": [
                    {
                        "role": "system",
                        "content": f"{INSTRUCTIONS}\n\n<document>\n{document}\n</document>",
                    },
                    {"role": "user", "content": build_user_message(requirement)},
                ],
            },
            self.timeout,
        )
        self.usage["requests"] += 1
        self.usage["input_tokens"] += response.get("prompt_eval_count") or 0
        self.usage["output_tokens"] += response.get("eval_count") or 0
        if (response.get("prompt_eval_count") or 0) >= self.num_ctx:
            return {
                "verdict": "non_trouve",
                "rationale": f"document plus long que la fenêtre de contexte ({self.num_ctx} jetons)",
            }
        return json.loads(response["message"]["content"])
