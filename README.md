# 🛡️ Cyber PME : Auto-évaluation de la maturité cybersécurité

Outil d'auto-évaluation de la maturité cybersécurité destiné aux PME
marocaines, développé dans le cadre d'un stage à distance (CMRPI / Espace Maroc
Cyberconfiance, été 2026), basé sur le **Guide de bonnes pratiques
cybersécurité des PME au Maroc (CMRPI/AUSIM)**.

**Stack :** Python · Streamlit · ReportLab · SQLite


<img width="937" height="907" alt="image" src="https://github.com/user-attachments/assets/5c3a5216-3b25-4fb7-aea4-4b54a8bf2b12" />


---

## Fonctionnalités

- **Questionnaire structuré** : 22 questions fermées (Oui / Non / Je ne
  sais pas), réparties en 5 thèmes : gouvernance, sensibilisation, postes
  de travail et accès, protection des données, réseaux et gestion des
  incidents.
- **Scoring automatique** : calcul d'un score global et d'un niveau de
  maturité (Débutant, Basique, Intermédiaire, Avancé), avec un score
  détaillé par thème.
- **Recommandations priorisées** : suggestions ciblées sur les thèmes les
  plus faibles.
- **Rapport PDF** : génération d'un rapport complet (score, niveau,
  analyse par domaine, recommandations) prêt à être partagé avec un
  dirigeant de PME sans expertise technique.
- **Suivi dans le temps** : chaque évaluation est associée à une
  entreprise ; une nouvelle évaluation pour la même entreprise affiche la
  comparaison avec le score précédent et un graphique d'évolution, à
  l'écran comme dans le rapport PDF.

<img width="937" height="907" alt="image" src="https://github.com/user-attachments/assets/6783a9a5-33e4-4ff7-973a-38d3a31066f9" />


## Structure du projet

```
cybersecurity_pme_updated/
├── app.py              # Interface Streamlit
├── questionnaire.py     # Questions, thèmes, scoring, recommandations
├── historique.py        # Suivi des évaluations dans le temps (SQLite)
├── rapport_pdf.py        # Génération du rapport PDF (ReportLab)
├── assets/               # Logos CMRPI / EMC
├── requirements.txt
└── .gitignore
```

## Installation locale

```bash
pip install -r requirements.txt
streamlit run app.py
```

La base `historique.db` est créée automatiquement au premier lancement et
n'est pas versionnée (voir `.gitignore`).

## Contexte du projet

Réalisé en 6 semaines (3 jalons de 15 jours) dans le cadre d'un stage chez
CMRPI / Espace Maroc Cyberconfiance, ce projet s'appuie sur un référentiel
unique et reconnu le guide CMRPI/AUSIM , pour livrer un outil concret,
directement utilisable par des dirigeants de PME sans expertise technique.
Le choix d'une stack légère (Streamlit, ReportLab, SQLite) a permis d'aller
du questionnaire au rapport PDF final en un temps court, avec un prototype
fonctionnel de bout en bout dès la fin du stage.

## Limites connues

- Pas de tests automatisés à ce stade.
- L'identification d'une entreprise se fait par son nom saisi librement
  (pas de compte/authentification) : deux entreprises avec un nom
  identique partageraient le même historique.
- Le scoring reste volontairement simple (comptage de bonnes pratiques),
  sans pondération par criticité.

## Auteure

Ilham Qarid Élève-ingénieure en Génie Informatique, ENSA Fès
