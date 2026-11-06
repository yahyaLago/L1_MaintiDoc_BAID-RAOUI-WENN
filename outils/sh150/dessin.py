# -*- coding: utf-8 -*-
"""Helpers de mise en page et dessins vectoriels pour le manuel Urbano S150 (fictif)."""
import math
from reportlab.lib.pagesizes import A4
from reportlab.lib.colors import HexColor, white, black
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Paragraph, Table, TableStyle
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER

FD = "/usr/share/fonts/truetype/liberation/"
pdfmetrics.registerFont(TTFont("LS", FD + "LiberationSans-Regular.ttf"))
pdfmetrics.registerFont(TTFont("LSB", FD + "LiberationSans-Bold.ttf"))
pdfmetrics.registerFont(TTFont("LSI", FD + "LiberationSans-Italic.ttf"))
pdfmetrics.registerFont(TTFont("LSBI", FD + "LiberationSans-BoldItalic.ttf"))
from reportlab.pdfbase.pdfmetrics import registerFontFamily
registerFontFamily("LS", normal="LS", bold="LSB", italic="LSI", boldItalic="LSBI")

W, H = A4
M = 28
CW = W - 2 * M

DARK = HexColor("#262a31")
ORANGE = HexColor("#f08a00")
ORANGE_L = HexColor("#fdf0dc")
RED = HexColor("#d7262e")
RED_L = HexColor("#fbe3e3")
GREY = HexColor("#8a8f98")
GREY_L = HexColor("#f1f2f4")
GREY_M = HexColor("#d5d8dd")
GREY_D = HexColor("#555b64")
BODY = HexColor("#e9ebee")
BLUE = HexColor("#2f6fd6")
GREEN = HexColor("#2aa84a")
OFF = HexColor("#4a4f57")

MODEL = "Urbano S150"
EQUIP = "SCT-M-01"
SERIE = "URB150-0001"
VERSION = "v1.0 (2026-10)"
MAKER = "Motora"

ST = {
    "p": ParagraphStyle("p", fontName="LS", fontSize=8.2, leading=11, textColor=DARK),
    "ps": ParagraphStyle("ps", fontName="LS", fontSize=7.2, leading=9.4, textColor=DARK),
    "pxs": ParagraphStyle("pxs", fontName="LS", fontSize=6.4, leading=8, textColor=GREY_D),
    "pc": ParagraphStyle("pc", fontName="LS", fontSize=7, leading=9, textColor=DARK, alignment=TA_CENTER),
    "cap": ParagraphStyle("cap", fontName="LSI", fontSize=6.6, leading=8.4, textColor=GREY_D),
    "th": ParagraphStyle("th", fontName="LSB", fontSize=7.2, leading=9, textColor=white),
    "td": ParagraphStyle("td", fontName="LS", fontSize=7.2, leading=9, textColor=DARK),
    "ct": ParagraphStyle("ct", fontName="LSB", fontSize=7.6, leading=9.5, textColor=DARK),
}


def P(text, st="p"):
    return Paragraph(text, ST[st])


def para(c, text, x, ytop, w, st="p"):
    p = P(text, st)
    _, h = p.wrap(w, 1000)
    p.drawOn(c, x, ytop - h)
    return h


def ptext(c, x, y, s, size=8, font="LS", color=DARK, anchor="l"):
    c.setFont(font, size)
    c.setFillColor(color)
    if anchor == "c":
        c.drawCentredString(x, y, s)
    elif anchor == "r":
        c.drawRightString(x, y, s)
    else:
        c.drawString(x, y, s)


# ------------------------------------------------------------------ page frame
def header(c, n, title):
    c.setFillColor(DARK)
    c.rect(0, H - 24, W, 24, fill=1, stroke=0)
    c.setFillColor(ORANGE)
    c.rect(0, H - 26, W, 2, fill=1, stroke=0)
    ptext(c, M, H - 16, MODEL, 8.5, "LSB", white)
    ptext(c, W - M, H - 16, "Manuel d'utilisation et d'entretien  |  %s  |  %s" % (MAKER, EQUIP), 6.8, "LS", white, "r")
    if title:
        c.setFillColor(ORANGE)
        c.roundRect(M, H - 58, 42, 15, 3, fill=1, stroke=0)
        ptext(c, M + 21, H - 53, "Page %d" % n, 7.5, "LSB", white, "c")
        ptext(c, M + 50, H - 55, title, 12.5, "LSB", DARK)
        c.setStrokeColor(GREY_M)
        c.setLineWidth(0.6)
        c.line(M, H - 66, W - M, H - 66)


def footer(c, n, total=24):
    c.setStrokeColor(GREY_M)
    c.setLineWidth(0.5)
    c.line(M, 36, W - M, 36)
    ptext(c, M, 27, "%s  |  Version %s" % (MODEL, VERSION), 6.5, "LS", GREY_D)
    ptext(c, W - M, 27, "Page %d / %d" % (n, total), 7, "LSB", DARK, "r")
    ptext(c, W / 2, 16, "Document synthétique d'un véhicule fictif : illustrations schématiques ; valeurs propres à ce modèle, à ne pas appliquer à un véhicule réel.",
          5.8, "LSI", GREY, "c")


TOP = H - 76  # premier y utilisable sous le titre


def section(c, x, y, title, w=None):
    c.setFillColor(ORANGE)
    y -= 10
    c.rect(x, y - 2, 3, 11, fill=1, stroke=0)
    ptext(c, x + 8, y, title, 8.6, "LSB", DARK)
    c.setStrokeColor(GREY_M)
    c.setLineWidth(0.5)
    c.line(x, y - 5, x + (w or CW), y - 5)
    return 26


# ------------------------------------------------------------------ boîtes
def tri_icon(c, x, y, s, col):
    c.setFillColor(col)
    p = c.beginPath()
    p.moveTo(x, y)
    p.lineTo(x + s, y)
    p.lineTo(x + s / 2, y + s * 0.88)
    p.close()
    c.drawPath(p, fill=1, stroke=0)
    ptext(c, x + s / 2, y + s * 0.16, "!", s * 0.6, "LSB", white, "c")


def info_icon(c, x, y, s, col=GREY_D):
    c.setStrokeColor(col)
    c.setLineWidth(1)
    c.circle(x + s / 2, y + s / 2, s / 2, fill=0, stroke=1)
    ptext(c, x + s / 2, y + s * 0.2, "i", s * 0.62, "LSB", col, "c")


def key_icon(c, x, y, s, col=DARK):
    c.setStrokeColor(col)
    c.setFillColor(col)
    c.setLineWidth(1.3)
    c.circle(x + s * 0.3, y + s * 0.5, s * 0.22, fill=0, stroke=1)
    c.line(x + s * 0.52, y + s * 0.5, x + s, y + s * 0.5)
    c.line(x + s * 0.85, y + s * 0.5, x + s * 0.85, y + s * 0.3)
    c.line(x + s * 0.72, y + s * 0.5, x + s * 0.72, y + s * 0.34)


def callout(c, kind, x, ytop, w, title, text):
    cfg = {
        "danger": (RED_L, RED, "tri"),
        "attention": (ORANGE_L, ORANGE, "tri"),
        "info": (GREY_L, GREY_D, "info"),
        "arret": (GREY_L, DARK, "key"),
    }[kind]
    bg, col, ic = cfg
    tw = w - 44
    hp = 0
    pt = P("<b>%s</b>" % title, "ct") if title else None
    pb = P(text, "ps")
    if pt:
        _, h1 = pt.wrap(tw, 1000)
        hp += h1 + 2
    _, h2 = pb.wrap(tw, 1000)
    hp += h2
    h = max(hp + 14, 30)
    c.setFillColor(bg)
    c.rect(x, ytop - h, w, h, fill=1, stroke=0)
    c.setFillColor(col)
    c.rect(x, ytop - h, 3, h, fill=1, stroke=0)
    iy = ytop - h / 2 - 7
    if ic == "tri":
        tri_icon(c, x + 12, iy, 15, col)
    elif ic == "info":
        info_icon(c, x + 12, iy, 14, col)
    else:
        key_icon(c, x + 10, iy + 1, 17, col)
    yy = ytop - 7
    if pt:
        pt.wrap(tw, 1000)
        if kind in ("danger", "attention"):
            pt = P('<font color="%s"><b>%s</b></font>' % (col.hexval().replace("0x", "#"), title), "ct")
            pt.wrap(tw, 1000)
        pt.drawOn(c, x + 36, yy - pt.height)
        yy -= pt.height + 2
    pb.drawOn(c, x + 36, yy - h2)
    return h


def frame(c, x, ytop, w, h, fill=GREY_L):
    c.setFillColor(fill)
    c.setStrokeColor(GREY_M)
    c.setLineWidth(0.6)
    c.roundRect(x, ytop - h, w, h, 3, fill=1, stroke=1)


def caption(c, x, ytop, w, num, text):
    return para(c, "<b>Figure %s</b> : %s" % (num, text), x, ytop, w, "cap")


def marker(c, x, y, n, col=DARK, r=5.2):
    c.setFillColor(col)
    c.circle(x, y, r, fill=1, stroke=0)
    ptext(c, x, y - r * 0.42, str(n), r * 1.25, "LSB", white, "c")


def leader(c, x1, y1, x2, y2, n, col=DARK):
    c.setStrokeColor(col)
    c.setLineWidth(0.6)
    c.line(x1, y1, x2, y2)
    c.setFillColor(col)
    c.circle(x1, y1, 1.3, fill=1, stroke=0)
    marker(c, x2, y2, n, col)


def steps(c, items, x, ytop, w, gap=5, st="p", r=5.2):
    y = ytop
    for i, t in enumerate(items):
        p = P(t, st)
        _, h = p.wrap(w - 18, 1000)
        marker(c, x + r, y - 6, i + 1, DARK, r)
        p.drawOn(c, x + 16, y - h)
        y -= max(h, 12) + gap
    return ytop - y


def flow(c, labels, x, ytop, w, h=30, hl=()):
    n = len(labels)
    gap = 9
    bw = (w - gap * (n - 1)) / n
    for i, lab in enumerate(labels):
        bx = x + i * (bw + gap)
        c.setFillColor(ORANGE_L if i in hl else white)
        c.setStrokeColor(GREY_M)
        c.setLineWidth(0.6)
        c.roundRect(bx, ytop - h, bw, h, 2, fill=1, stroke=1)
        marker(c, bx + 1, ytop, i + 1, DARK, 4.6)
        p = P(lab, "pc")
        p.wrap(bw - 4, 100)
        p.drawOn(c, bx + 2, ytop - h / 2 - p.height / 2 - 1)
        if i < n - 1:
            ax = bx + bw + 1.5
            c.setFillColor(ORANGE)
            pa = c.beginPath()
            pa.moveTo(ax, ytop - h / 2 + 3.5)
            pa.lineTo(ax + 6, ytop - h / 2)
            pa.lineTo(ax, ytop - h / 2 - 3.5)
            pa.close()
            c.drawPath(pa, fill=1, stroke=0)
    return h


def table(c, rows, x, ytop, widths, head=True, zebra=True, fs=None, hcol=DARK):
    data = []
    for i, r in enumerate(rows):
        data.append([P(str(v), "th" if (head and i == 0) else "td") if not hasattr(v, "wrap") else v for v in r])
    t = Table(data, colWidths=widths)
    sty = [
        ("GRID", (0, 0), (-1, -1), 0.4, GREY_M),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, -1), 2.6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 2.6),
        ("LEFTPADDING", (0, 0), (-1, -1), 4),
    ]
    if head:
        sty.append(("BACKGROUND", (0, 0), (-1, 0), hcol))
    if zebra:
        for i in range(1 if head else 0, len(rows)):
            if i % 2 == 0:
                sty.append(("BACKGROUND", (0, i), (-1, i), GREY_L))
    t.setStyle(TableStyle(sty))
    _, h = t.wrap(sum(widths), 2000)
    t.drawOn(c, x, ytop - h)
    return h


# ------------------------------------------------------------------ pictos voyants
def _rays(c, x, y, r, col):
    c.setStrokeColor(col)
    c.setLineWidth(0.9)
    for k in range(8):
        a = k * math.pi / 4 + math.pi / 8
        c.line(x + math.cos(a) * r * 1.25, y + math.sin(a) * r * 1.25, x + math.cos(a) * r * 1.6, y + math.sin(a) * r * 1.6)


def icon(c, name, x, y, s, col):
    """Pictogramme centré en (x,y), taille s (hauteur approx.)."""
    c.saveState()
    c.setStrokeColor(col)
    c.setFillColor(col)
    c.setLineWidth(max(0.7, s * 0.09))
    c.setLineJoin(1)
    h = s / 2
    if name == "moteur":  # bloc moteur stylisé
        p = c.beginPath()
        pts = [(-0.9, -0.5), (-0.9, 0.1), (-0.65, 0.1), (-0.65, 0.35), (-0.3, 0.35), (-0.3, 0.55), (0.25, 0.55), (0.25, 0.35),
               (0.55, 0.35), (0.7, 0.15), (0.9, 0.15), (0.9, -0.25), (0.7, -0.25), (0.55, -0.5)]
        p.moveTo(x + pts[0][0] * h, y + pts[0][1] * h)
        for a, b in pts[1:]:
            p.lineTo(x + a * h, y + b * h)
        p.close()
        c.drawPath(p, fill=0, stroke=1)
        c.line(x - 0.9 * h, y - 0.2 * h, x - 1.05 * h, y - 0.2 * h)
    elif name == "abs":
        c.circle(x, y, h * 0.7, fill=0, stroke=1)
        c.arc(x - h * 1.05, y - h * 0.85, x + h * 1.05, y + h * 0.85, 140, 80)
        c.arc(x - h * 1.05, y - h * 0.85, x + h * 1.05, y + h * 0.85, -40, 80)
        c.setFont("LSB", s * 0.34)
        c.drawCentredString(x, y - s * 0.12, "ABS")
    elif name == "cle":
        c.setLineWidth(max(1, s * 0.13))
        c.line(x - h * 0.6, y - h * 0.6, x + h * 0.35, y + h * 0.35)
        c.circle(x + h * 0.5, y + h * 0.5, h * 0.32, fill=0, stroke=1)
        c.setFillColor(white if False else col)
    elif name == "huile":
        p = c.beginPath()
        p.moveTo(x - h * 0.9, y - h * 0.45)
        p.lineTo(x + h * 0.3, y - h * 0.45)
        p.lineTo(x + h * 0.95, y + h * 0.2)
        p.lineTo(x + h * 0.2, y + h * 0.05)
        p.lineTo(x - h * 0.1, y + h * 0.3)
        p.lineTo(x - h * 0.65, y + h * 0.3)
        p.lineTo(x - h * 0.9, y + h * 0.05)
        p.close()
        c.drawPath(p, fill=0, stroke=1)
        c.circle(x + h * 0.95, y - h * 0.35, h * 0.13, fill=1, stroke=0)
    elif name == "batterie":
        c.rect(x - h * 0.85, y - h * 0.5, h * 1.7, h * 0.95, fill=0, stroke=1)
        c.rect(x - h * 0.6, y + h * 0.45, h * 0.3, h * 0.18, fill=1, stroke=0)
        c.rect(x + h * 0.3, y + h * 0.45, h * 0.3, h * 0.18, fill=1, stroke=0)
        c.setFont("LSB", s * 0.42)
        c.drawCentredString(x - h * 0.45, y - h * 0.3, "-")
        c.drawCentredString(x + h * 0.45, y - h * 0.3, "+")
    elif name == "temp":
        c.line(x, y - h * 0.35, x, y + h * 0.75)
        c.circle(x, y - h * 0.45, h * 0.2, fill=1, stroke=0)
        c.line(x, y + h * 0.5, x + h * 0.3, y + h * 0.5)
        c.line(x, y + h * 0.2, x + h * 0.3, y + h * 0.2)
        for dy in (-0.75,):
            for dx in (-0.8, 0.8):
                pass
        c.setLineWidth(max(0.6, s * 0.07))
        c.bezier(x - h * 0.95, y - h * 0.8, x - h * 0.6, y - h * 0.6, x - h * 0.4, y - h * 1.0, x - h * 0.1, y - h * 0.8)
        c.bezier(x + h * 0.1, y - h * 0.8, x + h * 0.4, y - h * 0.6, x + h * 0.6, y - h * 1.0, x + h * 0.95, y - h * 0.8)
    elif name == "route":
        c.arc(x - h * 0.5, y - h * 0.6, x + h * 0.7, y + h * 0.6, -90, 180)
        c.line(x + h * 0.1, y - h * 0.6, x + h * 0.1, y + h * 0.6)
        for k in (-0.45, -0.15, 0.15, 0.45):
            c.line(x - h * 0.15, y + k * h, x - h * 0.9, y + k * h)
    elif name in ("cli_g", "cli_d"):
        sg = -1 if name == "cli_g" else 1
        p = c.beginPath()
        p.moveTo(x + sg * h * 0.9, y)
        p.lineTo(x + sg * h * 0.05, y + h * 0.6)
        p.lineTo(x + sg * h * 0.05, y - h * 0.6)
        p.close()
        c.drawPath(p, fill=1, stroke=0)
        c.rect(x - (h * 0.75 if sg > 0 else -h * 0.05), y - h * 0.22, h * 0.7, h * 0.44, fill=1, stroke=0)
    elif name == "carburant":
        c.rect(x - h * 0.7, y - h * 0.8, h * 0.9, h * 1.5, fill=0, stroke=1)
        c.rect(x - h * 0.55, y + h * 0.1, h * 0.6, h * 0.4, fill=1, stroke=0)
        c.line(x + h * 0.2, y + h * 0.3, x + h * 0.7, y + h * 0.1)
        c.line(x + h * 0.7, y + h * 0.1, x + h * 0.7, y - h * 0.6)
    c.restoreState()


def voyant(c, name, x, y, s, col, state="on"):
    """Voyant: state off/on/blink."""
    if state == "off":
        icon(c, name, x, y, s, OFF)
    else:
        icon(c, name, x, y, s, col)
        if state == "blink":
            _rays(c, x, y, s * 0.62, col)


VOY_COL = {"moteur": ORANGE, "abs": ORANGE, "cle": ORANGE, "huile": RED, "batterie": RED, "temp": RED}


# ------------------------------------------------------------------ tableau de bord
def cluster(c, x, y, w, states=None, lcd="12 458 km", letters=False, numbers=False, speed=True):
    """Tableau de bord, coin bas-gauche (x,y), largeur w (hauteur = 0.42 w).
    Colonne gauche : voyants ORANGE (moteur, ABS, entretien) ; colonne droite : ROUGES (huile, batterie, température)."""
    states = states or {}
    s = w / 260.0
    hgt = 110 * s
    c.saveState()
    c.setFillColor(DARK)
    c.setStrokeColor(HexColor("#111317"))
    c.setLineWidth(1)
    c.roundRect(x, y, w, hgt, 14 * s, fill=1, stroke=1)
    cx = x + w / 2
    # compteur
    c.setStrokeColor(HexColor("#9aa0a8"))
    c.setLineWidth(3 * s)
    c.arc(cx - 52 * s, y + 18 * s, cx + 52 * s, y + 122 * s, 15, 150)
    c.setLineWidth(0.8 * s)
    for k in range(0, 13):
        a = math.radians(15 + k * 12.5)
        r1, r2 = 47 * s, 52 * s
        c.line(cx + math.cos(a) * r1, y + 70 * s + math.sin(a) * r1, cx + math.cos(a) * r2, y + 70 * s + math.sin(a) * r2)
    if speed:
        c.setStrokeColor(ORANGE)
        c.setLineWidth(1.6 * s)
        a = math.radians(150)
        c.line(cx, y + 70 * s, cx + math.cos(a) * 42 * s, y + 70 * s + math.sin(a) * 42 * s)
        c.setFillColor(ORANGE)
        c.circle(cx, y + 70 * s, 3 * s, fill=1, stroke=0)
    ptext(c, cx, y + 82 * s, "km/h", 6 * s, "LS", HexColor("#c8ccd2"), "c")
    # écran LCD
    c.setFillColor(HexColor("#b9c7b0"))
    c.roundRect(cx - 40 * s, y + 14 * s, 80 * s, 34 * s, 3 * s, fill=1, stroke=0)
    ptext(c, cx, y + 31 * s, lcd, 9.5 * s if len(lcd) < 7 else 8 * s, "LSB", DARK, "c")
    # jauge carburant 6 segments
    for k in range(6):
        c.setFillColor(DARK)
        c.rect(cx - 30 * s + k * 10 * s, y + 18 * s, 8 * s, 6 * s, fill=1, stroke=0)
    ptext(c, cx - 36 * s, y + 18.5 * s, "E", 5 * s, "LSB", DARK, "c")
    ptext(c, cx + 36 * s, y + 18.5 * s, "F", 5 * s, "LSB", DARK, "c")
    # clignotants et feu de route (haut)
    voyant(c, "cli_g", x + 22 * s, y + 92 * s, 13 * s, GREEN, states.get("cli_g", "off"))
    voyant(c, "cli_d", x + w - 22 * s, y + 92 * s, 13 * s, GREEN, states.get("cli_d", "off"))
    voyant(c, "route", cx, y + 100 * s, 12 * s, BLUE, states.get("route", "off"))
    # colonnes de voyants
    lx, rx = x + 34 * s, x + w - 34 * s
    rows = [70 * s, 46 * s, 22 * s]
    for nm, yy in zip(("moteur", "abs", "cle"), rows):
        voyant(c, nm, lx, y + yy, 15 * s, ORANGE, states.get(nm, "off"))
    for nm, yy in zip(("huile", "batterie", "temp"), rows):
        voyant(c, nm, rx, y + yy, 15 * s, RED, states.get(nm, "off"))
    # boutons SEL / SET sous l'écran
    c.setFillColor(HexColor("#3a3f47"))
    c.roundRect(x + w * 0.5 - 70 * s, y + 3 * s, 22 * s, 8 * s, 3 * s, fill=1, stroke=0)
    c.roundRect(x + w * 0.5 + 48 * s, y + 3 * s, 22 * s, 8 * s, 3 * s, fill=1, stroke=0)
    ptext(c, x + w * 0.5 - 59 * s, y + 5 * s, "SEL", 4.8 * s, "LSB", white, "c")
    ptext(c, x + w * 0.5 + 59 * s, y + 5 * s, "SET", 4.8 * s, "LSB", white, "c")
    c.restoreState()
    pos = {
        "moteur": (lx, y + rows[0]), "abs": (lx, y + rows[1]), "cle": (lx, y + rows[2]),
        "huile": (rx, y + rows[0]), "batterie": (rx, y + rows[1]), "temp": (rx, y + rows[2]),
        "lcd": (cx, y + 31 * s), "compteur": (cx, y + 70 * s), "route": (cx, y + 100 * s),
        "cli_g": (x + 22 * s, y + 92 * s), "cli_d": (x + w - 22 * s, y + 92 * s),
        "sel": (x + w * 0.5 - 59 * s, y + 7 * s), "set": (x + w * 0.5 + 59 * s, y + 7 * s), "jauge": (cx, y + 21 * s),
        "h": hgt,
    }
    return pos


# ------------------------------------------------------------------ scooter vue de profil (côté gauche, avant à gauche)
def wheel(c, x, y, r, s):
    c.setFillColor(HexColor("#2b2e33"))
    c.circle(x, y, r, fill=1, stroke=0)
    c.setFillColor(HexColor("#b8bdc4"))
    c.circle(x, y, r * 0.66, fill=1, stroke=0)
    c.setFillColor(HexColor("#7d838c"))
    c.circle(x, y, r * 0.5, fill=1, stroke=0)
    c.setStrokeColor(HexColor("#b8bdc4"))
    c.setLineWidth(2.2 * s)
    for k in range(5):
        a = k * 2 * math.pi / 5 + 0.3
        c.line(x + math.cos(a) * r * 0.12, y + math.sin(a) * r * 0.12, x + math.cos(a) * r * 0.5, y + math.sin(a) * r * 0.5)
    c.setFillColor(HexColor("#d9dce0"))
    c.circle(x, y, r * 0.12, fill=1, stroke=0)


def poly(c, pts, ox, oy, s, fill, stroke=None, lw=0.8):
    p = c.beginPath()
    p.moveTo(ox + pts[0][0] * s, oy + pts[0][1] * s)
    for a, b in pts[1:]:
        p.lineTo(ox + a * s, oy + b * s)
    p.close()
    c.setFillColor(fill)
    if stroke is not None:
        c.setStrokeColor(stroke)
        c.setLineWidth(lw)
    c.drawPath(p, fill=1, stroke=1 if stroke is not None else 0)


def scooter(c, ox, oy, w, seat_open=False, stand="centrale", hl=None, cvt_open=False, show_airbox=False):
    """Scooter vu du côté gauche. Repère local 300 x 175. Renvoie les positions (coord. page) des organes."""
    s = w / 300.0
    hl = hl or []
    T = lambda a, b: (ox + a * s, oy + b * s)
    # ombre
    c.setFillColor(HexColor("#dfe2e6"))
    c.ellipse(ox + 20 * s, oy - 3 * s, ox + 285 * s, oy + 5 * s, fill=1, stroke=0)
    # béquilles
    c.setStrokeColor(HexColor("#3c4048"))
    c.setLineWidth(2.2 * s)
    if stand == "centrale":
        c.line(*T(170, 40), *T(160, 3))
        c.line(*T(160, 3), *T(178, 3))
    else:
        c.line(*T(158, 40), *T(140, 6))
    # roue arrière + bras moteur
    wheel(c, *T(232, 34), 31 * s, s)
    # bloc moteur / carter CVT (côté gauche)
    poly(c, [(150, 30), (160, 56), (200, 60), (238, 46), (240, 30), (215, 24), (170, 24)], ox, oy, s,
         HexColor("#9aa1ab") if not cvt_open else HexColor("#c9ced5"), HexColor("#5c626b"), 0.8 * s)
    if cvt_open:
        c.setStrokeColor(DARK)
        c.setLineWidth(1.2 * s)
        c.circle(*T(174, 40), 11 * s, fill=0, stroke=1)
        c.circle(*T(226, 38), 8 * s, fill=0, stroke=1)
        c.setLineWidth(3 * s)
        c.line(*T(174, 51), *T(226, 46))
        c.line(*T(174, 29), *T(226, 30))
    else:
        c.setStrokeColor(HexColor("#6f757e"))
        c.setLineWidth(0.6 * s)
        for k in range(4):
            c.line(*T(180 + k * 12, 34), *T(186 + k * 12, 50))
    # boîte à air au-dessus du carter
    poly(c, [(178, 58), (182, 76), (226, 74), (230, 58)], ox, oy, s,
         ORANGE_L if show_airbox else HexColor("#7f868f"), ORANGE if show_airbox else HexColor("#5c626b"), (1.2 if show_airbox else 0.6) * s)
    # roue avant + fourche
    wheel(c, *T(58, 34), 31 * s, s)
    c.setStrokeColor(HexColor("#8b929b"))
    c.setLineWidth(4 * s)
    c.line(*T(58, 34), *T(80, 118))
    # garde-boue avant
    c.setStrokeColor(BODY)
    c.setLineWidth(5 * s)
    c.arc(ox + 22 * s, oy + 0 * s, ox + 94 * s, oy + 72 * s, 50, 95)
    # carrosserie : tablier + plancher + coque arrière
    body = [(70, 52), (86, 150), (104, 152), (116, 122), (120, 62), (162, 58), (166, 92), (278, 104), (292, 92), (284, 74),
            (250, 70), (234, 66), (200, 60), (160, 56), (108, 48)]
    poly(c, body, ox, oy, s, BODY, HexColor("#8f959e"), 0.9 * s)
    # plancher
    c.setFillColor(HexColor("#4b5058"))
    c.rect(*T(118, 56), 44 * s, 5 * s, fill=1, stroke=0)
    # liseré
    c.setStrokeColor(HexColor("#b5bac2"))
    c.setLineWidth(0.8 * s)
    c.line(*T(170, 82), *T(282, 92))
    # selle
    if seat_open:
        poly(c, [(166, 98), (176, 160), (188, 162), (182, 100)], ox, oy, s, HexColor("#30343a"), None)
        c.setFillColor(HexColor("#5a6069"))
        c.rect(*T(178, 92), 80 * s, 8 * s, fill=1, stroke=0)  # coffre ouvert
        c.setFillColor(HexColor("#2b2e33"))
        c.rect(*T(182, 95), 72 * s, 4 * s, fill=1, stroke=0)
    else:
        poly(c, [(166, 96), (172, 108), (215, 110), (228, 106), (272, 110), (280, 104), (270, 98), (225, 98), (170, 92)], ox, oy, s,
             HexColor("#30343a"), None)
    # feu arrière
    c.setFillColor(RED)
    c.roundRect(*T(284, 90), 9 * s, 6 * s, 2 * s, fill=1, stroke=0)
    # guidon / tête de fourche
    poly(c, [(80, 140), (84, 160), (122, 160), (124, 146), (104, 140)], ox, oy, s, HexColor("#3a3f47"), None)
    c.setStrokeColor(HexColor("#3a3f47"))
    c.setLineWidth(3 * s)
    c.line(*T(104, 160), *T(132, 164))  # poignée
    c.setLineWidth(1.4 * s)
    c.line(*T(112, 162), *T(128, 172))  # levier
    c.line(*T(96, 160), *T(90, 178))  # rétro
    c.setFillColor(HexColor("#3a3f47"))
    c.ellipse(*T(82, 176), *T(100, 184), fill=1, stroke=0)
    # tableau de bord (petit)
    c.setFillColor(HexColor("#1e2126"))
    c.roundRect(*T(90, 156), 22 * s, 6 * s, 2 * s, fill=1, stroke=0)
    # phare
    c.setFillColor(HexColor("#fff7d6"))
    c.setStrokeColor(HexColor("#8f959e"))
    c.setLineWidth(0.6 * s)
    poly(c, [(80, 128), (84, 142), (92, 140), (90, 126)], ox, oy, s, HexColor("#fff7d6"), HexColor("#8f959e"), 0.6 * s)
    # pot d'échappement (dépasse derrière la roue côté droit)
    c.setFillColor(HexColor("#6f757e"))
    c.roundRect(*T(238, 40), 50 * s, 12 * s, 5 * s, fill=1, stroke=0)
    # bouchon de vidange (sous le carter)
    c.setFillColor(HexColor("#2b2e33"))
    c.rect(*T(166, 20), 6 * s, 4 * s, fill=1, stroke=0)
    pos = {
        "phare": T(86, 134), "tableau": T(101, 159), "levier_av": T(126, 170), "levier_ar": T(120, 168),
        "selle": T(220, 106), "reservoir": T(200, 96), "cvt": T(205, 40), "bequille_c": T(168, 8),
        "bequille_l": T(150, 22), "feu_ar": T(288, 93), "roue_av": T(58, 34), "roue_ar": T(232, 34),
        "plancher": T(140, 59), "airbox": T(204, 67), "vidange": T(169, 21), "echappement": T(270, 46),
        "frein_av": T(58, 34), "batterie": T(140, 62), "bougie": T(170, 60), "jauge": T(186, 54),
    }
    return pos


# ------------------------------------------------------------------ petits dessins génériques
def tile(c, x, ytop, w, h, title, text, drawfn=None, title_col=DARK, bar=None):
    c.setFillColor(white)
    c.setStrokeColor(GREY_M)
    c.setLineWidth(0.6)
    c.rect(x, ytop - h, w, h, fill=1, stroke=1)
    if bar:
        c.setFillColor(bar)
        c.rect(x, ytop - h, 3, h, fill=1, stroke=0)
    tx = x + 8
    if drawfn:
        drawfn(c, x + 20, ytop - h / 2)
        tx = x + 42
    ptext(c, tx, ytop - 13, title, 7.6, "LSB", title_col)
    para(c, text, tx, ytop - 17, w - (tx - x) - 6, "ps")


def pic_circle(c, x, y, r, col=DARK, cross=False):
    c.setStrokeColor(RED if cross else col)
    c.setLineWidth(1.3)
    c.circle(x, y, r, fill=0, stroke=1)
    if cross:
        c.line(x - r * 0.7, y + r * 0.7, x + r * 0.7, y - r * 0.7)


def check(c, x, y, r=5, ok=True):
    c.setStrokeColor(DARK if ok else RED)
    c.setLineWidth(1)
    c.circle(x, y, r, fill=0, stroke=1)
    c.setLineWidth(1.3)
    if ok:
        c.line(x - r * 0.5, y, x - r * 0.1, y - r * 0.45)
        c.line(x - r * 0.1, y - r * 0.45, x + r * 0.55, y + r * 0.45)
    else:
        c.line(x - r * 0.45, y - r * 0.45, x + r * 0.45, y + r * 0.45)
        c.line(x - r * 0.45, y + r * 0.45, x + r * 0.45, y - r * 0.45)


def arrow(c, x1, y1, x2, y2, col=ORANGE, lw=1.4, hs=5):
    c.setStrokeColor(col)
    c.setFillColor(col)
    c.setLineWidth(lw)
    a = math.atan2(y2 - y1, x2 - x1)
    c.line(x1, y1, x2 - math.cos(a) * hs * 0.8, y2 - math.sin(a) * hs * 0.8)
    p = c.beginPath()
    p.moveTo(x2, y2)
    p.lineTo(x2 - math.cos(a - 0.45) * hs, y2 - math.sin(a - 0.45) * hs)
    p.lineTo(x2 - math.cos(a + 0.45) * hs, y2 - math.sin(a + 0.45) * hs)
    p.close()
    c.drawPath(p, fill=1, stroke=0)


def torque_badge(c, x, y, txt):
    c.setFillColor(ORANGE)
    c.roundRect(x, y, 34, 14, 3, fill=1, stroke=0)
    ptext(c, x + 17, y + 4, txt, 7.5, "LSB", white, "c")


def wrench(c, x, y, L, ang=20, col=GREY_D):
    c.saveState()
    c.translate(x, y)
    c.rotate(ang)
    c.setFillColor(col)
    c.roundRect(0, -2.5, L, 5, 2.5, fill=1, stroke=0)
    c.circle(0, 0, 6, fill=1, stroke=0)
    c.setFillColor(white)
    c.rect(-3, -2.2, 4.5, 4.4, fill=1, stroke=0)
    c.restoreState()


def drop(c, x, y, s, col=HexColor("#b07a10")):
    c.setFillColor(col)
    p = c.beginPath()
    p.moveTo(x, y + s)
    p.curveTo(x + s * 0.7, y + s * 0.2, x + s * 0.5, y - s * 0.5, x, y - s * 0.5)
    p.curveTo(x - s * 0.5, y - s * 0.5, x - s * 0.7, y + s * 0.2, x, y + s)
    c.drawPath(p, fill=1, stroke=0)


def dashed_box(c, x, y, w, h, col=ORANGE):
    c.saveState()
    c.setStrokeColor(col)
    c.setLineWidth(1.2)
    c.setDash(3, 2)
    c.roundRect(x, y, w, h, 3, fill=0, stroke=1)
    c.restoreState()
