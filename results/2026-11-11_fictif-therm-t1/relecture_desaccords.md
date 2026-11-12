# Fiche de relecture des désaccords — `fictif-therm-t1`, campagne du 2026-11-11

Document de travail produit par un agent (CLAUDE) pour la relecture humaine.
Il ne tranche rien : pour chaque unité, c'est au relecteur de dire qui a raison.
Aucune annotation n'est modifiée par cette fiche ; `review_status` reste `non_relu`
tant que l'utilisateur n'a pas validé `eval/cases/fictif-therm-t1/ground_truth.yaml`.

- **Texte des exigences** : repris du corpus public, `corpus/public/mdr/`
  (CELEX 02017R0745-20261109, français), unité par unité, avec son identifiant.
- **Dossier analysé** : `eval/cases/fictif-therm-t1/dossier.md` (dispositif fictif).
- **Verdict retenu** : verdict après la règle de citation ; il diffère du verdict
  du modèle quand une citation n'a pas été retrouvée mot pour mot.

**4 unités où les deux modèles contredisent le corrigé**, puis **9 où un seul le contredit**.

| Unité | Corrigé | qwen3.8:27b | gemma4:31b |
|---|---|---|---|
| `anx_II/4/d` | non_trouve | non_conforme | non_conforme |
| `anx_II/5/a` | non_trouve | non_conforme | non_conforme |
| `anx_II/6.1/a` | conforme | non_conforme | non_conforme |
| `anx_II/6.1/b/t2` | conforme | non_conforme | non_conforme |
| `anx_II/1.1/g` | non_trouve | non_conforme | d'accord |
| `anx_II/1.1/k` | conforme | non_conforme | d'accord |
| `anx_II/1.1/l` | conforme | d'accord | non_conforme |
| `anx_II/1.2/b` | non_trouve | non_conforme | d'accord |
| `anx_II/3/b` | conforme | non_conforme | d'accord |
| `anx_II/6.1/b/t1` | conforme | non_conforme | d'accord |
| `anx_II/6.1/b/t6` | conforme | d'accord | non_trouve |
| `anx_II/6.2/c/t2` | non_applicable | non_trouve | d'accord |
| `anx_II/6.2/c/t4` | non_applicable | non_trouve | d'accord |


# A. Les deux modèles contredisent le corrigé

---

## 1. `anx_II/4/d`

**Contexte dans le règlement**

- `anx_II` : La documentation technique et, le cas échéant, un résumé de celle-ci, que le fabricant doit établir, sont présentés de manière claire, organisée et non ambiguë, sous une forme facilement consultable, et comprennent en particulier les éléments énumérés dans la présente annexe.
- `anx_II/4` : La documentation contient des informations permettant de démontrer la conformité avec les exigences générales en matière de sécurité et de performances établies à l'annexe I qui sont applicables au dispositif compte tenu de sa destination, y compris une justification, une validation et une vérification des solutions retenues pour satisfaire auxdites exigences. La démonstration de conformité contient:

**Exigence** (texte de l'unité)

> la référence précise des documents contrôlés fournissant la preuve du respect de chaque norme harmonisée, spécification commune ou autre méthode appliquée pour démontrer la conformité avec les exigences générales en matière de sécurité et de performances. Les informations visées au présent point indiquent où trouver cette preuve dans la documentation technique complète et, le cas échéant, dans le résumé de la documentation technique.

**Corrigé actuel** : `non_trouve` — lacune voulue

- Justification : La section sur les exigences générales ne renvoie à aucun document contrôlé apportant la preuve du respect de chaque norme ou méthode.
- Passages du dossier retenus :
  - (aucun passage)

**qwen3.8:27b** : `non_conforme` (**en désaccord**)

- Justification : Le document énumère les normes appliquées et mentionne un tableau (EG-T1) indiquant la méthode de démonstration pour chaque exigence, mais il ne fournit pas la référence précise du document contrôlé qui constitue la preuve de conformité pour chacune des normes (par ex. « EN 60601-1 → rapport SEC-04 »), ni ne précise où trouver cette preuve dans la documentation technique complète ou dans un éventuel résumé.
- Passage du règlement cité : « la référence précise des documents contrôlés fournissant la preuve du respect de chaque norme harmonisée, spécification commune ou autre méthode appliquée pour démontrer la conformité avec les exigences générales en matière de sécurité et de performances »
- Passages du dossier cités :
  - « Les référentiels appliqués sont : EN ISO 14971 (gestion des risques), EN ISO 10993-1 (évaluation biologique), EN 60601-1 (sécurité de base des appareils électromédicaux), EN 62304 (cycle de vie du logiciel), EN 62366-1 (aptitude à l'utilisation), EN ISO 80601-2-56 (thermomètres médicaux) et EN ISO 15223-1 (symboles). »
  - « Pour chaque exigence retenue, le tableau indique la méthode de démonstration : essai en laboratoire, analyse de conception, évaluation clinique ou revue de l'étiquetage. »

**gemma4:31b** : `non_conforme` (**en désaccord**)

- Justification : Le document mentionne un tableau indiquant la méthode de démonstration, mais il n'est pas précisé que ce tableau contient la référence précise aux documents contrôlés prouvant le respect des normes harmonisées citées.
- Passage du règlement cité : « la référence précise des documents contrôlés fournissant la preuve du respect de chaque norme harmonisée, spécification commune ou autre méthode appliquée pour démontrer la conformité avec les exigences générales en matière de sécurité et de performances. »
- Passages du dossier cités :
  - « Le tableau EG-T1 liste les exigences générales de l'annexe I retenues comme applicables au dispositif »
  - « Pour chaque exigence retenue, le tableau indique la méthode de démonstration : essai en laboratoire, analyse de conception, évaluation clinique ou revue de l'étiquetage. »

**Décision du relecteur**

- [ ] le corrigé a raison
- [ ] un modèle a raison, le corrigé est à modifier ; verdict correct : ……
- [ ] l'exigence ou les consignes sont ambiguës ; à préciser : ……
- Remarque : 

---

## 2. `anx_II/5/a`

**Contexte dans le règlement**

- `anx_II` : La documentation technique et, le cas échéant, un résumé de celle-ci, que le fabricant doit établir, sont présentés de manière claire, organisée et non ambiguë, sous une forme facilement consultable, et comprennent en particulier les éléments énumérés dans la présente annexe.
- `anx_II/5` : La documentation contient des informations sur:

**Exigence** (texte de l'unité)

> l'analyse bénéfice/risque visée à l'annexe I, sections 1 et 8; et

**Corrigé actuel** : `non_trouve` — lacune voulue

- Justification : Le dossier présente la gestion des risques mais ne contient aucune analyse mettant en balance les bénéfices et les risques.
- Passages du dossier retenus :
  - (aucun passage)

**qwen3.8:27b** : `non_conforme` (**en désaccord**)

- Justification : Le document présente séparément la gestion des risques (section 5) et l'évaluation clinique (section 6.7), mais ne contient aucun passage explicite constituant une analyse bénéfice/risque intégrée qui met en balance les bénéfices cliniques attendus et les risques résiduels, comme l'exige la référence à l'annexe I, sections 1 et 8.
- Passage du règlement cité : « l'analyse bénéfice/risque visée à l'annexe I, sections 1 et 8 »
- Passages du dossier cités :
  - « Le dossier de gestion des risques DGR-T1 recense 46 situations dangereuses. Les mesures de maîtrise retenues sont, par ordre de priorité : la conception (limitation de l'énergie de la pile, double lecture de la thermistance), les protections (alarme de perte de liaison radio) et l'information de l'utilisateur. »
  - « Le rapport d'évaluation clinique REC-T1, révision B, mis à jour après l'étude de concordance EC-T1-01 menée sur 60 patients, conclut que le dispositif détecte une élévation de température avec une concordance satisfaisante par rapport à la mesure tympanique de référence. »

**gemma4:31b** : `non_conforme` (**en désaccord**)

- Justification : Le document décrit la gestion des risques (identification et maîtrise) et les performances cliniques, mais il ne contient pas d'analyse pesant explicitement les bénéfices attendus face aux risques résiduels.
- Passage du règlement cité : « l'analyse bénéfice/risque visée à l'annexe I, sections 1 et 8 »
- Passages du dossier cités :
  - « Le dossier de gestion des risques DGR-T1 recense 46 situations dangereuses. »
  - « le rapport de gestion des risques RGR-T1 conclut que toutes les mesures ont été mises en œuvre et vérifiées. »

**Décision du relecteur**

- [ ] le corrigé a raison
- [ ] un modèle a raison, le corrigé est à modifier ; verdict correct : ……
- [ ] l'exigence ou les consignes sont ambiguës ; à préciser : ……
- Remarque : 

---

## 3. `anx_II/6.1/a`

**Contexte dans le règlement**

- `anx_II` : La documentation technique et, le cas échéant, un résumé de celle-ci, que le fabricant doit établir, sont présentés de manière claire, organisée et non ambiguë, sous une forme facilement consultable, et comprennent en particulier les éléments énumérés dans la présente annexe.
- `anx_II/6` : La documentation contient les résultats et les analyses critiques de l'ensemble des études et/ou des essais de vérification et de validation qui ont été effectués pour démontrer que le dispositif respecte les exigences du présent règlement, en particulier les exigences générales en matière de sécurité et de performances.
- `anx_II/6.1` : Données précliniques et cliniques

**Exigence** (texte de l'unité)

> Les résultats d’essais, tels que des essais d’ingénierie, en laboratoire, des simulations d’utilisation, et des essais sur des animaux, et d’évaluations contenus dans la littérature publiée qui sont applicables au dispositif, compte tenu de sa destination, ou à des dispositifs similaires, concernant la sécurité préclinique du dispositif et le respect des spécifications.

**Corrigé actuel** : `conforme`

- Justification : Résultats d'essais d'ingénierie, de laboratoire et de simulation d'utilisation.
- Passages du dossier retenus :
  - « Le rapport ESS-LAB-07 présente les essais d'ingénierie réalisés en laboratoire »
  - « Une simulation d'utilisation par douze infirmiers (rapport APT-02) a confirmé que la pose, l'appairage et le retrait sont réalisés sans erreur critique. »

**qwen3.8:27b** : `non_conforme` (**en désaccord**)

- Justification : Le document couvre les essais d'ingénierie en laboratoire et une simulation d'utilisation, mais ne mentionne aucune évaluation issue de la littérature publiée applicable au dispositif ou à des dispositifs similaires, élément expressément requis par le point a) ; il ne déclare pas non plus que de telles évaluations ne seraient pas applicables.
- Passage du règlement cité : « Les résultats d'essais, tels que des essais d'ingénierie, en laboratoire, des simulations d'utilisation, et des essais sur des animaux, et d'évaluations contenus dans la littérature publiée qui sont applicables au dispositif, compte tenu de sa destination, ou à des dispositifs similaires, concernant la sécurité préclinique du dispositif et le respect des spécifications. »
- Passages du dossier cités :
  - « Le rapport ESS-LAB-07 présente les essais d'ingénierie réalisés en laboratoire : exactitude en bain thermostaté, autonomie, tenue de l'adhésif pendant 72 heures sur bras artificiel, résistance aux projections d'eau. Tous les critères d'acceptation des spécifications sont atteints. »
  - « Une simulation d'utilisation par douze infirmiers (rapport APT-02) a confirmé que la pose, l'appairage et le retrait sont réalisés sans erreur critique. »

**gemma4:31b** : `non_conforme` (**en désaccord**)

- Justification : Le document fournit des résultats d'essais d'ingénierie, de laboratoire et de simulations d'utilisation, mais il manque les évaluations contenues dans la littérature publiée.
- Passage du règlement cité : « Les résultats d’essais, tels que des essais d’ingénierie, en laboratoire, des simulations d’utilisation, et des essais sur des animaux, et d’évaluations contenus dans la littérature publiée qui sont applicables au dispositif »
- Passages du dossier cités :
  - « Le rapport ESS-LAB-07 présente les essais d'ingénierie réalisés en laboratoire »
  - « Une simulation d'utilisation par douze infirmiers (rapport APT-02) a confirmé que la pose, l'appairage et le retrait sont réalisés sans erreur critique. »

**Décision du relecteur**

- [ ] le corrigé a raison
- [ ] un modèle a raison, le corrigé est à modifier ; verdict correct : ……
- [ ] l'exigence ou les consignes sont ambiguës ; à préciser : ……
- Remarque : 

---

## 4. `anx_II/6.1/b/t2`

**Contexte dans le règlement**

- `anx_II` : La documentation technique et, le cas échéant, un résumé de celle-ci, que le fabricant doit établir, sont présentés de manière claire, organisée et non ambiguë, sous une forme facilement consultable, et comprennent en particulier les éléments énumérés dans la présente annexe.
- `anx_II/6` : La documentation contient les résultats et les analyses critiques de l'ensemble des études et/ou des essais de vérification et de validation qui ont été effectués pour démontrer que le dispositif respecte les exigences du présent règlement, en particulier les exigences générales en matière de sécurité et de performances.
- `anx_II/6.1` : Données précliniques et cliniques
- `anx_II/6.1/b` : Des informations détaillées relatives à la conception des essais, aux protocoles d'essai ou d'étude complets, aux méthodes d'analyse des données, ainsi que des synthèses de données et des conclusions des essais concernant en particulier:
Le cas échéant, il convient de démontrer la conformité avec les dispositions de la directive 2004/10/CE du Parlement européen et du Conseil ( 11 ).
Si aucun nouvel essai n'a été effectué, la documentation en explique la raison. Cela peut par exemple tenir au fait que des essais de biocompatibilité sur des matériaux identiques ont été réalisés lorsque ces matériaux ont été utilisés dans une version précédente du dispositif, qui a été légalement mise sur le marché ou mise en service.

**Exigence** (texte de l'unité)

> la caractérisation physico-chimique et microbiologique,

**Corrigé actuel** : `conforme`

- Justification : Caractérisation chimique et microbiologique avec protocole et conclusion.
- Passages du dossier retenus :
  - « Le rapport CAR-03 décrit la caractérisation chimique de l'adhésif par analyse des substances extractibles selon le protocole CAR-P-03, ainsi que le dénombrement microbien sur produit fini »

**qwen3.8:27b** : `non_conforme` (**en désaccord**)

- Justification : Le document mentionne la caractérisation physico-chimique et microbiologique et référence un protocole (CAR-P-03), mais il ne fournit ni les informations détaillées sur la conception des essais, ni le protocole complet, ni les méthodes d'analyse des données, ni les synthèses de données que l'exigence requiert ; seule une phrase de conclusion est donnée.
- Passage du règlement cité : « la caractérisation physico-chimique et microbiologique »
- Passages du dossier cités :
  - « Le rapport CAR-03 décrit la caractérisation chimique de l'adhésif par analyse des substances extractibles selon le protocole CAR-P-03, ainsi que le dénombrement microbien sur produit fini ; les teneurs mesurées sont inférieures aux seuils fixés dans l'évaluation toxicologique et la charge microbienne est conforme à la spécification interne. »

**gemma4:31b** : `non_conforme` (**en désaccord**)

- Justification : Le document mentionne le protocole et les conclusions, mais il manque des informations détaillées sur la conception des essais, les méthodes d'analyse des données et les synthèses de données.
- Passage du règlement cité : « — la caractérisation physico-chimique et microbiologique, »
- Passages du dossier cités :
  - « Le rapport CAR-03 décrit la caractérisation chimique de l'adhésif par analyse des substances extractibles selon le protocole CAR-P-03, ainsi que le dénombrement microbien sur produit fini ; les teneurs mesurées sont inférieures aux seuils fixés dans l'évaluation toxicologique et la charge microbienne est conforme à la spécification interne. »

**Décision du relecteur**

- [ ] le corrigé a raison
- [ ] un modèle a raison, le corrigé est à modifier ; verdict correct : ……
- [ ] l'exigence ou les consignes sont ambiguës ; à préciser : ……
- Remarque : 


# B. Un seul modèle contredit le corrigé

---

## 5. `anx_II/1.1/g`

**Contexte dans le règlement**

- `anx_II` : La documentation technique et, le cas échéant, un résumé de celle-ci, que le fabricant doit établir, sont présentés de manière claire, organisée et non ambiguë, sous une forme facilement consultable, et comprennent en particulier les éléments énumérés dans la présente annexe.
- `anx_II/1` : DESCRIPTION ET SPÉCIFICATION DU DISPOSITIF, Y COMPRIS LES VARIANTES ET LES ACCESSOIRES
- `anx_II/1.1` : Description et spécification du dispositif

**Exigence** (texte de l'unité)

> Une explication de toute nouvelle caractéristique.

**Corrigé actuel** : `non_trouve` — lacune voulue

- Justification : Le dossier ne dit rien des nouvelles caractéristiques, ni qu'il n'y en a pas.
- Passages du dossier retenus :
  - (aucun passage)

**qwen3.8:27b** : `non_conforme` (**en désaccord**)

- Justification : Le document indique que le principe de mesure par thermistance est établi et ne nécessite pas de démonstration scientifique nouvelle, mais il ne déclare pas explicitement qu'il n'existe pas de nouvelle caractéristique du dispositif (par exemple l'intégration de l'application mobile, la liaison radio, la surveillance continue) ni n'en fournit l'explication que l'exigence requiert.
- Passage du règlement cité : « Une explication de toute nouvelle caractéristique. »
- Passages du dossier cités :
  - « Ce principe de mesure par thermistance est établi de longue date pour la thermométrie de contact et ne nécessite pas de démonstration scientifique nouvelle. »

**gemma4:31b** : `non_trouve` (d'accord avec le corrigé)

- Justification : Le document ne mentionne aucune nouvelle caractéristique et ne précise pas explicitement que le dispositif n'en comporte pas.
- Passage du règlement cité : « Une explication de toute nouvelle caractéristique. »
- Passages du dossier cités :
  - (aucun passage)

**Décision du relecteur**

- [ ] le corrigé a raison
- [ ] un modèle a raison, le corrigé est à modifier ; verdict correct : ……
- [ ] l'exigence ou les consignes sont ambiguës ; à préciser : ……
- Remarque : 

---

## 6. `anx_II/1.1/k`

**Contexte dans le règlement**

- `anx_II` : La documentation technique et, le cas échéant, un résumé de celle-ci, que le fabricant doit établir, sont présentés de manière claire, organisée et non ambiguë, sous une forme facilement consultable, et comprennent en particulier les éléments énumérés dans la présente annexe.
- `anx_II/1` : DESCRIPTION ET SPÉCIFICATION DU DISPOSITIF, Y COMPRIS LES VARIANTES ET LES ACCESSOIRES
- `anx_II/1.1` : Description et spécification du dispositif

**Exigence** (texte de l'unité)

> Une description des matières premières intégrées dans les éléments fonctionnels clés et les éléments en contact direct avec le corps humain ou en contact indirect, par exemple, lors de la circulation extracorporelle des liquides corporels.

**Corrigé actuel** : `conforme`

- Justification : Les matières des éléments clés et de l'élément en contact direct sont décrites.
- Passages du dossier retenus :
  - « Le boîtier est en élastomère de silicone de qualité médicale ; la couche adhésive, seul élément en contact direct avec la peau, est un adhésif acrylique sur support en polyuréthane »

**qwen3.8:27b** : `non_conforme` (**en désaccord**)

- Justification : Le document décrit les matériaux du boîtier, de la couche adhésive et du film protecteur, mais ne fournit aucune description des matières premières des éléments fonctionnels clés internes (thermistance, microcontrôleur, émetteur radio, pile bouton), qui sont pourtant explicitement listés comme composants du dispositif.
- Passage du règlement cité : « Une description des matières premières intégrées dans les éléments fonctionnels clés et les éléments en contact direct avec le corps humain ou en contact indirect »
- Passages du dossier cités :
  - « Le boîtier est en élastomère de silicone de qualité médicale ; la couche adhésive, seul élément en contact direct avec la peau, est un adhésif acrylique sur support en polyuréthane ; le film protecteur est en polyester siliconé et n'entre pas en contact avec le patient. »
  - « Le dispositif comprend quatre éléments fonctionnels : (1) un boîtier souple contenant la thermistance, le microcontrôleur, l'émetteur radio et une pile bouton »

**gemma4:31b** : `conforme` (d'accord avec le corrigé)

- Justification : Le document décrit les matériaux utilisés pour les éléments fonctionnels et identifie explicitement l'élément en contact direct avec le corps humain.
- Passage du règlement cité : « Une description des matières premières intégrées dans les éléments fonctionnels clés et les éléments en contact direct avec le corps humain ou en contact indirect »
- Passages du dossier cités :
  - « Le boîtier est en élastomère de silicone de qualité médicale »
  - « la couche adhésive, seul élément en contact direct avec la peau, est un adhésif acrylique sur support en polyuréthane »
  - « le film protecteur est en polyester siliconé »

**Décision du relecteur**

- [ ] le corrigé a raison
- [ ] un modèle a raison, le corrigé est à modifier ; verdict correct : ……
- [ ] l'exigence ou les consignes sont ambiguës ; à préciser : ……
- Remarque : 

---

## 7. `anx_II/1.1/l`

**Contexte dans le règlement**

- `anx_II` : La documentation technique et, le cas échéant, un résumé de celle-ci, que le fabricant doit établir, sont présentés de manière claire, organisée et non ambiguë, sous une forme facilement consultable, et comprennent en particulier les éléments énumérés dans la présente annexe.
- `anx_II/1` : DESCRIPTION ET SPÉCIFICATION DU DISPOSITIF, Y COMPRIS LES VARIANTES ET LES ACCESSOIRES
- `anx_II/1.1` : Description et spécification du dispositif

**Exigence** (texte de l'unité)

> Les spécifications techniques, telles que caractéristiques, dimensions et caractéristiques de performance, du dispositif et de toute variante/configuration ou de tout accessoire qui figurent habituellement dans les spécifications du produit mises à disposition de l'utilisateur, par exemple dans des brochures, des catalogues et des publications similaires.

**Corrigé actuel** : `conforme`

- Justification : Caractéristiques, dimensions et performances sont spécifiées.
- Passages du dossier retenus :
  - « Plage de mesure : 30,0 °C à 43,0 °C. Exactitude annoncée : ± 0,1 °C entre 35,0 °C et 42,0 °C. »
  - « Dimensions du capteur : 48 mm × 30 mm × 5 mm. »

**qwen3.8:27b** : `conforme` (d'accord avec le corrigé)

- Justification : La section 1.10 fournit les caractéristiques, dimensions et performances du dispositif ; la section 1.6 précise l'absence d'accessoire ; la section 1.7 mentionne l'existence de variantes (plusieurs tailles). L'ensemble couvre ce que l'exigence demande.
- Passage du règlement cité : « Les spécifications techniques, telles que caractéristiques, dimensions et caractéristiques de performance, du dispositif et de toute variante/configuration ou de tout accessoire qui figurent habituellement dans les spécifications du produit mises à disposition de l'utilisateur »
- Passages du dossier cités :
  - « Plage de mesure : 30,0 °C à 43,0 °C. Exactitude annoncée : ± 0,1 °C entre 35,0 °C et 42,0 °C. Résolution d'affichage : 0,1 °C. Autonomie : 72 heures. Portée radio : 10 mètres en champ libre. Dimensions du capteur : 48 mm × 30 mm × 5 mm. Masse : 7 g. »
  - « Le dispositif n'a pas d'accessoire. »
  - « Le capteur est disponible en plusieurs tailles. »

**gemma4:31b** : `non_conforme` (**en désaccord**)

- Justification : Le document indique que le capteur existe en plusieurs tailles, mais ne fournit les dimensions et spécifications techniques que pour une seule configuration.
- Passage du règlement cité : « Les spécifications techniques, telles que caractéristiques, dimensions et caractéristiques de performance, du dispositif et de toute variante/configuration ou de tout accessoire »
- Passages du dossier cités :
  - « Le capteur est disponible en plusieurs tailles. »
  - « Dimensions du capteur : 48 mm × 30 mm × 5 mm. »

**Décision du relecteur**

- [ ] le corrigé a raison
- [ ] un modèle a raison, le corrigé est à modifier ; verdict correct : ……
- [ ] l'exigence ou les consignes sont ambiguës ; à préciser : ……
- Remarque : 

---

## 8. `anx_II/1.2/b`

**Contexte dans le règlement**

- `anx_II` : La documentation technique et, le cas échéant, un résumé de celle-ci, que le fabricant doit établir, sont présentés de manière claire, organisée et non ambiguë, sous une forme facilement consultable, et comprennent en particulier les éléments énumérés dans la présente annexe.
- `anx_II/1` : DESCRIPTION ET SPÉCIFICATION DU DISPOSITIF, Y COMPRIS LES VARIANTES ET LES ACCESSOIRES
- `anx_II/1.2` : Référence à des générations précédentes et similaires du dispositif

**Exigence** (texte de l'unité)

> Une présentation générale des dispositifs similaires identifiés disponibles sur le marché de l'Union ou le marché international, s'il en existe.

**Corrigé actuel** : `non_trouve` — lacune voulue

- Justification : Aucune présentation de dispositifs similaires, ni déclaration qu'il n'en existe pas.
- Passages du dossier retenus :
  - (aucun passage)

**qwen3.8:27b** : `non_conforme` (**en désaccord**)

- Justification : Le document indique qu'il n'existe pas de génération précédente du dispositif (section 1.11), mais ne fournit aucune présentation générale de dispositifs similaires disponibles sur le marché de l'Union ou international, ni ne déclare explicitement qu'aucun tel dispositif similaire n'existe sur ces marchés.
- Passage du règlement cité : « Une présentation générale des dispositifs similaires identifiés disponibles sur le marché de l'Union ou le marché international, s'il en existe. »
- Passages du dossier cités :
  - « FICTIF-Therm T1 est le premier dispositif de ce type conçu par Exemplia Dispositifs ; il n'existe pas de génération précédente. »

**gemma4:31b** : `non_trouve` (d'accord avec le corrigé)

- Justification : Le document ne mentionne aucun dispositif similaire disponible sur le marché, ni ne précise explicitement qu'il n'en existe pas.
- Passage du règlement cité : « Une présentation générale des dispositifs similaires identifiés disponibles sur le marché de l'Union ou le marché international, s'il en existe. »
- Passages du dossier cités :
  - (aucun passage)

**Décision du relecteur**

- [ ] le corrigé a raison
- [ ] un modèle a raison, le corrigé est à modifier ; verdict correct : ……
- [ ] l'exigence ou les consignes sont ambiguës ; à préciser : ……
- Remarque : 

---

## 9. `anx_II/3/b`

**Contexte dans le règlement**

- `anx_II` : La documentation technique et, le cas échéant, un résumé de celle-ci, que le fabricant doit établir, sont présentés de manière claire, organisée et non ambiguë, sous une forme facilement consultable, et comprennent en particulier les éléments énumérés dans la présente annexe.
- `anx_II/3` : INFORMATIONS SUR LA CONCEPTION ET LA FABRICATION

**Exigence** (texte de l'unité)

> Informations et spécifications complètes, y compris concernant les processus de fabrication et leur validation, les adjuvants, le contrôle continu et les essais sur le produit final. Les données figurent intégralement dans la documentation technique.

**Corrigé actuel** : `conforme`

- Justification : Procédés, validation, adjuvant, contrôles en cours et essai final sont couverts.
- Passages du dossier retenus :
  - « La fabrication comprend l'assemblage de la carte électronique, le surmoulage du boîtier, la pose de la couche adhésive, la programmation du micrologiciel, l'étalonnage et le conditionnement en sachet unitaire. »
  - « leur validation est consignée dans les rapports VAL-SM-02 et VAL-AD-01 »
  - « Le surmoulage utilise un agent de démoulage, éliminé par un nettoyage dont l'efficacité est vérifiée dans le rapport VAL-NET-01. »
  - « Chaque lot fait l'objet de contrôles en cours de fabrication »

**qwen3.8:27b** : `non_conforme` (**en désaccord**)

- Justification : Le document mentionne l'adjuvant (agent de démoulage) sans en fournir les spécifications (composition, quantité utilisée), et renvoie l'intégralité des données de validation des procédés spéciaux ainsi que les détails des essais sur produit final à des rapports et procédures externes (VAL-SM-02, VAL-AD-01, VAL-NET-01, CTL-FIN-03) dont le contenu n'est pas reproduit dans la documentation technique présentée, alors que l'exigence demande que les données figurent intégralement dans celle-ci.
- Passage du règlement cité : « Informations et spécifications complètes, y compris concernant les processus de fabrication et leur validation, les adjuvants, le contrôle continu et les essais sur le produit final. Les données figurent intégralement dans la documentation technique. »
- Passages du dossier cités :
  - « La fabrication comprend l'assemblage de la carte électronique, le surmoulage du boîtier, la pose de la couche adhésive, la programmation du micrologiciel, l'étalonnage et le conditionnement en sachet unitaire. »
  - « Le surmoulage et la pose de l'adhésif sont des procédés spéciaux ; leur validation est consignée dans les rapports VAL-SM-02 et VAL-AD-01. »
  - « Le surmoulage utilise un agent de démoulage, éliminé par un nettoyage dont l'efficacité est vérifiée dans le rapport VAL-NET-01. »
  - « Chaque lot fait l'objet de contrôles en cours de fabrication (inspection visuelle de la carte, contrôle dimensionnel du boîtier) et d'un essai final unitaire de fonctionnement et d'exactitude selon la procédure CTL-FIN-03. »

**gemma4:31b** : `conforme` (d'accord avec le corrigé)

- Justification : Le document détaille les spécifications techniques, le processus de fabrication, la validation des procédés spéciaux, l'utilisation d'un adjuvant (agent de démoulage), les contrôles en cours de fabrication et les essais sur le produit final.
- Passage du règlement cité : « Informations et spécifications complètes, y compris concernant les processus de fabrication et leur validation, les adjuvants, le contrôle continu et les essais sur le produit final. »
- Passages du dossier cités :
  - « Plage de mesure : 30,0 °C à 43,0 °C. Exactitude annoncée : ± 0,1 °C entre 35,0 °C et 42,0 °C. Résolution d'affichage : 0,1 °C. Autonomie : 72 heures. Portée radio : 10 mètres en champ libre. Dimensions du capteur : 48 mm × 30 mm × 5 mm. Masse : 7 g. »
  - « La fabrication comprend l'assemblage de la carte électronique, le surmoulage du boîtier, la pose de la couche adhésive, la programmation du micrologiciel, l'étalonnage et le conditionnement en sachet unitaire. »
  - « Le surmoulage et la pose de l'adhésif sont des procédés spéciaux ; leur validation est consignée dans les rapports VAL-SM-02 et VAL-AD-01. »
  - « Le surmoulage utilise un agent de démoulage »
  - « Chaque lot fait l'objet de contrôles en cours de fabrication (inspection visuelle de la carte, contrôle dimensionnel du boîtier) »
  - « et d'un essai final unitaire de fonctionnement et d'exactitude selon la procédure CTL-FIN-03. »

**Décision du relecteur**

- [ ] le corrigé a raison
- [ ] un modèle a raison, le corrigé est à modifier ; verdict correct : ……
- [ ] l'exigence ou les consignes sont ambiguës ; à préciser : ……
- Remarque : 

---

## 10. `anx_II/6.1/b/t1`

**Contexte dans le règlement**

- `anx_II` : La documentation technique et, le cas échéant, un résumé de celle-ci, que le fabricant doit établir, sont présentés de manière claire, organisée et non ambiguë, sous une forme facilement consultable, et comprennent en particulier les éléments énumérés dans la présente annexe.
- `anx_II/6` : La documentation contient les résultats et les analyses critiques de l'ensemble des études et/ou des essais de vérification et de validation qui ont été effectués pour démontrer que le dispositif respecte les exigences du présent règlement, en particulier les exigences générales en matière de sécurité et de performances.
- `anx_II/6.1` : Données précliniques et cliniques
- `anx_II/6.1/b` : Des informations détaillées relatives à la conception des essais, aux protocoles d'essai ou d'étude complets, aux méthodes d'analyse des données, ainsi que des synthèses de données et des conclusions des essais concernant en particulier:
Le cas échéant, il convient de démontrer la conformité avec les dispositions de la directive 2004/10/CE du Parlement européen et du Conseil ( 11 ).
Si aucun nouvel essai n'a été effectué, la documentation en explique la raison. Cela peut par exemple tenir au fait que des essais de biocompatibilité sur des matériaux identiques ont été réalisés lorsque ces matériaux ont été utilisés dans une version précédente du dispositif, qui a été légalement mise sur le marché ou mise en service.

**Exigence** (texte de l'unité)

> la biocompatibilité du dispositif, y compris le recensement de tous les matériaux en contact direct ou indirect avec le patient ou l'utilisateur,

**Corrigé actuel** : `conforme`

- Justification : Recensement des matériaux en contact, protocole et conclusions de biocompatibilité.
- Passages du dossier retenus :
  - « Les matériaux en contact avec le patient ou l'utilisateur sont recensés dans le rapport BIO-01 »
  - « Le protocole BIO-P-01 prévoit des essais de cytotoxicité, de sensibilisation et d'irritation cutanée »

**qwen3.8:27b** : `non_conforme` (**en désaccord**)

- Justification : Le document recense les matériaux en contact direct (adhésif, silicone) et décrit les essais de biocompatibilité, mais ne mentionne pas explicitement les matériaux en contact indirect (par exemple les composants internes encapsulés dans le boîtier) ni ne justifie leur absence du recensement, alors que l'exigence vise « tous les matériaux en contact direct ou indirect ».
- Passage du règlement cité : « la biocompatibilité du dispositif, y compris le recensement de tous les matériaux en contact direct ou indirect avec le patient ou l'utilisateur »
- Passages du dossier cités :
  - « Les matériaux en contact avec le patient ou l'utilisateur sont recensés dans le rapport BIO-01 : adhésif acrylique sur polyuréthane (contact cutané direct avec le patient, jusqu'à 72 heures) et silicone du boîtier (contact cutané avec le soignant lors de la pose). »

**gemma4:31b** : `conforme` (d'accord avec le corrigé)

- Justification : Le document recense les matériaux en contact avec le patient et l'utilisateur et présente les conclusions des essais de biocompatibilité.
- Passage du règlement cité : « la biocompatibilité du dispositif, y compris le recensement de tous les matériaux en contact direct ou indirect avec le patient ou l'utilisateur, »
- Passages du dossier cités :
  - « Les matériaux en contact avec le patient ou l'utilisateur sont recensés dans le rapport BIO-01 : adhésif acrylique sur polyuréthane (contact cutané direct avec le patient, jusqu'à 72 heures) et silicone du boîtier (contact cutané avec le soignant lors de la pose). »
  - « les résultats, analysés dans le rapport BIO-01, ne montrent aucun effet cytotoxique, sensibilisant ou irritant. »

**Décision du relecteur**

- [ ] le corrigé a raison
- [ ] un modèle a raison, le corrigé est à modifier ; verdict correct : ……
- [ ] l'exigence ou les consignes sont ambiguës ; à préciser : ……
- Remarque : 

---

## 11. `anx_II/6.1/b/t6`

**Contexte dans le règlement**

- `anx_II` : La documentation technique et, le cas échéant, un résumé de celle-ci, que le fabricant doit établir, sont présentés de manière claire, organisée et non ambiguë, sous une forme facilement consultable, et comprennent en particulier les éléments énumérés dans la présente annexe.
- `anx_II/6` : La documentation contient les résultats et les analyses critiques de l'ensemble des études et/ou des essais de vérification et de validation qui ont été effectués pour démontrer que le dispositif respecte les exigences du présent règlement, en particulier les exigences générales en matière de sécurité et de performances.
- `anx_II/6.1` : Données précliniques et cliniques
- `anx_II/6.1/b` : Des informations détaillées relatives à la conception des essais, aux protocoles d'essai ou d'étude complets, aux méthodes d'analyse des données, ainsi que des synthèses de données et des conclusions des essais concernant en particulier:
Le cas échéant, il convient de démontrer la conformité avec les dispositions de la directive 2004/10/CE du Parlement européen et du Conseil ( 11 ).
Si aucun nouvel essai n'a été effectué, la documentation en explique la raison. Cela peut par exemple tenir au fait que des essais de biocompatibilité sur des matériaux identiques ont été réalisés lorsque ces matériaux ont été utilisés dans une version précédente du dispositif, qui a été légalement mise sur le marché ou mise en service.

**Exigence** (texte de l'unité)

> les performances et la sécurité.

**Corrigé actuel** : `conforme`

- Justification : Protocole, méthode d'analyse et conclusion des essais de performance.
- Passages du dossier retenus :
  - « Le protocole PERF-P-05 compare les mesures du capteur à celles d'un thermomètre de référence étalonné, sur 30 points de température »

**qwen3.8:27b** : `conforme` (d'accord avec le corrigé)

- Justification : Le document présente, pour les performances, un protocole (PERF-P-05), une méthode (comparaison à un étalon sur 30 points) et une synthèse des résultats (écart maximal 0,08 °C) ; pour la sécurité, un protocole (SEC-P-04), une méthode (laboratoire externe) et une conclusion de conformité sur les paramètres testés, ce qui couvre les éléments demandés par l'exigence.
- Passage du règlement cité : « les performances et la sécurité. »
- Passages du dossier cités :
  - « Le protocole PERF-P-05 compare les mesures du capteur à celles d'un thermomètre de référence étalonné, sur 30 points de température ; l'analyse des écarts (rapport PERF-05) donne un écart maximal de 0,08 °C sur la plage de 35,0 °C à 42,0 °C. »
  - « Les essais de sécurité électrique ont été réalisés par un laboratoire externe selon le protocole SEC-P-04 ; le rapport SEC-04 conclut à la conformité pour les courants de fuite, l'échauffement de surface et la protection contre le court-circuit de la pile. »

**gemma4:31b** : `non_trouve` (**en désaccord**)

- Verdict du modèle avant la règle de citation : `non_conforme` ; motif du retrait : 2 passage(s) du document introuvable(s)
- Justification : Le document fournit des synthèses et des conclusions concernant les performances et la sécurité, mais il ne contient pas les informations détaillées sur la conception des essais, les protocoles complets, ni les méthodes d'analyse des données demandées.
- Passage du règlement cité : « — les performances et la sécurité. »
- Passages du dossier cités :
  - (aucun passage)
- Passages cités mais non retrouvés mot pour mot :
  - « Le rapport PERF-05 donne un écart maximal de 0,08 °C sur la plage de 35,0 °C à 42,0 °C. »
  - « Le rapport SEC-04 conclut à la conformité pour les courants de fuite, l'échauffement de surface et la protection contre le court-circuit de la pile. »

**Décision du relecteur**

- [ ] le corrigé a raison
- [ ] un modèle a raison, le corrigé est à modifier ; verdict correct : ……
- [ ] l'exigence ou les consignes sont ambiguës ; à préciser : ……
- Remarque : 

---

## 12. `anx_II/6.2/c/t2`

**Contexte dans le règlement**

- `anx_II` : La documentation technique et, le cas échéant, un résumé de celle-ci, que le fabricant doit établir, sont présentés de manière claire, organisée et non ambiguë, sous une forme facilement consultable, et comprennent en particulier les éléments énumérés dans la présente annexe.
- `anx_II/6` : La documentation contient les résultats et les analyses critiques de l'ensemble des études et/ou des essais de vérification et de validation qui ont été effectués pour démontrer que le dispositif respecte les exigences du présent règlement, en particulier les exigences générales en matière de sécurité et de performances.
- `anx_II/6.2` : Informations supplémentaires requises dans des cas spécifiques
- `anx_II/6.2/c` : Dans le cas des dispositifs qui sont composés de substances ou de combinaisons de substances qui sont destinées à être introduites dans le corps humain et qui sont absorbées par le corps humain ou dispersées localement dans celui-ci, des informations détaillées relatives notamment à la conception des essais, aux protocoles d'essai ou d'étude complets, aux méthodes d'analyse des données, ainsi que des synthèses de données et des conclusions des essais, dans le cas d'études portant sur:
En l'absence de telles études, une justification est fournie.

**Exigence** (texte de l'unité)

> d'éventuelles interactions de ces substances ou de leurs produits de métabolisme dans le corps humain, avec d'autres dispositifs, médicaments ou substances, eu égard à la population cible et à son état de santé,

**Corrigé actuel** : `non_applicable`

- Justification : L'unité ne vise que les dispositifs composés de substances introduites dans le corps humain ; le dossier déclare que ce n'est pas le cas.
- Passages du dossier retenus :
  - « Le dispositif n'est pas composé de substances destinées à être introduites dans le corps humain ; il reste à la surface de la peau. »

**qwen3.8:27b** : `non_trouve` (**en désaccord**)

- Verdict du modèle avant la règle de citation : `non_applicable` ; motif du retrait : passage du règlement introuvable dans l'unité
- Justification : L'exigence ne vise que les dispositifs composés de substances destinées à être introduites dans le corps humain ; le document déclare explicitement que ce cas ne concerne pas le dispositif, qui reste à la surface de la peau.
- Passage du règlement cité : «  »
- Passages du dossier cités :
  - (aucun passage)

**gemma4:31b** : `non_applicable` (d'accord avec le corrigé)

- Justification : Le document déclare explicitement que le dispositif n'est pas composé de substances destinées à être introduites dans le corps humain, ce qui rend cette exigence non applicable.
- Passage du règlement cité : « — d'éventuelles interactions de ces substances ou de leurs produits de métabolisme dans le corps humain, avec d'autres dispositifs, médicaments ou substances, eu égard à la population cible et à son état de santé, »
- Passages du dossier cités :
  - « Le dispositif n'est pas composé de substances destinées à être introduites dans le corps humain ; il reste à la surface de la peau. »

**Décision du relecteur**

- [ ] le corrigé a raison
- [ ] un modèle a raison, le corrigé est à modifier ; verdict correct : ……
- [ ] l'exigence ou les consignes sont ambiguës ; à préciser : ……
- Remarque : 

---

## 13. `anx_II/6.2/c/t4`

**Contexte dans le règlement**

- `anx_II` : La documentation technique et, le cas échéant, un résumé de celle-ci, que le fabricant doit établir, sont présentés de manière claire, organisée et non ambiguë, sous une forme facilement consultable, et comprennent en particulier les éléments énumérés dans la présente annexe.
- `anx_II/6` : La documentation contient les résultats et les analyses critiques de l'ensemble des études et/ou des essais de vérification et de validation qui ont été effectués pour démontrer que le dispositif respecte les exigences du présent règlement, en particulier les exigences générales en matière de sécurité et de performances.
- `anx_II/6.2` : Informations supplémentaires requises dans des cas spécifiques
- `anx_II/6.2/c` : Dans le cas des dispositifs qui sont composés de substances ou de combinaisons de substances qui sont destinées à être introduites dans le corps humain et qui sont absorbées par le corps humain ou dispersées localement dans celui-ci, des informations détaillées relatives notamment à la conception des essais, aux protocoles d'essai ou d'étude complets, aux méthodes d'analyse des données, ainsi que des synthèses de données et des conclusions des essais, dans le cas d'études portant sur:
En l'absence de telles études, une justification est fournie.

**Exigence** (texte de l'unité)

> la toxicité, y compris la toxicité résultant d'une dose unique et de doses répétées, la génotoxicité, la carcinogénicité et la toxicité pour la reproduction ou le développement, selon le cas, en fonction du niveau et de la nature de l'exposition au dispositif.

**Corrigé actuel** : `non_applicable`

- Justification : L'unité ne vise que les dispositifs composés de substances introduites dans le corps humain ; le dossier déclare que ce n'est pas le cas.
- Passages du dossier retenus :
  - « Le dispositif n'est pas composé de substances destinées à être introduites dans le corps humain ; il reste à la surface de la peau. »

**qwen3.8:27b** : `non_trouve` (**en désaccord**)

- Verdict du modèle avant la règle de citation : `non_applicable` ; motif du retrait : passage du règlement introuvable dans l'unité
- Justification : L'exigence 6.2.c) ne vise que les dispositifs composés de substances destinées à être introduites dans le corps humain ; le document déclare explicitement dans la section 7 que ce cas ne le concerne pas, le dispositif restant à la surface de la peau.
- Passage du règlement cité : «  »
- Passages du dossier cités :
  - (aucun passage)

**gemma4:31b** : `non_applicable` (d'accord avec le corrigé)

- Justification : Le document déclare explicitement que le dispositif n'est pas composé de substances destinées à être introduites dans le corps humain, rendant cette exigence non applicable.
- Passage du règlement cité : « la toxicité, y compris la toxicité résultant d'une dose unique et de doses répétées, la génotoxicité, la carcinogénicité et la toxicité pour la reproduction ou le développement, selon le cas, en fonction du niveau et de la nature de l'exposition au dispositif. »
- Passages du dossier cités :
  - « Le dispositif n'est pas composé de substances destinées à être introduites dans le corps humain ; il reste à la surface de la peau. »

**Décision du relecteur**

- [ ] le corrigé a raison
- [ ] un modèle a raison, le corrigé est à modifier ; verdict correct : ……
- [ ] l'exigence ou les consignes sont ambiguës ; à préciser : ……
- Remarque : 
