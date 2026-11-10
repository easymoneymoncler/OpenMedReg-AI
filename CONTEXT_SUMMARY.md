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
- 2026-11-11 : moteur `src/openmedreg/gap_analysis.py` (choix des unités
  feuilles et de leur contexte, règle de citation) et juge
  `src/openmedreg/engines/claude.py` (un appel par unité, sortie JSON
  contrainte, document dans le préfixe mis en cache, repli sur refus).
  67 tests, tous sans réseau. **Jamais exécuté contre l'API réelle** : pas
  de clé d'API sur la machine.
- Dépôt public : `github.com/easymoneymoncler/OpenMedReg-AI`, branche `main`,
  licence Apache-2.0.

## 4. Décisions en vigueur

- Premier périmètre : MDR, Annexe II puis Annexe I. ISO/IEC en mode
  « exemplaire apporté par l'utilisateur ».
- Jeu d'évaluation construit en phase 1, avant le moteur d'analyse.
- Pas de framework d'orchestration tant qu'il n'est pas nécessaire.
- Push direct sur `main` en fin de session, protégé par les hooks.

## 5. Prochaine tâche immédiate

Mesurer le moteur sur `fictif-therm-t1` : il faut une clé d'API dans `.env`
et l'accord de l'utilisateur sur le coût (44 appels à claude-opus-5-5).

En attente de l'utilisateur :
- il soumet le choix « API Claude ou modèle local » à une autre IA pour avis ;
- clé d'API et accord sur le coût de la première mesure ;
- relecture de `eval/cases/fictif-therm-t1/ground_truth.yaml` ;
- confirmation du verdict `non_applicable` ;
- validation de `corpus/public/mdr/SOURCE.yaml`.
