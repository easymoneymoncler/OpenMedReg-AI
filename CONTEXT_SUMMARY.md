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
- 2026-11-11 : cas d'évaluation `eval/cases/fictif-therm-t1` (dossier fictif
  en français, 44 unités feuilles de l'Annexe II : 23 conforme, 6
  non_conforme, 7 non_trouve, 8 non_applicable ; tout en `non_relu`).
  `src/openmedreg/citations.py` (citation mot pour mot) et
  `src/openmedreg/evaluation.py` (mesures, règle de citation appliquée avant
  calcul). 56 tests.
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

Phase 2 : premier moteur d'analyse d'écarts face à l'Annexe II (recherche
des passages du document par unité, appel à un modèle, sortie au format de
prédiction de `eval/README.md`), mesuré sur `fictif-therm-t1`.

En attente de l'utilisateur :
- relecture de `eval/cases/fictif-therm-t1/ground_truth.yaml` ;
- confirmation du verdict `non_applicable` ;
- validation de `corpus/public/mdr/SOURCE.yaml` ;
- choix du modèle pour le premier moteur (local ou API).
