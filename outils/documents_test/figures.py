# -*- coding: utf-8 -*-
"""Figures vectorielles originales (dessins de l'équipe, CC BY 4.0) utilisées dans les documents du corpus."""
import math
import os
import sys

sys.path.insert(0, __import__("os").path.dirname(os.path.abspath(__file__)))
from dessin import icon, _rays, ptext, arrow, check, wrench, drop  # noqa: E402
from reportlab.lib.colors import HexColor, white  # noqa: E402

DARK = HexColor("#262a31")
RED = HexColor("#d7262e")
AMB = HexColor("#f0a000")
GREEN = HexColor("#2aa84a")
BLUE = HexColor("#2f6fd6")
GREY = HexColor("#8a8f98")
GREY_D = HexColor("#555b64")


def f_couleurs(c, w, h):
    cols = [("ROUGE", RED, "Danger ou défaut grave : arrêt dès que possible en sécurité", "huile"),
            ("JAUNE / ORANGE", AMB, "Attention : anomalie à faire contrôler", "moteur"),
            ("VERT", GREEN, "Fonction active (information)", "cli_g"),
            ("BLEU", BLUE, "Feu de route allumé (information)", "route")]
    bw = (w - 50) / 4
    for i, (t, col, d, ic) in enumerate(cols):
        x = 10 + i * (bw + 10)
        c.setFillColor(white)
        c.setStrokeColor(HexColor("#d5d8dd"))
        c.roundRect(x, 12, bw, h - 24, 4, fill=1, stroke=1)
        c.setFillColor(DARK)
        c.roundRect(x + bw / 2 - 22, h - 60, 44, 34, 6, fill=1, stroke=0)
        icon(c, ic, x + bw / 2, h - 43, 20, col)
        ptext(c, x + bw / 2, h - 76, t, 8, "LSB", col, "c")
        from reportlab.platypus import Paragraph
        from reportlab.lib.styles import ParagraphStyle
        p = Paragraph(d, ParagraphStyle("x", fontName="LS", fontSize=7.2, leading=9, alignment=1))
        p.wrap(bw - 10, 60)
        p.drawOn(c, x + 5, h - 84 - p.height)


def f_pictos(c, w, h):
    items = [("moteur", "Moteur / injection", AMB), ("huile", "Pression d'huile", RED), ("batterie", "Charge batterie", RED),
             ("temp", "Température liquide", RED), ("abs", "ABS", AMB), ("cle", "Entretien", AMB),
             ("carburant", "Réserve carburant", AMB), ("route", "Feu de route", BLUE), ("cli_g", "Clignotant", GREEN)]
    cols = 3
    cw = (w - 20) / cols
    rh = (h - 20) / 3
    for k, (ic, lab, col) in enumerate(items):
        x = 10 + (k % cols) * cw
        y = h - 10 - (k // cols + 1) * rh
        c.setFillColor(DARK)
        c.roundRect(x + 8, y + 8, 46, rh - 16, 6, fill=1, stroke=0)
        icon(c, ic, x + 31, y + rh / 2, 22, col)
        ptext(c, x + 64, y + rh / 2 + 2, lab, 8.4, "LSB", DARK)
        ptext(c, x + 64, y + rh / 2 - 10, "pictogramme n° %d" % (k + 1), 7, "LS", GREY_D)


def f_jump(c, w, h):
    def batt(x, y, lab):
        c.setFillColor(HexColor("#3a3f47"))
        c.roundRect(x, y, 120, 70, 6, fill=1, stroke=0)
        c.setFillColor(RED)
        c.rect(x + 90, y + 70, 18, 8, fill=1, stroke=0)
        c.setFillColor(GREY_D)
        c.rect(x + 12, y + 70, 18, 8, fill=1, stroke=0)
        ptext(c, x + 99, y + 52, "+", 14, "LSB", white, "c")
        ptext(c, x + 21, y + 52, "-", 14, "LSB", white, "c")
        ptext(c, x + 60, y + 20, lab, 8, "LSB", white, "c")
    y0 = 40
    batt(30, y0, "batterie déchargée")
    batt(w - 150, y0, "batterie de secours")
    c.setLineWidth(3)
    c.setStrokeColor(RED)
    c.bezier(129, y0 + 78, 200, y0 + 140, w - 200, y0 + 140, w - 51, y0 + 78)
    c.setStrokeColor(DARK)
    c.bezier(w - 129, y0 + 78, w - 190, y0 + 120, 210, y0 + 20, 190, y0 + 10)
    c.setFillColor(GREY)
    c.rect(170, y0 - 6, 60, 12, fill=1, stroke=0)
    ptext(c, 200, y0 - 20, "masse moteur (pièce métallique", 7, "LS", DARK, "c")
    ptext(c, 200, y0 - 29, "non peinte, loin de la batterie)", 7, "LS", DARK, "c")
    for n, (x, y) in enumerate([(129, y0 + 92), (w - 51, y0 + 92), (w - 129, y0 + 92), (200, y0 + 14)]):
        c.setFillColor(DARK)
        c.circle(x, y, 7, fill=1, stroke=0)
        ptext(c, x, y - 3, str(n + 1), 8, "LSB", white, "c")
    ptext(c, w / 2, h - 16, "Ordre de branchement : 1 - 2 - 3 - 4    |    Ordre de débranchement : 4 - 3 - 2 - 1", 8, "LSB", DARK, "c")


def f_etoile(c, w, h):
    cx, cy, r = w / 2 - 80, h / 2, min(h, w) / 2 - 22
    c.setFillColor(HexColor("#b8bdc4"))
    c.circle(cx, cy, r, fill=1, stroke=0)
    c.setFillColor(HexColor("#d9dce0"))
    c.circle(cx, cy, r * 0.32, fill=1, stroke=0)
    order = [0, 2, 4, 1, 3]
    pts = []
    for k in range(5):
        a = math.pi / 2 + k * 2 * math.pi / 5
        pts.append((cx + math.cos(a) * r * 0.62, cy + math.sin(a) * r * 0.62))
    for i in range(5):
        a, b = pts[order[i]], pts[order[(i + 1) % 5]]
        arrow(c, a[0], a[1], b[0], b[1], AMB, 1.2, 6)
    for n, k in enumerate(order):
        x, y = pts[k]
        c.setFillColor(DARK)
        c.circle(x, y, 9, fill=1, stroke=0)
        ptext(c, x, y - 3.5, str(n + 1), 9, "LSB", white, "c")
    tx = cx + r + 30
    for j, t in enumerate(["Serrer en étoile, en croix :", "jamais écrou par écrou en tournant.", "1re passe : approche à la main,",
                           "2e passe : couple du manuel", "constructeur (clé dynamométrique)."]):
        ptext(c, tx, h - 40 - j * 14, t, 8.2, "LSB" if j == 0 else "LS", DARK)


def f_cvt(c, w, h):
    cx1, cx2, cy = w * 0.28, w * 0.72, h / 2 + 4
    c.setFillColor(HexColor("#c9ced5"))
    c.setStrokeColor(GREY_D)
    c.roundRect(w * 0.12, 16, w * 0.76, h - 32, 36, fill=1, stroke=1)
    c.setFillColor(HexColor("#9aa1ab"))
    c.circle(cx1, cy, 38, fill=1, stroke=0)
    c.circle(cx2, cy, 30, fill=1, stroke=0)
    c.setStrokeColor(DARK)
    c.setLineWidth(5)
    c.line(cx1, cy + 34, cx2, cy + 26)
    c.line(cx1, cy - 34, cx2, cy - 26)
    c.arc(cx1 - 34, cy - 34, cx1 + 34, cy + 34, 90, 180)
    c.arc(cx2 - 26, cy - 26, cx2 + 26, cy + 26, -90, 180)
    ptext(c, cx1, 24, "poulie motrice (variateur)", 7.4, "LSB", DARK, "c")
    ptext(c, cx2, 24, "poulie menée + embrayage centrifuge", 7.4, "LSB", DARK, "c")
    ptext(c, w / 2, cy + 44, "courroie", 7.4, "LSB", AMB, "c")


def f_jauge(c, w, h):
    x = 90
    top = h - 20
    c.setFillColor(DARK)
    c.roundRect(x - 12, top - 14, 24, 14, 3, fill=1, stroke=0)
    c.setFillColor(HexColor("#b8bdc4"))
    c.rect(x - 3, 18, 6, top - 32, fill=1, stroke=0)
    c.setFillColor(HexColor("#c88a1b"))
    c.rect(x - 3, 18, 6, (top - 32) * 0.45, fill=1, stroke=0)
    for lab, yy in [("MAX (ou H / F)", 18 + (top - 32) * 0.55), ("MIN (ou L / ADD)", 18 + (top - 32) * 0.3)]:
        c.setStrokeColor(DARK)
        c.setLineWidth(1)
        c.line(x - 8, yy, x + 8, yy)
        ptext(c, x + 14, yy - 3, lab, 8, "LSB", DARK)
    ptext(c, x + 160, h / 2 + 10, "Niveau correct : entre les deux repères.", 8.2, "LSB", DARK)
    ptext(c, x + 160, h / 2 - 4, "Le libellé des repères varie selon le constructeur ;", 7.6, "LS", DARK)
    ptext(c, x + 160, h / 2 - 16, "les conditions de mesure sont dans le manuel.", 7.6, "LS", DARK)


def f_pneu(c, w, h):
    bx, by = 40, h / 2 - 20
    c.setFillColor(HexColor("#2b2e33"))
    c.rect(bx, by, w - 200, 40, fill=1, stroke=0)
    c.setFillColor(white)
    for k in range(6):
        c.rect(bx + 20 + k * ((w - 240) / 6), by + 18, 14, 22, fill=1, stroke=0)
    c.setFillColor(AMB)
    c.rect(bx + 20 + 2 * ((w - 240) / 6) + 14, by + 18, (w - 240) / 6 - 14, 7, fill=1, stroke=0)
    ptext(c, bx + 40 + 2 * ((w - 240) / 6), by + 52, "témoin d'usure (TWI)", 7.6, "LSB", AMB, "c")
    ptext(c, w - 150, by + 26, "Sculptures arasées au", 7.8, "LS", DARK)
    ptext(c, w - 150, by + 14, "niveau du témoin :", 7.8, "LS", DARK)
    ptext(c, w - 150, by + 2, "pneu à remplacer.", 7.8, "LSB", RED)


def f_obd(c, w, h):
    x, y = w / 2 - 110, h / 2 - 25
    c.setFillColor(HexColor("#3a3f47"))
    p = c.beginPath()
    p.moveTo(x, y + 50)
    p.lineTo(x + 220, y + 50)
    p.lineTo(x + 205, y)
    p.lineTo(x + 15, y)
    p.close()
    c.drawPath(p, fill=1, stroke=0)
    for row, n in ((y + 32, 8), (y + 14, 8)):
        for k in range(n):
            c.setFillColor(HexColor("#d9dce0"))
            c.circle(x + 35 + k * 21.5, row, 4, fill=1, stroke=0)
            num = k + 1 if row > y + 20 else k + 9
            ptext(c, x + 35 + k * 21.5, row + (7 if row > y + 20 else -13), str(num), 6.2, "LS", white if row > y + 20 else DARK, "c")
    ptext(c, w / 2, h - 18, "Prise de diagnostic OBD-II à 16 broches (norme SAE J1962), vue de face", 8, "LSB", DARK, "c")
    ptext(c, w / 2, 12, "Emplacement habituel : sous la planche de bord, côté conducteur (voir le manuel du véhicule).", 7.4, "LS", DARK, "c")


def f_hv(c, w, h):
    c.setStrokeColor(HexColor("#f07800"))
    c.setLineWidth(7)
    c.bezier(40, h / 2, 140, h - 20, 260, 20, w - 140, h / 2)
    ptext(c, w / 2, h - 18, "Câbles haute tension : gaine ORANGE", 8.4, "LSB", HexColor("#f07800"), "c")
    tx = w - 120
    c.setFillColor(HexColor("#f0c000"))
    p = c.beginPath()
    p.moveTo(tx, 30)
    p.lineTo(tx + 70, 30)
    p.lineTo(tx + 35, 92)
    p.close()
    c.drawPath(p, fill=1, stroke=0)
    c.setStrokeColor(DARK)
    c.setLineWidth(2)
    c.line(tx + 38, 80, tx + 30, 60)
    c.line(tx + 30, 60, tx + 42, 58)
    c.line(tx + 42, 58, tx + 33, 38)
    ptext(c, 40, 16, "Ne jamais toucher, couper ni débrancher : intervention réservée au personnel habilité.", 7.8, "LSB", DARK)


def f_check(c, w, h):
    zones = ["Avant", "Arrière", "Côté gauche", "Côté droit", "Tableau de bord", "Compartiment moteur"]
    bw = (w - 70) / 6
    for i, z in enumerate(zones):
        x = 10 + i * (bw + 10)
        c.setFillColor(white)
        c.setStrokeColor(HexColor("#d5d8dd"))
        c.roundRect(x, 14, bw, h - 28, 4, fill=1, stroke=1)
        check(c, x + bw / 2, h / 2 + 8, 9)
        ptext(c, x + bw / 2, 26, z, 7.4, "LSB", DARK, "c")
        ptext(c, x + 10, h - 30, "photo %d" % (i + 1), 6.8, "LS", GREY_D)


FIGS = {
    "couleurs": (f_couleurs, 140), "pictos": (f_pictos, 210), "jump": (f_jump, 200), "etoile": (f_etoile, 170),
    "cvt": (f_cvt, 140), "jauge": (f_jauge, 150), "pneu": (f_pneu, 110), "obd": (f_obd, 130), "hv": (f_hv, 120),
    "checkphotos": (f_check, 90),
}
