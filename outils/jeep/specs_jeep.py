# -*- coding: utf-8 -*-
"""Contenu des 20 fiches-problèmes Jeep Wrangler JL 2026 et schémas de l'équipe.
Toutes les valeurs : manuel du propriétaire Jeep Wrangler 2026 (105655_26_JL_OM_EN_USC, E2), page imprimée « OM p. N »."""
import math
from dessin import *  # noqa: F401,F403
from dessin import _rays  # noqa: F401

EQ = "JEEP-WRA-01"
COLM = HexColor("#2f5d3a")


def ref(p):
    return "OM p. %d" % p


# ------------------------------------------------------------------ schémas (c, x, ytop, w, h)
def fig_cluster(states=None, lcd="0 km/h", note=None):
    def f(c, x, ytop, w, h):
        cw = min(w - 40, (h - (26 if note else 14)) * 260 / 110)
        cluster(c, x + (w - cw) / 2, ytop - 8 - cw * 110 / 260, cw, states or {}, lcd)
        if note:
            ptext(c, x + w / 2, ytop - h + 9, note, 7.4, "LSI", GREY_D, "c")
    return f


def fig_jump(c, x, ytop, w, h):
    by = ytop - h / 2 - 20
    for i, (lab, bx) in enumerate((("Véhicule en panne", x + 40), ("Véhicule de secours", x + w - 170))):
        c.setFillColor(DARK)
        c.roundRect(bx, by, 130, 52, 4, fill=1, stroke=0)
        ptext(c, bx + 65, by + 22, lab, 8, "LSB", white, "c")
        c.setFillColor(RED)
        c.rect(bx + 98, by + 52, 16, 8, fill=1, stroke=0)
        ptext(c, bx + 106, by + 64, "+", 11, "LSB", RED, "c")
        if i:
            c.setFillColor(GREY_D)
            c.rect(bx + 16, by + 52, 16, 8, fill=1, stroke=0)
            ptext(c, bx + 24, by + 64, "-", 11, "LSB", GREY_D, "c")
    c.setStrokeColor(RED)
    c.setLineWidth(2)
    c.line(x + 146, by + 60, x + w - 64, by + 60)
    c.setStrokeColor(DARK)
    c.line(x + w - 146, by + 60, x + w - 146, by - 16)
    c.line(x + w - 146, by - 16, x + 60, by - 16)
    c.setFillColor(GREY_M)
    c.rect(x + 50, by - 22, 20, 10, fill=1, stroke=0)
    ptext(c, x + 60, by - 34, "masse moteur", 7, "LSB", DARK, "c")
    for n, (px, py) in enumerate(((x + 146, by + 62), (x + w - 64, by + 62), (x + w - 146, by + 62), (x + 60, by - 10))):
        pic_circle(c, px, py + 10, n + 1)
    ptext(c, x + w / 2, ytop - 12, "Ordre de branchement 1-2-3-4 ; débranchement dans l'ordre inverse", 7.4, "LSI", GREY_D, "c")


def pic_circle(c, x, y, n):
    c.setFillColor(ORANGE)
    c.circle(x, y, 7, fill=1, stroke=0)
    ptext(c, x, y - 3, str(n), 7.5, "LSB", white, "c")


def fig_start(c, x, ytop, w, h):
    cx, cy = x + w * 0.32, ytop - h / 2
    r = min(h / 2 - 16, 46)
    c.setFillColor(HexColor("#2b2e33"))
    c.circle(cx, cy, r, fill=1, stroke=0)
    c.setFillColor(HexColor("#4a4f57"))
    c.circle(cx, cy, r * 0.7, fill=1, stroke=0)
    ptext(c, cx, cy + 4, "START", 8, "LSB", white, "c")
    ptext(c, cx, cy - 8, "STOP", 8, "LSB", white, "c")
    for lab, ang in (("OFF", 150), ("ACC", 90), ("RUN", 30)):
        a = math.radians(ang)
        ptext(c, cx + math.cos(a) * (r + 12), cy + math.sin(a) * (r + 8) - 3, lab, 7.4, "LSB", DARK, "c")
    tx = x + w * 0.58
    for i, t in enumerate(("1. Levier sur P (ou N)", "2. Pied sur le frein", "3. Appui bref sur START", "Démarreur coupé seul après 10 s")):
        ptext(c, tx, ytop - 36 - i * 18, t, 8 if i < 3 else 7.4, "LSB" if i < 3 else "LSI", DARK if i < 3 else GREY_D)


def fig_4x4(c, x, ytop, w, h):
    pos = [("2H", "0 à 72 km/h, à l'arrêt ou en roulant"), ("4H AUTO", "0 à 72 km/h"), ("4H PART TIME", "0 à 72 km/h"),
           ("N", "ne pas s'arrêter sur N"), ("4L", "3 à 5 km/h, boîte auto sur N")]
    gx = x + 70
    top = ytop - 18
    step = (h - 34) / (len(pos) - 1)
    c.setStrokeColor(GREY_D)
    c.setLineWidth(6)
    c.line(gx, top, gx, top - step * (len(pos) - 1))
    for i, (p, t) in enumerate(pos):
        yy = top - i * step
        c.setFillColor(COLOR_4 if p == "4L" else DARK)
        c.circle(gx, yy, 7, fill=1, stroke=0)
        ptext(c, gx - 14, yy - 3, p, 8, "LSB", DARK, "r")
        ptext(c, gx + 16, yy - 3, t, 7.6, "LS", DARK)


COLOR_4 = HexColor("#c0392b")


def fig_tread(c, x, ytop, w, h):
    bx, bw = x + 30, w - 60
    by = ytop - h / 2 - 10
    c.setFillColor(HexColor("#2b2e33"))
    c.rect(bx, by, bw, 34, fill=1, stroke=0)
    c.setFillColor(white)
    for k in range(7):
        c.rect(bx + 10 + k * bw / 7, by + 14, bw / 7 * 0.35, 20, fill=1, stroke=0)
    c.setFillColor(ORANGE)
    c.rect(bx + 10 + 3 * bw / 7 + bw / 7 * 0.35, by + 14, bw / 7 * 0.65 - 10, 5, fill=1, stroke=0)
    ptext(c, bx + 3.5 * bw / 7 + 10, by + 42, "bande d'usure", 7.4, "LSB", ORANGE, "c")
    ptext(c, x + w / 2, by - 16, "Bande visible = profondeur 1,6 mm (1/16 in) : pneu à remplacer", 7.8, "LSB", DARK, "c")


def fig_roue(c, x, ytop, w, h):
    cx, cy = x + w * 0.3, ytop - h / 2
    r = min(h / 2 - 14, 48)
    c.setFillColor(HexColor("#b8bdc4"))
    c.setStrokeColor(DARK)
    c.circle(cx, cy, r, fill=1, stroke=1)
    order = [0, 2, 4, 1, 3]
    for i in range(5):
        a = math.radians(90 + i * 72)
        px, py = cx + math.cos(a) * r * 0.55, cy + math.sin(a) * r * 0.55
        c.setFillColor(DARK)
        c.circle(px, py, 6, fill=1, stroke=0)
        ptext(c, px, py - 2.5, str(order.index(i) + 1), 6.5, "LSB", white, "c")
    tx = x + w * 0.56
    for i, t in enumerate(("Serrage en étoile", "176 N·m (130 ft-lb)", "écrous M14 x 1,50 ; douille 22 mm", "Recontrôler après 40 km")):
        ptext(c, tx, ytop - 34 - i * 18, t, 8 if i < 2 else 7.4, "LSB" if i < 2 else "LS", COLOR_4 if i == 1 else DARK)


def fig_jauge(c, x, ytop, w, h):
    jx, top = x + w * 0.35, ytop - 14
    L = h - 36
    c.setFillColor(HexColor("#e2b100"))
    c.roundRect(jx - 14, top - 12, 28, 12, 4, fill=1, stroke=0)
    c.setFillColor(HexColor("#b8bdc4"))
    c.rect(jx - 3, top - 12 - L, 6, L, fill=1, stroke=0)
    c.setFillColor(HexColor("#c88a1b"))
    c.rect(jx - 3, top - 12 - L, 6, L * 0.30, fill=1, stroke=0)
    for lab, k in (("MAX", 0.58), ("MIN", 0.36)):
        yy = top - 12 - L + L * k
        c.setStrokeColor(DARK)
        c.line(jx - 8, yy, jx + 8, yy)
        ptext(c, jx + 12, yy - 3, lab, 7.6, "LSB", DARK)
    ptext(c, jx + 12, top - 12 - L + L * 0.30 - 10, "niveau sous MIN", 7.4, "LSB", RED)
    ptext(c, x + w * 0.62, ytop - h / 2, "De MIN à MAX : environ 1 L", 8, "LSB", DARK)


def fig_bocal(lab_low="niveau bas", liquide=HexColor("#f4a3c4")):
    def f(c, x, ytop, w, h):
        bw, bh = 70, h - 40
        bx, by = x + w / 2 - bw, ytop - h + 18
        c.setFillColor(white)
        c.setStrokeColor(DARK)
        c.roundRect(bx, by, bw, bh, 8, fill=1, stroke=1)
        c.setFillColor(liquide)
        c.rect(bx + 4, by + 4, bw - 8, bh * 0.22, fill=1, stroke=0)
        for lab, k in (("MAX", 0.72), ("MIN", 0.34)):
            yy = by + bh * k
            c.line(bx - 6, yy, bx + bw + 6, yy)
            ptext(c, bx + bw + 10, yy - 3, lab, 7.6, "LSB", DARK)
        ptext(c, bx + bw + 10, by + bh * 0.12, lab_low, 7.2, "LSB", RED)
    return f


def fig_fusibles(c, x, ytop, w, h):
    fus = [("40 A", "vert", "démarreur F02", HexColor("#4caf50")), ("20 A", "jaune", "pompe à carburant F04", HexColor("#f2c14e")),
           ("15 A", "bleu", "TCM F08", HexColor("#4f86c6")), ("5 A", "beige", "capteur batterie F03", HexColor("#d9c7a3"))]
    fw = 50
    x0 = x + (w - len(fus) * (fw + 30)) / 2 + 15
    yb = ytop - h / 2 - 12
    for i, (a, col, t, rgb) in enumerate(fus):
        fx = x0 + i * (fw + 30)
        c.setFillColor(rgb)
        c.setStrokeColor(DARK)
        c.roundRect(fx, yb, fw, 34, 4, fill=1, stroke=1)
        ptext(c, fx + fw / 2, yb + 13, a, 9, "LSB", DARK, "c")
        ptext(c, fx + fw / 2, yb - 12, t, 6.6, "LS", DARK, "c")
    ptext(c, x + w / 2, ytop - 14, "Exemples du boîtier PDC (moteur essence), OM p. 284", 7.2, "LSI", GREY_D, "c")
    ptext(c, x + w / 2, yb - 30, "Remplacer par le MÊME calibre ; jamais plus fort, jamais de fil métallique", 7.6, "LSB", COLOR_4, "c")


def fig_filtre(c, x, ytop, w, h):
    bx, by = x + w * 0.2, ytop - h + 26
    bw, bh = w * 0.42, h - 56
    c.setFillColor(HexColor("#2b2e33"))
    c.roundRect(bx, by, bw, bh * 0.45, 4, fill=1, stroke=0)
    c.setFillColor(HexColor("#e8e4da"))
    c.rect(bx + 8, by + bh * 0.45, bw - 16, 12, fill=1, stroke=0)
    c.setStrokeColor(GREY_D)
    for k in range(14):
        c.line(bx + 10 + k * (bw - 20) / 14, by + bh * 0.45, bx + 10 + k * (bw - 20) / 14, by + bh * 0.45 + 12)
    c.setFillColor(HexColor("#3a3f47"))
    c.roundRect(bx, by + bh * 0.68, bw, bh * 0.3, 4, fill=1, stroke=0)
    for k in (0.12, 0.88):
        c.setFillColor(ORANGE)
        c.circle(bx + bw * k, by + bh * 0.83, 4, fill=1, stroke=0)
    arrow(c, bx + bw / 2, by + bh * 0.98, bx + bw / 2, by + bh * 0.98 + 18, ORANGE, 1.4)
    tx = bx + bw + 20
    for i, t in enumerate(("1. Desserrer les fixations du couvercle", "2. Soulever le couvercle", "3. Sortir le filtre", "4. Nettoyer le boîtier si sale",
                           "5. Filtre neuf, face d'inspection en bas")):
        ptext(c, tx, ytop - 26 - i * 16, t, 7.4, "LS", DARK)


def fig_intervalles(bars):
    def f(c, x, ytop, w, h):
        maxv = max(v for _, v, _, _ in bars)
        by = ytop - 24
        bwmax = w - 240
        for lbl, v, txt, col in bars:
            ptext(c, x + 10, by - 3, lbl, 7.4, "LSB", DARK)
            c.setFillColor(col)
            c.rect(x + 130, by - 6, bwmax * v / maxv, 11, fill=1, stroke=0)
            ptext(c, x + 136 + bwmax * v / maxv, by - 3, txt, 7.2, "LS", DARK)
            by -= 22
    return f


def fig_tpms(c, x, ytop, w, h):
    cx, cy = x + w * 0.3, ytop - h / 2
    c.setFillColor(GREY_L)
    c.setStrokeColor(DARK)
    c.roundRect(cx - 30, cy - 52, 60, 104, 10, fill=1, stroke=1)
    for i, (dx, dy) in enumerate(((-36, 30), (36, 30), (-36, -30), (36, -30))):
        low = i == 3
        c.setFillColor(HexColor("#e2b100") if low else DARK)
        c.roundRect(cx + dx - 7, cy + dy - 14, 14, 28, 3, fill=1, stroke=0)
        ptext(c, cx + dx + (24 if dx > 0 else -24), cy + dy - 3, "BAS" if low else "OK", 7.4, "LSB", COLOR_4 if low else GREEN, "c")
    tx = x + w * 0.58
    for i, t in enumerate(("Témoin fixe : pression basse", "Clignote ~1 min puis fixe : défaut TPMS", "Pression : étiquette du montant B", "Mesure à froid, chaque mois")):
        ptext(c, tx, ytop - 34 - i * 18, t, 7.8, "LSB" if i < 2 else "LS", DARK)


def fig_frein_reservoir(c, x, ytop, w, h):
    fig_bocal("liquide sous la plage", HexColor("#e9c46a"))(c, x, ytop, w, h)
    ptext(c, x + w / 2, ytop - 12, "réservoir du maître-cylindre (schéma) : repères sur le côté du réservoir", 7, "LSI", GREY_D, "c")


# ------------------------------------------------------------------ les 20 fiches
def F(**k):
    return k


SPECS = [
 F(id="jl_temoin_moteur_mil", titre="Témoin moteur (MIL) allumé", usage="normal", pages="139, 143", photo="jl_temoin_moteur_mil",
   photo_brief="tableau de bord Wrangler avec le témoin moteur orange allumé, moteur tournant.",
   symptome="Moteur tournant, le témoin orange Engine Check / MIL reste allumé, ou clignote.",
   fig=fig_cluster({"moteur": "on"}, "0 km/h"), fig_cap="témoin moteur orange (colonne de gauche) sur un tableau de bord schématique.",
   sens=[["Allumé au contact, avant démarrage", "Contrôle de l'ampoule (normal)", "aucune", ref(139)],
         ["Allumé fixe après démarrage", "Défaut moteur ou antipollution (bouchon d'essence mal serré, carburant de mauvaise qualité...)", "contrôle rapide", ref(139)],
         ["Clignotant moteur tournant", "Risque de perte de puissance ou de dégât grave du catalyseur", "élevée", ref(139)]],
   securite=("danger", "Risque d'incendie", "Un catalyseur défaillant chauffe davantage : ne pas rouler lentement ni stationner au-dessus d'herbe sèche, de bois ou de carton (" + ref(139) + ")."),
   flow=["Contact ON : témoin s'allume ?", "Après démarrage : fixe ou clignotant ?", "Fixe : bouchon d'essence bien serré ?", "Clignotant : atelier au plus vite", "Lecture OBD II"],
   flow_cap="lecture du témoin moteur.",
   steps=["Contact sur ON sans démarrer : le témoin doit s'allumer (contrôle d'ampoule) ; sinon, faire contrôler (" + ref(139) + ").",
          "Démarrer et noter si le témoin reste fixe ou clignote.",
          "Fixe : vérifier que le bouchon de réservoir est bien en place et serré ; noter le dernier plein.",
          "S'il reste allumé sur plusieurs trajets normaux : rendez-vous atelier ; le véhicule roule normalement en général.",
          "Clignotant : réduire la charge et faire réparer au plus vite (" + ref(139) + ").",
          "À l'atelier, lire les codes OBD II avec l'outil de diagnostic et les noter dans le ticket."],
   valeurs=[["Système de surveillance", "OBD II (moteur et transmission automatique)", ref(139)],
            ["Test de disponibilité OBD", "Contact ON sans démarrer ; environ 15 s plus tard, MIL clignotant 10 s = système non prêt", ref(143)]],
   negatif="Juste après un débranchement de batterie, le système OBD II peut être « non prêt » sans aucun défaut (" + ref(143) + ").",
   absent="Signification des codes de défaut : non donnée par le manuel du propriétaire ; voir les fiches codes OBD du corpus atelier.",
   liens="jl_temoin_pression_huile, jl_temoin_temperature_moteur"),
 F(id="jl_temoin_temperature_moteur", titre="Témoin de température moteur allumé (surchauffe)", usage="normal", pages="136, 247, 280, 332", photo="jl_temoin_temperature_moteur",
   photo_brief="aiguille de température vers H et témoin rouge allumé.",
   symptome="Le témoin rouge de température du liquide de refroidissement s'allume avec un carillon ; l'aiguille monte vers H.",
   fig=fig_cluster({"temp": "on"}), fig_cap="témoin rouge de température (colonne de droite, en bas).",
   sens=[["Témoin + un carillon", "Température du liquide trop élevée", "élevée", ref(136)],
         ["Carillon continu (jusqu'à 4 min)", "Limite haute atteinte", "arrêt", ref(136)],
         ["Odeur de liquide, fumée blanche, bulles dans le bocal", "Signes de surchauffe", "arrêt", ref(247)]],
   securite=("danger", "Brûlures graves", "Ne jamais ouvrir le bouchon sous pression moteur chaud ; si de la vapeur sort, ne pas ouvrir le capot avant refroidissement (" + ref(247) + ")."),
   flow=["Témoin allumé", "Se garer, couper la clim", "Boîte sur N, ralenti", "Aiguille redescend ?", "Non : moteur coupé, assistance"], flow_hl=(1, 4),
   flow_cap="conduite à tenir (" + ref(136) + ").",
   steps=["Se garer en sécurité et couper la climatisation.", "Passer la boîte sur NEUTRAL (N) et laisser tourner au ralenti, sans accélérer (" + ref(136) + ").",
          "Si l'aiguille ne revient pas dans la zone normale : couper le moteur immédiatement et appeler l'assistance.",
          "En attendant d'arriver : chauffage au maximum et ventilation forte aident à évacuer la chaleur (" + ref(247) + ").",
          "Moteur froid seulement : contrôler le niveau dans le bocal (fiche jl_niveau_liquide_refroidissement).",
          "Faire contrôler le véhicule chez un concessionnaire : une surchauffe demande une intervention (" + ref(247) + ")."],
   valeurs=[["Capacité circuit 2.0L (bocal au MAX)", "11,4 L", ref(332)], ["Contrôle de la protection antigel", "Tous les 12 mois", ref(278)]],
   negatif="Embouteillage par forte chaleur : l'aiguille peut monter sans panne ; rouler moins vite ou passer au point mort à l'arrêt suffit souvent (" + ref(247) + ").",
   absent="Capacité du circuit 3.6L et température d'ouverture du thermostat : non relevées dans cette fiche.",
   liens="jl_niveau_liquide_refroidissement"),
 F(id="jl_temoin_pression_huile", titre="Témoin de pression d'huile allumé", usage="normal", pages="136, 137, 269, 329, 332", photo="jl_temoin_pression_huile",
   photo_brief="témoin rouge de pression d'huile allumé au tableau de bord.",
   symptome="En roulant, le témoin rouge de pression d'huile s'allume avec un carillon.",
   fig=fig_cluster({"huile": "on"}), fig_cap="témoin rouge de pression d'huile (colonne de droite, en haut).",
   sens=[["Témoin + carillon en roulant", "Pression d'huile basse", "arrêt", ref(136)], ["Témoin éteint après redémarrage", "Rouler possible, atelier rapidement", "contrôle rapide", ref(137)]],
   securite=("danger", "Arrêt du moteur", "S'arrêter en sécurité et couper le moteur dès que possible. Ne pas rouler tant que la cause n'est pas corrigée (" + ref(137) + ")."),
   flow=["Témoin + carillon", "Arrêt, moteur coupé", "Contrôle niveau à la jauge", "Redémarrer : encore allumé ?", "Oui : moteur coupé, atelier"], flow_hl=(1,),
   flow_cap="conduite à tenir (" + ref(136) + "-" + ref(137) + ").",
   steps=["S'arrêter en sécurité et couper le moteur.", "Attendre cinq minutes que l'huile redescende, véhicule à plat (" + ref(269) + ").",
          "Contrôler le niveau à la jauge : le témoin n'indique PAS la quantité d'huile (" + ref(137) + ").",
          "Redémarrer et surveiller le témoin.", "S'il reste allumé : couper le moteur et contacter un concessionnaire ; ne pas rouler.",
          "S'il s'éteint : rouler possible, mais faire contrôler le véhicule au plus vite."],
   fig2=fig_jauge, fig2_cap="jauge d'huile : niveau à maintenir entre MIN et MAX (schéma).", fig2_h=110,
   valeurs=[["Huile 2.0L", "SAE 5W-30 synthétique, API SP / GF-6A (MS-13340)", ref(329)], ["Huile 3.6L", "SAE 0W-20 synthétique (MS-6395)", ref(329)],
            ["Capacité avec filtre 2.0L / 3.6L", "4,73 L", ref(332)], ["De MIN à MAX", "Environ 1 L", ref(269)]],
   negatif="Le témoin de température d'huile (autre pictogramme) signale une huile trop chaude, pas une pression basse (" + ref(137) + ").",
   absent="Pression d'huile chiffrée et seuil d'allumage : non donnés par le manuel du propriétaire.",
   liens="jl_vidange_huile, jl_temoin_moteur_mil"),
 F(id="jl_temoin_charge_batterie", titre="Témoin de charge de la batterie allumé", usage="normal", pages="136", photo="jl_temoin_charge_batterie",
   photo_brief="témoin rouge de batterie allumé, moteur tournant.",
   symptome="Moteur tournant, le témoin rouge de batterie reste allumé.",
   fig=fig_cluster({"batterie": "on"}), fig_cap="témoin rouge de charge (colonne de droite, au milieu).",
   sens=[["Allumé moteur tournant", "La batterie ne se charge pas correctement", "contrôle rapide", ref(136)], ["Allumé + baisse de l'éclairage", "Système de charge défaillant", "élevée", ref(136)]],
   securite=("attention", "Risque de panne", "Sans charge, le véhicule fonctionne sur la batterie jusqu'à décharge : limiter les consommateurs et rejoindre un concessionnaire au plus vite (" + ref(136) + ")."),
   flow=["Témoin allumé moteur tournant", "Couper les consommateurs", "Afficher la tension (menu Batterie)", "Concessionnaire au plus vite", "Test du système de charge"],
   flow_cap="démarche en cas de défaut de charge.",
   steps=["Éteindre les accessoires non indispensables (climatisation, radio, prises 12 V).",
          "Si le tableau de bord le permet, afficher la tension de batterie dans les menus (« Battery Voltage », " + ref(128) + ").",
          "Contrôler visuellement les bornes et les câbles de la batterie, moteur coupé.",
          "Rejoindre un concessionnaire au plus vite pour tester le système de charge (" + ref(136) + ")."],
   valeurs=[["Signification", "Charge de batterie incorrecte", ref(136)], ["Affichage de la tension", "Menu Battery Voltage du combiné", ref(128)]],
   negatif="Un témoin de batterie qui s'allume brièvement au contact, avant démarrage, fait partie du contrôle des témoins.",
   absent="Tension de charge normale et courroie d'alternateur : non chiffrées par le manuel du propriétaire.",
   liens="jl_batterie_dechargee"),
 F(id="jl_batterie_dechargee", titre="Batterie déchargée : démarrage avec câbles", usage="normal", pages="244, 245, 246", photo="jl_batterie_dechargee",
   photo_brief="borne positive (+) de la batterie du Wrangler, capuchon soulevé.",
   symptome="Le moteur ne se lance pas ou le démarreur tourne très lentement ; l'éclairage est faible.",
   fig=fig_jump, fig_cap="ordre de branchement des câbles de démarrage (schéma).",
   sens=[["Démarreur lent ou muet", "Batterie déchargée", "moyenne", ref(244)], ["Démarrages assistés fréquents", "Batterie ou charge à tester", "moyenne", ref(246)]],
   securite=("danger", "Risque d'explosion", "Ne pas démarrer si la batterie est gelée. Source de secours de 12 V maximum. Ne jamais brancher le câble négatif sur la borne (-) de la batterie déchargée (" + ref(244) + "-" + ref(246) + ")."),
   flow=["Frein à main, P, contact OFF", "Accessoires coupés", "Brancher 1-2-3-4", "Démarrer le secours puis le Jeep", "Débrancher 4-3-2-1"],
   flow_cap="démarrage avec câbles (" + ref(245) + "-" + ref(246) + ").",
   steps=["Serrer le frein de stationnement, boîte sur P (manuelle sur N), contact OFF ; couper chauffage, radio et accessoires.",
          "Soulever le capuchon de la borne positive (+) : la batterie est à l'arrière droit du compartiment moteur (" + ref(245) + ").",
          "Brancher : (+) Jeep, puis (+) secours, puis (-) secours, puis masse métallique du moteur loin de la batterie (" + ref(246) + ").",
          "Démarrer le véhicule de secours, laisser tourner quelques minutes, puis démarrer le Jeep ; ne pas dépasser 2 000 tr/min sur le véhicule de secours.",
          "Débrancher dans l'ordre inverse et remettre le capuchon de la borne (+).",
          "Véhicule avec Stop/Start : n'utiliser que la borne (+) de la batterie principale (" + ref(245) + ")."],
   valeurs=[["Tension de la source de secours", "12 V maximum", ref(244)], ["Régime maximal du véhicule de secours", "2 000 tr/min", ref(246)],
            ["Emplacement batterie", "Arrière droit du compartiment moteur", ref(245)]],
   negatif="Avec Stop/Start, il existe une seconde batterie : ne jamais l'utiliser pour le démarrage assisté (" + ref(245) + ").",
   absent="Capacité (Ah) et référence de la batterie : non données par le manuel du propriétaire.",
   liens="jl_temoin_charge_batterie, jl_moteur_ne_demarre_pas"),
 F(id="jl_moteur_ne_demarre_pas", titre="Le moteur ne démarre pas (bouton Start)", usage="ambigu", pages="158, 160, 161", photo="jl_moteur_ne_demarre_pas",
   photo_brief="bouton START/STOP du Wrangler avec les positions OFF, ACC, RUN.",
   symptome="Appui sur START : le moteur ne démarre pas, ou le démarreur tourne sans que le moteur prenne.",
   fig=fig_start, fig_cap="procédure normale de démarrage (schéma).",
   sens=[["Pas de démarrage, pied pas sur le frein", "Le bouton passe seulement en ACC / RUN", "aucune", ref(158)],
         ["Démarreur tourne, moteur ne prend pas", "Moteur peut-être noyé", "moyenne", ref(160)], ["Démarreur lent", "Batterie faible : autre fiche", "moyenne", ref(160)]],
   securite=("attention", "Protéger le démarreur", "Ne pas lancer plus de 10 à 15 secondes d'affilée ; attendre 10 à 15 secondes avant un nouvel essai (" + ref(161) + ")."),
   flow=["Levier sur P ou N ?", "Pied sur le frein ?", "Appui bref sur START", "Moteur noyé ? accélérateur à fond", "Batterie : fiche démarrage assisté"],
   flow_cap="vérifications avant de conclure à une panne.",
   steps=["Placer la boîte sur PARK ou NEUTRAL.", "Appuyer sur la pédale de frein et la maintenir, puis appuyer une fois sur START (" + ref(158) + ").",
          "Sans démarrage, le démarreur se coupe seul après 10 secondes.",
          "Moteur peut-être noyé : accélérateur enfoncé à fond et maintenu, lancer 10 à 15 s au plus, relâcher l'accélérateur et refaire la procédure normale (" + ref(160) + ").",
          "Véhicule immobilisé plus de 30 jours : brancher un chargeur ou des câbles avant de lancer ; après 8 essais, laisser refroidir le démarreur au moins 10 min.",
          "Démarreur lent : passer à la fiche jl_batterie_dechargee."],
   valeurs=[["Coupure automatique du démarreur", "10 secondes", ref(158)], ["Durée max. d'un lancement", "10 à 15 secondes", ref(161)],
            ["Immobilisation prolongée", "Au moins 30 jours ; refroidir 10 min après 8 essais", ref(160)]],
   negatif="Cas ambigu : « il ne démarre pas » peut venir du pied absent du frein, de la batterie ou d'une clé non détectée. L'assistant doit demander ce qui se passe à l'appui sur START.",
   absent="Méthode de secours en cas de pile de clé vide pour la version essence : non relevée dans cette fiche.",
   liens="jl_batterie_dechargee"),
 F(id="jl_temoin_frein", titre="Témoin de frein rouge allumé", usage="normal", pages="135, 281, 331", photo="jl_temoin_frein",
   photo_brief="témoin rouge BRAKE allumé au tableau de bord.",
   symptome="Le témoin rouge BRAKE reste allumé, frein de stationnement desserré.",
   fig=fig_cluster(None, "BRAKE", "témoin rouge BRAKE affiché (schéma)"), fig_cap="message de frein sur l'écran du tableau de bord (schéma).",
   sens=[["Allumé, frein de stationnement serré", "Normal", "aucune", ref(135)], ["Allumé, frein desserré", "Niveau de liquide bas ou défaut hydraulique / assistance", "arrêt", ref(135)],
         ["Allumé avec le témoin ABS", "Défaut de répartition électronique (EBD)", "arrêt", ref(135)]],
   securite=("danger", "Freinage dégradé", "Rouler avec le témoin rouge allumé est dangereux : une partie du freinage peut être défaillante et la distance d'arrêt plus longue. Faire contrôler immédiatement (" + ref(135) + ")."),
   flow=["Témoin rouge allumé", "Frein de stationnement desserré ?", "Niveau du liquide de frein", "Témoin ABS aussi ?", "Réparation immédiate"], flow_hl=(4,),
   flow_cap="diagnostic du témoin de frein.",
   steps=["Vérifier que le frein de stationnement est complètement desserré.", "Contrôler le niveau du maître-cylindre (fiche jl_niveau_liquide_frein) (" + ref(281) + ").",
          "Si le niveau est correct et le témoin allumé : défaut hydraulique ou d'assistance possible (" + ref(135) + ").",
          "Si le témoin ABS est aussi allumé : réparation immédiate (EBD).", "Contrôle de l'ampoule : contact sur ON, le témoin s'allume environ 2 secondes."],
   valeurs=[["Contrôle d'ampoule", "Environ 2 secondes au contact", ref(135)], ["Liquide de frein", "Mopar DOT 3, SAE J1703", ref(331)]],
   negatif="Le témoin peut clignoter brièvement en virage serré : le niveau varie, faire contrôler le niveau (" + ref(135) + ").",
   absent="Épaisseur minimale des plaquettes et des disques : manuel d'atelier, absent du corpus.",
   liens="jl_niveau_liquide_frein, jl_temoin_abs"),
 F(id="jl_temoin_abs", titre="Témoin ABS allumé", usage="normal", pages="138", photo="jl_temoin_abs",
   photo_brief="témoin jaune ABS allumé au tableau de bord.",
   symptome="Le témoin jaune ABS reste allumé ou s'allume en roulant.",
   fig=fig_cluster({"abs": "on"}), fig_cap="témoin ABS orange (colonne de gauche, au milieu).",
   sens=[["Allumé au contact jusqu'à 4 s", "Contrôle normal", "aucune", ref(138)], ["Reste allumé en roulant", "Antiblocage inactif ; freinage classique conservé", "contrôle rapide", ref(138)],
         ["Ne s'allume pas au contact", "Témoin ou système à contrôler", "contrôle rapide", ref(138)]],
   securite=("attention", "Sans antiblocage", "Le freinage classique fonctionne si le témoin rouge de frein est éteint, mais les roues peuvent se bloquer : allonger les distances (" + ref(138) + ")."),
   flow=["Témoin ABS allumé", "Témoin de frein rouge aussi ?", "Oui : fiche témoin de frein", "Non : freinage classique OK", "Atelier au plus vite"],
   flow_cap="lecture du témoin ABS.",
   steps=["Vérifier qu'il s'allume au contact puis s'éteint en moins de 4 secondes (" + ref(138) + ").",
          "S'il reste allumé : vérifier si le témoin rouge de frein est aussi allumé.",
          "Rouge éteint : rouler prudemment, freinage classique disponible ; prendre rendez-vous au plus vite.",
          "Rouge allumé : traiter comme un défaut de freinage (fiche jl_temoin_frein)."],
   valeurs=[["Durée de l'autotest", "Jusqu'à 4 secondes", ref(138)], ["Si allumé", "Partie antiblocage inactive", ref(138)]],
   negatif="Un témoin ABS seul ne signifie pas une perte de freinage : c'est le témoin rouge qui signale un défaut du freinage principal.",
   absent="Contrôle des capteurs de roue : manuel d'atelier, absent du corpus.",
   liens="jl_temoin_frein, jl_temoin_esc"),
 F(id="jl_temoin_tpms", titre="Témoin de pression des pneus (TPMS) allumé", usage="normal", pages="140, 306, 310", photo="jl_temoin_tpms",
   photo_brief="témoin TPMS et écran de pression des quatre pneus.",
   symptome="Le témoin jaune TPMS s'allume et l'écran indique un ou plusieurs pneus en pression basse.",
   fig=fig_tpms, fig_cap="lecture du TPMS (schéma).",
   sens=[["Témoin fixe + message", "Pression sous la valeur recommandée ou fuite lente", "contrôle rapide", ref(140)],
         ["Clignote ~1 min puis fixe", "Défaut du système TPMS", "moyenne", ref(140)], ["Pneu à plat", "Ne pas continuer à rouler", "arrêt", ref(140)]],
   securite=("attention", "Pneu à plat", "Ne pas continuer à rouler avec un pneu à plat ; s'arrêter sans freinage ni coup de volant brusques (" + ref(140) + ")."),
   flow=["Témoin TPMS", "Fixe ou clignotant ?", "Fixe : mesure à froid", "Gonfler à la valeur du montant B", "Clignotant : capteur à contrôler"],
   flow_cap="diagnostic TPMS.",
   steps=["S'arrêter dès que possible et regarder quel pneu est signalé.", "Mesurer la pression à froid avec un manomètre (pas à l'œil) (" + ref(310) + ").",
          "Gonfler à la valeur de l'étiquette du montant B côté conducteur ou du chant de porte.",
          "Remettre le bouchon de valve.", "Si le témoin clignote environ une minute puis reste fixe : défaut TPMS, faire contrôler les capteurs (" + ref(140) + ")."],
   valeurs=[["Pression recommandée", "Étiquette du montant B côté conducteur", ref(310)], ["Pneu « froid »", "Non roulé depuis 3 h, ou moins de 1,6 km", ref(306)],
            ["Contrôle", "Chaque mois, roue de secours comprise", ref(140)]],
   negatif="Après un produit anticrevaison du commerce, le capteur peut ne plus fonctionner : le témoin peut rester allumé même pneu regonflé (" + ref(140) + ").",
   absent="Valeurs de pression chiffrées : elles dépendent de la monte et figurent sur l'étiquette du véhicule.",
   liens="jl_crevaison_roue_secours, jl_usure_pneus"),
 F(id="jl_crevaison_roue_secours", titre="Crevaison : pose de la roue de secours", usage="normal", pages="241, 242, 244, 333", photo="jl_crevaison_roue_secours",
   photo_brief="dépose de la roue de secours montée sur le hayon du Wrangler.",
   symptome="Un pneu est crevé ou à plat ; il faut monter la roue de secours.",
   fig=fig_roue, fig_cap="ordre de serrage des écrous et couple (schéma).",
   sens=[["Pneu à plat", "Remplacer la roue avant de rouler", "arrêt", ref(140)]],
   securite=("danger", "Véhicule sur cric", "Ne jamais démarrer le moteur ni passer sous le véhicule sur cric ; personne à bord ; cric seulement aux points prévus (" + ref(242) + ")."),
   flow=["Feux de détresse, P, frein", "Caler la roue opposée", "Sortir la roue de secours", "Lever et changer", "Couple 176 N·m"], flow_cap="changement de roue.",
   steps=["Se garer sur sol plat et ferme, feux de détresse, boîte sur P, frein de stationnement serré.",
          "Caler la roue diagonalement opposée.", "Déposer la roue de secours du hayon (" + ref(242) + ").",
          "Desserrer légèrement les écrous avant de lever, puis lever avec le cric aux points indiqués.",
          "Monter la roue et serrer les écrous en étoile au couple de 176 N·m (" + ref(333) + ").",
          "Après 40 km, recontrôler le serrage à la clé dynamométrique (" + ref(244) + ")."],
   valeurs=[["Couple des écrous", "176 N·m (130 ft-lb)", ref(333)], ["Écrous ; douille", "M14 x 1,50 ; 22 mm", ref(333)], ["Recontrôle", "Après 40 km (25 miles)", ref(244)]],
   negatif="Ne pas confondre avec une pression simplement basse signalée par le TPMS : regonfler suffit alors (fiche jl_temoin_tpms).",
   absent="Couple des écrous de la roue de secours : tableau séparé (" + ref(333) + "), à relever.",
   liens="jl_temoin_tpms, jl_usure_pneus"),
 F(id="jl_usure_pneus", titre="Pneus usés (témoins d'usure visibles)", usage="normal", pages="255, 311, 312", photo="jl_usure_pneus",
   photo_brief="bande de roulement d'un pneu du Wrangler avec les témoins d'usure.",
   symptome="Les témoins d'usure apparaissent en bandes sur la bande de roulement, ou l'usure est irrégulière.",
   fig=fig_tread, fig_cap="témoin d'usure atteint (schéma).",
   sens=[["Bande d'usure visible", "Profondeur 1,6 mm : remplacer le pneu", "élevée", ref(311)], ["Usure irrégulière", "Pression ou permutation à revoir", "moyenne", ref(255)]],
   securite=("danger", "Adhérence", "Un pneu usé jusqu'aux témoins doit être remplacé : adhérence réduite, surtout sur sol mouillé (" + ref(311) + ")."),
   flow=["Inspection visuelle", "Témoins visibles ?", "Oui : remplacement", "Usure irrégulière ?", "Permutation, pression"], flow_cap="contrôle d'usure.",
   steps=["Inspecter chaque pneu : témoins d'usure, coupures, hernies.", "Remplacer tout pneu dont la bande atteint les témoins (" + ref(311) + ").",
          "En 4x4, garder des pneus de même taille, type et circonférence sur les quatre roues (" + ref(176) + ").",
          "Permuter les pneus à chaque vidange, ou dès la première usure irrégulière (" + ref(255) + ").", "Régler la pression à froid après intervention."],
   valeurs=[["Profondeur aux témoins", "1,6 mm (1/16 in)", ref(311)], ["Permutation", "À chaque vidange indiquée par le système", ref(255)]],
   negatif="Pneus de tailles différentes : cela perturbe aussi les passages 4x4 et peut endommager la transmission (" + ref(176) + ").",
   absent="Durée de vie en kilomètres : elle dépend de la conduite, le manuel n'en donne pas.",
   liens="jl_temoin_tpms, jl_4x4_ne_s_engage_pas"),
 F(id="jl_vidange_huile", titre="Message « Oil Change Required » (vidange due)", usage="normal", pages="128, 131, 255, 329, 332", photo="jl_vidange_huile",
   photo_brief="compartiment moteur 3.6L : jauge et bouchon de remplissage d'huile.",
   symptome="Le message « Oil Change Required » s'affiche 5 secondes après un carillon à chaque mise du contact.",
   fig=fig_intervalles([("Vidange : maximum", 16000, "16 000 km / 12 mois / 350 h moteur", COLM), ("Filtre à air : remplacement", 48000, "48 000 km", ORANGE)]),
   fig_cap="limites d'intervalle (" + ref(255) + ", " + ref(256) + ").", fig_h=90,
   sens=[["Message affiché", "Vidange et filtre à faire", "faible", ref(131)]],
   securite=("info", "Bon à savoir", "L'intervalle varie avec la conduite (système basé sur le cycle d'utilisation) ; ne jamais dépasser les limites maximales (" + ref(255) + ")."),
   flow=["Message affiché", "Vidange + filtre", "Contrôles associés", "Remise à zéro Oil Life", "Contrôle du message"], flow_cap="traitement de l'échéance.",
   steps=["Vidanger et remplacer le filtre à huile avec l'huile préconisée pour le moteur (2.0L ou 3.6L).",
          "Au même passage : permuter les pneus, contrôler la batterie, les plaquettes et disques, le circuit de refroidissement, l'échappement (" + ref(255) + ").",
          "Remise à zéro : contact sur ON sans appuyer sur le frein, menu « Oil Life », maintenir OK jusqu'à 100 % (" + ref(128) + ", " + ref(131) + ").",
          "Couper puis remettre le contact : le message ne doit plus apparaître."],
   valeurs=[["Intervalle maximal", "16 000 km (10 000 miles), 12 mois ou 350 h moteur", ref(255)], ["Huile 2.0L ; 3.6L", "SAE 5W-30 ; SAE 0W-20, synthétiques", ref(329)],
            ["Capacité avec filtre", "4,73 L (2.0L et 3.6L)", ref(332)], ["Masquer temporairement", "Appui bref sur OK", ref(131)]],
   negatif="Le message peut apparaître avant 16 000 km : c'est normal, l'intervalle dépend de l'usage.",
   absent="Couple de la vis de vidange et référence du filtre : non donnés par le manuel du propriétaire.",
   liens="jl_temoin_pression_huile, jl_filtre_air"),
 F(id="jl_filtre_air", titre="Filtre à air moteur encrassé", usage="normal", pages="255, 256, 270", photo="jl_filtre_air",
   photo_brief="couvercle du filtre à air ouvert, filtre visible.",
   symptome="Usage poussiéreux ou tout-terrain : perte de reprise, filtre visiblement sale à l'inspection.",
   fig=fig_filtre, fig_cap="dépose et pose du filtre à air (schéma).",
   sens=[["Filtre sale", "Admission d'air réduite", "moyenne", ref(270)], ["Usage poussiéreux / tout-terrain", "Inspecter à chaque vidange", "faible", ref(255)]],
   securite=("attention", "Système d'admission", "Ne pas démarrer avec le système d'admission déposé si quelqu'un est près du compartiment moteur (" + ref(270) + ")."),
   flow=["Usage poussiéreux ?", "Inspection à la vidange", "Filtre sale ?", "Remplacement Mopar", "Couvercle verrouillé"], flow_cap="contrôle du filtre à air.",
   steps=["Moteur coupé, ouvrir le capot.", "Desserrer les fixations du couvercle et le soulever (" + ref(270) + ").",
          "Sortir le filtre ; nettoyer le boîtier s'il contient beaucoup de saletés.", "Poser un filtre neuf, face d'inspection vers le bas.", "Refermer et serrer les fixations du couvercle."],
   valeurs=[["Remplacement", "Tous les 48 000 km (30 000 miles)", ref(256)], ["Usage poussiéreux / tout-terrain", "Inspecter à chaque vidange", ref(255)],
            ["Qualité", "Filtres Mopar de qualité recommandés", ref(270)]],
   negatif="Une perte de puissance avec le témoin moteur allumé relève d'abord de la fiche jl_temoin_moteur_mil.",
   absent="Référence du filtre : catalogue de pièces, absent du corpus.",
   liens="jl_vidange_huile"),
 F(id="jl_niveau_liquide_refroidissement", titre="Niveau de liquide de refroidissement bas", usage="normal", pages="278, 280, 281, 332", photo="jl_niveau_liquide_refroidissement",
   photo_brief="bocal de liquide de refroidissement, moteur froid, repères visibles.",
   symptome="Au contrôle mensuel, le niveau du bocal est sous la plage indiquée.",
   fig=fig_bocal("sous la plage du bocal"), fig_cap="bocal de liquide de refroidissement (schéma).",
   sens=[["Niveau sous la plage", "Appoint et recherche de fuite", "moyenne", ref(280)], ["Liquide sale ou rouillé", "Vidange, rinçage, remplissage OAT", "moyenne", ref(278)]],
   securite=("danger", "Moteur froid uniquement", "Ne jamais ouvrir le bouchon sous pression moteur chaud et ne pas ajouter de liquide sur un moteur en surchauffe (" + ref(279) + ")."),
   flow=["Moteur froid, OFF", "Lire le niveau du bocal", "Sous la plage ?", "Appoint OAT", "Rechercher une fuite"], flow_cap="contrôle du niveau.",
   steps=["Moteur coupé et froid.", "Lire le niveau dans le bocal : il doit être dans la plage indiquée (" + ref(280) + ").",
          "Ne pas ouvrir le bouchon du radiateur : il reste normalement plein.", "Compléter avec du liquide OAT conforme (MS-90032).",
          "Si le niveau baisse souvent, rechercher une fuite et ouvrir un ticket."],
   valeurs=[["Capacité 2.0L (bocal au MAX)", "11,4 L", ref(332)], ["Type de liquide", "OAT (MS-90032)", ref(278)], ["Contrôle", "Niveau une fois par mois ; protection tous les 12 mois", ref(280) + " ; " + ref(278)]],
   negatif="Le circuit de l'intercooler (2.0L) a son propre bocal : ne pas le confondre avec celui du moteur (photo, repère 10).",
   absent="Point de congélation et proportion de mélange : non relevés dans cette fiche.",
   liens="jl_temoin_temperature_moteur"),
 F(id="jl_fusible_grille", titre="Un équipement électrique ne fonctionne plus (fusible)", usage="normal", pages="283, 284", photo="jl_fusible_grille",
   photo_brief="boîtier de distribution PDC dans le compartiment moteur, couvercle ouvert.",
   symptome="Un équipement électrique s'arrête d'un coup alors que le reste fonctionne.",
   fig=fig_fusibles, fig_cap="calibres et couleurs de quelques fusibles (schéma).", fig_h=120,
   sens=[["Fusible au filament coupé", "Surcharge ou court-circuit", "moyenne", ref(283)], ["Grille de nouveau", "Défaut du circuit à corriger", "élevée", ref(283)]],
   securite=("danger", "Même calibre", "Toujours le même calibre ; jamais plus fort, jamais de fil métallique : risque d'incendie (" + ref(283) + ")."),
   flow=["Équipement en panne", "Contact OFF", "Couvercle du PDC", "Contrôler le fusible", "Grille encore : atelier"], flow_cap="contrôle d'un fusible.",
   steps=["Couper le contact et tous les consommateurs.", "Ouvrir le PDC, près de la batterie ; le couvercle indique l'emplacement, la fonction et le calibre de chaque fusible (" + ref(283) + ").",
          "Contrôler le fusible du circuit et le remplacer par le même calibre.", "Bien remettre et verrouiller le couvercle (risque d'infiltration d'eau).",
          "Si le fusible grille de nouveau : concessionnaire."],
   valeurs=[["F02 (démarreur)", "40 A, vert", ref(284)], ["F04 (pompe à carburant)", "20 A, jaune", ref(284)], ["F03 (capteur de batterie IBS)", "5 A, beige", ref(284)]],
   negatif="Un fusible de sécurité (airbag, freinage) qui grille demande un contrôle atelier, pas un simple remplacement (" + ref(283) + ").",
   absent="Liste complète des fusibles de l'habitacle : à relever dans le manuel (" + ref(284) + " et suivantes).",
   liens="jl_temoin_charge_batterie"),
 F(id="jl_temoin_esc", titre="Témoin ESC allumé en continu", usage="normal", pages="138", photo="jl_temoin_esc",
   photo_brief="témoin ESC (voiture qui dérape) allumé au tableau de bord.",
   symptome="Le témoin ESC reste allumé en continu moteur tournant, même sur route sèche.",
   fig=fig_cluster(None, "ESC", "témoin ESC (schéma)"), fig_cap="indication ESC sur l'écran (schéma).",
   sens=[["Clignote en virage ou sur sol glissant", "ESC en action : normal", "aucune", ref(138)], ["Allumé en continu moteur tournant", "Défaut ESC détecté", "contrôle rapide", ref(138)],
         ["Témoin ESC OFF", "ESC désactivé ; il se réactive à chaque contact", "aucune", ref(138)]],
   securite=("attention", "Conduite sans aide", "En cas de défaut, la stabilité électronique peut ne plus aider en cas de perte d'adhérence : adapter la vitesse."),
   flow=["Témoin ESC allumé", "Clignote ou fixe ?", "Fixe : plusieurs démarrages", "Rouler > 48 km/h quelques km", "Toujours allumé : atelier"], flow_cap="lecture du témoin ESC.",
   steps=["Vérifier s'il clignote (ESC actif, normal) ou s'il reste fixe.", "Le témoin s'allume au contact et doit s'éteindre moteur tournant (" + ref(138) + ").",
          "Fixe : couper et remettre le contact plusieurs fois et rouler quelques kilomètres au-dessus de 48 km/h.",
          "S'il reste allumé après cela : concessionnaire au plus vite.", "Bourdonnements ou cliquetis quand l'ESC agit : normaux."],
   valeurs=[["Vitesse d'essai", "Plus de 48 km/h (30 mph)", ref(138)], ["ESC OFF", "Revient sur ON à chaque mise du contact", ref(138)]],
   negatif="Le témoin qui clignote en tout-terrain ou sur sol glissant n'est pas une panne : l'ESC travaille.",
   absent="Diagnostic des capteurs (angle volant, lacet) : manuel d'atelier, absent du corpus.",
   liens="jl_temoin_abs"),
 F(id="jl_4x4_ne_s_engage_pas", titre="Le 4x4 (4L) ne s'engage pas", usage="normal", pages="139, 175, 176, 177", photo="jl_4x4_ne_s_engage_pas",
   photo_brief="levier de boîte de transfert du Wrangler sur la console.",
   symptome="Le levier de boîte de transfert est difficile à passer en 4L, ou le passage ne se termine pas.",
   fig=fig_4x4, fig_cap="positions de la boîte de transfert à 5 positions et conditions de passage.",
   sens=[["Passage 4L difficile à l'arrêt", "Dents non alignées (normal)", "faible", ref(177)], ["Témoin Service 4WD", "Défaut du système 4x4", "élevée", ref(139)],
         ["Passage incomplet", "Risque de perte de motricité et de contrôle", "arrêt", ref(177)]],
   securite=("danger", "Passage complet obligatoire", "Ne pas rouler tant que la boîte de transfert n'est pas complètement engagée : risque de perte de puissance et de contrôle (" + ref(177) + ")."),
   flow=["Rouler à 3-5 km/h", "Boîte auto sur N", "Levier franchement en 4L", "Pas de pause sur N", "Boîte sur D"], flow_cap="passage en 4L (" + ref(176) + "-" + ref(177) + ").",
   steps=["Rouler à 3 à 5 km/h (2 à 3 mph).", "Boîte automatique sur NEUTRAL (N), ou embrayage enfoncé en boîte manuelle (" + ref(176) + ").",
          "Pousser le levier de transfert franchement jusqu'à 4L, sans s'arrêter sur N.", "Remettre la boîte sur DRIVE ou relâcher l'embrayage.",
          "À l'arrêt complet, plusieurs essais peuvent être nécessaires (" + ref(177) + ").", "Témoin Service 4WD allumé : atelier au plus vite (" + ref(139) + ")."],
   valeurs=[["Vitesse de passage 4L", "3 à 5 km/h", ref(177)], ["Passage 2H / 4H", "0 à 72 km/h, à l'arrêt ou en roulant", ref(175)],
            ["Régime en 4L", "Environ 3 fois celui de 4H AUTO à même vitesse", ref(176)]],
   negatif="Effort de passage plus grand par temps froid, ou passages retardés avec des pneus usés ou mal gonflés : pas forcément une panne (" + ref(176) + ").",
   absent="Huile de boîte de transfert et contrôle du moteur de commande : manuel d'atelier, absent du corpus.",
   liens="jl_usure_pneus"),
 F(id="jl_temoin_airbag", titre="Témoin d'airbag allumé", usage="normal", pages="135", photo="jl_temoin_airbag",
   photo_brief="témoin rouge d'airbag allumé au tableau de bord.",
   symptome="Le témoin rouge d'airbag reste allumé, ou ne s'allume pas au contact.",
   fig=fig_cluster(None, "AIRBAG", "témoin d'airbag (schéma)"), fig_cap="indication d'airbag sur l'écran (schéma).",
   sens=[["Allumé 4 à 8 s au contact", "Contrôle normal", "aucune", ref(135)], ["Allumé + carillon", "Défaut d'airbag détecté", "élevée", ref(135)],
         ["Ne s'allume pas au démarrage", "Témoin ou système à contrôler", "élevée", ref(135)]],
   securite=("danger", "Système de retenue", "Avec ce témoin allumé, l'airbag peut ne pas fonctionner en cas de choc. Ne pas intervenir soi-même sur le système : concessionnaire au plus vite (" + ref(135) + ")."),
   flow=["Contact ON", "Allumé 4-8 s puis éteint ?", "Reste allumé ou carillon ?", "Ne pas toucher au système", "Concessionnaire"], flow_cap="lecture du témoin d'airbag.",
   steps=["Mettre le contact : le témoin doit s'allumer 4 à 8 secondes puis s'éteindre (" + ref(135) + ").",
          "S'il reste allumé, s'allume en roulant, ou ne s'allume pas : faire inspecter le système au plus vite.",
          "Ne pas débrancher de connecteur ni intervenir sous les sièges ou dans le volant.", "Noter l'apparition du témoin dans le ticket."],
   valeurs=[["Autotest", "4 à 8 secondes", ref(135)], ["Défaut", "Témoin + un carillon, reste allumé jusqu'à correction", ref(135)]],
   negatif="Ne pas confondre avec le témoin de ceinture, qui signale une ceinture non bouclée.",
   absent="Diagnostic du calculateur d'airbag : réservé au concessionnaire.",
   liens="jl_fusible_grille"),
 F(id="jl_temoin_temperature_transmission", titre="Témoin de température de transmission allumé", usage="normal", pages="137, 138", photo="jl_temoin_temperature_transmission",
   photo_brief="témoin de température de transmission allumé, par exemple en traction de remorque.",
   symptome="Le témoin de température de transmission s'allume, souvent en traction de remorque ou en usage difficile.",
   fig=fig_cluster(None, "TRANS", "témoin de température de transmission (schéma)"), fig_cap="indication sur l'écran (schéma).",
   sens=[["Témoin allumé", "Liquide de transmission trop chaud", "arrêt", ref(137)], ["Message « CLUTCH HOT » (boîte manuelle)", "Embrayage trop chaud", "arrêt", ref(138)]],
   securite=("danger", "Risque d'incendie", "Continuer à rouler peut faire bouillir le liquide, qui peut toucher l'échappement chaud et prendre feu (" + ref(137) + "-" + ref(138) + ")."),
   flow=["Témoin allumé", "S'arrêter", "P ou N, ralenti", "Attendre l'extinction", "Reprendre normalement"], flow_hl=(1,), flow_cap="conduite à tenir (" + ref(137) + ").",
   steps=["S'arrêter dès que possible.", "Boîte sur PARK (P) ou NEUTRAL (N), moteur au ralenti ou un peu au-dessus.",
          "Attendre que le témoin s'éteigne.", "Reprendre la route normalement ; réduire la charge si possible.",
          "Si le témoin revient souvent : ticket atelier pour contrôle de la transmission."],
   valeurs=[["Conduite à tenir", "Arrêt, P ou N, ralenti jusqu'à extinction", ref(137)], ["Risque", "Dégât grave ou panne de transmission", ref(138)]],
   negatif="Ce témoin ne concerne pas le moteur : le témoin de température du liquide de refroidissement est différent.",
   absent="Niveau et type de liquide de transmission : manuel d'atelier, absent du corpus.",
   liens="jl_temoin_temperature_moteur"),
 F(id="jl_niveau_liquide_frein", titre="Niveau de liquide de frein bas", usage="normal", pages="255, 281, 331", photo="jl_niveau_liquide_frein",
   photo_brief="réservoir du maître-cylindre de frein, repères de niveau visibles.",
   symptome="Le niveau du réservoir de liquide de frein est sous les repères, parfois avec le témoin rouge allumé.",
   fig=fig_frein_reservoir, fig_cap="réservoir du maître-cylindre (schéma).",
   sens=[["Niveau sous les repères", "Usure des plaquettes ou fuite", "élevée", ref(281)], ["Témoin de frein allumé", "Contrôle immédiat", "arrêt", ref(281)]],
   securite=("danger", "Liquide adapté", "Utiliser uniquement le liquide préconisé, neuf ou issu d'un récipient fermé : un mauvais liquide peut endommager gravement le freinage (" + ref(281) + ")."),
   flow=["Nettoyer le dessus du réservoir", "Lire le niveau", "Sous les repères ?", "Appoint DOT 3", "Rechercher une fuite"], flow_cap="contrôle du niveau (" + ref(281) + ").",
   steps=["Contrôler le niveau à chaque entretien, ou immédiatement si le témoin de frein est allumé.", "Nettoyer le dessus du maître-cylindre avant d'ouvrir le bouchon.",
          "Compléter jusqu'aux repères sur le côté du réservoir.", "Le niveau baisse normalement avec l'usure des plaquettes ; contrôler après leur remplacement.",
          "Niveau anormalement bas : rechercher une fuite (" + ref(281) + ")."],
   valeurs=[["Liquide", "Mopar DOT 3, SAE J1703", ref(331)], ["Contrôle", "À chaque entretien ; une fois par mois", ref(255)]],
   negatif="Un niveau qui baisse lentement suit l'usure des plaquettes ; une baisse rapide signale une fuite.",
   absent="Purge du circuit et intervalle de remplacement du liquide : non relevés dans cette fiche.",
   liens="jl_temoin_frein"),
]
