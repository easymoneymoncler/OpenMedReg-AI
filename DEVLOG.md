# Journal de développement

Gabarit d'entrée : objectifs, décisions, problèmes, prochaines étapes.

## 2026-11-10 — Socle du dépôt (CLAUDE)

**Objectifs.** Évaluer la faisabilité à partir du YAML initial et poser la
structure du dépôt sur le modèle de NeuroMetrics.

**Décisions.**
- Les normes ISO/IEC sont sous copyright : elles sortent du dépôt, mode
  « exemplaire apporté par l'utilisateur ». Le corpus versionné commence par
  le MDR.
- Périmètre du premier cas d'usage réduit à l'Annexe II du MDR.
- Le jeu d'évaluation passe en phase 1.
- Le « score de confiance minimum » est remplacé par la citation obligatoire
  vérifiée mécaniquement.
- Modèle économique et gain chiffré retirés du périmètre actuel.
- Push automatique conservé, protégé par des hooks pre-commit et pre-push.
- Protocole de coordination étendu à trois agents (CLAUDE, CHATGPT, GEMINI).

**Problèmes.** Aucun.

**Publication.** Dépôt GitHub public créé avec l'accord de l'utilisateur,
licence Apache-2.0 ajoutée, premier commit poussé.

**Prochaines étapes.** Phase 1 : ingestion du MDR, jeu d'évaluation fictif.

## 2026-11-10 — Phase 1 : ingestion du MDR (CLAUDE)

**Objectifs.** Mettre le MDR dans le corpus public et le découper en unités
citables.

**Fait.**
- Texte consolidé `02017R0745-20261109` (FR et EN) récupéré depuis le dépôt
  de l'Office des publications ; `scripts/fetch_eurlex.py` redonne les mêmes
  empreintes SHA-256.
- `src/openmedreg/corpus/eurlex.py` : reconstruction de la hiérarchie
  (articles, paragraphes, alinéas, chapitres et parties d'annexe, sections
  numérotées, points a), i), tirets). 2 445 unités par langue.
- Contrôles : identifiants uniques et identiques FR/EN, aucun caractère du
  texte perdu, liens parent-enfant cohérents.

**Décisions.**
- Source XHTML versionnée ; le JSONL dérivé est régénéré dans `build/`.
- Identifiants indépendants de la langue : « 1 bis » et « 1a » donnent
  `1a` ; les tirets sont numérotés `t1`, `t2` ; les titres sans numéro `h1`.
- Le chapitre ou la partie d'annexe figure dans l'identifiant
  (`anx_I/chap_II/10.4.1`) car la numérotation recommence dans certaines
  annexes (annexe VI, parties A à C).

**Problèmes rencontrés.**
- Article 123(3) : le point h) a été supprimé par un acte modificatif, si
  bien que la lettre « i) » suit une liste romaine « i), ii), iii) ». Réglé
  par une règle dédiée et un test.

**Limites.** Le texte consolidé n'a pas d'effet juridique et ne contient pas
les considérants. Le découpage n'a été essayé que sur le MDR.

**Prochaines étapes.** Dossier technique fictif annoté, puis banc
d'évaluation.

## 2026-11-11 — Phase 1 : cas fictif et banc d'évaluation (CLAUDE)

**Objectifs.** Disposer d'un moyen de mesurer un moteur avant de l'écrire.

**Fait.**
- `eval/cases/fictif-therm-t1/dossier.md` : documentation technique d'un
  capteur de température inventé, avec 13 lacunes volontaires.
- `ground_truth.yaml` : un verdict attendu pour chacune des 44 unités
  feuilles de l'Annexe II, avec passages cités mot pour mot et motif.
- `citations.py` : comparaison exacte, tolérante aux seuls espaces,
  apostrophes et formes Unicode.
- `evaluation.py` : taux de faux « conforme », rappel des lacunes,
  exactitude, validité des citations ; un verdict mal cité est ramené à
  `non_trouve` avant le calcul.

**Décisions.**
- Ajout proposé d'un quatrième verdict, `non_applicable`, pour les unités
  qui ne visent qu'un cas particulier. À confirmer par l'utilisateur.
- Une unité qui demande « une mention indiquant si… » est `conforme` dès que
  la mention existe, même négative (annexe II, 6.2 a) et b)).
- Le périmètre d'un cas est l'ensemble des unités feuilles ; un test échoue
  si une unité n'est pas annotée.

**Limites.** Dossier et annotations écrits par le même agent, non relus ;
lacunes plus nettes que dans un dossier réel ; un seul cas, en français.

**Prochaines étapes.** Relecture des annotations par l'utilisateur ; premier
moteur d'analyse mesuré sur ce cas.

## 2026-11-11 — Phase 2 : premier moteur d'analyse (CLAUDE)

**Objectifs.** Écrire le moteur d'analyse d'écarts avec un juge API Claude,
choisi par l'utilisateur pour ce premier moteur.

**Fait.**
- `gap_analysis.py` : indépendant du fournisseur. Sélectionne les unités
  feuilles, joint le texte introductif de leurs parents, applique la règle
  de citation et conserve le verdict brut du modèle à côté du verdict retenu.
- `engines/claude.py` : un appel par unité, sortie JSON contrainte par
  schéma, document placé dans le préfixe mis en cache, repli côté serveur en
  cas de refus, compteur de jetons.
- Tests avec un faux client : forme de la requête, refus, rejet des
  citations inventées, panne d'un appel sans perte des autres verdicts.

**Limites.** Aucun appel réel n'a été fait : la forme de la requête est
vérifiée contre la signature du SDK (anthropic 2.8.0), pas contre l'API.
Le document entier est envoyé à chaque appel, ce qui ne tiendra pas pour un
dossier de plusieurs centaines de pages.

**En suspens.** L'utilisateur demande un avis externe sur le choix API ou
modèle local avant d'aller plus loin.

## 2026-11-11 — Avis externe sur le choix du modèle (CLAUDE)

**Contexte.** L'utilisateur a soumis le choix « API Claude ou modèle local »
à une autre IA et demandé d'en juger la pertinence.

**Retenu.**
- Risque de concevoir pour un grand modèle : fondé. Réponse : un juge local
  écrit tout de suite, avec les mêmes consignes, pour mesurer les deux dès
  la première fois.
- Biais du cas écrit par une IA : fondé, et plus précis que ce qui était
  noté : il avantage un juge de la même famille de modèles.
- Échantillon trop petit : fondé. Le banc publie désormais les intervalles
  de confiance.
- Cas supplémentaires et validation humaine : fondé, inscrit à la feuille
  de route, avec un guide pour les testeurs.

**Non retenu.**
- Consignes réécrites en mode directif avec exemples : pas avant d'avoir
  mesuré un échec ; un exemple risque d'être recopié comme citation.
- Modèle local de 32 ou 70 milliards de paramètres dès le premier jour :
  impossible sur la machine de développement (8 Go de mémoire).
- API européenne à poids ouverts comme premier choix : sans objet pour un
  dossier fictif, et ne règle pas la confidentialité des utilisateurs
  finaux ; possible plus tard grâce à l'interface de juge.
- « Les modèles locaux ont comblé l'essentiel de l'écart » : affirmation non
  vérifiée ; c'est ce que le banc doit mesurer.
- Grammaires GBNF dans Ollama : Ollama s'utilise ici avec un schéma JSON
  passé dans le champ `format`, ce qui remplit le même rôle.

## 2026-11-11 — Reprise après clear (CLAUDE)

**Objectif.** Poursuivre le travail autorisé restant.

**Constat.** Aucun : chaque suite attend une décision ou une ressource de
l'utilisateur (clé d'API et accord de coût, machine pour le modèle local,
relecture des 44 annotations, verdict `non_applicable`, `SOURCE.yaml`, cas
humains). État revérifié, tests OK, aucun changement de code.

**Prochaine étape.** Première mesure sur `fictif-therm-t1` dès l'accord.

## 2026-11-11 — Juge local : GPU loué plutôt que réécriture (CLAUDE)

**Décisions.** Pas de passage à Rust : la mémoire qui manque est celle des
poids du modèle local, pas celle du pipeline Python. Le juge local tournera
sur un GPU loué à l'heure, joint par tunnel SSH via `OLLAMA_HOST`, sans
changement de code. L'utilisateur a accordé la première mesure du juge API
Claude (44 appels) ; elle attend la clé dans `.env`.

**Fait.** Plugin Runpod installé pour Claude Code, hors dépôt.

**Réserves.** Ollama n'a pas d'authentification : ne jamais exposer son
port, passer par SSH. Prix des fournisseurs non vérifiés. Un serveur loué
ne règle pas la confidentialité pour les utilisateurs finaux.

**Prochaines étapes.** Connexion de l'utilisateur au fournisseur, choix du
modèle, accord avant tout lancement facturé ; clé d'API pour le juge Claude.

## 2026-11-11 — Masquage réversible des termes sensibles (CLAUDE)

**Objectif.** Demande de l'utilisateur : pouvoir remplacer les termes
sensibles d'un dossier par des étiquettes neutres avant l'envoi à un juge,
de façon réversible, pour revenir en arrière si les résultats paraissent
moins robustes.

**Décisions.**
- Masquage par liste déclarée (termes et motifs), sans détection
  automatique : rien n'est deviné, et la limite est écrite dans le README.
- Étiquettes stables par entité (`[FABRICANT_1]`), avec un suffixe pour
  chaque forme exacte supplémentaire (`[FABRICANT_1~2]`) : le retour au
  texte d'origine est exact, caractère pour caractère, et contrôlé à chaque
  masquage.
- Les citations sont vérifiées deux fois : contre le document masqué (celui
  que le juge a vu), puis contre le document d'origine après démasquage. Un
  échec ramène le verdict à `non_trouve`.
- Option `--mask` désactivée par défaut ; chaque prédiction porte un champ
  `masked`. La table de correspondance est refusée hors d'un chemin ignoré
  par git, et `*.masking.json` est ajouté à `.gitignore`.
- Règles de masquage du dossier fictif rangées dans `tests/fixtures/`
  (voir l'entrée suivante).

**Problèmes.** Aucun juge réel n'a tourné : l'effet du masquage sur les
verdicts est inconnu. 83 tests passent, tous sans réseau.

**Prochaines étapes.** Lors de la première mesure, lancer chaque juge avec
et sans `--mask` et comparer les deux séries avant d'adopter le masquage
pour des dossiers réels.

## 2026-11-11 — Arbitrage après un second avis externe (CLAUDE)

**Contexte.** L'utilisateur a soumis trois décisions à une autre IA, puis a
retenu la synthèse proposée par CLAUDE.

**Décisions de l'utilisateur.**
- Consignes du juge (`prompt.py`) inchangées. La demande de lister chaque
  élément manquant pour `non_conforme` est reportée après la mesure de
  référence, conformément à la règle de ne pas retoucher les consignes avant
  d'avoir mesuré.
- Test d'ablation avec un prompt générique : reporté, inscrit comme tâche
  optionnelle dans `project.yaml`.
- Masquage : les règles du dossier fictif quittent `eval/` pour
  `tests/fixtures/` ; le banc ne contient que des séries de référence sans
  masque. Point de l'avis non suivi : renoncer à toute mesure du masquage.
  Sa mesure sur un cas à vérité terrain connue reste une condition avant
  usage sur un dossier réel, écrite dans le README.

**Problèmes.** Sur 44 unités, l'effet du masquage se confondra avec la
variation entre deux séries : il faudra plusieurs séries par configuration,
ou davantage de cas.

## 2026-11-11 — Première mesure réelle : deux juges locaux (CLAUDE)

**Objectif.** Mesurer enfin un juge sur `fictif-therm-t1`.

**Fait.** Machine GPU louée à l'heure (0,69 USD/h), obtenue à la septième
tentative de création, les six premières refusées faute de capacité malgré
un stock annoncé. Ollama en écoute locale sur la machine, joint par tunnel
SSH. Essai sur 3 unités, puis 44 appels par modèle, code du commit
`e2b1fc5`, sans masque.

**Mesures.** `qwen3.8:27b` : 33/44. `gemma4:31b` : 38/44. Pour les deux :
0/13 faux `conforme`, 13/13 lacunes repérées, citations retenues toutes
valides, aucun échec technique. Toutes les erreurs vont vers la sévérité.
Quatre unités mettent les deux modèles en désaccord avec la vérité terrain
dans le même sens. Détail, limites et coût dans
`results/2026-11-11_fictif-therm-t1/rapport.tex`.

**Décisions.**
- `results/` reste ignoré par défaut, sauf les campagnes datées, versionnées
  sur demande de l'utilisateur (une mesure sur GPU loué coûte à refaire).
  Le PDF n'est pas versionné : le garde-fou bloque les PDF hors corpus.
- Plafond de durée assoupli par l'utilisateur : laisser une mesure finir,
  sans aller vers 10 USD par test.
- Mode de raisonnement laissé par défaut. Un avis externe prédisait qu'il
  casserait la sortie JSON : l'essai a montré que non.

**Problèmes.**
- Le catalogue du fournisseur annonce du stock que la création refuse.
- La règle de citation a annulé deux verdicts justes de `qwen3.8:27b`
  (passage du règlement non retrouvé dans l'unité) : à examiner.
- Hypothèse fausse de l'agent en cours de route : un compte sans crédit.

**Limites.** Vérité terrain écrite par une IA et non relue ; un seul cas ;
une seule série par modèle ; écart entre modèles non significatif.

**Prochaines étapes.** Relecture humaine des 13 désaccords ; juge API sur le
même cas ; second cas moins propre ; deux séries identiques pour connaître
la variation de fond.

**Clôture (18:11 UTC).** Machine terminée sur demande de l'utilisateur, après
rapatriement des résultats ; relecture : aucune machine ni volume sur le
compte. Durée totale d'environ 2 h 45.
