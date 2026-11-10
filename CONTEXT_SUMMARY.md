# Résumé de contexte — point de reprise

## 1. Le projet en trois lignes

Assistant open source d'aide à la relecture réglementaire MDR pour ingénieurs
de dispositifs médicaux. Verdicts avec citations vérifiées, `non_trouve` par
défaut. Référence : `project.yaml`.

## 2. Règles à ne jamais oublier

Voir `CLAUDE.md`, section « Règles propres au domaine réglementaire » :
aucune norme sous copyright ni document réel dans le dépôt, aucune
affirmation réglementaire sans source du corpus, `review_status` validé par
l'utilisateur uniquement.

## 3. État technique

- 2026-11-10 : socle créé (protocole multi-agent, garde-fous git, tests du
  garde-fou).
- 2026-11-10 : MDR consolidé du 2026-11-09 (FR et EN) dans
  `corpus/public/mdr/`, provenance dans `SOURCE.yaml`. Découpage dans
  `src/openmedreg/corpus/eurlex.py` : 2 445 unités, identifiants identiques
  dans les deux langues (`art_10/4`, `anx_II/1.1/a`), aucun texte perdu,
  aucun avertissement. 43 tests. Sortie JSONL dans `build/` (non versionné).
- Pas encore de recherche, de modèle ni d'analyse d'écarts.
- Dépôt public : `github.com/easymoneymoncler/OpenMedReg-AI`, branche `main`,
  licence Apache-2.0.

## 4. Décisions en vigueur

- Premier périmètre : MDR, Annexe II puis Annexe I. ISO/IEC en mode
  « exemplaire apporté par l'utilisateur ».
- Jeu d'évaluation construit en phase 1, avant le moteur d'analyse.
- Pas de framework d'orchestration tant qu'il n'est pas nécessaire.
- Push direct sur `main` en fin de session, protégé par les hooks.

## 5. Prochaine tâche immédiate

Phase 1, suite : dossier technique fictif (dispositif inventé) avec écarts
injectés face à l'Annexe II, vérité terrain annotée par identifiant d'unité
(`anx_II/...`) et `review_status: non_relu`, puis banc d'évaluation.

À faire valider par l'utilisateur : la version consolidée retenue et la
liste des actes modificatifs (`corpus/public/mdr/SOURCE.yaml`).
