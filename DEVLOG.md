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
