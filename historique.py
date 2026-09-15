"""
Suivi des évaluations dans le temps, par entreprise.

Extension suggérée par le cahier des charges du stage ("Ajouter un suivi
des scores dans le temps pour une même PME"). Utilise SQLite, déjà cité
dans le document de cadrage comme option de stockage légère — pas de
nouvelle dépendance ajoutée au projet.
"""

import json
import os
import sqlite3
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(__file__), "historique.db")


def _connexion():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Crée la table si elle n'existe pas encore. À appeler au démarrage de l'app."""
    conn = _connexion()
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS evaluations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nom_pme TEXT NOT NULL,
            date_evaluation TEXT NOT NULL,
            score INTEGER NOT NULL,
            total_questions INTEGER NOT NULL,
            niveau TEXT NOT NULL,
            scores_par_theme TEXT NOT NULL
        )
        """
    )
    conn.commit()
    conn.close()


def enregistrer_evaluation(nom_pme: str, score: int, total_questions: int, niveau: str, scores_par_theme: list) -> None:
    """Enregistre le résultat d'une évaluation pour une PME donnée."""
    conn = _connexion()
    conn.execute(
        """
        INSERT INTO evaluations (nom_pme, date_evaluation, score, total_questions, niveau, scores_par_theme)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (
            nom_pme.strip(),
            datetime.now().isoformat(timespec="seconds"),
            score,
            total_questions,
            niveau,
            json.dumps(scores_par_theme, ensure_ascii=False),
        ),
    )
    conn.commit()
    conn.close()


def get_historique(nom_pme: str) -> list:
    """
    Renvoie toutes les évaluations passées d'une PME (par nom), triées de la
    plus ancienne à la plus récente. Chaque entrée est un dict avec :
    date_evaluation, score, total_questions, niveau, scores_par_theme.
    """
    conn = _connexion()
    lignes = conn.execute(
        """
        SELECT date_evaluation, score, total_questions, niveau, scores_par_theme
        FROM evaluations
        WHERE nom_pme = ?
        ORDER BY date_evaluation ASC
        """,
        (nom_pme.strip(),),
    ).fetchall()
    conn.close()

    return [
        {
            "date_evaluation": ligne["date_evaluation"],
            "score": ligne["score"],
            "total_questions": ligne["total_questions"],
            "niveau": ligne["niveau"],
            "scores_par_theme": json.loads(ligne["scores_par_theme"]),
        }
        for ligne in lignes
    ]


def get_derniere_evaluation_avant(nom_pme: str, avant_id_courant=None) -> dict | None:
    """
    Renvoie la dernière évaluation enregistrée pour cette PME (avant celle en
    cours), ou None s'il n'y en a pas. Utile pour afficher "vous étiez à X,
    vous êtes maintenant à Y".
    """
    historique = get_historique(nom_pme)
    if len(historique) < 1:
        return None
    return historique[-1]


def liste_entreprises() -> list:
    """Renvoie la liste des noms de PME distincts déjà évalués, triés par ordre alphabétique."""
    conn = _connexion()
    lignes = conn.execute("SELECT DISTINCT nom_pme FROM evaluations ORDER BY nom_pme ASC").fetchall()
    conn.close()
    return [ligne["nom_pme"] for ligne in lignes]
