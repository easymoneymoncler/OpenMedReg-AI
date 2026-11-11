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

## 2026-11-11 — Reprise après clear

- Revérifié : tests et contrôle des fichiers interdits OK ; pas de `.env`,
  Ollama absent, aucun verrou, dépôt à jour avec `origin/main`.
- Rien lancé : toutes les suites sont dans `awaiting_user` de
  `.ai/SHARED_STATE.yaml`.

## 2026-11-11 — Outillage pour le juge local sur GPU loué

- Fait : plugin `runpod` 2.0.0 installé pour Claude Code (portée
  utilisateur, rien dans le dépôt), après vérification de l'origine du
  dépôt de plugins.
- Non fait : compte, crédit, connexion OAuth (à l'utilisateur) ; aucune
  machine lancée, aucun modèle téléchargé.
- Fait repris d'une session annexe, revérifié : `engines/ollama.py` lit
  `OLLAMA_HOST`, donc aucun changement de code pour un Ollama distant.

## 2026-11-11 — Masquage réversible

- Ajouté : `src/openmedreg/masking.py`, option `--mask` et `--mask-map` de
  `gap_analysis.py`, `tests/test_masking.py`,
  `tests/fixtures/masquage_fictif-therm-t1.yaml`, `*.masking.json` ignoré.
- Mesuré : 83 tests passent. Sur le cas fictif, 10 occurrences masquées,
  aller-retour identique au fichier d'origine ; avec un juge qui répond la
  vérité terrain sur le document masqué, l'exactitude reste de 1.
- Non vérifié : aucun juge réel ; l'effet du masquage sur les verdicts est
  inconnu. Fait dans une session annexe, modifications non commitées.

## 2026-11-11 — Première mesure : deux juges locaux

- Ajouté : `results/2026-11-11_fictif-therm-t1/` (rapport LaTeX, 88
  prédictions, sorties du banc, fiche des modèles) ; exception dans
  `.gitignore` pour les campagnes datées.
- Mesuré, code du commit `e2b1fc5`, sans masque : `qwen3.8:27b` 33/44,
  `gemma4:31b` 38/44 ; 0/13 faux `conforme` et 13/13 lacunes repérées pour
  les deux ; accord entre modèles sur 35 unités.
- Non vérifié par un humain : la vérité terrain (`non_relu`). L'écart entre
  les deux modèles n'est pas significatif sur 44 unités.
- Hors dépôt : clé SSH dédiée, plugin du fournisseur, journal du serveur
  (`build/runs/serveur/`).
