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
  garde-fou). Aucun code de pipeline.
- Dépôt public : `github.com/easymoneymoncler/OpenMedReg-AI`, branche `main`,
  licence Apache-2.0.

## 4. Décisions en vigueur

- Premier périmètre : MDR, Annexe II puis Annexe I. ISO/IEC en mode
  « exemplaire apporté par l'utilisateur ».
- Jeu d'évaluation construit en phase 1, avant le moteur d'analyse.
- Pas de framework d'orchestration tant qu'il n'est pas nécessaire.
- Push direct sur `main` en fin de session, protégé par les hooks.

## 5. Prochaine tâche immédiate

Phase 1 : ingestion du MDR depuis EUR-Lex, découpé par article et point
d'annexe, puis dossier technique fictif annoté.
