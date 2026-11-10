# Jeu d'évaluation

Dossiers techniques de dispositifs **fictifs**, avec lacunes volontaires et
vérité terrain annotée unité par unité. Aucun document réel ici.

## Cas disponibles

| Cas | Document | Périmètre | Unités | État de relecture |
| --- | --- | --- | --- | --- |
| `cases/fictif-therm-t1` | capteur de température cutané connecté (inventé) | Annexe II du MDR | 44 | `non_relu` |

Le contenu réglementaire des dossiers fictifs (classe, normes citées,
résultats) est inventé et n'a pas valeur d'exemple. La vérité terrain ne juge
que la présence et la cohérence des informations demandées par chaque unité.

## Verdicts

| Verdict | Signification |
| --- | --- |
| `conforme` | Le document contient un passage qui couvre ce que l'unité demande. |
| `non_conforme` | Le document traite le sujet, mais de façon incomplète ou contradictoire au regard du texte de l'unité. |
| `non_trouve` | Rien dans le document ne traite le sujet. C'est le verdict par défaut. |
| `non_applicable` | L'unité ne vise qu'un cas particulier (« dans le cas des dispositifs… », « s'il en existe ») et le document déclare que ce cas ne le concerne pas. Si le document se tait, le verdict est `non_trouve`. |

`non_applicable` est une proposition de l'agent, absente du YAML initial du
projet : à confirmer par l'utilisateur.

## Format de la vérité terrain

`ground_truth.yaml` contient une entrée par unité feuille du périmètre :

```yaml
- unit: anx_II/1.1/f            # identifiant d'unité du corpus
  expected: non_conforme
  evidence:                     # passages du document, mot pour mot
    - "Le dispositif relève de la classe IIa."
  rationale: "La classe est indiquée, mais aucune règle n'est citée ni justifiée."
  injected_gap: true            # vrai pour non_conforme et non_trouve
  review_status: non_relu       # seul l'utilisateur passe à « relu »
```

Les tests vérifient que chaque unité du périmètre est annotée et que chaque
passage cité existe mot pour mot dans le document.

## Mesurer

```bash
.venv/bin/python -m openmedreg.evaluation eval/cases/fictif-therm-t1 --baseline non_trouve
```

Avec des prédictions (une par ligne, JSONL) :

```json
{"unit": "anx_II/1.1/f", "verdict": "non_conforme", "requirement_quote": "la justification de la ou des règles de classification", "evidence": ["Le dispositif relève de la classe IIa."]}
```

Avant le calcul, la règle du projet est appliquée : un verdict autre que
`non_trouve` dont une citation n'existe pas mot pour mot, ou qui ne cite
aucun passage du document, est ramené à `non_trouve`.

| Mesure | Lecture |
| --- | --- |
| `false_conforme_rate` | Part des lacunes réelles déclarées `conforme`. L'erreur la plus grave ; une hausse bloque un changement. |
| `gap_recall` | Part des lacunes réelles signalées comme lacune. |
| `false_conforme_ci95`, `accuracy_ci95` | Intervalles de confiance à 95 % (méthode de Wilson). |
| `accuracy` | Part des verdicts exacts. |
| `citation_validity` | Part des citations qui existent mot pour mot. |
| `verdicts_downgraded_for_citation` | Verdicts ramenés à `non_trouve` par la règle de citation. |

Repères sur `fictif-therm-t1` : répondre toujours `non_trouve` donne une
exactitude de 7/44 (16 %) avec un taux de faux `conforme` nul ; un moteur
n'a d'intérêt que s'il fait mieux en exactitude sans dégrader ce taux.

## Limites

- **Un seul cas, écrit et annoté par une IA.** Les lacunes sont plus nettes
  que dans un dossier réel et les annotations n'ont pas été relues par un
  expert.
- **Avantage à la même famille de modèles.** Le dossier et sa vérité terrain
  ont été produits par un modèle Claude : un juge Claude est jugé sur un
  texte qui lui ressemble. Un écart entre un juge Claude et un autre modèle
  mesuré sur ce seul cas surestime probablement l'avantage du premier.
- **Trop peu d'unités pour départager finement.** Avec 13 lacunes, une seule
  erreur déplace le taux de faux `conforme` de près de 8 points. Le banc
  publie l'intervalle de confiance à 95 % : zéro faux `conforme` sur 13
  reste compatible avec un taux réel allant jusqu'à 23 %. Deux moteurs dont
  les intervalles se recouvrent ne sont pas départagés.

Les résultats mesurés ici ne se généralisent pas. Pour y remédier :
[NOUVEAU_CAS.md](NOUVEAU_CAS.md).
