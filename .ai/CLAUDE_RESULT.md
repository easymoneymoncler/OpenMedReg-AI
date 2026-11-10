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
