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
