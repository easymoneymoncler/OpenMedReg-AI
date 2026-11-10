"""Juge reposant sur l'API Claude (SDK officiel ``anthropic``)."""
from __future__ import annotations

import json

from openmedreg.engines.prompt import INSTRUCTIONS, OUTPUT_SCHEMA, build_user_message

FALLBACK_BETA = "server-side-fallback-2026-07-01"


class ClaudeJudge:
    """Un appel par exigence ; le document est placé dans le préfixe mis en cache."""

    def __init__(
        self,
        model: str = "claude-opus-5-5",
        effort: str = "medium",
        client=None,
        refusal_fallback: bool = True,
    ):
        if client is None:
            import anthropic

            client = anthropic.Anthropic()
        self.client = client
        self.model = model
        self.effort = effort
        self.refusal_fallback = refusal_fallback
        self.usage = {
            "requests": 0,
            "input_tokens": 0,
            "output_tokens": 0,
            "cache_read_input_tokens": 0,
            "cache_creation_input_tokens": 0,
        }

    def judge(self, requirement: dict, document: str) -> dict:
        request = dict(
            model=self.model,
            max_tokens=16000,
            output_config={
                "effort": self.effort,
                "format": {"type": "json_schema", "schema": OUTPUT_SCHEMA},
            },
            system=[
                {"type": "text", "text": INSTRUCTIONS},
                {
                    "type": "text",
                    "text": f"<document>\n{document}\n</document>",
                    # Le document ne change pas d'une exigence à l'autre.
                    "cache_control": {"type": "ephemeral"},
                },
            ],
            messages=[{"role": "user", "content": build_user_message(requirement)}],
        )
        if self.refusal_fallback:
            # En cas de refus du modèle, l'API rejoue la requête sur un modèle de repli.
            response = self.client.beta.messages.create(
                betas=[FALLBACK_BETA], fallbacks="default", **request
            )
        else:
            response = self.client.messages.create(**request)
        self._count(response)

        if response.stop_reason == "refusal":
            return {"verdict": "non_trouve", "rationale": "le modèle a refusé de répondre"}
        if response.stop_reason == "max_tokens":
            return {"verdict": "non_trouve", "rationale": "réponse tronquée (max_tokens)"}
        text = next((b.text for b in response.content if b.type == "text"), "")
        return json.loads(text)

    def _count(self, response) -> None:
        self.usage["requests"] += 1
        usage = getattr(response, "usage", None)
        for key in list(self.usage)[1:]:
            self.usage[key] += getattr(usage, key, 0) or 0
