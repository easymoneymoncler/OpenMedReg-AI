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
- 2026-11-11 (après avis d'une autre IA) : second juge
  `src/openmedreg/engines/ollama.py` (modèle local, mêmes consignes dans
  `engines/prompt.py`) ; intervalles de confiance dans le banc ; guide
  `eval/NOUVEAU_CAS.md`. 71 tests. **Aucun juge n'a tourné pour de vrai** :
  pas de clé d'API, pas d'Ollama, et la machine n'a que 8 Go de mémoire.
- 2026-11-11 : masquage réversible `src/openmedreg/masking.py`, option
  `--mask` de `gap_analysis` (désactivée par défaut), règles du dossier
  fictif dans `tests/fixtures/` (hors du banc). Citations revérifiées
  contre le document d'origine après démasquage. 83 tests. **Effet sur les
  verdicts non mesuré.**

- 2026-11-11 : **première mesure réelle**, deux juges locaux sur un GPU
  loué (Ollama joint par tunnel SSH, `OLLAMA_HOST`), code du commit
  `e2b1fc5`, sans masque. Sur `fictif-therm-t1` : `qwen3.8:27b` 33/44,
  `gemma4:31b` 38/44 ; 0/13 faux `conforme` et 13/13 lacunes repérées pour
  les deux ; toutes les erreurs vont vers la sévérité. Écart entre modèles
  non significatif. Rapport et sorties brutes :
  `results/2026-11-11_fictif-therm-t1/` (`rapport.tex`). Vérité terrain
  toujours `non_relu` : ces chiffres mesurent un accord avec une annotation
  écrite par une IA.

## 4. Décisions en vigueur

- Premier périmètre : MDR, Annexe II puis Annexe I. ISO/IEC en mode
  « exemplaire apporté par l'utilisateur ».
- Jeu d'évaluation construit en phase 1, avant le moteur d'analyse.
- Pas de framework d'orchestration tant qu'il n'est pas nécessaire.
- Push direct sur `main` en fin de session, protégé par les hooks.

## 5. Prochaine tâche immédiate

Relecture par l'utilisateur des 13 unités où un modèle contredit la vérité
terrain, en commençant par les quatre communes aux deux modèles
(`anx_II/4/d`, `5/a`, `6.1/a`, `6.1/b/t2`). Puis mesure du juge API sur le
même cas. `prompt.py` reste inchangé d'ici là ; l'effet du masquage se
mesure à part, avec plusieurs séries par configuration.

La machine GPU louée a été terminée le 2026-11-11 vers 18:11 UTC ; le compte
du fournisseur n'a plus ni machine ni volume.

En attente de l'utilisateur :
- clé d'API dans `.env` (accord donné pour 44 appels) ;
- relecture de `eval/cases/fictif-therm-t1/ground_truth.yaml` ;
- cas rédigés par des humains (`eval/NOUVEAU_CAS.md`) ; les travaux
  étudiants regardés le 2026-11-11 sont des rapports de conception, pas des
  dossiers techniques ;
- confirmation du verdict `non_applicable` ;
- validation de `corpus/public/mdr/SOURCE.yaml` ;
- corrections de robustesse du masquage, à lancer ou non.
