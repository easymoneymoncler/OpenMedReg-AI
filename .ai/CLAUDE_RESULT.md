# Résultats CLAUDE

## 2026-11-10 — Socle du dépôt

- Créé : `project.yaml`, `CLAUDE.md`, `AGENTS.md`, `.ai/`, `scripts/`
  (verrou, journal, tests, garde-fou), `.githooks/`, `.gitignore`,
  arborescence `corpus/`, `data/client/`, `eval/`.
- Vérifié : voir l'entrée du jour dans `.ai/PROMPT_LOG.yaml` pour le
  résultat des tests et de l'essai du hook.
- Publié : dépôt GitHub public `easymoneymoncler/OpenMedReg-AI`, licence
  Apache-2.0, premier commit poussé sur `main`.

## 2026-11-10 — Phase 1 : ingestion du MDR

- Ajouté : `corpus/public/mdr/` (XHTML FR et EN, `SOURCE.yaml`),
  `src/openmedreg/corpus/eurlex.py`, `scripts/fetch_eurlex.py`,
  `tests/test_eurlex_mdr.py`, `pyproject.toml`.
- Mesuré : 2 445 unités par langue ; ensembles d'identifiants FR et EN
  identiques ; 0 avertissement ; texte de chaque article et annexe repris
  intégralement ; 43 tests passent (`./scripts/run_tests.sh`).
- Non vérifié par un humain : le choix de la version consolidée du
  2026-11-09 et la liste des actes modificatifs (`review_status: non_relu`).

## 2026-11-11 — Cas fictif et banc d'évaluation

- Ajouté : `eval/cases/fictif-therm-t1/` (dossier, vérité terrain),
  `src/openmedreg/citations.py`, `src/openmedreg/evaluation.py`,
  `tests/test_eval_case.py`, `eval/README.md` réécrit.
- Mesuré : 56 tests passent. Repère « toujours non_trouve » : exactitude
  7/44, taux de faux conforme 0, rappel des lacunes 1. Repère « oracle » :
  exactitude 1, validité des citations 1.
- Non vérifié par un humain : les 44 annotations (`non_relu`) et le verdict
  `non_applicable`, proposé par l'agent.

## 2026-11-11 — Premier moteur d'analyse

- Ajouté : `src/openmedreg/gap_analysis.py`, `src/openmedreg/engines/claude.py`,
  `tests/test_gap_analysis.py`, `.env.example`.
- Mesuré : 67 tests passent, aucun n'appelle le réseau. Avec un juge qui
  répond la vérité terrain, la chaîne complète donne une exactitude de 1.
- Non vérifié : aucun appel réel à l'API (pas de clé). Les performances du
  moteur sur le cas fictif sont inconnues.

## 2026-11-11 — Suites de l'avis externe

- Ajouté : `engines/ollama.py`, `engines/prompt.py` (consignes communes),
  intervalles de Wilson dans `evaluation.py`, `eval/NOUVEAU_CAS.md`.
- Mesuré : 71 tests passent. Repère « toujours non_trouve » : 0/13 faux
  conforme, intervalle à 95 % de 0 à 23 %.
- Constaté : machine de développement Apple M2, 8 Go de mémoire, Ollama non
  installé. Le juge local n'a tourné que contre un faux serveur.
