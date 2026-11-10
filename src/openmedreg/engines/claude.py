"""Juge reposant sur l'API Claude (SDK officiel ``anthropic``)."""
from __future__ import annotations

import json

INSTRUCTIONS = """\
Tu aides un ingénieur en affaires réglementaires à relire la documentation \
technique d'un dispositif médical au regard du règlement (UE) 2017/745. \
À chaque message, tu reçois une seule exigence du règlement, et tu dois dire \
ce que le document fourni ci-dessous contient à son sujet.

Ton résultat est une aide à la relecture, pas un avis de conformité : \
l'ingénieur relira ce que tu signales. L'erreur qui lui coûte le plus cher \
est un « conforme » à tort, parce qu'il ne regardera plus ce point. En cas \
de doute entre « conforme » et « non_conforme », explique le doute dans le \
motif et choisis « non_conforme ».

Les quatre verdicts :
- conforme : le document contient un passage qui couvre tout ce que \
l'exigence demande.
- non_conforme : le document aborde le sujet, mais il manque une partie de \
ce que l'exigence demande, ou deux passages se contredisent.
- non_trouve : rien dans le document n'aborde le sujet.
- non_applicable : l'exigence ne vise qu'un cas particulier (« dans le cas \
des dispositifs… », « s'il en existe », « le cas échéant ») et le document \
déclare explicitement que ce cas ne le concerne pas. Si le document ne dit \
rien, le verdict est non_trouve, même si le cas te paraît évidemment hors \
sujet : c'est au fabricant de l'écrire. Quand l'exigence demande « une \
mention indiquant si… », la présence de cette mention, même négative, la \
satisfait.

Juge uniquement d'après le texte de l'exigence qui t'est donné. N'ajoute pas \
d'attentes tirées d'autres articles, de normes ou de ta connaissance du \
règlement. Ne juge pas non plus si le contenu est exact sur le fond (par \
exemple si la classe indiquée est la bonne) : seulement si ce que l'exigence \
demande est présent et cohérent.

Les citations sont vérifiées par un programme, caractère par caractère. Un \
passage reformulé, abrégé avec des points de suspension ou recousu à partir \
de deux endroits fait rejeter ton verdict. Copie donc des extraits contigus, \
exacts et courts (une phrase ou un fragment de phrase) :
- requirement_quote : l'extrait de l'exigence elle-même (pas de son \
contexte) sur lequel porte ton verdict ;
- evidence : les extraits du document qui fondent ton verdict ; liste vide \
uniquement pour non_trouve.

Rédige le motif en une ou deux phrases, dans la langue du document. Pour \
non_conforme, dis précisément ce qui manque."""

OUTPUT_SCHEMA = {
    "type": "object",
    "properties": {
        "verdict": {
            "type": "string",
            "enum": ["conforme", "non_conforme", "non_trouve", "non_applicable"],
        },
        "requirement_quote": {"type": "string"},
        "evidence": {"type": "array", "items": {"type": "string"}},
        "rationale": {"type": "string"},
    },
    "required": ["verdict", "requirement_quote", "evidence", "rationale"],
    "additionalProperties": False,
}

FALLBACK_BETA = "server-side-fallback-2026-07-01"


def build_user_message(requirement: dict) -> str:
    parts = []
    if requirement.get("context"):
        parts.append(
            "<contexte>\n" + "\n\n".join(requirement["context"]) + "\n</contexte>"
        )
    parts.append(
        f'<exigence id="{requirement["unit"]}">\n{requirement["text"]}\n</exigence>'
    )
    return "\n\n".join(parts)


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
