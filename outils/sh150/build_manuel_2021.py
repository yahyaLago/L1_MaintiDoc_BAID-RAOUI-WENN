# -*- coding: utf-8 -*-
"""manuel_sh150i_2021 : Honda SH150i (SH150AD, génération 2020-2024) - manuel de synthèse illustré MaintiDoc.
Valeurs relevées dans le manuel du propriétaire Honda SH125/SH150 21YM (réf. 32K0RA000), page citée pour chacune.
Aucun texte ni figure Honda reproduit : rédaction et schémas originaux de l'équipe."""
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from reportlab.pdfgen import canvas  # noqa: E402
from dessin import *  # noqa: E402,F401,F403
from dessin import _rays  # noqa: E402,F401

OUT = sys.argv[1] if len(sys.argv) > 1 else "manuel_sh150i_2021.pdf"
DOC = "manuel_sh150i_2021"
TITLE_MODEL = "Honda SH150i (SH150AD) 2020-2024"
VERS = "1.0 (2026-11)"
EQ = "SH150-21-01"
TOTAL = 21
COLM = HexColor("#c8102e")
MP = "MP"  # manuel du propriétaire


def ref(p):
    """Référence au manuel du propriétaire : page imprimée (page du PDF = imprimée + 4)."""
    return "MP p. %d" % p


def header(c, n, title):
    c.setFillColor(DARK)
    c.rect(0, H - 24, W, 24, fill=1, stroke=0)
    c.setFillColor(ORANGE)
    c.rect(0, H - 26, W, 2, fill=1, stroke=0)
    ptext(c, M, H - 16, "MaintiDoc  |  %s" % DOC, 8.5, "LSB", white)
    ptext(c, W - M, H - 16, "%s  |  %s  |  synthèse non officielle" % (TITLE_MODEL, EQ), 6.8, "LS", white, "r")
    if title:
        c.setFillColor(ORANGE)
        c.roundRect(M, H - 58, 42, 15, 3, fill=1, stroke=0)
        ptext(c, M + 21, H - 53, "Page %d" % n, 7.5, "LSB", white, "c")
        ptext(c, M + 50, H - 55, title, 12.5, "LSB", DARK)
        c.setStrokeColor(GREY_M)
        c.setLineWidth(0.6)
        c.line(M, H - 66, W - M, H - 66)


def footer(c, n):
    c.setStrokeColor(GREY_M)
    c.setLineWidth(0.5)
    c.line(M, 36, W - M, 36)
    ptext(c, M, 27, "%s  |  version %s  |  MP p. N = manuel du propriétaire Honda 21YM, page imprimée N" % (DOC, VERS), 6.4, "LS", GREY_D)
    ptext(c, W - M, 27, "Page %d / %d" % (n, TOTAL), 7, "LSB", DARK, "r")
    ptext(c, W / 2, 16, "Synthèse rédigée par l'équipe MaintiDoc avec assistance IA à partir du manuel du propriétaire Honda (réf. 32K0RA000). "
          "Non affiliée à Honda ; le manuel Honda fait foi.", 5.8, "LSI", GREY, "c")


def page(c, n, title, fn):
    header(c, n, title)
    fn(c)
    footer(c, n)
    c.showPage()


# ------------------------------------------------------------------ pictogrammes propres à ce modèle
def pic(c, name, x, y, s, col):
    c.saveState()
    c.setStrokeColor(col)
    c.setFillColor(col)
    c.setLineWidth(max(0.8, s * 0.09))
    h = s / 2
    if name == "smartkey":
        c.circle(x - h * 0.45, y, h * 0.38, fill=0, stroke=1)
        c.line(x - h * 0.07, y, x + h * 0.9, y)
        c.line(x + h * 0.6, y, x + h * 0.6, y - h * 0.35)
        c.line(x + h * 0.85, y, x + h * 0.85, y - h * 0.3)
    elif name == "idling":
        c.circle(x, y, h * 0.8, fill=0, stroke=1)
        c.setFont("LSB", s * 0.62)
        c.drawCentredString(x, y - s * 0.22, "A")
        c.setFillColor(col)
        p = c.beginPath()
        p.moveTo(x + h * 0.85, y + h * 0.15)
        p.lineTo(x + h * 1.1, y - h * 0.15)
        p.lineTo(x + h * 0.6, y - h * 0.15)
        p.close()
        c.drawPath(p, fill=1, stroke=0)
    elif name == "tc":
        c.roundRect(x - h * 0.9, y - h * 0.6, h * 1.8, h * 1.2, h * 0.3, fill=0, stroke=1)
        c.setFont("LSB", s * 0.48)
        c.drawCentredString(x, y - s * 0.16, "TC")
    elif name == "tcoff":
        c.roundRect(x - h * 0.9, y - h * 0.6, h * 1.8, h * 1.2, h * 0.3, fill=0, stroke=1)
        c.setFont("LSB", s * 0.3)
        c.drawCentredString(x, y + s * 0.0, "TC")
        c.drawCentredString(x, y - s * 0.24, "OFF")
    elif name == "oil":
        c.setFont("LSB", s * 0.32)
        c.drawCentredString(x, y + s * 0.05, "OIL")
        c.drawCentredString(x, y - s * 0.28, "CHG")
    else:
        c.restoreState()
        icon(c, name, x, y, s, col)
        return
    c.restoreState()


INDIC = [  # (clé, libellé, couleur, page MP)
    ("moteur", "Voyant d'injection PGM-FI (MIL)", ORANGE, 40),
    ("abs", "Témoin ABS", ORANGE, 41),
    ("tc", "Témoin de contrôle de couple (HSTC)", ORANGE, 41),
    ("tcoff", "Témoin HSTC désactivé", ORANGE, 41),
    ("temp", "Témoin de température élevée du liquide", RED, 40),
    ("smartkey", "Témoin Honda SMART Key", GREEN, 40),
    ("idling", "Témoin Idling Stop", GREEN, 40),
    ("route", "Témoin de feu de route", BLUE, 41),
    ("cli_g", "Témoins de clignotants", GREEN, 41),
]


def panel(c, x, y, w, states=None, lcd="12 458 km"):
    """Instrumentation schématique originale (ne reproduit pas la disposition Honda)."""
    states = states or {}
    s = w / 300.0
    h = 120 * s
    c.setFillColor(DARK)
    c.roundRect(x, y, w, h, 16 * s, fill=1, stroke=0)
    c.setFillColor(HexColor("#b9c7b0"))
    c.roundRect(x + 80 * s, y + 38 * s, 140 * s, 60 * s, 5 * s, fill=1, stroke=0)
    ptext(c, x + 150 * s, y + 72 * s, "88", 26 * s, "LSB", DARK, "c")
    ptext(c, x + 196 * s, y + 72 * s, "km/h", 7 * s, "LS", DARK, "c")
    ptext(c, x + 150 * s, y + 46 * s, lcd, 8.5 * s, "LSB", DARK, "c")
    pos = {}
    slots = [("cli_g", 22, 100), ("route", 150, 108), ("cli_d", 278, 100),
             ("moteur", 30, 70), ("abs", 30, 44), ("tc", 30, 18),
             ("temp", 270, 70), ("smartkey", 270, 44), ("idling", 270, 18), ("tcoff", 150, 18)]
    colmap = {k: col for k, _, col, _ in INDIC}
    colmap["cli_d"] = GREEN
    for k, sx, sy in slots:
        st = states.get(k, "off")
        col = colmap[k] if st != "off" else OFF
        px, py = x + sx * s, y + sy * s
        if k == "cli_d":
            icon(c, "cli_d", px, py, 13 * s, col)
        else:
            pic(c, k, px, py, 15 * s, col)
        if st == "blink":
            _rays(c, px, py, 9 * s, colmap[k])
        pos[k] = (px, py)
    pos["lcd"] = (x + 150 * s, y + 60 * s)
    return pos


# =================================================================== pages
TOC = [(1, "Couverture"), (2, "Sommaire et mode de lecture"), (3, "Consignes de sécurité"),
       (4, "Identifier la génération 2020-2024"), (5, "Caractéristiques techniques"), (6, "Vue d'ensemble et équipements"),
       (7, "Figure 7.1 : instrumentation et témoins"), (8, "Témoins : fonctionnement normal et anomalies"),
       (9, "Honda SMART Key"), (10, "Système Idling Stop"), (11, "Contrôle de couple HSTC"),
       (12, "Démarrage du moteur"), (13, "Programme d'entretien"), (14, "Huile moteur : contrôle et vidange"),
       (15, "Liquide de refroidissement et surchauffe"), (16, "Pneumatiques, bougie et ralenti"),
       (17, "Freins et ABS"), (18, "Batterie, fusibles et éclairage"), (19, "Tableau de dépannage rapide"),
       (20, "Négatifs difficiles et limites du document"), (21, "Sources et traçabilité")]


def p1(c):
    c.setFillColor(DARK)
    c.rect(0, H - 262, W, 236, fill=1, stroke=0)
    c.setFillColor(ORANGE)
    c.roundRect(M, H - 58, 42, 15, 3, fill=1, stroke=0)
    ptext(c, M + 21, H - 53, "Page 1", 7.5, "LSB", white, "c")
    ptext(c, M, H - 92, "MAINTIDOC  |  CORPUS DEUX-ROUES", 9, "LSB", ORANGE)
    ptext(c, M, H - 132, "Honda SH150i", 32, "LSB", white)
    ptext(c, M, H - 154, "SH150AD, génération 2020-2024 (millésime 21YM)", 14, "LS", white)
    ptext(c, M, H - 174, "Manuel de synthèse illustré pour l'atelier : témoins, entretien, valeurs et dépannage", 8.6, "LS", HexColor("#c8ccd2"))
    ptext(c, M, H - 204, "Document %s   |   Équipement %s   |   Version %s" % (DOC, EQ, VERS), 8.5, "LSB", ORANGE)
    ptext(c, M, H - 222, "Valeurs issues du manuel du propriétaire Honda 21YM (réf. 32K0RA000), page citée. Document non officiel.", 7.4, "LSI", HexColor("#c8ccd2"))
    frame(c, M, H - 274, CW, 236, white)
    ptext(c, M + 8, H - 286, "Silhouette schématique (dessin de l'équipe, ne reproduit pas le design Honda)", 6.5, "LSI", GREY)
    scooter(c, M + 90, H - 490, 350)
    y = H - 524
    rows = [["Élément", "Valeur", "Source"], ["Modèle couvert", "SH150AD (et SH125AD dans le même manuel), types II ED et III ED", ref(152)],
            ["Moteur", "157 cm³, alésage x course 60,0 x 55,5 mm, rapport 12,0:1", ref(152)],
            ["Transmission", "V-Matic (2,68:1 à 0,82:1), réduction finale 10,552", ref(152)],
            ["Équipements", "Honda SMART Key, Idling Stop, HSTC, ABS, éclairage LED", "%s, %s, %s" % (ref(40), ref(41), ref(154))],
            ["Identifiant MaintiDoc", EQ + "  |  groupes : techniciens_moto, responsables", "-"]]
    y -= table(c, rows, M, y, [110, CW - 190, 80]) + 10
    tw = (CW - 20) / 3
    for i, (t, ic) in enumerate([("Témoins", "moteur"), ("Entretien", "cle"), ("Dépannage", "temp")]):
        x = M + i * (tw + 10)
        c.setFillColor(white)
        c.setStrokeColor(GREY_M)
        c.rect(x, y - 34, tw, 34, fill=1, stroke=1)
        icon(c, ic, x + 22, y - 17, 18, DARK)
        ptext(c, x + 42, y - 20, t, 8.6, "LSB", DARK)


def p2(c):
    y = TOP
    for n, t in TOC:
        c.setFillColor(DARK)
        c.rect(M, y - 9, 3, 11, fill=1, stroke=0)
        ptext(c, M + 10, y - 6, "Page %d" % n, 7, "LS", DARK)
        ptext(c, M + 50, y - 6, t, 7.6, "LS", DARK)
        c.setStrokeColor(GREY_M)
        c.setDash(1, 2)
        c.line(M + 54 + c.stringWidth(t, "LS", 7.6), y - 6, W - M - 14, y - 6)
        c.setDash()
        ptext(c, W - M, y - 6, str(n), 7.6, "LSB", DARK, "r")
        y -= 15.6
    y -= 4
    y -= section(c, M, y, "Mode de lecture") + 4
    hw = (CW - 10) / 2
    h1 = callout(c, "danger", M, y, hw, "DANGER", "Risque de blessure, de chute ou d'incendie : arrêt nécessaire.")
    callout(c, "attention", M + hw + 10, y, hw, "ATTENTION", "Précaution à respecter, ou valeur propre à cette génération.")
    y -= h1 + 8
    h2 = callout(c, "info", M, y, hw, "INFORMATION", "Complément ou renvoi vers un autre document du corpus.")
    callout(c, "arret", M + hw + 10, y, hw, "MOTEUR ARRÊTÉ", "Contact sur Off, moteur froid, béquille centrale.")
    y -= h2 + 10
    para(c, "<b>Références.</b> « MP p. 153 » renvoie à la page imprimée 153 du manuel du propriétaire Honda SH125/SH150 21YM "
            "(réf. 32K0RA000) ; la page du fichier PDF est la page imprimée + 4. Les schémas sont des dessins originaux de l'équipe : "
            "ils montrent un principe, pas la forme exacte des pièces Honda.", M, y, CW, "ps")


def p3(c):
    y = TOP
    y -= callout(c, "danger", M, y, CW, "AVANT TOUTE INTERVENTION", "Contact sur <b>Off</b>, moteur et échappement froids, scooter sur sa "
                 "<b>béquille centrale</b> sur sol ferme et plat (" + ref(98) + "). Les gaz d'échappement contiennent du monoxyde de carbone : "
                 "ne faites tourner le moteur que dans un lieu ventilé.") + 12
    items = [("Idling Stop", "Ne vous éloignez pas du scooter quand le témoin Idling Stop clignote : le moteur peut redémarrer si la poignée est ouverte. "
              "Coupez toujours le contact (" + ref(56) + ")."),
             ("Béquille latérale", "Béquille latérale dépliée : le moteur ne démarre pas, et il se coupe si on la déplie moteur tournant (" + ref(59) + ")."),
             ("Surchauffe", "Témoin de température allumé : arrêtez le moteur, laissez refroidir contact coupé avant tout contrôle (" + ref(116) + ")."),
             ("Voyant PGM-FI clignotant", "Ratés détectés : garez-vous loin de toute matière inflammable, moteur arrêté au moins 10 minutes (" + ref(117) + ")."),
             ("Vidange", "La vidange et le nettoyage de la crépine demandent des outils spéciaux : Honda recommande le concessionnaire (" + ref(99) + ")."),
             ("Liquides", "Liquide de frein et huile de transmission finale : leur remplacement demande des compétences mécaniques (" + ref(78) + ")."),
             ("Smart Key", "Gardez la Smart Key sur vous en roulant ; pendant une intervention, éloignez-la du scooter."),
             ("Scooter renversé", "Après une chute, coupez le contact puis inspectez le scooter avant de redémarrer (" + ref(59) + ").")]
    tw = (CW - 10) / 2
    th = 62
    for i, (t, txt) in enumerate(items):
        x = M + (i % 2) * (tw + 10)
        yy = y - (i // 2) * (th + 8)
        c.setFillColor(white)
        c.setStrokeColor(GREY_M)
        c.rect(x, yy - th, tw, th, fill=1, stroke=1)
        c.setFillColor(ORANGE)
        c.rect(x, yy - th, 3, th, fill=1, stroke=0)
        tri_icon(c, x + 14, yy - th / 2 - 7, 15, RED if i in (0, 2, 3) else ORANGE)
        ptext(c, x + 40, yy - 15, t, 8, "LSB", DARK)
        para(c, txt, x + 40, yy - 21, tw - 48, "pxs")
    y -= 4 * (th + 8) + 6
    y -= section(c, M, y, "Situation anormale : réflexe en trois étapes") + 4
    flow(c, ["Témoin rouge, voyant PGM-FI clignotant, fumée ou fuite", "Arrêt en sécurité, contact sur Off", "Contrôle ou concessionnaire, sans improviser"],
         M, y, CW, 34, hl=(1,))


def p4(c):
    y = TOP
    y -= para(c, "Ce document couvre la <b>SH150AD de 2020 à 2024</b> (manuel du propriétaire 21YM). Une valeur juste pour cette génération "
                 "peut être fausse pour une SH150i de 2018 ou de 2005 : l'assistant identifie toujours la génération avant de répondre.", M, y, CW) + 10
    fh = 150
    frame(c, M, y, CW, fh, white)
    x0, x1 = M + 30, W - M - 30
    ly = y - 78
    c.setStrokeColor(DARK)
    c.setLineWidth(2)
    c.line(x0, ly, x1, ly)
    ms = [("2005", "Génération 2005 : 152,7 cm³, frein AR à tambour (fiche_entretien_sh150_2005)", False),
          ("2013", "Moteur eSP, Idling Stop, roues 16 pouces, ABS en option", False),
          ("2017", "Smart Key et LED ; génération du manuel_sh150i_2018", False),
          ("2020", "CE DOCUMENT : 157 cm³, 4 soupapes eSP+, HSTC, Euro 5", True),
          ("2024", "Le manuel 21YM couvre les types II ED et III ED", False)]
    for k, (yr, txt, hl) in enumerate(ms):
        px = x0 + 20 + k * (x1 - x0 - 40) / 4
        c.setFillColor(COLM if hl else DARK)
        c.circle(px, ly, 7 if hl else 5, fill=1, stroke=0)
        ptext(c, px, ly + (14 if k % 2 == 0 else -22), yr, 9, "LSB", COLM if hl else DARK, "c")
        p = P(("<b>%s</b>" % txt) if hl else txt, "pxs")
        bw = 104
        p.wrap(bw, 60)
        bx = min(max(px - bw / 2, M + 6), W - M - bw - 6)
        p.drawOn(c, bx, ly + 28) if k % 2 == 0 else p.drawOn(c, bx, ly - 30 - p.height)
    y -= fh + 4
    y -= caption(c, M, y, CW, "4.1", "jalons de la SH150 et documents du corpus correspondants (frise schématique, intervalles non proportionnels).") + 10
    rows = [["Point de contrôle", "2020-2024 (ce document)", "2017-2019", "2005-2008", "Source"],
            ["Cylindrée", "157 cm³", "153 cm³", "152,7 cm³", ref(152) + " ; autres docs"],
            ["Distribution", "4 soupapes (eSP+)", "2 soupapes (eSP)", "2 soupapes", "-"],
            ["Bougie", "NGK LMAR8L-9", "absente du corpus", "NGK CR8EH-9", ref(153)],
            ["Huile après vidange", "0,8 L", "absente du corpus", "0,9 L", ref(153)],
            ["Pression AV (seul)", "200 kPa", "absente du corpus", "175 kPa", ref(153)],
            ["HSTC", "oui", "non", "non", ref(58)],
            ["Réservoir", "7,0 L", "7,5 L", "7,5 L", ref(152)]]
    y -= table(c, rows, M, y, [100, 110, 95, 85, CW - 390]) + 10
    callout(c, "attention", M, y, CW, "Négatif difficile", "Pression avant, bougie, quantité d'huile et réservoir changent d'une génération à l'autre. "
            "Si le millésime n'est pas connu, l'assistant demande la carte grise ou la plaque du cadre au lieu de répondre.")


def p5(c):
    y = TOP
    y -= para(c, "Toutes les valeurs de cette page proviennent des caractéristiques du manuel du propriétaire (" + ref(152) + " à " + ref(154) + ").", M, y, CW) + 8
    hw = (CW - 14) / 2
    section(c, M, y, "Moteur et dimensions (" + ref(152) + ")", hw)
    section(c, M + hw + 14, y, "Données d'entretien (" + ref(153) + ")", hw)
    y -= 26
    r1 = [["Élément", "SH150AD"], ["Cylindrée", "157 cm³"], ["Alésage x course", "60,0 x 55,5 mm"], ["Rapport volumétrique", "12,0:1"],
          ["Carburant", "Sans plomb, RON 95 ou plus ; jusqu'à 10 % d'éthanol"], ["Réservoir", "7,0 L"], ["Batterie", "YTZ8V, 12 V - 7,0 Ah (10 h)"],
          ["Transmission", "V-Matic 2,68:1 à 0,82:1 ; finale 10,552"], ["Longueur x largeur x hauteur", "2 090 x 730 x 1 130 mm"],
          ["Empattement ; garde au sol", "1 350 mm ; 145 mm"], ["Masse en ordre de marche", "138 kg (types II ED, III ED) ; 137 kg sinon"],
          ["Charge maximale", "180 kg"]]
    r2 = [["Élément", "Valeur"], ["Pneus", "AV 100/80-16M/C 50P ; AR 120/80-16M/C 60P"], ["Type", "Diagonal, sans chambre"],
          ["Pression AV / AR", "200 / 225 kPa (seul ou en duo)"], ["Sculptures mini", "AV 1,5 mm ; AR 2,0 mm"],
          ["Bougie", "NGK LMAR8L-9 ; écartement 0,8 à 0,9 mm"], ["Ralenti", "1 700 ± 100 tr/min"],
          ["Huile moteur", "Honda 4 temps API SG ou plus, SAE 10W-30, JASO MB"], ["Huile après vidange", "0,8 L"],
          ["Vidange + crépine ; démontage", "0,9 L ; 0,9 L"], ["Huile de transmission", "0,12 L (vidange) ; 0,14 L (démontage)"],
          ["Liquide de frein", "Honda DOT 3 ou DOT 4"], ["Refroidissement", "0,47 L, Pro Honda HP Coolant"]]
    h1 = table(c, r1, M, y, [100, hw - 100])
    h2 = table(c, r2, M + hw + 14, y, [100, hw - 100])
    y -= max(h1, h2) + 10
    y -= section(c, M, y, "Couples de serrage donnés par le manuel du propriétaire (" + ref(154) + ")") + 2
    rows = [["Élément", "Couple"], ["Bouchon de remplissage d'huile (oil plug)", "20 N·m"], ["Vis de vidange d'huile moteur", "24 N·m"]]
    y -= table(c, rows, M, y, [250, CW - 250]) + 8
    callout(c, "info", M, y, CW, None, "Les autres couples (axes de roue, étriers, bougie) ne figurent pas dans le manuel du propriétaire : ils relèvent du "
            "manuel d'atelier de la génération, absent du corpus pour 2020-2024.")


def p6(c):
    y = TOP
    fh = 206
    frame(c, M, y, CW, fh, white)
    pos = scooter(c, M + 95, y - fh + 26, 330)
    lab = [("phare", 1, -40, 6), ("tableau", 2, -48, 12), ("selle", 3, 14, 36), ("cvt", 4, 34, -34), ("bequille_c", 5, -46, -6),
           ("bequille_l", 6, -56, 4), ("feu_ar", 7, 26, 22), ("jauge", 8, 30, -44)]
    for k, n, dx, dy in lab:
        px, py = pos[k]
        leader(c, px, py, px + dx, py + dy, n)
    y -= fh + 4
    y -= caption(c, M, y, CW, "6.1", "repères principaux sur une silhouette schématique (côté gauche) ; les formes ne reproduisent pas la SH150i.") + 8
    rows = [["N°", "Élément", "Ce qu'en dit le manuel du propriétaire", "Source"],
            ["1", "Éclairage", "Phare, feu stop, clignotants, éclairage de plaque et feux de position à LED", ref(154)],
            ["2", "Instrumentation", "Témoins décrits page 7 de ce document ; boutons INFO A et INFO B", "%s, %s" % (ref(40), ref(58))],
            ["3", "Selle", "Ouverture par la commande de contact en position SEAT FUEL (Smart Key)", ref(120)],
            ["4", "Transmission", "V-Matic à courroie ; courroie contrôlée à 12 000 km, remplacée à 24 000 km", "%s, %s" % (ref(152), ref(78))],
            ["5", "Béquille centrale", "Position de référence pour les contrôles d'huile et de liquide", ref(98)],
            ["6", "Béquille latérale", "Coupe-circuit d'allumage : démarrage impossible béquille dépliée", ref(59)],
            ["7", "Feu arrière", "LED", ref(154)],
            ["8", "Jauge-bouchon d'huile", "Contrôle sans visser la jauge", ref(98)]]
    y -= table(c, rows, M, y, [24, 100, CW - 194, 70]) + 12
    y -= section(c, M, y, "Équipements de la génération") + 4
    tiles = [("SMART Key", "Contact sans clé ; témoin vert de vérification.", "smartkey", GREEN),
             ("Idling Stop", "Arrêt automatique au feu ; témoin vert.", "idling", GREEN),
             ("HSTC", "Contrôle de couple, désactivable à l'arrêt.", "tc", ORANGE),
             ("ABS", "Témoin éteint au-dessus d'environ 10 km/h.", "abs", ORANGE)]
    tw = (CW - 30) / 4
    for i, (t, d, ic, col) in enumerate(tiles):
        x = M + i * (tw + 10)
        c.setFillColor(white)
        c.setStrokeColor(GREY_M)
        c.rect(x, y - 70, tw, 70, fill=1, stroke=1)
        c.setFillColor(DARK)
        c.roundRect(x + 8, y - 34, 26, 26, 4, fill=1, stroke=0)
        pic(c, ic, x + 21, y - 21, 14, col)
        ptext(c, x + 40, y - 24, t, 8, "LSB", DARK)
        para(c, d, x + 8, y - 40, tw - 14, "pxs")


def p7(c):
    y = TOP
    y -= para(c, "L'instrumentation de la SH150AD regroupe un écran LCD et des témoins (" + ref(40) + " et " + ref(41) + "). Le schéma ci-dessous "
                 "est une <b>disposition schématique</b> dessinée par l'équipe pour nommer les témoins : il ne reproduit pas l'emplacement réel des "
                 "témoins sur le tableau Honda.", M, y, CW) + 8
    fh = 230
    frame(c, M, y, CW, fh, GREY_L)
    pw = 330
    px0 = M + (CW - pw) / 2
    pos = panel(c, px0, y - fh + 50, pw, {k: "on" for k in ["moteur", "abs", "tc", "tcoff", "temp", "smartkey", "idling", "route", "cli_g", "cli_d"]})
    order = ["moteur", "abs", "tc", "tcoff", "temp", "smartkey", "idling", "route", "cli_g"]
    off = {"moteur": (-40, 6), "abs": (-40, 0), "tc": (-40, -6), "temp": (40, 6), "smartkey": (40, 0), "idling": (40, -6), "tcoff": (0, -30),
           "route": (34, 14), "cli_g": (-28, 16)}
    for i, k in enumerate(order):
        x, yy = pos[k]
        dx, dy = off[k]
        c.setStrokeColor(ORANGE)
        c.setLineWidth(0.6)
        c.line(x, yy, x + dx, yy + dy)
        marker(c, x + dx, yy + dy, i + 1, DARK, 5.5)
    ptext(c, W / 2, y - fh + 14, "Tous les témoins sont représentés allumés pour les identifier ; en usage normal, ils s'éteignent après le contrôle au contact.",
          6.4, "LSI", GREY_D, "c")
    y -= fh + 4
    y -= caption(c, M, y, CW, "7.1", "témoins de la SH150AD, repères 1 à 9 (disposition schématique, pictogrammes de l'équipe).") + 6
    rows = [["N°", "Témoin", "Couleur", "Comportement normal", "Source"],
            ["1", "Voyant d'injection PGM-FI (MIL)", "orange", "S'allume brièvement au contact, puis s'éteint", ref(40)],
            ["2", "ABS", "orange", "Allumé au contact ; s'éteint vers 10 km/h", ref(41)],
            ["3", "Contrôle de couple (HSTC)", "orange", "Allumé au contact ; s'éteint vers 3 km/h ; clignote quand le système agit", ref(41)],
            ["4", "HSTC désactivé", "orange", "Allumé quand le HSTC est coupé (« HSTC OFF »)", "%s, %s" % (ref(41), ref(58))],
            ["5", "Température élevée du liquide", "rouge", "Éteint ; s'allume si la température dépasse la valeur prévue", ref(40)],
            ["6", "Honda SMART Key", "vert", "Allumé quand la clé est vérifiée ; s'éteint au passage sur On", ref(40)],
            ["7", "Idling Stop", "vert", "Allumé quand le système est prêt ; clignote moteur arrêté par le système", "%s, %s" % (ref(40), ref(55))],
            ["8", "Feu de route", "bleu", "Allumé feu de route en service", ref(41)],
            ["9", "Clignotants", "vert", "Clignotent avec le clignotant", ref(41)]]
    table(c, rows, M, y, [22, 130, 46, CW - 258, 60])


def p8(c):
    y = TOP
    y -= para(c, "Matrice de lecture des témoins : ce qui est <b>normal</b> et ce qui signale une <b>anomalie</b>, avec la conduite à tenir "
                 "indiquée par le manuel du propriétaire.", M, y, CW) + 8
    cards = [("moteur", ORANGE, "MIL allumé moteur tournant", "Problème du système antipollution du moteur.", "Éviter les vitesses élevées ; contrôle rapide chez le concessionnaire.", ref(117), {"moteur": "on"}),
             ("moteur", RED, "MIL clignotant", "Ratés d'allumage détectés.", "Se garer loin de toute matière inflammable, moteur arrêté au moins 10 min. Si le voyant clignote encore au redémarrage : rouler à 50 km/h maximum jusqu'au concessionnaire.", ref(117), {"moteur": "blink"}),
             ("abs", ORANGE, "ABS allumé ou clignotant en roulant", "Problème possible de l'ABS ; le freinage reste conventionnel, sans antiblocage.", "Réduire la vitesse et faire contrôler. Clignotement après rotation de la roue AR levée : couper puis remettre le contact.", ref(118), {"abs": "on"}),
             ("tc", ORANGE, "HSTC allumé fixe en roulant", "Problème possible du contrôle de couple ; conduite normale sans HSTC.", "Réduire la vitesse et faire contrôler. Si le système agissait : refermer complètement les gaz.", ref(119), {"tc": "on"}),
             ("temp", RED, "Température élevée allumé", "Surchauffe du moteur ; accélération molle.", "S'arrêter, couper le contact, laisser refroidir, chercher une fuite, contrôler le vase (page 15).", ref(116), {"temp": "on"}),
             ("smartkey", GREEN, "SMART Key clignote 5 fois au contact", "Pile de la Smart Key faible.", "Remplacer la pile CR2032 dès que possible (page 9).", "%s, %s" % (ref(112), ref(120)), {"smartkey": "blink"})]
    cw = (CW - 12) / 2
    ch = 140
    for i, (ic, col, t, sig, act, src, st) in enumerate(cards):
        x = M + (i % 2) * (cw + 12)
        yy = y - (i // 2) * (ch + 8)
        c.setFillColor(white)
        c.setStrokeColor(GREY_M)
        c.rect(x, yy - ch, cw, ch, fill=1, stroke=1)
        c.setFillColor(DARK)
        c.roundRect(x + 10, yy - 46, 40, 36, 6, fill=1, stroke=0)
        pic(c, ic, x + 30, yy - 28, 20, col if col != RED or ic != "moteur" else ORANGE)
        if "blink" in st.values():
            _rays(c, x + 30, yy - 28, 12, col)
        p = P("<b>%s</b>" % t, "ct")
        p.wrap(cw - 70, 40)
        p.drawOn(c, x + 60, yy - 14 - p.height)
        para(c, "<b>Signification</b> : " + sig, x + 10, yy - 54, cw - 20, "pxs")
        para(c, "<b>Action</b> : " + act, x + 10, yy - 78, cw - 20, "pxs")
        c.setFillColor(col)
        c.rect(x, yy - ch, cw, 15, fill=1, stroke=0)
        ptext(c, x + 8, yy - ch + 4.5, "Source : " + src, 7, "LSB", white)
    y -= 3 * (ch + 8) + 2
    callout(c, "info", M, y, CW, "Aucun code de clignotement dans le manuel du propriétaire",
            "Le manuel du propriétaire 2020-2024 ne donne pas de codes de défaut chiffrés. Les codes de clignotement de fiche_entretien_sh150_2005 "
            "concernent la génération 2005 et ne s'appliquent pas ici.")


def p9(c):
    y = TOP
    y -= para(c, "La Honda SMART Key permet d'utiliser le contact sans introduire de clé : la clé reste sur le pilote pendant la conduite (" + ref(59) + ").", M, y, CW) + 8
    fh = 140
    frame(c, M, y, CW, fh, white)
    kx, ky = M + 80, y - 74
    c.setFillColor(DARK)
    c.roundRect(kx - 20, ky - 30, 40, 60, 10, fill=1, stroke=0)
    c.setFillColor(HexColor("#5a6069"))
    c.circle(kx, ky + 8, 8, fill=1, stroke=0)
    ptext(c, kx, ky - 44, "Smart Key (pile CR2032)", 7.4, "LSB", DARK, "c")
    for r in (40, 56, 72):
        c.setStrokeColor(GREEN)
        c.setLineWidth(1)
        c.arc(kx + 10 - r, ky - r, kx + 10 + r, ky + r, -35, 70)
    cx = M + 270
    c.setFillColor(GREY_L)
    c.setStrokeColor(GREY_D)
    c.circle(cx, ky, 34, fill=1, stroke=1)
    c.setFillColor(DARK)
    c.circle(cx, ky, 20, fill=1, stroke=0)
    for lbl, ang in (("Lock", 150), ("Off", 110), ("On", 50), ("SEAT FUEL", 10)):
        a = math.radians(ang)
        ptext(c, cx + math.cos(a) * 52, ky + math.sin(a) * 44 - 3, lbl, 7, "LSB", DARK, "c")
    ptext(c, cx, ky - 50, "commande de contact (schéma)", 7, "LSI", GREY_D, "c")
    y -= fh + 4
    y -= caption(c, M, y, CW, "9.1", "principe de la Smart Key et positions de la commande de contact citées par le manuel (schéma de l'équipe).") + 10
    rows = [["Situation", "Ce que dit le manuel", "Source"],
            ["Témoin SMART Key clignote 5 fois au passage sur On", "Pile de la clé faible : la remplacer dès que possible (pile CR2032) ; Honda recommande le concessionnaire", "%s, %s" % (ref(112), ref(120))],
            ["Témoin clignotant contact sur On", "Communication interrompue : ondes radio fortes ou clé perdue en roulant ; le scooter fonctionne jusqu'au verrouillage", ref(120)],
            ["Arrêt du clignotement", "Maintenir la commande de contact appuyée plus de 2 secondes : le contact se verrouille", ref(120)],
            ["Contact sur SEAT FUEL, Off ou Lock pendant le clignotement", "La bague et le témoin s'allument environ 20 s, puis le contact se verrouille", ref(120)],
            ["Smart Key absente", "Le contact peut être déverrouillé par une autre méthode décrite dans le manuel", ref(129)]]
    y -= table(c, rows, M, y, [160, CW - 230, 70]) + 10
    callout(c, "attention", M, y, CW, "Pendant une intervention", "Moteur arrêté contact sur On, l'authentification se désactive après un certain temps "
            "ou quand la clé s'éloigne (" + ref(59) + "). En atelier, éloigner la clé du scooter.")


def p10(c):
    y = TOP
    y -= para(c, "L'Idling Stop arrête le moteur à l'arrêt, par exemple à un carrefour, pour réduire la consommation et le bruit (" + ref(55) + ").", M, y, CW) + 8
    y -= section(c, M, y, "Conditions d'activation (" + ref(55) + ")") + 2
    y -= steps(c, ["Commutateur Idling Stop sur IDLING STOP.", "Moteur démarré avec le bouton de démarreur.", "Moteur suffisamment chaud.",
                   "Vitesse supérieure à 10 km/h : le témoin Idling Stop s'allume, le système est prêt."], M, y, CW, gap=3, st="ps") + 8
    y -= section(c, M, y, "Cycle de fonctionnement (Figure 10.1)") + 4
    flow(c, ["Témoin allumé (prêt)", "Gaz refermés, scooter arrêté", "Moteur coupé, témoin clignote", "Ouverture des gaz : redémarrage"], M, y, CW, 34, hl=(2,))
    y -= 40
    y -= caption(c, M, y, CW, "10.1", "fonctionnement de l'Idling Stop (" + ref(56) + ").") + 8
    rows = [["Situation", "Ce que dit le manuel", "Source"],
            ["Moteur arrêté par le système, commutateur passé sur IDLING", "Système annulé : le moteur ne redémarre pas à l'ouverture des gaz", ref(56)],
            ["Arrêt prolongé par l'Idling Stop", "Peut décharger la batterie", ref(56)],
            ["Contrôle ou vidange d'huile", "Commutateur sur IDLING (système désactivé)", "%s, %s" % (ref(98), ref(99))],
            ["Le témoin ne s'allume pas", "Voir la page de dépannage du manuel", ref(122)],
            ["Le moteur ne s'arrête pas alors que le témoin est allumé", "Voir la page de dépannage du manuel", ref(123)]]
    y -= table(c, rows, M, y, [180, CW - 250, 70]) + 10
    y -= callout(c, "danger", M, y, CW, "Ne pas s'éloigner", "Ne vous éloignez jamais du scooter quand le témoin Idling Stop clignote : le moteur peut "
                 "redémarrer si la poignée est ouverte. Coupez le contact (" + ref(56) + ").") + 8
    callout(c, "info", M, y, CW, "Négatif difficile", "Un moteur qui s'arrête au feu rouge avec le témoin Idling Stop clignotant n'est pas une panne. "
            "Un moteur qui s'arrête en roulant en est une.")


def p11(c):
    y = TOP
    y -= para(c, "Le contrôle de couple sélectionnable Honda (<b>HSTC</b>) limite la puissance du moteur pour gérer la motricité de la roue arrière. "
                 "Il peut être désactivé (" + ref(58) + ").", M, y, CW) + 8
    hw = (CW - 14) / 2
    section(c, M, y, "Activer ou désactiver (" + ref(58) + ")", hw)
    section(c, M + hw + 14, y, "Témoins HSTC (Figure 11.1)", hw)
    y -= 28
    h = steps(c, ["Arrêter le scooter : ne jamais manœuvrer le commutateur en roulant.", "Sélectionner le mode Torque Control à l'écran.",
                  "Maintenir le bouton <b>INFO B</b> appuyé : l'écran affiche « HSTC ON » ou « HSTC OFF ».",
                  "À chaque mise du contact, le HSTC revient automatiquement sur ON.",
                  "Impossible de le désactiver pendant qu'il agit (témoin clignotant)."], M, y, hw, gap=4, st="ps")
    fx = M + hw + 14
    fh = 160
    frame(c, fx, y + 2, hw, fh, white)
    for i, (k, t, d) in enumerate([("tc", "Témoin HSTC", "allumé au contact, éteint vers 3 km/h, clignote quand il agit"),
                                   ("tcoff", "Témoin HSTC OFF", "allumé quand le HSTC est désactivé")]):
        yy = y - 30 - i * 60
        c.setFillColor(DARK)
        c.roundRect(fx + 14, yy - 18, 40, 34, 6, fill=1, stroke=0)
        pic(c, k, fx + 34, yy, 20, ORANGE)
        ptext(c, fx + 64, yy + 4, t, 8, "LSB", DARK)
        para(c, d, fx + 64, yy - 2, hw - 80, "pxs")
    y -= max(h, fh) + 6
    caption(c, fx, y + 4, hw, "11.1", "les deux témoins HSTC (" + ref(41) + ").")
    y -= 14
    y -= callout(c, "attention", M, y, CW, "Témoin HSTC allumé fixe en roulant", "Problème possible du contrôle de couple : réduire la vitesse et faire "
                 "contrôler. La conduite reste normale sans la fonction HSTC (" + ref(119) + ").") + 8
    y -= callout(c, "info", M, y, CW, "Roue arrière levée", "Faire tourner la roue arrière scooter levé peut allumer le témoin HSTC (ou ABS) : couper puis "
                 "remettre le contact ; le témoin s'éteint dès environ 3 km/h (" + ref(119) + ").") + 8
    callout(c, "info", M, y, CW, "Négatif difficile", "Le HSTC n'existe pas sur la SH150i 2017-2019 (manuel_sh150i_2018) : une question sur le HSTC "
            "d'une 2018 doit faire vérifier le millésime.")


def p12(c):
    y = TOP
    y -= callout(c, "attention", M, y, CW, "Coupe-circuit de béquille latérale", "Béquille latérale dépliée, le moteur ne démarre pas ; si on la déplie "
                 "moteur tournant, il se coupe (" + ref(59) + ").") + 10
    y -= section(c, M, y, "Règles de démarrage (" + ref(59) + ")") + 2
    y -= steps(c, ["Garder la Smart Key sur soi ; béquille latérale repliée.", "Contact sur On : les témoins s'allument brièvement (contrôle).",
                   "Poignée d'accélérateur fermée : le moteur ne démarre pas poignée grande ouverte.",
                   "Si le moteur ne démarre pas en 5 secondes : contact sur Off, attendre 10 secondes avant un nouvel essai.",
                   "Ne pas laisser le moteur tourner longtemps en ralenti accéléré ni l'emballer."], M, y, CW, gap=4, st="ps") + 8
    y -= section(c, M, y, "Séquence (Figure 12.1)") + 4
    flow(c, ["Smart Key sur soi", "Béquille latérale repliée", "Contact sur On, contrôle des témoins", "Gaz fermés, démarreur", "5 s max, sinon Off 10 s"],
         M, y, CW, 34, hl=(2,))
    y -= 40
    y -= caption(c, M, y, CW, "12.1", "démarrage normal.") + 10
    rows = [["Le moteur ne démarre pas", "Vérifier", "Document"],
            ["Béquille latérale", "Repliée ?", "page 12"], ["Smart Key", "Sur le pilote ? témoin clignotant ?", "page 9"],
            ["Batterie", "Tension suffisante ? (5 s / 10 s)", "page 18"], ["Poignée", "Fermée ?", "page 12"],
            ["Voyant PGM-FI", "Allumé moteur tournant ou clignotant ?", "page 8"]]
    y -= table(c, rows, M, y, [140, CW - 220, 80]) + 10
    callout(c, "danger", M, y, CW, "Après une chute", "Couper le contact (Off) et inspecter le scooter avant de redémarrer (" + ref(59) + ").")


def p13(c):
    y = TOP
    y -= para(c, "Extrait du programme d'entretien Honda (" + ref(77) + " et " + ref(78) + "). Kilométrages en milliers de km ; au-delà de 36 000 km, "
                 "répéter les intervalles. I = inspecter (et nettoyer, régler, lubrifier ou remplacer si nécessaire), R = remplacer, C = nettoyer.", M, y, CW) + 8
    cols = ["Opération", "1", "6", "12", "18", "24", "30", "36", "Annuel", "Remplacement"]
    rows = [cols,
            ["Huile moteur", "R", "R", "R", "R", "R", "R", "R", "R", "-"],
            ["Crépine d'huile moteur", "", "", "C", "", "C", "", "C", "", "-"],
            ["Filtre à air", "", "", "", "R", "", "", "R", "", "-"],
            ["Bougie", "", "I", "R", "I", "R", "I", "R", "", "-"],
            ["Jeu aux soupapes", "", "I", "I", "I", "I", "I", "I", "", "-"],
            ["Reniflard du carter", "", "C", "C", "C", "C", "C", "C", "", "-"],
            ["Liquide de refroidissement", "", "", "I", "", "I", "", "I", "I", "3 ans"],
            ["Courroie de transmission", "", "", "I", "", "R", "", "I", "", "-"],
            ["Huile de transmission finale", "", "", "", "", "", "", "", "", "2 ans"],
            ["Liquide de frein", "", "I", "I", "I", "I", "I", "I", "I", "2 ans"],
            ["Usure des plaquettes", "", "I", "I", "I", "I", "I", "I", "I", "-"],
            ["Batterie", "", "I", "I", "I", "I", "I", "I", "I", "-"],
            ["Béquille latérale", "", "I", "I", "I", "I", "I", "I", "I", "-"],
            ["Roues et pneus", "", "I", "I", "I", "I", "I", "I", "I", "-"]]
    y -= table(c, rows, M, y, [150] + [32] * 7 + [52, CW - 426]) + 8
    y -= section(c, M, y, "Intervalles de remplacement (Figure 13.1)") + 4
    fh = 96
    frame(c, M, y, CW, fh, white)
    bars = [("Huile moteur", 6, ORANGE), ("Bougie", 12, GREY_D), ("Filtre à air", 18, GREY_D), ("Courroie", 24, DARK)]
    maxw = CW - 200
    by = y - 20
    for lbl, v, col in bars:
        ptext(c, M + 10, by - 3, lbl, 7.2, "LSB", DARK)
        c.setFillColor(col)
        c.rect(M + 100, by - 6, maxw * v / 24, 11, fill=1, stroke=0)
        ptext(c, M + 104 + maxw * v / 24, by - 3, "%d 000 km" % v, 7, "LS", DARK)
        by -= 18
    ptext(c, M + 10, by - 2, "Huile moteur : aussi chaque année. Première vidange à 1 000 km.", 6.6, "LSI", GREY_D)
    y -= fh + 4
    y -= caption(c, M, y, CW, "13.1", "intervalles de remplacement relevés dans le programme (schéma proportionnel).") + 8
    callout(c, "info", M, y, CW, "Indicateur d'entretien", "L'écran affiche un indicateur d'entretien et la distance restante ; la remise à zéro se fait en "
            "maintenant le bouton INFO A dans le mode prévu (" + ref(39) + ").")


def p14(c):
    y = TOP
    y -= callout(c, "arret", M, y, CW, "Conditions de mesure (" + ref(98) + ")", "Commutateur Idling Stop sur <b>IDLING</b>. Moteur froid : le faire tourner "
                 "3 à 5 minutes au ralenti. Contact sur Off, attendre 2 à 3 minutes. Scooter sur béquille centrale, sol ferme et plat.") + 10
    hw = (CW - 14) / 2
    section(c, M, y, "Contrôle du niveau (" + ref(98) + ")", hw)
    section(c, M + hw + 14, y, "Jauge-bouchon (Figure 14.1)", hw)
    y -= 28
    h = steps(c, ["Retirer la jauge-bouchon et l'essuyer.", "La réinsérer jusqu'en butée <b>sans la visser</b>.",
                  "Vérifier que le niveau est entre les repères haut et bas.", "Si besoin, compléter jusqu'au repère haut sans le dépasser (" + ref(99) + ").",
                  "Remettre la jauge-bouchon fermement."], M, y, hw, gap=4, st="ps")
    fx = M + hw + 14
    fh = 170
    frame(c, fx, y + 2, hw, fh, white)
    jx, top = fx + 60, y - 12
    c.setFillColor(DARK)
    c.roundRect(jx - 12, top - 14, 24, 14, 3, fill=1, stroke=0)
    c.setFillColor(HexColor("#b8bdc4"))
    c.rect(jx - 3, top - 150, 6, 136, fill=1, stroke=0)
    c.setFillColor(HexColor("#c88a1b"))
    c.rect(jx - 3, top - 150, 6, 58, fill=1, stroke=0)
    for lab, yy in (("repère haut", top - 80), ("repère bas", top - 112)):
        c.setStrokeColor(DARK)
        c.line(jx - 8, yy, jx + 8, yy)
        ptext(c, jx + 12, yy - 3, lab, 7.6, "LSB", DARK)
    ptext(c, jx + 90, top - 96, "Niveau correct", 7.6, "LSB", ORANGE)
    y -= max(h, fh) + 6
    caption(c, fx, y + 4, hw, "14.1", "jauge-bouchon (schéma de principe).")
    y -= 12
    y -= section(c, M, y, "Vidange et crépine") + 2
    rows = [["Élément", "Valeur", "Source"], ["Huile", "Honda 4 temps, API SG ou plus, SAE 10W-30, JASO MB (sauf huiles « Energy Conserving »)", ref(153)],
            ["Quantité après vidange", "0,8 L", ref(153)], ["Après vidange et nettoyage de la crépine", "0,9 L", ref(153)],
            ["Vis de vidange", "24 N·m", ref(154)], ["Bouchon de remplissage", "20 N·m", ref(154)],
            ["Intervalle", "1 000 km, puis tous les 6 000 km et chaque année ; crépine tous les 12 000 km", ref(77)]]
    y -= table(c, rows, M, y, [150, CW - 220, 70]) + 8
    callout(c, "attention", M, y, CW, "Outils spéciaux", "Honda indique que la vidange et le nettoyage de la crépine demandent des outils spéciaux et "
            "recommande le concessionnaire (" + ref(99) + "). Ne pas mélanger des huiles de marques ou de grades différents (" + ref(99) + ").")


def p15(c):
    y = TOP
    y -= para(c, "Le niveau se contrôle <b>moteur froid</b> sur le vase d'expansion, scooter sur béquille centrale (" + ref(102) + ").", M, y, CW) + 8
    hw = (CW - 14) / 2
    fh = 150
    frame(c, M, y, hw, fh, white)
    bx, by = M + 60, y - 130
    c.setFillColor(white)
    c.setStrokeColor(DARK)
    c.roundRect(bx, by, 70, 100, 8, fill=1, stroke=1)
    c.setFillColor(HexColor("#9fd0a8"))
    c.rect(bx + 4, by + 4, 62, 52, fill=1, stroke=0)
    for lab, yy in (("UPPER", by + 76), ("LOWER", by + 30)):
        c.setStrokeColor(DARK)
        c.line(bx - 6, yy, bx + 76, yy)
        ptext(c, bx + 82, yy - 3, lab, 7.6, "LSB", DARK)
    caption(c, M, y - fh - 4, hw, "15.1", "vase d'expansion : niveau entre UPPER et LOWER (schéma).")
    rows = [["Élément", "Valeur", "Source"], ["Capacité du circuit", "0,47 L", ref(153)], ["Liquide", "Pro Honda HP Coolant", ref(153)],
            ["Remplacement", "Tous les 3 ans", ref(77)], ["Contrôle", "Avant départ, 12 000 km, 24 000 km, 36 000 km, chaque année", ref(77)]]
    table(c, rows, M + hw + 14, y, [80, hw - 140, 60])
    y -= fh + 26
    y -= section(c, M, y, "Surchauffe : témoin de température allumé (" + ref(116) + ")") + 4
    flow(c, ["Témoin allumé, accélération molle", "Arrêt en sécurité, contact Off", "Refroidissement contact coupé", "Durites : fuite ?", "Niveau du vase, appoint"],
         M, y, CW, 34, hl=(1,))
    y -= 40
    y -= caption(c, M, y, CW, "15.2", "conduite à tenir en cas de surchauffe.") + 8
    y -= callout(c, "danger", M, y, CW, "Fuite constatée", "En cas de fuite, ne pas redémarrer : transporter le scooter chez le concessionnaire. "
                 "Rouler moteur en surchauffe peut l'endommager gravement (" + ref(116) + ").") + 8
    y -= callout(c, "info", M, y, CW, None, "Un ralenti accéléré prolongé peut allumer le témoin. Si les contrôles 1 à 4 sont normaux, la route peut "
                 "reprendre en surveillant le témoin (" + ref(116) + ").") + 8
    callout(c, "attention", M, y, CW, "Niveau qui baisse", "Un niveau qui baisse nettement ou un vase vide signale probablement une fuite importante : "
            "contrôle chez le concessionnaire (" + ref(102) + ").")


def p16(c):
    y = TOP
    rows = [["Élément", "Avant", "Arrière", "Source"], ["Dimension", "100/80-16M/C 50P", "120/80-16M/C 60P", ref(153)],
            ["Pneus recommandés", "IRC SS-530F ou MICHELIN CITY GRIP", "IRC SS-530R ou MICHELIN CITY GRIP", ref(153)],
            ["Pression à froid, pilote seul", "200 kPa (2,00 bar, 29 psi)", "225 kPa (2,25 bar, 33 psi)", ref(153)],
            ["Pression à froid, avec passager", "200 kPa (2,00 bar, 29 psi)", "225 kPa (2,25 bar, 33 psi)", ref(153)],
            ["Profondeur minimale des sculptures", "1,5 mm", "2,0 mm", ref(153)]]
    y -= table(c, rows, M, y, [150, (CW - 210) / 2, (CW - 210) / 2, 60]) + 10
    y -= callout(c, "attention", M, y, CW, "Même pression seul ou en duo", "Sur cette génération, la pression ne change pas avec un passager. Sur la "
                 "génération 2005, l'arrière passe de 200 à 225 kPa en duo et l'avant est à 175 kPa (fiche_entretien_sh150_2005).") + 10
    hw = (CW - 14) / 2
    fh = 150
    frame(c, M, y, hw, fh, white)
    bx, top = M + 60, y - 16
    c.setFillColor(white)
    c.setStrokeColor(DARK)
    c.rect(bx - 7, top - 14, 14, 14, fill=1, stroke=1)
    c.setFillColor(HexColor("#f1f1ee"))
    c.rect(bx - 10, top - 56, 20, 42, fill=1, stroke=1)
    c.setFillColor(HexColor("#9aa1ab"))
    c.rect(bx - 13, top - 76, 26, 20, fill=1, stroke=1)
    c.setFillColor(HexColor("#b8bdc4"))
    c.rect(bx - 8, top - 112, 16, 36, fill=1, stroke=1)
    c.setStrokeColor(DARK)
    c.setLineWidth(2)
    c.line(bx, top - 112, bx, top - 120)
    c.line(bx - 7, top - 112, bx - 7, top - 126)
    c.line(bx - 7, top - 126, bx + 4, top - 126)
    ptext(c, bx + 22, top - 126, "écartement 0,8 à 0,9 mm", 7.4, "LSB", COLM)
    ptext(c, bx + 22, top - 40, "NGK LMAR8L-9", 7.4, "LSB", DARK)
    caption(c, M, y - fh - 4, hw, "16.1", "bougie standard et écartement (" + ref(153) + "), schéma non à l'échelle.")
    fx = M + hw + 14
    rows2 = [["Élément", "Valeur", "Source"], ["Bougie standard", "NGK LMAR8L-9", ref(153)], ["Écartement", "0,8 à 0,9 mm", ref(153)],
             ["Ralenti", "1 700 ± 100 tr/min", ref(153)], ["Bougie", "Inspecter tous les 6 000 km, remplacer tous les 12 000 km", ref(77)]]
    table(c, rows2, fx, y, [80, hw - 140, 60])
    y -= fh + 26
    y -= section(c, M, y, "Contrôles des pneus") + 2
    y -= steps(c, ["Contrôler à froid, scooter sur béquille centrale.", "Corriger la pression selon le tableau ci-dessus.",
                   "Inspecter flancs et bande de roulement : coupures, clous, déformations.", "Mesurer la profondeur : remplacer sous 1,5 mm (AV) ou 2,0 mm (AR)."],
               M, y, CW, gap=3, st="ps") + 6
    callout(c, "info", M, y, CW, None, "Le couple de serrage de la bougie n'est pas donné par le manuel du propriétaire : il relève du manuel d'atelier.")


def p17(c):
    y = TOP
    y -= para(c, "La SH150AD est équipée de l'<b>ABS</b>. Le manuel du propriétaire décrit le comportement du témoin, le liquide de frein et le contrôle "
                 "d'usure des plaquettes ; le remplacement des pièces relève du concessionnaire.", M, y, CW) + 8
    rows = [["Élément", "Valeur", "Source"], ["Liquide de frein", "Honda DOT 3 ou DOT 4", ref(153)], ["Remplacement du liquide", "Tous les 2 ans", ref(78)],
            ["Contrôle du liquide, des plaquettes, du système", "Avant départ, tous les 6 000 km et chaque année", ref(78)],
            ["Témoin ABS normal", "Allumé au contact, éteint vers 10 km/h", ref(41)]]
    y -= table(c, rows, M, y, [200, CW - 270, 70]) + 10
    y -= section(c, M, y, "Témoin ABS : quand faire contrôler (" + ref(118) + ")") + 4
    tw = (CW - 20) / 3
    for i, t in enumerate(["S'allume ou clignote en roulant", "Ne s'allume pas au contact", "Ne s'éteint pas au-dessus de 10 km/h"]):
        x = M + i * (tw + 10)
        c.setFillColor(white)
        c.setStrokeColor(GREY_M)
        c.rect(x, y - 50, tw, 50, fill=1, stroke=1)
        c.setFillColor(DARK)
        c.roundRect(x + 8, y - 40, 30, 30, 5, fill=1, stroke=0)
        pic(c, "abs", x + 23, y - 25, 16, ORANGE)
        para(c, "<b>%s</b>" % t, x + 46, y - 12, tw - 54, "ps")
    y -= 62
    y -= callout(c, "attention", M, y, CW, "ABS en défaut", "Réduire la vitesse et faire contrôler dès que possible. Témoin allumé fixe : le freinage "
                 "fonctionne de façon conventionnelle, <b>sans antiblocage</b> (" + ref(118) + ").") + 8
    y -= callout(c, "info", M, y, CW, "Roue arrière levée", "Le témoin ABS peut clignoter si on fait tourner la roue arrière scooter levé : couper puis "
                 "remettre le contact ; il s'éteint au-dessus de 30 km/h (" + ref(118) + ").") + 8
    callout(c, "danger", M, y, CW, "Intervention réservée", "Remplacement des plaquettes, purge et remplacement du liquide : concessionnaire ou technicien "
            "formé ; le remplacement du liquide demande des compétences mécaniques (" + ref(78) + ").")


def p18(c):
    y = TOP
    hw = (CW - 14) / 2
    section(c, M, y, "Batterie (" + ref(152) + ")", hw)
    section(c, M + hw + 14, y, "Fusibles (" + ref(154) + ")", hw)
    y -= 28
    rows = [["Élément", "Valeur"], ["Type", "YTZ8V"], ["Capacité", "12 V - 7,0 Ah (10 h) / 7,4 Ah (20 h)"], ["Contrôle", "Tous les 6 000 km et chaque année (" + ref(78) + ")"]]
    h1 = table(c, rows, M, y, [80, hw - 80])
    rows2 = [["Fusible", "Calibre"], ["Principal", "20 A"], ["Autres", "30 A, 15 A, 10 A, 7,5 A"]]
    table(c, rows2, M + hw + 14, y, [80, hw - 80])
    y -= max(h1, 70) + 12
    y -= callout(c, "danger", M, y, CW, "Ordre des bornes", "Débrancher la borne négative (-) en premier, rebrancher la positive (+) en premier "
                 "(règle d'atelier, voir proc_batterie_scooter).") + 10
    y -= section(c, M, y, "Éclairage (" + ref(154) + ")") + 2
    rows3 = [["Feu", "Technologie"], ["Phare", "LED"], ["Feu stop et feu arrière", "LED"], ["Clignotants avant et arrière", "LED"],
             ["Éclairage de plaque", "LED"], ["Feux de position", "LED"]]
    y -= table(c, rows3, M, y, [200, CW - 200]) + 10
    y -= callout(c, "info", M, y, CW, "Batterie et Idling Stop", "Un arrêt prolongé par l'Idling Stop peut décharger la batterie (" + ref(56) + "). "
                 "Moteur qui ne démarre pas en 5 secondes : contact sur Off et 10 secondes d'attente pour laisser remonter la tension (" + ref(59) + ").") + 8
    callout(c, "attention", M, y, CW, "Feu LED défaillant", "Un feu à LED ne se remplace pas comme une ampoule : orienter vers le concessionnaire.")


def p19(c):
    y = TOP
    rows = [["Situation", "Première action", "Voir"],
            ["Voyant PGM-FI allumé moteur tournant", "Éviter les vitesses élevées ; contrôle rapide", "page 8"],
            ["Voyant PGM-FI clignotant", "Se garer, moteur arrêté 10 min ; ensuite 50 km/h max jusqu'au concessionnaire", "page 8"],
            ["Témoin de température allumé", "Arrêt, refroidissement, durites, niveau du vase", "page 15"],
            ["Témoin ABS allumé en roulant", "Freinage sans antiblocage : prudence, contrôle", "page 17"],
            ["Témoin HSTC allumé fixe", "Conduite sans HSTC : prudence, contrôle", "page 11"],
            ["Témoin SMART Key clignote 5 fois", "Remplacer la pile CR2032", "page 9"],
            ["Moteur coupé au feu, témoin Idling Stop clignotant", "Fonctionnement normal", "page 10"],
            ["Moteur coupé en roulant", "Panne : diagnostic", "pages 8, 12"],
            ["Ne démarre pas", "Béquille latérale, Smart Key, batterie, poignée fermée", "page 12"],
            ["Indicateur d'entretien affiché", "Faire l'entretien, puis remise à zéro (INFO A)", "page 13"],
            ["Question sur une SH150i 2018 ou 2005", "Changer de document : manuel_sh150i_2018 ou fiche_entretien_sh150_2005", "page 20"]]
    y -= table(c, rows, M, y, [180, CW - 240, 60]) + 12
    y -= section(c, M, y, "Arbre de lecture (Figure 19.1)") + 4
    fh = 170
    frame(c, M, y, CW, fh, white)

    def node(x, yy, w, h, t, col=white):
        c.setFillColor(col)
        c.setStrokeColor(GREY_D)
        c.setLineWidth(0.8)
        c.roundRect(x, yy - h, w, h, 4, fill=1, stroke=1)
        p = P("<b>%s</b>" % t, "pc")
        p.wrap(w - 6, 100)
        p.drawOn(c, x + 3, yy - h / 2 - p.height / 2)
    yy = y - 16
    node(M + 12, yy - 50, 100, 40, "Un témoin reste allumé ou clignote ?")
    node(M + 150, yy - 50, 80, 40, "Lequel ?")
    arrow(c, M + 112, yy - 70, M + 148, yy - 70, GREY_D, 1)
    node(M + 270, yy - 4, 120, 36, "Rouge (température) : arrêt", RED_L)
    node(M + 270, yy - 48, 120, 36, "Orange (PGM-FI, ABS, HSTC) : contrôle", ORANGE_L)
    node(M + 270, yy - 92, 120, 36, "Vert (Smart Key, Idling Stop) : souvent normal")
    for ty in (yy - 22, yy - 66, yy - 110):
        arrow(c, M + 230, yy - 70, M + 268, ty, GREY_D, 1)
    node(M + 410, yy - 4, CW - 422, 36, "page 15")
    node(M + 410, yy - 48, CW - 422, 36, "pages 8, 11, 17")
    node(M + 410, yy - 92, CW - 422, 36, "pages 9, 10")
    for ty in (yy - 22, yy - 66, yy - 110):
        arrow(c, M + 390, ty, M + 408, ty, GREY_D, 1)
    y -= fh + 4
    caption(c, M, y, CW, "19.1", "lecture des témoins par couleur, puis renvoi vers la bonne page.")


def p20(c):
    y = TOP
    y -= para(c, "Ce document ne couvre que la <b>SH150AD 2020-2024</b>. Les questions ci-dessous servent aux tests de la semaine 5.", M, y, CW) + 8
    rows = [["Question type", "Réponse attendue", "Catégorie de test"],
            ["Pression avant d'une SH150i 2021 avec passager ?", "200 kPa (" + ref(153) + ")", "normal"],
            ["Couple de la vis de vidange d'une SH150i 2021 ?", "24 N·m (" + ref(154) + ")", "normal"],
            ["Bougie d'une SH150i 2021 ?", "NGK LMAR8L-9, écartement 0,8 à 0,9 mm (" + ref(153) + ")", "normal"],
            ["Bougie d'une SH150 de 2005 ?", "NGK CR8EH-9 : autre génération (fiche_entretien_sh150_2005)", "contradictoire"],
            ["Huile pour la vidange d'une SH150i 2018 ?", "Absente du corpus pour 2018 ; ne pas reprendre 0,8 L de la 2021", "contradictoire"],
            ["Comment désactiver le HSTC sur ma 2018 ?", "Pas de HSTC avant 2020 : vérifier le millésime", "ambigu"],
            ["Référence de courroie d'une SH150i ?", "Dépend du marché : fiche_pieces_sh150i_au_id concerne l'Australie et l'Indonésie", "ambigu"],
            ["Couple des axes de roue d'une SH150i 2021 ?", "Absent du manuel du propriétaire : manuel d'atelier", "source absente"],
            ["Code de défaut PGM-FI d'une SH150i 2021 ?", "Aucun code dans le manuel du propriétaire", "source absente"],
            ["[Photo] témoin vert « A » clignotant au feu", "Idling Stop actif : normal (" + ref(55) + ")", "image"]]
    y -= table(c, rows, M, y, [180, CW - 280, 100]) + 10
    y -= callout(c, "attention", M, y, CW, "Ce que ce document ne contient pas", "Codes de défaut chiffrés, couples autres que vidange et remplissage, "
                 "jeu aux soupapes, procédures de démontage : ils relèvent du manuel d'atelier de la génération 2020-2024, absent du corpus.") + 8
    callout(c, "info", M, y, CW, "SH125AD", "Le même manuel couvre la SH125AD (125 cm³, 53,5 x 55,5 mm, 11,5:1). Ce document ne retient que la "
            "SH150AD ; ne pas appliquer ses valeurs moteur à la SH125AD (" + ref(152) + ").")


def p21(c):
    y = TOP
    rows = [["Référence", "Document"],
            ["MP", P("Honda Motor Co., manuel du propriétaire SH125/SH150 21YM, réf. 32K0RA000 (anglais, PDF du 14/01/2020). Document fourni par l'équipe, "
                     "<b>non redistribué</b> et non versé au corpus. Pages imprimées citées : 39 à 41, 55 à 59, 77, 78, 98, 99, 102, 112, 116 à 120, 122, 123, 129, 152 à 154.", "td")]]
    y -= table(c, rows, M, y, [60, CW - 60]) + 12
    y -= section(c, M, y, "Traçabilité") + 2
    rows = [["Élément", "Valeur"], ["Document", "%s, version %s" % (DOC, VERS)], ["Équipement", EQ],
            ["Rédaction", "Équipe MaintiDoc avec assistance IA (Claude Opus 5.5), prompt P15 de prompts_corpus.md"],
            ["Méthode", "Valeurs factuelles relevées et reformulées en français ; aucun texte, tableau ni figure Honda reproduit"],
            ["Illustrations", "Schémas vectoriels originaux de l'équipe (CC BY 4.0)"],
            ["Licence de la fiche", "synthetique ; CC BY 4.0 ; source Honda non redistribuée : choix à valider par l'enseignante"],
            ["Groupes d'accès", "techniciens_moto, responsables"],
            ["Documents liés", "manuel_sh150i_2018, fiche_entretien_sh150_2005, fiche_pieces_sh150i_au_id, codes_temoins_honda, proc_*_scooter"],
            ["Vérification", "À relire par un membre de l'équipe : chaque valeur contre la page MP citée"]]
    table(c, rows, M, y, [120, CW - 120])


PAGES = [p1, p2, p3, p4, p5, p6, p7, p8, p9, p10, p11, p12, p13, p14, p15, p16, p17, p18, p19, p20, p21]

if __name__ == "__main__":
    c = canvas.Canvas(OUT, pagesize=A4)
    c.setTitle("%s - Honda SH150i (SH150AD) 2020-2024 - manuel de synthèse illustré" % DOC)
    c.setAuthor("Équipe MaintiDoc")
    c.setSubject("Synthèse non officielle à partir du manuel du propriétaire Honda 21YM")
    for i, fn in enumerate(PAGES):
        n = i + 1
        page(c, n, dict(TOC)[n] if n > 1 else None, fn)
    c.save()
    print("ok", OUT)
