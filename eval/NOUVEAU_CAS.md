# Ajouter un cas d'évaluation rédigé par un humain

Le premier cas (`fictif-therm-t1`) a été rédigé et annoté par une IA. Un
moteur de la même famille de modèles a donc un avantage sur lui, et ses
lacunes sont plus nettes que celles d'un vrai dossier. Le banc ne devient
fiable qu'avec des cas écrits par des personnes du métier.

## Ce qu'il faut viser

Trois profils de dossier, pour que le banc ne mesure pas un seul style :

| Profil | Ce qu'il met à l'épreuve |
| --- | --- |
| Propre | Dossier bien structuré, lacunes isolées. Cas nominal. |
| Désordonné | Informations dispersées, renvois entre sections, formulations vagues, tableaux, contradictions entre deux passages. |
| Piège | Dispositif pour lequel beaucoup de points conditionnels ne s'appliquent pas, certains déclarés, d'autres passés sous silence. |

## Règles

- **Dispositif inventé.** Aucun extrait d'un dossier réel, aucun nom de
  fabricant, de produit ou de personne existant. Écrire en tête de document :
  `DOCUMENT FICTIF`.
- **Aucun texte de norme** (ISO, IEC, EN) : seuls le numéro et le titre
  court sont admis.
- **Rédaction sans IA**, ou réécrite à la main : c'est tout l'intérêt du cas.
- **Annotation par une personne différente** de celle qui a rédigé, si
  possible, sans regarder la sortie d'un moteur.

## Étapes

1. Créer `eval/cases/<nom-du-cas>/dossier.md`.
2. Copier `eval/cases/fictif-therm-t1/ground_truth.yaml` et l'adapter : une
   entrée par unité feuille du périmètre (44 pour l'Annexe II), avec le
   verdict attendu, les passages du dossier cités mot pour mot et le motif.
   Définition des verdicts : [README.md](README.md).
3. Renseigner `authored_by` avec un pseudonyme et mettre `review_status`
   à `relu` seulement pour les entrées vérifiées par un relecteur compétent.
4. Lancer `./scripts/run_tests.sh` : le garde-fou refuse les fichiers
   interdits.
5. Vérifier le cas avec le repère « oracle », qui doit donner une
   exactitude de 1 et une validité des citations de 1 :

```bash
.venv/bin/python -m openmedreg.evaluation eval/cases/<nom-du-cas> --baseline oracle
```
