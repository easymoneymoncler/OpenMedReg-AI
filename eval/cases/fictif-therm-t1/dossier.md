# Documentation technique — FICTIF-Therm T1

> DOCUMENT FICTIF. Le dispositif, le fabricant, les sites, les rapports et les résultats cités ici sont inventés pour servir de jeu d'essai. Ce document contient des lacunes volontaires. Il ne constitue ni un modèle de documentation technique ni un avis réglementaire.

Fabricant : Exemplia Dispositifs SAS (société fictive)
Référence du document : DT-T1, révision C

## 1. Présentation du dispositif

### 1.1 Identification et destination

FICTIF-Therm T1 est un capteur de température cutané adhésif, à usage unique, associé à une application mobile de suivi.

Le dispositif est destiné à la mesure continue de la température cutanée axillaire de patients hospitalisés, afin de signaler au personnel soignant une élévation de température.

Les utilisateurs prévus sont les infirmiers et les médecins des services d'hospitalisation ; le dispositif n'est pas destiné à être posé par le patient lui-même.

### 1.2 Patients et conditions d'emploi

La population visée est constituée des patients adultes hospitalisés en service de médecine ou de chirurgie, nécessitant une surveillance de la température pendant une durée maximale de 72 heures.

L'affection surveillée est la fièvre, notamment post-opératoire ou d'origine infectieuse.

Contre-indications : ne pas utiliser sur une peau lésée, chez un patient présentant une allergie connue aux adhésifs acryliques, ni chez l'enfant de moins de 18 ans.

Mise en garde : le dispositif ne remplace pas une mesure de température centrale lorsque celle-ci est cliniquement requise.

### 1.3 Principe de fonctionnement

Une thermistance placée au contact de la peau voit sa résistance varier avec la température ; un microcontrôleur convertit cette résistance en température toutes les 60 secondes et transmet la valeur à l'application par liaison radio à basse consommation.

Ce principe de mesure par thermistance est établi de longue date pour la thermométrie de contact et ne nécessite pas de démonstration scientifique nouvelle.

### 1.4 Qualification en tant que dispositif médical

Le produit est un dispositif médical car il est destiné par le fabricant à être utilisé chez l'homme à des fins de surveillance d'une maladie, et son action principale n'est obtenue ni par des moyens pharmacologiques ou immunologiques ni par métabolisme.

### 1.5 Classification

Le dispositif relève de la classe IIa.

### 1.6 Accessoires et produits associés

Le dispositif n'a pas d'accessoire. Il est utilisé avec un téléphone ou une tablette du commerce, fourni par l'établissement, sur lequel l'application FICTIF-Therm est installée ; ce téléphone n'est pas un dispositif médical.

### 1.7 Présentation commerciale

Le capteur est disponible en plusieurs tailles.

### 1.8 Constitution

Le dispositif comprend quatre éléments fonctionnels : (1) un boîtier souple contenant la thermistance, le microcontrôleur, l'émetteur radio et une pile bouton ; (2) une couche adhésive de fixation ; (3) un film protecteur à retirer avant la pose ; (4) le logiciel, composé du micrologiciel du capteur (version 1.4) et de l'application mobile FICTIF-Therm (version 2.1).

La figure 1 du plan PL-T1-001 représente une vue éclatée légendée du capteur et repère chacun de ces éléments.

### 1.9 Matériaux

Le boîtier est en élastomère de silicone de qualité médicale ; la couche adhésive, seul élément en contact direct avec la peau, est un adhésif acrylique sur support en polyuréthane ; le film protecteur est en polyester siliconé et n'entre pas en contact avec le patient.

### 1.10 Spécifications techniques

Plage de mesure : 30,0 °C à 43,0 °C. Exactitude annoncée : ± 0,1 °C entre 35,0 °C et 42,0 °C. Résolution d'affichage : 0,1 °C. Autonomie : 72 heures. Portée radio : 10 mètres en champ libre. Dimensions du capteur : 48 mm × 30 mm × 5 mm. Masse : 7 g.

### 1.11 Historique

FICTIF-Therm T1 est le premier dispositif de ce type conçu par Exemplia Dispositifs ; il n'existe pas de génération précédente.

## 2. Étiquetage et notice

Le dispositif est destiné à être mis sur le marché en France, en Belgique et en Allemagne.

L'annexe ETQ-T1 reproduit l'étiquette du sachet unitaire et l'étiquette de la boîte de vente de 20 capteurs. Ces étiquettes sont établies en français uniquement.

L'annexe NOT-T1 contient la notice d'utilisation en français, en néerlandais et en allemand.

## 3. Conception et fabrication

### 3.1 Étapes de conception

La conception a suivi cinq étapes, chacune close par une revue documentée : recueil des besoins utilisateurs (revue RC-01), spécification des exigences (RC-02), conception détaillée du matériel et du logiciel (RC-03), vérification (RC-04), validation et transfert en production (RC-05).

### 3.2 Procédé de fabrication

La fabrication comprend l'assemblage de la carte électronique, le surmoulage du boîtier, la pose de la couche adhésive, la programmation du micrologiciel, l'étalonnage et le conditionnement en sachet unitaire.

Le surmoulage et la pose de l'adhésif sont des procédés spéciaux ; leur validation est consignée dans les rapports VAL-SM-02 et VAL-AD-01.

Le surmoulage utilise un agent de démoulage, éliminé par un nettoyage dont l'efficacité est vérifiée dans le rapport VAL-NET-01.

Chaque lot fait l'objet de contrôles en cours de fabrication (inspection visuelle de la carte, contrôle dimensionnel du boîtier) et d'un essai final unitaire de fonctionnement et d'exactitude selon la procédure CTL-FIN-03.

### 3.3 Sites

La conception et le conditionnement sont réalisés sur le site d'Exemplia Dispositifs SAS, 12 rue des Exemples, 00000 Ville-Fictive, France.

L'assemblage de la carte électronique est confié à un sous-traitant.

## 4. Exigences générales en matière de sécurité et de performances

Le tableau EG-T1 liste les exigences générales de l'annexe I retenues comme applicables au dispositif : sections 1 à 9, 10.1, 10.2, 10.4, 11.1, 14.1, 14.2, 15.1, 17.1 à 17.4, 18.1, 18.2, 18.5 à 18.8, 21.1, 21.2 et 23.

Pour chaque exigence retenue, le tableau indique la méthode de démonstration : essai en laboratoire, analyse de conception, évaluation clinique ou revue de l'étiquetage.

Les référentiels appliqués sont : EN ISO 14971 (gestion des risques), EN ISO 10993-1 (évaluation biologique), EN 60601-1 (sécurité de base des appareils électromédicaux), EN 62304 (cycle de vie du logiciel), EN 62366-1 (aptitude à l'utilisation), EN ISO 80601-2-56 (thermomètres médicaux) et EN ISO 15223-1 (symboles).

## 5. Gestion des risques

Le dossier de gestion des risques DGR-T1 recense 46 situations dangereuses. Les mesures de maîtrise retenues sont, par ordre de priorité : la conception (limitation de l'énergie de la pile, double lecture de la thermistance), les protections (alarme de perte de liaison radio) et l'information de l'utilisateur.

Après application de ces mesures, 43 risques sont classés acceptables et 3 risques résiduels sont signalés dans la notice ; le rapport de gestion des risques RGR-T1 conclut que toutes les mesures ont été mises en œuvre et vérifiées.

## 6. Vérification et validation

### 6.1 Essais précliniques

Le rapport ESS-LAB-07 présente les essais d'ingénierie réalisés en laboratoire : exactitude en bain thermostaté, autonomie, tenue de l'adhésif pendant 72 heures sur bras artificiel, résistance aux projections d'eau. Tous les critères d'acceptation des spécifications sont atteints.

Une simulation d'utilisation par douze infirmiers (rapport APT-02) a confirmé que la pose, l'appairage et le retrait sont réalisés sans erreur critique.

### 6.2 Biocompatibilité

Les matériaux en contact avec le patient ou l'utilisateur sont recensés dans le rapport BIO-01 : adhésif acrylique sur polyuréthane (contact cutané direct avec le patient, jusqu'à 72 heures) et silicone du boîtier (contact cutané avec le soignant lors de la pose).

Le protocole BIO-P-01 prévoit des essais de cytotoxicité, de sensibilisation et d'irritation cutanée ; les résultats, analysés dans le rapport BIO-01, ne montrent aucun effet cytotoxique, sensibilisant ou irritant.

### 6.3 Caractérisation physico-chimique et microbiologique

Le rapport CAR-03 décrit la caractérisation chimique de l'adhésif par analyse des substances extractibles selon le protocole CAR-P-03, ainsi que le dénombrement microbien sur produit fini ; les teneurs mesurées sont inférieures aux seuils fixés dans l'évaluation toxicologique et la charge microbienne est conforme à la spécification interne.

### 6.4 Sécurité électrique

Les essais de sécurité électrique ont été réalisés par un laboratoire externe selon le protocole SEC-P-04 ; le rapport SEC-04 conclut à la conformité pour les courants de fuite, l'échauffement de surface et la protection contre le court-circuit de la pile.

### 6.5 Logiciel

Le logiciel a été développé selon un cycle en V décrit dans le plan de développement PDL-T1 : exigences, architecture, conception détaillée, codage, tests unitaires, tests d'intégration et tests système.

Le rapport de validation logicielle RVL-T1 résume les résultats : 412 tests unitaires, 88 tests d'intégration et 57 tests système exécutés en interne, tous passés, complétés par une validation en environnement d'utilisation simulé dans un service hospitalier de démonstration avant la libération de la version 2.1.

Les essais ont couvert les deux systèmes d'exploitation mobiles pris en charge et les six modèles de téléphone et de tablette listés dans la notice.

### 6.6 Performances et sécurité

Le protocole PERF-P-05 compare les mesures du capteur à celles d'un thermomètre de référence étalonné, sur 30 points de température ; l'analyse des écarts (rapport PERF-05) donne un écart maximal de 0,08 °C sur la plage de 35,0 °C à 42,0 °C.

### 6.7 Évaluation clinique

Le plan d'évaluation clinique PEC-T1 définit la destination, les critères de performance clinique et les sources de données retenues.

Le rapport d'évaluation clinique REC-T1, révision B, mis à jour après l'étude de concordance EC-T1-01 menée sur 60 patients, conclut que le dispositif détecte une élévation de température avec une concordance satisfaisante par rapport à la mesure tympanique de référence.

## 7. Cas particuliers

Le dispositif n'incorpore aucune substance qui, utilisée séparément, pourrait être considérée comme un médicament.

Le dispositif n'est fabriqué à partir d'aucun tissu ni d'aucune cellule d'origine humaine ou animale, ni de leurs dérivés, et n'en incorpore pas.

Le dispositif n'est pas composé de substances destinées à être introduites dans le corps humain ; il reste à la surface de la peau.

Le dispositif ne contient aucune substance cancérogène, mutagène ou toxique pour la reproduction, ni aucun perturbateur endocrinien.

Le dispositif est mis sur le marché à l'état non stérile et sans condition microbiologique particulière.

Le dispositif a une fonction de mesurage. Pour garantir l'exactitude annoncée, chaque capteur est étalonné en fin de fabrication sur deux points de température dans un bain thermostaté raccordé à un étalon national, puis contrôlé sur un troisième point ; les capteurs dont l'écart dépasse 0,05 °C sont rebutés (procédure ETA-02).

Le capteur ne doit être raccordé à aucun autre dispositif pour fonctionner comme prévu : il communique uniquement avec l'application FICTIF-Therm, qui fait partie du dispositif.
