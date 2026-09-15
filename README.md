# Cyber PME — Auto-évaluation cybersécurité

Outil d'auto-évaluation de la maturité cybersécurité pour les PME
marocaines, développé dans le cadre d'un stage (CMPRI, été 2026), basé sur
le guide de bonnes pratiques **CMRPI/AUSIM**.

## Ce que fait l'application

- Questionnaire de 22 questions fermées (Oui / Non / Je ne sais pas),
  réparties en 5 thèmes : gouvernance, sensibilisation, postes de travail
  et accès, protection des données, réseaux et gestion des incidents.
- Calcul d'un score global et d'un niveau de maturité (Débutant, Basique,
  Intermédiaire, Avancé).
- Score détaillé par thème, avec recommandations prioritaires ciblées sur
  les points les plus faibles.
- Génération d'un rapport PDF complet (score, niveau, analyse par domaine,
  recommandations).
- **Suivi de l'évolution dans le temps** : chaque évaluation est associée à
  une entreprise (par nom) et enregistrée localement. Lors d'une nouvelle
  évaluation pour la même entreprise, l'application affiche la comparaison
  avec le score précédent et un graphique d'évolution, à l'écran comme dans
  le rapport PDF.

## Stack technique

Python, Streamlit (interface), ReportLab (génération PDF), SQLite
(historique des évaluations — module standard `sqlite3`, aucune dépendance
supplémentaire).

## Installation locale

```bash
pip install -r requirements.txt
streamlit run app.py
```

La base `historique.db` est créée automatiquement au premier lancement.

## Note sur le périmètre du projet

Ce projet a été réalisé dans le cadre d'un stage de 6 semaines (3 jalons de
15 jours), avec un périmètre volontairement limité : questionnaire simple,
scoring basique, pas de comparaison à une norme internationale (ISO 27001,
NIST), pas de développement full-stack — ces choix sont documentés dans le
cahier des charges du stage et assumés comme tels.

**Le suivi des évaluations dans le temps** (module `historique.py`) a été
ajouté après le stage, en reprenant une extension explicitement suggérée
par le cahier des charges ("ajouter un suivi des scores dans le temps pour
une même PME"). Le reste de l'application correspond au livrable produit
pendant le stage.

## Limites connues

- Pas de tests automatisés à ce stade.
- L'identification d'une entreprise se fait par son nom saisi librement (pas
  de compte/authentification) : deux entreprises avec un nom identique
  partageraient le même historique.
- Le scoring reste volontairement simple (comptage de bonnes pratiques),
  sans pondération par criticité — cohérent avec le périmètre initial du
  stage.
