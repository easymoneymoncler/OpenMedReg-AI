# OpenMedReg-AI

Assistant open source d'aide à la relecture réglementaire pour les ingénieurs
de dispositifs médicaux. Il confronte un document interne à une exigence du
règlement (UE) 2017/745 (MDR) et rend un verdict accompagné de citations
vérifiables : `conforme`, `non_conforme` ou `non_trouve`.

> **Ce que ce projet n'est pas.** Il ne délivre pas d'avis de conformité et ne
> remplace pas une personne compétente en affaires réglementaires. Chaque
> verdict doit être relu.

## État

Phase 1 en cours. Le MDR consolidé (version du 9 novembre 2026, français et
anglais) est dans le corpus et se découpe en 2 445 unités citables. Aucun
moteur d'analyse n'existe encore. Périmètre et feuille de route :
[project.yaml](project.yaml).

## Principes

- **Citation obligatoire.** Pas de verdict sans l'article cité et le passage
  exact du document ; à défaut, `non_trouve`.
- **Sources libres dans le dépôt, normes payantes chez vous.** Le MDR et les
  guides MDCG sont versionnés. Les normes ISO/IEC sont sous copyright : vous
  ingérez en local votre propre exemplaire, rien n'en est publié.
- **Hors ligne possible.** Le moteur doit fonctionner avec un modèle local
  pour les documents confidentiels.
- **Mesuré.** Tout changement est évalué sur un dossier technique fictif
  annoté.

## Installation (développement)

```bash
python3 -m venv .venv && .venv/bin/pip install -r requirements-dev.txt -e .
```

```bash
./scripts/install_hooks.sh
```

```bash
./scripts/run_tests.sh
```

## Découper le MDR en unités citables

```bash
.venv/bin/python -m openmedreg.corpus.eurlex corpus/public/mdr/02017R0745-20261109.fr.xhtml --out build/mdr.fr.jsonl
```

Chaque article, paragraphe, point d'annexe et élément de liste reçoit un
identifiant stable, identique en français et en anglais : `art_10/4` pour
l'article 10, paragraphe 4 ; `anx_II/1.1/a` pour l'annexe II, section 1.1,
point a). Provenance et limites du texte : [SOURCE.yaml](corpus/public/mdr/SOURCE.yaml).

## Organisation

| Chemin | Contenu |
| --- | --- |
| `corpus/public/` | Textes librement réutilisables (MDR, MDCG) |
| `corpus/private/` | Vos normes achetées — ignoré par git |
| `data/client/` | Vos documents réels — ignoré par git |
| `eval/` | Dossiers fictifs et vérité terrain |
| `src/openmedreg/` | Code du projet (découpage du corpus pour l'instant) |
| `scripts/` | Tests, garde-fous git, coordination des agents |
| `.ai/` | État partagé et journal des agents |

## Développement assisté par agents

Ce dépôt est développé avec plusieurs agents IA coordonnés. Les règles sont
dans [CLAUDE.md](CLAUDE.md) et [AGENTS.md](AGENTS.md).

## Licence

[Apache-2.0](LICENSE).
