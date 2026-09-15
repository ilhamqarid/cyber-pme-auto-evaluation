import streamlit as st
from questionnaire import (
    QUESTIONS,
    THEMES,
    TOTAL_QUESTIONS,
    REPONSES_POSSIBLES,
    calculer_score,
    niveau_maturite,
    INTERPRETATIONS,
    score_par_theme,
    recommandations_prioritaires,
)
from rapport_pdf import generer_rapport_pdf
import historique

historique.init_db()


def html(contenu: str) -> None:
    lignes_nettoyees = "\n".join(ligne.strip() for ligne in contenu.strip().split("\n"))
    st.markdown(lignes_nettoyees, unsafe_allow_html=True)


st.set_page_config(
    page_title="Cyber PME | Auto-évaluation",
    page_icon="🛡️",
    layout="centered",
    initial_sidebar_state="collapsed",
)

THEME_ICONS = {
    THEMES[0]: "📋",
    THEMES[1]: "🎓",
    THEMES[2]: "💻",
    THEMES[3]: "🗄️",
    THEMES[4]: "🌐",
}

THEME_LABELS_COURTS = {
    THEMES[0]: "Gouvernance",
    THEMES[1]: "Sensibilisation",
    THEMES[2]: "Postes & accès",
    THEMES[3]: "Protection données",
    THEMES[4]: "Réseaux & incidents",
}

NIVEAU_COULEUR = {
    "Débutant": "#c23b34",
    "Basique": "#c98a1f",
    "Intermédiaire": "#1857b0",
    "Avancé": "#1c7c4d",
}

ZONES_NIVEAU = [
    ("Débutant", 0, 6, "#c23b34"),
    ("Basique", 7, 13, "#c98a1f"),
    ("Intermédiaire", 14, 18, "#1857b0"),
    ("Avancé", 19, 22, "#1c7c4d"),
]

html(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Manrope:wght@600;700;800&family=Inter:wght@400;500;600;700&display=swap');

    :root {
        /* Palette institutionnelle inspirée des logos CMRPI (arc rouge/vert/bleu) et EMC (bleu marine) */
        --navy: #0b1f3a;
        --navy-2: #14315a;
        --blue: #1857b0;
        --blue-dark: #0e3d80;
        --red: #c23b34;
        --red-dark: #a02e28;
        --green: #1c7c4d;
        --bg: #eef2f8;
        --text-muted: #5b6b82;
        --card-border: #e3e9f2;
    }

    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
    h1, h2, h3, .brand-name, .theme-card-header h3, .section-title h2 { font-family: 'Manrope', sans-serif; }

    #MainMenu, footer, header {visibility: hidden;}

    .stApp { background-color: var(--bg); }
    .block-container { padding-top: 1.2rem; max-width: 780px; }

    .brand-bar {
        position: relative;
        display: flex;
        align-items: center;
        justify-content: space-between;
        background: #ffffff;
        border-radius: 14px;
        padding: 14px 20px 12px 20px;
        margin-bottom: 22px;
        box-shadow: 0 4px 16px rgba(11, 31, 58, 0.08);
        border: 1px solid var(--card-border);
        overflow: hidden;
    }

    .brand-bar::before {
        content: "";
        position: absolute; top: 0; left: 0; right: 0; height: 4px;
        background: linear-gradient(90deg, var(--red) 0% 33%, var(--green) 33% 66%, var(--blue) 66% 100%);
    }
    .brand-left { display: flex; align-items: center; gap: 12px; }
    .brand-icon {
        width: 54px; height: 54px; border-radius: 13px;
        background: linear-gradient(135deg, var(--navy) 0%, var(--blue) 100%);
        display: flex; align-items: center; justify-content: center;
        font-size: 1.15rem;
        box-shadow: 0 3px 8px rgba(24, 87, 176, 0.35);
        flex-shrink: 0;
    }
    .brand-name { color: var(--navy); font-weight: 800; font-size: 1.05rem; line-height: 1.1; letter-spacing: .01em; }
    .brand-tag { color: var(--text-muted); font-size: 0.72rem; }
    .brand-step {
        color: var(--blue); font-weight: 700; font-size: 0.85rem;
        background: rgba(24,87,176,0.10); padding: 4px 12px; border-radius: 999px;
        border: 1px solid rgba(24,87,176,0.18);
    }
    .intro-text { text-align: center; margin: 4px 0 22px 0; }
    .intro-text p {
        color: var(--text-muted);
        font-size: 0.9rem;
        margin: 0;
    }
    .stepper {
        position: relative;
        display: flex;
        justify-content: space-between;
        margin: 4px 4px 26px 4px;
    }
    .stepper::before {
        content: "";
        position: absolute;
        top: 13px;
        left: 5%;
        right: 5%;
        height: 2px;
        background: #dde5ee;
        z-index: 0;
    }
    .stepper-fill {
        position: absolute;
        top: 13px;
        left: 5%;
        height: 2px;
        background: linear-gradient(90deg, var(--red), var(--green), var(--blue));
        z-index: 1;
        transition: width .3s ease;
    }
    .step {
        flex: 1;
        text-align: center;
        font-size: 0.64rem;
        color: var(--text-muted);
        position: relative;
        z-index: 2;
        padding: 0 2px;
    }
    .step .dot {
        width: 27px; height: 27px;
        border-radius: 50%;
        background: #ffffff;
        color: #7a8aa0;
        display: flex; align-items: center; justify-content: center;
        margin: 0 auto 6px auto;
        font-size: 0.78rem;
        font-weight: 700;
        border: 2px solid #dde5ee;
    }
    .step.done .dot { background: var(--green); border-color: var(--green); color: #fff; }
    .step.active .dot {
        background: #ffffff; border-color: var(--blue); color: var(--blue);
        box-shadow: 0 0 0 4px rgba(24,87,176,0.15);
    }
    .step.active { color: var(--navy); font-weight: 700; }
    .step .label { display: block; line-height: 1.2; }

    .theme-card-header {
        background: #ffffff;
        border-radius: 12px;
        padding: 18px 22px;
        margin-bottom: 18px;
        box-shadow: 0 2px 10px rgba(10, 37, 64, 0.07);
        border-left: 5px solid var(--blue);
    }
    .theme-card-header .eyebrow {
        text-transform: uppercase;
        letter-spacing: .06em;
        font-size: 0.68rem;
        color: var(--blue);
        font-weight: 700;
        margin-bottom: 2px;
    }
    .theme-card-header h3 { margin: 0; color: var(--navy); font-size: 1.18rem; font-weight: 700; }
    .theme-card-header span.meta { color: var(--text-muted); font-size: 0.82rem; }

    div[data-testid="stForm"] {
        background: #ffffff;
        padding: 10px 26px 22px 26px;
        border-radius: 16px;
        box-shadow: 0 4px 18px rgba(11, 31, 58, 0.08);
        border: 1px solid var(--card-border);
    }
    .q-block { padding: 18px 0 8px 0; border-bottom: 1px solid #eef1f5; }
    .q-block:last-of-type { border-bottom: none; }
    .q-number {
        display: inline-flex; align-items: center; justify-content: center;
        width: 23px; height: 23px; border-radius: 7px;
        background: var(--navy); color: #fff;
        font-size: 0.72rem; font-weight: 700; margin-right: 9px; flex-shrink: 0;
    }
    .q-text { font-size: 0.96rem; color: #1c2b3a; font-weight: 600; line-height: 1.4; }

    div[data-testid="stForm"] div[data-testid="stRadio"] label p {
        font-size: 0.86rem; color: #33445a; font-weight: 500;
    }
    div[data-testid="stForm"] div[data-testid="stRadio"] { margin-top: 6px; }
    /* Cartes de réponse radio (Oui / Non / Je ne sais pas) */
    div[data-testid="stForm"] div[data-testid="stRadio"] > div {
        gap: 8px;
    }
    div[data-testid="stForm"] div[data-testid="stRadio"] label {
        background: #f6f8fb;
        border: 1px solid #e3e9f2;
        border-radius: 8px;
        padding: 6px 14px !important;
        margin: 0 !important;
        transition: all .15s ease;
    }
    div[data-testid="stForm"] div[data-testid="stRadio"] label:hover {
        border-color: var(--blue);
        background: #eef4fc;
    }
    div[data-testid="stForm"] div[data-testid="stRadio"] label[data-baseweb="radio"]:has(input:checked) {
        border-color: var(--blue);
        background: rgba(24,87,176,0.08);
    }
    div[data-testid="stForm"] div[data-testid="column"] {
        display: flex;
        align-items: stretch;
    }
    div[data-testid="stForm"] div[data-testid="stFormSubmitButton"] {
        width: 100%;
        margin-top: 14px;
    }
    .stButton > button, button[kind="secondaryFormSubmit"], button[kind="primaryFormSubmit"] {
        border-radius: 10px;
        font-weight: 700;
        font-size: 0.9rem;
        padding: 0.62rem 1.2rem;
        width: 100%;
        border: 1.5px solid transparent;
        transition: all .15s ease;
        letter-spacing: .01em;
    }
    button[kind="secondaryFormSubmit"] {
        background: #ffffff;
        color: var(--red-dark);
        border-color: #ecc9c6;
    }
    button[kind="secondaryFormSubmit"]:hover:not(:disabled) {
        background: #fdf3f2;
        border-color: var(--red);
        color: var(--red-dark);
    }
    button[kind="secondaryFormSubmit"]:disabled { opacity: 0.4; }
    /* Suivant / Voir mes résultats : bouton principal bleu institutionnel */
    button[kind="primaryFormSubmit"] {
        background: linear-gradient(135deg, var(--blue-dark) 0%, var(--blue) 100%);
        box-shadow: 0 3px 10px rgba(24, 87, 176, 0.28);
    }
    button[kind="primaryFormSubmit"]:hover {
        background: linear-gradient(135deg, var(--navy) 0%, var(--blue-dark) 100%);
        box-shadow: 0 4px 14px rgba(24, 87, 176, 0.36);
        transform: translateY(-1px);
    }
    .section-title {
        display: flex; align-items: center; gap: 10px;
        margin: 6px 0 16px 0;
    }
    .section-title-icon {
        width: 32px; height: 32px; border-radius: 9px;
        background: linear-gradient(135deg, var(--navy) 0%, var(--blue) 100%);
        display: flex; align-items: center; justify-content: center;
        flex-shrink: 0;
    }
    .section-title h2 {
        color: var(--navy); font-size: 1.28rem; font-weight: 800; margin: 0;
    }
div[data-testid="stHorizontalBlock"]:has(.result-card) {
    display: grid !important;
    grid-template-columns: repeat(2, minmax(0, 1fr));
    gap: 1rem;
    align-items: stretch;
}
div[data-testid="stHorizontalBlock"]:has(.result-card) > div {
    min-width: 0 !important;
    width: 100% !important;
    display: flex !important;
}
div[data-testid="stHorizontalBlock"]:has(.donut) {
    min-height: 250px !important;
}

div[data-testid="stHorizontalBlock"]:has(.donut) .result-card {
    height: 250px !important;
    min-height: 250px !important;
    box-sizing: border-box;
}
div[data-testid="stHorizontalBlock"]:has(.theme-score-row) {
    min-height: 390px !important;
}

div[data-testid="stHorizontalBlock"]:has(.theme-score-row) .result-card {
    height: 390px !important;
    min-height: 390px !important;
    box-sizing: border-box;
}
div[data-testid="stHorizontalBlock"]:has(.result-card) > div > div {
    width: 100%;
    height: 100%;
    display: flex;
}

div[data-testid="stHorizontalBlock"]:has(.result-card) > div > div > div {
    width: 100%;
    height: 100%;
}

.result-card {
    box-sizing: border-box;
    width: 100%;
}

    .result-card {
        background: #ffffff;
        border-radius: 14px;
        padding: 18px 16px;
        box-shadow: 0 2px 10px rgba(10, 37, 64, 0.07);
        border: 1px solid #e8edf3;
        text-align: center;
        height: 100%;
        flex: 1;
        display: flex;
        flex-direction: column;
        justify-content: center;
    }
    .result-card[style*="text-align:left"] { justify-content: flex-start; }
    .result-card .label {
        color: var(--text-muted); font-size: 0.72rem; text-transform: uppercase;
        letter-spacing: .04em; font-weight: 700; margin-bottom: 10px;
    }
    .donut {
        width: 108px; height: 108px; border-radius: 50%;
        margin: 0 auto 8px auto;
        display: flex; align-items: center; justify-content: center;
    }
    .donut-inner {
        width: 80px; height: 80px; border-radius: 50%; background: #fff;
        display: flex; flex-direction: column; align-items: center; justify-content: center;
    }
    .donut-inner .score-num { font-size: 1.5rem; font-weight: 800; color: var(--navy); line-height: 1; }
    .donut-inner .score-den { font-size: 0.68rem; color: var(--text-muted); }
    .donut-pct { font-size: 0.78rem; color: var(--text-muted); margin-top: 2px; }

    .niveau-badge {
        display: inline-block; padding: 8px 16px; border-radius: 10px;
        font-weight: 800; font-size: 1.05rem; margin: 18px 0 8px 0;
    }
    .niveau-desc { color: var(--text-muted); font-size: 0.78rem; padding: 0 4px; }

    .position-track {
        position: relative; height: 10px; border-radius: 6px; overflow: visible;
        display: flex; margin: 30px 6px 6px 6px;
    }
    .position-zone:first-child { border-radius: 6px 0 0 6px; }
    .position-zone:last-child { border-radius: 0 6px 6px 0; }
    .position-marker {
        position: absolute; top: -14px;
        transform: translateX(-50%);
        font-size: 0.9rem;
        color: var(--navy);
    }
    .position-scale {
        display: flex; justify-content: space-between;
        font-size: 0.65rem; color: var(--text-muted); margin: 2px 6px 0 6px;
    }
    .theme-score-row { margin-bottom: 14px; }
    .theme-score-row .top-line {
        display: flex; justify-content: space-between; align-items: baseline;
        font-size: 0.85rem; color: #1c2b3a; margin-bottom: 5px;
    }
    .theme-score-row .top-line b { font-weight: 700; }
    .theme-score-row .pct { color: var(--text-muted); font-size: 0.78rem; }
    .bar-track { background: #e9edf3; border-radius: 6px; height: 8px; overflow: hidden; }
    .bar-fill { height: 100%; border-radius: 6px; }

    .reco-card {
        background: #fdf3f2; border: 1px solid #f1cdc9; border-radius: 12px;
        padding: 14px 16px; margin-bottom: 10px; border-left: 4px solid var(--red);
    }
    .reco-card b { color: var(--red-dark); }
    .reco-list { margin: 6px 0 0 18px; padding: 0; color: #4a2a26; font-size: 0.85rem; }
    .reco-list li { margin-bottom: 4px; }

    div[data-testid="stVerticalBlock"] .stButton > button {
        background: #ffffff;
        color: var(--navy);
        border: 1.5px solid #d7deea;
    }
    div[data-testid="stVerticalBlock"] .stButton > button:hover {
        border-color: var(--blue);
        color: var(--blue);
        background: #f5f8fd;
    }

    .app-footer {
        text-align: center; color: #9aa8bb; font-size: 0.76rem;
        margin-top: 30px; padding-top: 14px; border-top: 1px solid #e2e8f0;
    }
    </style>
    """
)
if "reponses" not in st.session_state:
    st.session_state.reponses = {}
if "theme_index" not in st.session_state:
    st.session_state.theme_index = 0
if "termine" not in st.session_state:
    st.session_state.termine = False
if "nom_pme" not in st.session_state:
    st.session_state.nom_pme = ""
if "historique_enregistre" not in st.session_state:
    st.session_state.historique_enregistre = False
if "eval_precedente" not in st.session_state:
    st.session_state.eval_precedente = None


def reset_questionnaire():
    st.session_state.reponses = {}
    st.session_state.theme_index = 0
    st.session_state.termine = False
    st.session_state.nom_pme = ""
    st.session_state.historique_enregistre = False
    st.session_state.eval_precedente = None

etape_txt = ""
if not st.session_state.termine:
    etape_txt = f'<div class="brand-step">{st.session_state.theme_index + 1} / {len(THEMES)}</div>'

html(
    f"""
    <div class="brand-bar">
        <div class="brand-left">
            <div class="brand-icon">
                <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="#ffffff" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M12 2 4 5v6c0 5 3.4 9 8 11 4.6-2 8-6 8-11V5l-8-3Z"></path>
                    <path d="m9 12 2 2 4-4"></path>
                </svg>
            </div>
            <div>
                <div class="brand-name">CYBER PME</div>
                <div class="brand-tag">Auto-évaluation cybersécurité</div>
            </div>
        </div>
        {etape_txt}
    </div>
    """
)
if st.session_state.termine:
    reponses = st.session_state.reponses
    score = calculer_score(reponses)
    niveau = niveau_maturite(score)
    couleur = NIVEAU_COULEUR[niveau]
    pct = round(100 * score / TOTAL_QUESTIONS)

    if not st.session_state.historique_enregistre:
        st.session_state.eval_precedente = historique.get_derniere_evaluation_avant(st.session_state.nom_pme)
        historique.enregistrer_evaluation(
            st.session_state.nom_pme,
            score,
            TOTAL_QUESTIONS,
            niveau,
            score_par_theme(reponses),
        )
        st.session_state.historique_enregistre = True

    html(
        f"""
        <div class="theme-card-header">
            <div class="eyebrow">Entreprise évaluée</div>
            <h3>🏢 {st.session_state.nom_pme}</h3>
        </div>
        """
    )

    html(
        """
        <div class="section-title">
            <div class="section-title-icon">
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#ffffff" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <line x1="12" y1="20" x2="12" y2="10"></line>
                    <line x1="18" y1="20" x2="18" y2="4"></line>
                    <line x1="6" y1="20" x2="6" y2="16"></line>
                </svg>
            </div>
            <h2>Résultats de votre évaluation</h2>
        </div>
        """
    )
    zones_html = ""
    for nom, lo, hi, coul in ZONES_NIVEAU:
        largeur = (hi - lo + 1) / TOTAL_QUESTIONS * 100
        zones_html += f'<div class="position-zone" style="width:{largeur}%; background:{coul};"></div>'
    marker_pos = score / TOTAL_QUESTIONS * 100

    html(
        f"""
        <div class="result-card" style="text-align:left;">
            <div class="label" style="text-align:center;">Positionnement</div>
            <div class="position-track">
                {zones_html}
                <div class="position-marker" style="left:{marker_pos}%;">▼</div>
            </div>
            <div class="position-scale"><span>0</span><span>6</span><span>13</span><span>18</span><span>22</span></div>
        </div>
        """
)

    st.markdown("")
    col1, col2 = st.columns(2, gap="medium")
    with col1:
        html(
            f"""
            <div class="result-card">
                <div class="label">Score global</div>
                <div class="donut" style="background: conic-gradient({couleur} 0% {pct}%, #e6ebf1 {pct}% 100%);">
                    <div class="donut-inner">
                        <div class="score-num">{score}</div>
                        <div class="score-den">/ {TOTAL_QUESTIONS}</div>
                    </div>
                </div>
                <div class="donut-pct">{pct}% des bonnes pratiques</div>
            </div>
            """
)
    with col2:
        html(
            f"""
            <div class="result-card">
                <div class="label">Niveau de maturité</div>
                <div class="niveau-badge" style="background:{couleur}18; color:{couleur};">{niveau}</div>
                <div class="niveau-desc">{INTERPRETATIONS[niveau]}</div>
            </div>
            """
)

    st.markdown("")
    col_a, col_b = st.columns(2, gap="medium")

    with col_a:
        lignes_html = ""
        for i, t in enumerate(score_par_theme(reponses), start=1):
            barre_couleur = "#1c7c4d" if t["taux"] >= 75 else ("#1857b0" if t["taux"] >= 50 else "#c98a1f" if t["taux"] >= 25 else "#c23b34")
            lignes_html += f"""
                <div class="theme-score-row">
                    <div class="top-line">
                        <span>{i}. {t['theme']}</span>
                        <span class="pct">{t['score_obtenu']}/{t['score_max']} · {t['taux']}%</span>
                    </div>
                    <div class="bar-track"><div class="bar-fill" style="width:{t['taux']}%; background:{barre_couleur};"></div></div>
                </div>
            """
        html(
            f"""
            <div class="result-card" style="text-align:left;">
                <div class="label">Score par thème</div>
                {lignes_html}
            </div>
            """
)

    with col_b:
        recos = recommandations_prioritaires(reponses, nb_max=3)
        if recos:
            items = "".join(f"<li>{r}</li>" for r in recos)
            reco_body = f"""
                <div class="reco-card">
                    <b>Thèmes à améliorer en priorité</b>
                    <ul class="reco-list">{items}</ul>
                </div>
            """
        else:
            reco_body = """
                <div class="reco-card" style="background:#eaf7ee; border-color:#bfe6cc;">
                    <b style="color:#1c7c4d;">Bravo, aucun point faible majeur détecté !</b>
                </div>
            """
        html(
            f"""
            <div class="result-card" style="text-align:left;">
                <div class="label">Recommandations prioritaires</div>
                {reco_body}
            </div>
            """
)

    st.markdown("")

    html(
        """
        <div class="section-title">
            <div class="section-title-icon">
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#ffffff" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <polyline points="3 17 9 11 13 15 21 7"></polyline>
                    <polyline points="14 7 21 7 21 14"></polyline>
                </svg>
            </div>
            <h2>Évolution dans le temps</h2>
        </div>
        """
    )

    eval_precedente = st.session_state.eval_precedente
    if eval_precedente is None:
        html(
            """
            <div class="result-card" style="text-align:left;">
                <span style="color:var(--text-muted); font-size:0.88rem;">
                    Il s'agit de la première évaluation enregistrée pour cette entreprise.
                    Revenez après une nouvelle évaluation pour suivre la progression du score dans le temps.
                </span>
            </div>
            """
        )
    else:
        ecart = score - eval_precedente["score"]
        signe = "+" if ecart >= 0 else ""
        couleur_ecart = "#1c7c4d" if ecart >= 0 else "#c23b34"
        date_precedente = eval_precedente["date_evaluation"][:10]
        html(
            f"""
            <div class="result-card" style="text-align:left;">
                <div class="label">Comparaison avec l'évaluation précédente ({date_precedente})</div>
                <span style="font-size:0.92rem; color:#1c2b3a;">
                    Score précédent : <b>{eval_precedente['score']}/{TOTAL_QUESTIONS}</b> ({eval_precedente['niveau']})
                    &nbsp;→&nbsp; Score actuel : <b>{score}/{TOTAL_QUESTIONS}</b> ({niveau})
                    &nbsp;·&nbsp;
                    <b style="color:{couleur_ecart};">{signe}{ecart} point{'s' if abs(ecart) > 1 else ''}</b>
                </span>
            </div>
            """
        )

    historique_complet = historique.get_historique(st.session_state.nom_pme)
    if len(historique_complet) > 1:
        st.markdown("")
        chart_data = {
            entry["date_evaluation"][:10]: entry["score"]
            for entry in historique_complet
        }
        st.line_chart(chart_data, height=220)
        st.caption(f"Score sur {TOTAL_QUESTIONS} points, au fil des évaluations de {st.session_state.nom_pme}.")

    st.markdown("<br>", unsafe_allow_html=True)
    col_reset, col_pdf = st.columns(2)
    with col_reset:
        if st.button("Recommencer l'évaluation", use_container_width=True):
            reset_questionnaire()
            st.rerun()
    with col_pdf:
        pdf_bytes = generer_rapport_pdf(
            reponses,
            score,
            niveau,
            nom_pme=st.session_state.nom_pme,
            eval_precedente=st.session_state.eval_precedente,
        )
        st.download_button(
            "📄 Télécharger le rapport PDF",
            data=pdf_bytes,
            file_name="rapport_cybersecurite_pme.pdf",
            mime="application/pdf",
            use_container_width=True,
        )

else:
    if not st.session_state.nom_pme:
        html(
            """
            <div class="theme-card-header">
                <div class="eyebrow">Avant de commencer</div>
                <h3>🏢 Nom de votre entreprise</h3>
                <span class="meta">Utilisé pour suivre l'évolution de votre score dans le temps</span>
            </div>
            """
        )
        with st.form(key="form_nom_pme"):
            nom_saisi = st.text_input(
                "Nom de l'entreprise",
                placeholder="Ex. Atelier Ben Salem",
                label_visibility="collapsed",
            )
            demarrer = st.form_submit_button("Commencer l'évaluation ➡️", type="primary", use_container_width=True)

        if demarrer:
            if nom_saisi.strip():
                st.session_state.nom_pme = nom_saisi.strip()
                st.rerun()
            else:
                st.warning("Merci de renseigner un nom d'entreprise pour continuer.")
        st.stop()

    idx = st.session_state.theme_index
    theme_courant = THEMES[idx]
    questions_theme = [q for q in QUESTIONS if q["theme"] == theme_courant]
    icone = THEME_ICONS.get(theme_courant, "•")

    fill_pct = (idx / (len(THEMES) - 1)) * 90 if len(THEMES) > 1 else 0

    steps_html = f'<div class="stepper"><div class="stepper-fill" style="width:{fill_pct}%;"></div>'
    for i in range(len(THEMES)):
        if i < idx:
            cls, content = "done", "✓"
        elif i == idx:
            cls, content = "active", str(i + 1)
        else:
            cls, content = "", str(i + 1)
        label = THEME_LABELS_COURTS[THEMES[i]]
        steps_html += f'<div class="step {cls}"><div class="dot">{content}</div><span class="label">{label}</span></div>'
    steps_html += "</div>"
    st.markdown(steps_html, unsafe_allow_html=True)

    html(
        f"""
        <div class="theme-card-header">
            <div class="eyebrow">Section {idx + 1} / {len(THEMES)}</div>
            <h3>{icone} {theme_courant}</h3>
            <span class="meta">{len(questions_theme)} question(s) dans cette section</span>
        </div>
        """
)

    with st.form(key=f"form_{idx}"):
        reponses_locales = {}
        for q in questions_theme:
            valeur_par_defaut = st.session_state.reponses.get(q["id"], REPONSES_POSSIBLES[0])
            index_defaut = REPONSES_POSSIBLES.index(valeur_par_defaut) if valeur_par_defaut in REPONSES_POSSIBLES else 0

            html(
                f"""
                <div class="q-block">
                    <span class="q-number">{q['id']}</span>
                    <span class="q-text">{q['texte']}</span>
                </div>
                """
)
            reponse = st.radio(
                f"Réponse à la question {q['id']}",
                REPONSES_POSSIBLES,
                index=index_defaut,
                horizontal=True,
                key=f"q_{q['id']}",
                label_visibility="collapsed",
            )
            reponses_locales[q["id"]] = reponse

        col_prev, col_next = st.columns(2)
        with col_prev:
            precedent = st.form_submit_button(
                "⬅️ Précédent", disabled=(idx == 0), use_container_width=True
            )
        with col_next:
            est_dernier = idx == len(THEMES) - 1
            suivant = st.form_submit_button(
                "Voir mes résultats ✅" if est_dernier else "Suivant ➡️",
                type="primary",
                use_container_width=True,
            )

    if precedent:
        st.session_state.reponses.update(reponses_locales)
        st.session_state.theme_index -= 1
        st.rerun()

    if suivant:
        st.session_state.reponses.update(reponses_locales)
        if est_dernier:
            st.session_state.termine = True
        else:
            st.session_state.theme_index += 1
        st.rerun()