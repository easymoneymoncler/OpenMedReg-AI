# Instructions permanentes — OpenMedReg-AI

Projet open source au long cours : assistant d'aide à la relecture
réglementaire (MDR) pour ingénieurs de dispositifs médicaux. Périmètre,
principes techniques et feuille de route : `project.yaml`, qui fait foi.

Le dépôt est édité par plusieurs agents (Claude Code, ChatGPT/Codex, Gemini)
coordonnés via `.ai/`. Le 2026-11-10, l'utilisateur a demandé que ce projet
reprenne le mode de fonctionnement de NeuroMetrics, y compris le commit et le
push automatiques en fin de session, **sans confirmation à chaque fois**.
Cette instruction prévaut sur le comportement par défaut qui consisterait à
demander avant un `git push`, une fois le dépôt distant créé.

## Coordination multi-agent — à chaque prompt, avant toute réponse ou action

Lire et appliquer **AGENTS.md**, source unique des règles de coordination :
lecture croisée de l'état et du journal, consignation compacte de chaque
demande, verrou avant écriture, sauvegarde avant clear ou relais. Ne pas
maintenir une seconde version de ces règles ici.

## Règles propres au domaine réglementaire (non négociables)

1. **Aucun texte de norme sous copyright dans le dépôt** : ISO, IEC, EN, AFNOR
   et équivalents. Ni texte intégral, ni extraits, ni reformulation clause par
   clause, ni embeddings, ni dans le code, les tests, les prompts ou les
   journaux `.ai/`. Seuls le numéro et le titre court d'une clause sont
   admis. Les exemplaires de l'utilisateur vivent dans `corpus/private/`,
   ignoré par git.
2. **Aucun document client ou réel** dans le dépôt. Les jeux de test sont des
   dispositifs fictifs, dans `eval/`. Les documents réels vivent dans
   `data/client/`, ignoré par git.
3. **Aucune affirmation réglementaire tirée de la mémoire du modèle.** Tout
   contenu réglementaire écrit dans le dépôt (liste de contrôle, exigence,
   vérité terrain du jeu d'évaluation) cite sa source : fichier du corpus
   public et article ou point d'annexe. Si la source n'est pas dans le
   corpus, l'ajouter d'abord ou signaler le manque à l'utilisateur.
4. **Statut de relecture.** Tout élément réglementaire porte un champ
   `review_status` : `non_relu` à la création par un agent, `relu` uniquement
   après validation explicite de l'utilisateur (qui a l'expertise RA). Un
   agent ne passe jamais lui-même un élément à `relu`.
5. **Positionnement.** L'outil aide à la relecture ; il ne délivre pas d'avis
   de conformité. Aucun texte du dépôt (README, rapports générés, messages)
   ne doit suggérer le contraire, ni avancer un gain chiffré non mesuré.
6. **Verdicts.** Sans citation vérifiée de l'exigence et du passage du
   document, le verdict est `non_trouve`. Toute modification du pipeline est
   évaluée sur le banc d'évaluation ; une hausse du taux de faux `conforme`
   bloque le changement.

## En fin de session (automatique, sans demander confirmation)

1. **Tester** : `./scripts/run_tests.sh` (tests unitaires et contrôle des
   fichiers interdits sur tout le dépôt). Ne rien pousser si le script échoue.
2. **Mettre à jour `DEVLOG.md`** : entrée datée du jour (objectifs,
   décisions, problèmes, prochaines étapes).
3. **Mettre à jour `CONTEXT_SUMMARY.md`** : sections « État technique » et
   « Prochaine tâche immédiate » ; ce fichier sert de point de reprise après
   un `/clear`.
4. **Mettre à jour `project.yaml`** si une tâche de la feuille de route est
   terminée ou si le périmètre a changé sur décision de l'utilisateur.
5. **Committer et pousser** sur `main`, dans un commit séparé et clair, après
   lecture de `git status` et `git diff`. Jamais de `--force`, jamais de
   `--no-verify` : les hooks de `.githooks/` sont le garde-fou qui rend ce
   push automatique acceptable sur un dépôt public.

## Toujours soumis à confirmation explicite

- Création du dépôt GitHub, changement de visibilité, publication d'une
  version, ajout d'un collaborateur ou d'un secret.
- Toute action destructive : `git push --force`, `git reset --hard`,
  suppression de fichiers ou de branches, réécriture d'historique.
- Tout contournement d'un hook, y compris pour un faux positif : corriger la
  règle dans `scripts/check_staged.py` avec l'accord de l'utilisateur.
- Tout ajout d'un fichier dans `corpus/public/` dont la licence de
  réutilisation n'est pas établie.
- Tout téléchargement volumineux (modèles, corpus de plus de 1 Go) : vérifier
  `df -H /` avant.

## Environnement

- Python via `.venv/` (`python3 -m venv .venv && .venv/bin/pip install -r requirements-dev.txt`).
- Hooks git : `./scripts/install_hooks.sh` après chaque clone.
