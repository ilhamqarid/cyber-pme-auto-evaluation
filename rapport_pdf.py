import io
import os
from datetime import datetime

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.utils import ImageReader
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    HRFlowable,
    KeepTogether,
    Image,
)

from questionnaire import (
    TOTAL_QUESTIONS,
    INTERPRETATIONS,
    score_par_theme,
    recommandations_prioritaires,
)

NAVY = colors.HexColor("#0B1F3A")
BLUE = colors.HexColor("#1857B0")
GREEN = colors.HexColor("#1C7C4D")
ORANGE = colors.HexColor("#C98A1F")
RED = colors.HexColor("#C23B34")

TEXT = colors.HexColor("#243447")
MUTED = colors.HexColor("#66758A")
BORDER = colors.HexColor("#DCE4ED")
LIGHT_BLUE = colors.HexColor("#F3F7FC")
LIGHT_GREEN = colors.HexColor("#EDF7F1")
LIGHT_ORANGE = colors.HexColor("#FFF7E8")
LIGHT_RED = colors.HexColor("#FFF0EF")
WHITE = colors.white


NIVEAU_COULEUR_PDF = {
    "Débutant": RED,
    "Basique": ORANGE,
    "Intermédiaire": BLUE,
    "Avancé": GREEN,
}

ASSETS_DIR = os.path.join(os.path.dirname(__file__), "assets")
LOGO_CMRPI = os.path.join(ASSETS_DIR, "logo_cmrpi.png")
LOGO_EMC = os.path.join(ASSETS_DIR, "logo_emc.png")


def _image_hauteur_fixe(chemin, hauteur_cm):
    """Charge une image et calcule sa largeur pour une hauteur donnée, en conservant les proportions."""
    reader = ImageReader(chemin)
    largeur_px, hauteur_px = reader.getSize()
    largeur = hauteur_cm * cm * (largeur_px / hauteur_px)
    return Image(chemin, width=largeur, height=hauteur_cm * cm)


def _couleur_taux(taux: int):
    if taux >= 75:
        return GREEN
    if taux >= 50:
        return BLUE
    if taux >= 25:
        return ORANGE
    return RED


def _fond_niveau(couleur):
    if couleur == GREEN:
        return LIGHT_GREEN
    if couleur == ORANGE:
        return LIGHT_ORANGE
    if couleur == RED:
        return LIGHT_RED
    return LIGHT_BLUE


def _styles():
    styles = getSampleStyleSheet()

    styles.add(ParagraphStyle(
        name="HeaderSmall",
        fontName="Helvetica-Bold",
        fontSize=8,
        leading=10,
        textColor=colors.HexColor("#BFD0E5"),
        spaceAfter=3,
    ))

    styles.add(ParagraphStyle(
        name="TitlePro",
        fontName="Helvetica-Bold",
        fontSize=22,
        leading=26,
        textColor=WHITE,
        spaceAfter=5,
    ))

    styles.add(ParagraphStyle(
        name="SubtitlePro",
        fontName="Helvetica",
        fontSize=9.5,
        leading=13,
        textColor=colors.HexColor("#D9E5F3"),
    ))

    styles.add(ParagraphStyle(
        name="TitreCentre",
        fontName="Helvetica-Bold",
        fontSize=24,
        leading=28,
        textColor=NAVY,
        alignment=TA_CENTER,
        spaceBefore=6,
        spaceAfter=4,
    ))

    styles.add(ParagraphStyle(
        name="SousTitreCentre",
        fontName="Helvetica-Bold",
        fontSize=11,
        leading=14,
        textColor=colors.HexColor("#3a4a5e"),
        alignment=TA_CENTER,
        spaceAfter=8,
    ))

    styles.add(ParagraphStyle(
        name="MetaCentre",
        fontName="Helvetica",
        fontSize=8.3,
        leading=11,
        textColor=MUTED,
        alignment=TA_CENTER,
    ))

    styles.add(ParagraphStyle(
        name="Section",
        fontName="Helvetica-Bold",
        fontSize=13,
        leading=16,
        textColor=NAVY,
        spaceBefore=14,
        spaceAfter=7,
    ))

    styles.add(ParagraphStyle(
        name="BodyPro",
        fontName="Helvetica",
        fontSize=9.5,
        leading=13.5,
        textColor=TEXT,
    ))

    styles.add(ParagraphStyle(
        name="BodyMuted",
        fontName="Helvetica",
        fontSize=8.5,
        leading=11.5,
        textColor=MUTED,
    ))

    styles.add(ParagraphStyle(
        name="CardLabel",
        fontName="Helvetica-Bold",
        fontSize=8,
        leading=10,
        textColor=MUTED,
        alignment=TA_CENTER,
    ))

    styles.add(ParagraphStyle(
        name="BigScore",
        fontName="Helvetica-Bold",
        fontSize=28,
        leading=31,
        textColor=NAVY,
        alignment=TA_CENTER,
    ))

    styles.add(ParagraphStyle(
        name="ScorePercent",
        fontName="Helvetica-Bold",
        fontSize=9,
        leading=11,
        textColor=NAVY,
        alignment=TA_CENTER,
    ))

    styles.add(ParagraphStyle(
        name="Level",
        fontName="Helvetica-Bold",
        fontSize=17,
        leading=20,
        alignment=TA_CENTER,
    ))

    styles.add(ParagraphStyle(
        name="TableHead",
        fontName="Helvetica-Bold",
        fontSize=8.5,
        leading=10,
        textColor=WHITE,
    ))

    styles.add(ParagraphStyle(
        name="TableText",
        fontName="Helvetica",
        fontSize=8.7,
        leading=11,
        textColor=TEXT,
    ))

    styles.add(ParagraphStyle(
        name="RecommendationTitle",
        fontName="Helvetica-Bold",
        fontSize=9.5,
        leading=12,
        textColor=NAVY,
    ))

    return styles

def _draw_page(canvas, doc):
    canvas.saveState()

    width, height = A4

    canvas.setStrokeColor(BORDER)
    canvas.setLineWidth(0.5)
    canvas.line(
        doc.leftMargin,
        1.25 * cm,
        width - doc.rightMargin,
        1.25 * cm,
    )

    canvas.setFont("Helvetica", 7.5)
    canvas.setFillColor(MUTED)
    canvas.drawString(
        doc.leftMargin,
        0.82 * cm,
        "CYBER PME  |  Rapport d'auto-évaluation cybersécurité",
    )

    canvas.drawRightString(
        width - doc.rightMargin,
        0.82 * cm,
        f"Page {doc.page}",
    )

    canvas.restoreState()

def generer_rapport_pdf(reponses: dict, score: int, niveau: str, nom_pme: str = "", eval_precedente: dict | None = None) -> bytes:
    """
    Génère un rapport PDF professionnel et retourne son contenu en bytes.
    Compatible avec st.download_button(data=...).

    nom_pme : nom de l'entreprise évaluée, affiché dans l'en-tête du rapport.
    eval_precedente : dict optionnel (comme renvoyé par historique.get_historique)
        de la dernière évaluation enregistrée pour cette entreprise, pour
        afficher une comparaison. None si c'est la première évaluation.
    """

    styles = _styles()

    pct = round(100 * score / TOTAL_QUESTIONS)
    couleur_niveau = NIVEAU_COULEUR_PDF.get(niveau, BLUE)
    fond_niveau = _fond_niveau(couleur_niveau)

    themes = score_par_theme(reponses)
    recos = recommandations_prioritaires(reponses, nb_max=3)

    buffer = io.BytesIO()

    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        topMargin=1.45 * cm,
        bottomMargin=1.65 * cm,
        leftMargin=1.65 * cm,
        rightMargin=1.65 * cm,
        title="CYBER PME — Rapport d'auto-évaluation",
        author="Cyber PME",
        subject="Évaluation de la maturité cybersécurité",
    )

    story = []

    logo_cmrpi = _image_hauteur_fixe(LOGO_CMRPI, 1.5)
    logo_emc = _image_hauteur_fixe(LOGO_EMC, 1.5)

    logos_row = Table(
        [[logo_cmrpi, logo_emc]],
        colWidths=[8.15 * cm, 8.15 * cm],
    )
    logos_row.setStyle(TableStyle([
        ("ALIGN", (0, 0), (0, 0), "LEFT"),
        ("ALIGN", (1, 0), (1, 0), "RIGHT"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
        ("RIGHTPADDING", (0, 0), (-1, -1), 0),
        ("TOPPADDING", (0, 0), (-1, -1), 0),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
    ]))
    story.append(logos_row)
    story.append(Spacer(1, 0.3 * cm))

    story.append(Paragraph("Rapport d'auto-évaluation", styles["TitreCentre"]))
    story.append(Paragraph(
        "Évaluation de la maturité cybersécurité des PME marocaines",
        styles["SousTitreCentre"],
    ))

    date_export = datetime.now().strftime("%d/%m/%Y à %Hh%M")
    entreprise_txt = f"Entreprise : {nom_pme} · " if nom_pme else ""
    story.append(Paragraph(
        f"{entreprise_txt}22 questions évaluées · Guide de bonnes pratiques CMRPI/AUSIM · "
        f"Rapport généré le {date_export}",
        styles["MetaCentre"],
    ))
    story.append(Spacer(1, 0.15 * cm))

    story.append(
        Table(
            [[""]],
            colWidths=[4 * cm],
            rowHeights=[0.09 * cm],
            hAlign="CENTER",
            style=TableStyle([("BACKGROUND", (0, 0), (-1, -1), couleur_niveau)]),
        )
    )
    story.append(Spacer(1, 0.45 * cm))

    score_percent_style = ParagraphStyle(
        "ScorePercentDynamic",
        parent=styles["ScorePercent"],
        textColor=couleur_niveau,
    )

    score_card = Table(
        [
            [Paragraph("SCORE GLOBAL", styles["CardLabel"])],
            [Paragraph(f"{score} / {TOTAL_QUESTIONS}", styles["BigScore"])],
            [Paragraph(f"{pct}% des bonnes pratiques respectées", score_percent_style)],
        ],
        colWidths=[7.85 * cm],
        rowHeights=[0.55 * cm, 1.05 * cm, 0.6 * cm],
    )

    score_card.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), WHITE),
        ("BACKGROUND", (0, 0), (-1, 0), LIGHT_BLUE),
        ("BOX", (0, 0), (-1, -1), 0.8, BORDER),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
    ]))

    level_style = ParagraphStyle(
        "LevelDynamic",
        parent=styles["Level"],
        textColor=couleur_niveau,
    )

    level_card = Table(
        [
            [Paragraph("NIVEAU DE MATURITÉ", styles["CardLabel"])],
            [Paragraph(niveau, level_style)],
            [Paragraph(INTERPRETATIONS.get(niveau, ""), styles["BodyMuted"])],
        ],
        colWidths=[7.85 * cm],
        rowHeights=[0.55 * cm, 0.8 * cm, 0.85 * cm],
    )

    level_card.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), WHITE),
        ("BACKGROUND", (0, 1), (-1, 1), fond_niveau),
        ("BOX", (0, 0), (-1, -1), 0.8, BORDER),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("LEFTPADDING", (0, 2), (-1, 2), 12),
        ("RIGHTPADDING", (0, 2), (-1, 2), 12),
    ]))

    cards = Table(
        [[score_card, level_card]],
        colWidths=[8.05 * cm, 8.05 * cm],
    )

    cards.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
        ("RIGHTPADDING", (0, 0), (-1, -1), 0),
        ("TOPPADDING", (0, 0), (-1, -1), 0),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
    ]))

    story.append(cards)

    if eval_precedente is not None:
        ecart = score - eval_precedente["score"]
        signe = "+" if ecart >= 0 else ""
        couleur_ecart_hex = "1C7C4D" if ecart >= 0 else "C23B34"
        date_precedente = eval_precedente["date_evaluation"][:10]

        comparaison_box = Table(
            [[
                Paragraph(
                    f"<b>Évolution depuis la dernière évaluation</b> ({date_precedente})<br/>"
                    f"Score précédent : {eval_precedente['score']}/{TOTAL_QUESTIONS} ({eval_precedente['niveau']}) "
                    f"&rarr; Score actuel : {score}/{TOTAL_QUESTIONS} ({niveau}) "
                    f"&mdash; <font color='#{couleur_ecart_hex}'><b>{signe}{ecart} point(s)</b></font>",
                    styles["BodyPro"],
                )
            ]],
            colWidths=[16.3 * cm],
        )
        comparaison_box.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), LIGHT_BLUE),
            ("BOX", (0, 0), (-1, -1), 0.7, BORDER),
            ("LEFTPADDING", (0, 0), (-1, -1), 12),
            ("RIGHTPADDING", (0, 0), (-1, -1), 12),
            ("TOPPADDING", (0, 0), (-1, -1), 8),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
        ]))
        story.append(Spacer(1, 0.3 * cm))
        story.append(comparaison_box)

    story.append(Paragraph("1. Analyse par domaine", styles["Section"]))

    rows = [[
        Paragraph("Domaine évalué", styles["TableHead"]),
        Paragraph("Score", styles["TableHead"]),
        Paragraph("Progression", styles["TableHead"]),
    ]]

    for i, theme in enumerate(themes, start=1):
        taux = int(theme["taux"])
        couleur = _couleur_taux(taux)

        full_width = 3.7 * cm
        filled_width = max(0.03 * cm, full_width * taux / 100)

        bar_filled = Table(
            [[""]],
            colWidths=[filled_width],
            rowHeights=[0.18 * cm],
        )
        bar_filled.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), couleur),
            ("LEFTPADDING", (0, 0), (-1, -1), 0),
            ("RIGHTPADDING", (0, 0), (-1, -1), 0),
            ("TOPPADDING", (0, 0), (-1, -1), 0),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
        ]))

        bar = Table(
            [[bar_filled]],
            colWidths=[full_width],
            rowHeights=[0.18 * cm],
        )
        bar.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#E8EDF3")),
            ("LEFTPADDING", (0, 0), (-1, -1), 0),
            ("RIGHTPADDING", (0, 0), (-1, -1), 0),
            ("TOPPADDING", (0, 0), (-1, -1), 0),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ]))

        rows.append([
            Paragraph(f"{i}. {theme['theme']}", styles["TableText"]),
            Paragraph(
                f"<b>{theme['score_obtenu']}/{theme['score_max']}</b> · {taux}%",
                styles["TableText"],
            ),
            bar,
        ])

    theme_table = Table(
        rows,
        colWidths=[8.35 * cm, 3.35 * cm, 4.3 * cm],
        repeatRows=1,
    )

    theme_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), NAVY),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [WHITE, LIGHT_BLUE]),
        ("GRID", (0, 0), (-1, -1), 0.45, BORDER),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("RIGHTPADDING", (0, 0), (-1, -1), 8),
        ("TOPPADDING", (0, 0), (-1, -1), 7),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
    ]))

    story.append(theme_table)

    story.append(Paragraph("2. Recommandations prioritaires", styles["Section"]))

    themes_tries = sorted(themes, key=lambda t: t["taux"])
    themes_recommandes = [t for t in themes_tries if t["taux"] < 100][:3]

    if recos:
        recommendation_rows = []

        for index, (theme_info, recommendation) in enumerate(zip(themes_recommandes, recos), start=1):
            number = Table(
                [[str(index)]],
                colWidths=[0.55 * cm],
                rowHeights=[0.55 * cm],
            )
            number.setStyle(TableStyle([
                ("BACKGROUND", (0, 0), (-1, -1), RED),
                ("TEXTCOLOR", (0, 0), (-1, -1), WHITE),
                ("FONTNAME", (0, 0), (-1, -1), "Helvetica-Bold"),
                ("FONTSIZE", (0, 0), (-1, -1), 9),
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("BOX", (0, 0), (-1, -1), 0, RED),
                ("ROUNDEDCORNERS", [4, 4, 4, 4]),
            ]))

            content = Table(
                [[
                    Paragraph(theme_info["theme"], styles["RecommendationTitle"]),
                ], [
                    Paragraph(recommendation, styles["BodyPro"]),
                ]],
                colWidths=[14.9 * cm],
            )
            content.setStyle(TableStyle([
                ("BACKGROUND", (0, 0), (-1, -1), WHITE),
                ("LEFTPADDING", (0, 0), (-1, -1), 10),
                ("RIGHTPADDING", (0, 0), (-1, -1), 10),
                ("TOPPADDING", (0, 0), (-1, -1), 5),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
            ]))

            recommendation_rows.append([number, content])

        recommendation_table = Table(
            recommendation_rows,
            colWidths=[0.75 * cm, 15.55 * cm],
            hAlign="LEFT",
        )

        recommendation_table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), LIGHT_RED),
            ("BOX", (0, 0), (-1, -1), 0.6, BORDER),
            ("INNERGRID", (0, 0), (-1, -1), 0.4, BORDER),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("LEFTPADDING", (0, 0), (-1, -1), 6),
            ("RIGHTPADDING", (0, 0), (-1, -1), 6),
            ("TOPPADDING", (0, 0), (-1, -1), 6),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ]))

        story.append(recommendation_table)

    else:
        success_box = Table(
            [[
                Paragraph(
                    "<b>Évaluation favorable</b><br/>"
                    "Aucun point faible majeur n'a été détecté. "
                    "Les bonnes pratiques sont largement appliquées et intégrées.",
                    styles["BodyPro"],
                )
            ]],
            colWidths=[16.3 * cm],
        )

        success_box.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), LIGHT_GREEN),
            ("BOX", (0, 0), (-1, -1), 0.7, colors.HexColor("#B9DFC8")),
            ("LEFTPADDING", (0, 0), (-1, -1), 12),
            ("RIGHTPADDING", (0, 0), (-1, -1), 12),
            ("TOPPADDING", (0, 0), (-1, -1), 10),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
        ]))

        story.append(success_box)

    doc.build(
        story,
        onFirstPage=_draw_page,
        onLaterPages=_draw_page,
    )

    buffer.seek(0)
    return buffer.getvalue()