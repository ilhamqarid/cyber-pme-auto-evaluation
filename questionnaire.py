THEMES = [
    "Gouvernance et politique de sécurité",
    "Sensibilisation des utilisateurs",
    "Sécurité des postes de travail et gestion des accès",
    "Protection des données",
    "Sécurité des réseaux et gestion des incidents",
]

QUESTIONS = [
    {"id": 1, "theme": THEMES[0], "texte": "Votre entreprise dispose-t-elle d'une politique de sécurité informatique écrite ?"},
    {"id": 2, "theme": THEMES[0], "texte": "Les rôles et responsabilités en matière de sécurité sont-ils clairement définis ?"},
    {"id": 3, "theme": THEMES[0], "texte": "Effectuez-vous un suivi régulier des risques de sécurité informatique ?"},
    {"id": 4, "theme": THEMES[0], "texte": "Votre entreprise respecte-t-elle les normes et la réglementation en vigueur (ex. protection des données) ?"},

    {"id": 5, "theme": THEMES[1], "texte": "Les employés reçoivent-ils une formation ou une sensibilisation à la cybersécurité ?"},
    {"id": 6, "theme": THEMES[1], "texte": "Les employés savent-ils reconnaître un e-mail ou message frauduleux (phishing) ?"},
    {"id": 7, "theme": THEMES[1], "texte": "Des campagnes de sensibilisation sont-elles organisées régulièrement ?"},
    {"id": 8, "theme": THEMES[1], "texte": "Existe-t-il une procédure claire pour signaler un incident ou un comportement suspect ?"},

    {"id": 9, "theme": THEMES[2], "texte": "Tous les postes de travail sont-ils équipés d'un antivirus à jour ?"},
    {"id": 10, "theme": THEMES[2], "texte": "Les logiciels et systèmes d'exploitation sont-ils régulièrement mis à jour ?"},
    {"id": 11, "theme": THEMES[2], "texte": "Un pare-feu est-il installé et actif sur le réseau ou les postes ?"},
    {"id": 12, "theme": THEMES[2], "texte": "Les mots de passe utilisés sont-ils robustes (longueur, complexité) ?"},
    {"id": 13, "theme": THEMES[2], "texte": "Les droits d'accès sont-ils limités selon les besoins de chaque utilisateur ?"},

    {"id": 14, "theme": THEMES[3], "texte": "Les données de l'entreprise sont-elles sauvegardées régulièrement ?"},
    {"id": 15, "theme": THEMES[3], "texte": "Les sauvegardes sont-elles testées pour vérifier qu'elles sont restaurables ?"},
    {"id": 16, "theme": THEMES[3], "texte": "Les données sensibles sont-elles chiffrées lorsque nécessaire ?"},
    {"id": 17, "theme": THEMES[3], "texte": "Les données sont-elles stockées de manière sécurisée (accès contrôlé, hébergement fiable) ?"},

    {"id": 18, "theme": THEMES[4], "texte": "Le réseau Wi-Fi de l'entreprise est-il protégé (mot de passe fort, chiffrement) ?"},
    {"id": 19, "theme": THEMES[4], "texte": "Les connexions à distance (télétravail, VPN) sont-elles sécurisées ?"},
    {"id": 20, "theme": THEMES[4], "texte": "Existe-t-il une procédure de réponse en cas d'incident de sécurité ?"},
    {"id": 21, "theme": THEMES[4], "texte": "Un plan de continuité ou de reprise d'activité est-il prévu en cas d'incident majeur ?"},
    {"id": 22, "theme": THEMES[4], "texte": "La sécurité de l'entreprise fait-elle l'objet d'une réévaluation et d'une amélioration continue ?"},
]

TOTAL_QUESTIONS = len(QUESTIONS)  # 22

REPONSES_POSSIBLES = ["Oui", "Non", "Je ne sais pas"]

RECOMMANDATIONS = {
    THEMES[0]: "Rédiger une politique de sécurité simple et désigner un responsable sécurité.",
    THEMES[1]: "Organiser une sensibilisation régulière des employés (phishing, bonnes pratiques).",
    THEMES[2]: "Mettre à jour les antivirus/systèmes et renforcer les mots de passe et les accès.",
    THEMES[3]: "Mettre en place des sauvegardes régulières et testées, et chiffrer les données sensibles.",
    THEMES[4]: "Sécuriser le Wi-Fi/VPN et définir une procédure de réponse aux incidents.",
}


def calculer_score(reponses: dict) -> int:
    return sum(1 for q in QUESTIONS if reponses.get(q["id"]) == "Oui")


def niveau_maturite(score: int) -> str:
    if score <= 6:
        return "Débutant"
    elif score <= 13:
        return "Basique"
    elif score <= 18:
        return "Intermédiaire"
    else:
        return "Avancé"


INTERPRETATIONS = {
    "Débutant": "Risques élevés, mesures de base à mettre en place en priorité.",
    "Basique": "Quelques bonnes pratiques en place, mais des lacunes importantes subsistent.",
    "Intermédiaire": "Bon niveau de maturité, avec des axes d'amélioration ciblés.",
    "Avancé": "Bonnes pratiques largement appliquées et intégrées.",
}


def score_par_theme(reponses: dict) -> list:
    resultats = []
    for theme in THEMES:
        questions_theme = [q for q in QUESTIONS if q["theme"] == theme]
        score_max = len(questions_theme)
        score_obtenu = sum(1 for q in questions_theme if reponses.get(q["id"]) == "Oui")
        taux = round(100 * score_obtenu / score_max) if score_max else 0
        resultats.append({
            "theme": theme,
            "score_obtenu": score_obtenu,
            "score_max": score_max,
            "taux": taux,
        })
    return resultats


def recommandations_prioritaires(reponses: dict, nb_max: int = 3) -> list:
    themes_tries = sorted(score_par_theme(reponses), key=lambda t: t["taux"])
    recos = []
    for t in themes_tries[:nb_max]:
        if t["taux"] < 100:  # inutile de recommander un thème déjà parfait
            recos.append(RECOMMANDATIONS[t["theme"]])
    return recos