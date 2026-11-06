# -*- coding: utf-8 -*-
"""20 fiches-problèmes Jeep Wrangler JL 2026, 2 pages chacune, un seul problème par fiche.

Valeurs relevées dans le manuel du propriétaire Jeep Wrangler 2026 (105655_26_JL_OM_EN_USC, E2), page imprimée citée
(« OM p. N »). Rédaction et schémas originaux de l'équipe ; image réelle : extrait cité du manuel.
Photos réelles : déposer <cle>.jpg (ou .png) dans PHOTOS_DIR et une ligne dans PHOTOS_DIR/credits.csv
(cle,auteur,licence,url) ; sans photo, la fiche affiche un emplacement « photo réelle à ajouter ».

Usage : python build_sh150_20.py <dossier_sortie> [dossier_photos]
"""
import csv
import io
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from reportlab.lib.utils import ImageReader  # noqa: E402
from reportlab.pdfgen import canvas  # noqa: E402
from dessin import *  # noqa: E402,F401,F403
from dessin import _rays  # noqa: E402,F401
from build_manuel_2021 import pic  # noqa: E402

OUTDIR = sys.argv[1] if len(sys.argv) > 1 else "documents/famille_1"
PHOTOS_DIR = sys.argv[2] if len(sys.argv) > 2 else "images"
CREDITS_CSV = sys.argv[3] if len(sys.argv) > 3 else "outils/photos_sources.csv"
MODEL = "Jeep Wrangler JL 2026 (2.0L / 3.6L)"
EQ = "JEEP-WRA-01"
VERS = "1.0 (2026-11)"
COLM = HexColor("#2f5d3a")
BOTTOM = 48


def ref(p):
    return "OM p. %d" % p


def load_credits():
    cr = {}
    if os.path.exists(CREDITS_CSV):
        for r in csv.DictReader(open(CREDITS_CSV, encoding="utf-8")):
            if r.get("auteur"):
                cr[r["document_id"]] = r
    return cr


CREDITS = load_credits()


def photo_file(key):
    for ext in (".jpg", ".jpeg", ".png"):
        p = os.path.join(PHOTOS_DIR, key + ext)
        if os.path.exists(p) and key in CREDITS:
            return p
    return None


# ------------------------------------------------------------------ figures (c, x, ytop, w, h)
def fig_panel(states, lcd="12 458 km"):
    def f(c, x, ytop, w, h):
        pw = min(w - 20, (h - 16) * 300 / 120)
        panel(c, x + (w - pw) / 2, ytop - h + (h - pw * 120 / 300) / 2, pw, states, lcd)
    return f


def fig_jauge(c, x, ytop, w, h):
    jx, top = x + w * 0.35, ytop - 14
    L = h - 36
    c.setFillColor(DARK)
    c.roundRect(jx - 12, top - 14, 24, 14, 3, fill=1, stroke=0)
    c.setFillColor(HexColor("#b8bdc4"))
    c.rect(jx - 3, top - 14 - L, 6, L, fill=1, stroke=0)
    c.setFillColor(HexColor("#c88a1b"))
    c.rect(jx - 3, top - 14 - L, 6, L * 0.30, fill=1, stroke=0)
    for lab, k in (("repère haut", 0.58), ("repère bas", 0.36)):
        yy = top - 14 - L + L * k
        c.setStrokeColor(DARK)
        c.setLineWidth(1)
        c.line(jx - 8, yy, jx + 8, yy)
        ptext(c, jx + 12, yy - 3, lab, 7.4, "LSB", DARK)
    ptext(c, jx + 12, top - 14 - L + L * 0.30 - 10, "niveau trop bas", 7.4, "LSB", RED)


def fig_vase(c, x, ytop, w, h):
    bw, bh = 66, h - 40
    bx, by = x + w / 2 - bw, ytop - h + 18
    c.setFillColor(white)
    c.setStrokeColor(DARK)
    c.setLineWidth(1)
    c.roundRect(bx, by, bw, bh, 8, fill=1, stroke=1)
    c.setFillColor(HexColor("#9fd0a8"))
    c.rect(bx + 4, by + 4, bw - 8, bh * 0.22, fill=1, stroke=0)
    for lab, k in (("UPPER", 0.72), ("LOWER", 0.32)):
        yy = by + bh * k
        c.setStrokeColor(DARK)
        c.line(bx - 6, yy, bx + bw + 6, yy)
        ptext(c, bx + bw + 10, yy - 3, lab, 7.6, "LSB", DARK)
    ptext(c, bx + bw + 10, by + bh * 0.12, "niveau sous LOWER", 7.2, "LSB", RED)


def fig_bougie(c, x, ytop, w, h):
    bx, top = x + w * 0.3, ytop - 12
    c.setFillColor(white)
    c.setStrokeColor(DARK)
    c.setLineWidth(0.8)
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
    c.line(bx - 7, top - 112, bx - 7, top - 128)
    c.line(bx - 7, top - 128, bx + 4, top - 128)
    ptext(c, bx + 22, top - 126, "écartement 0,8 à 0,9 mm", 7.4, "LSB", COLM)
    ptext(c, bx + 22, top - 40, "NGK LMAR8L-9", 7.4, "LSB", DARK)


def fig_smartkey(c, x, ytop, w, h):
    kx, ky = x + w * 0.25, ytop - h / 2
    c.setFillColor(DARK)
    c.roundRect(kx - 18, ky - 28, 36, 56, 9, fill=1, stroke=0)
    c.setFillColor(HexColor("#5a6069"))
    c.circle(kx, ky + 8, 7, fill=1, stroke=0)
    ptext(c, kx, ky - 42, "pile CR2032", 7.2, "LSB", DARK, "c")
    for r in (34, 48, 62):
        c.setStrokeColor(GREEN)
        c.setLineWidth(1)
        c.arc(kx + 10 - r, ky - r, kx + 10 + r, ky + r, -35, 70)
    cx = x + w * 0.72
    c.setFillColor(GREY_L)
    c.setStrokeColor(GREY_D)
    c.circle(cx, ky, 30, fill=1, stroke=1)
    c.setFillColor(DARK)
    c.circle(cx, ky, 18, fill=1, stroke=0)
    pic(c, "smartkey", cx, ky, 16, GREEN)
    _rays(c, cx, ky, 11, GREEN)
    for lbl, ang in (("Lock", 150), ("Off", 110), ("On", 50), ("SEAT FUEL", 0)):
        a = math.radians(ang)
        ptext(c, cx + math.cos(a) * 48, ky + math.sin(a) * 42 - 3, lbl, 6.8, "LSB", DARK, "c")


def fig_scooter(*keys):
    def f(c, x, ytop, w, h):
        sw = min(w - 30, (h - 16) * 300 / 175)
        ox, oy = x + (w - sw) / 2, ytop - h + 12
        pos = scooter(c, ox, oy, sw)
        for i, k in enumerate(keys):
            px, py = pos[k]
            c.setStrokeColor(RED)
            c.setLineWidth(1.6)
            c.circle(px, py, 9, fill=0, stroke=1)
            leader(c, px, py, px + (24 if i % 2 == 0 else -24), py + 22, i + 1)
    return f


def fig_pneu(c, x, ytop, w, h):
    bw = w - 40
    bx, by = x + 20, ytop - h / 2 - 14
    c.setFillColor(HexColor("#2b2e33"))
    c.rect(bx, by, bw, 36, fill=1, stroke=0)
    c.setFillColor(white)
    n = 6
    step = bw / n
    for k in range(n):
        c.rect(bx + 8 + k * step, by + 16, step * 0.35, 20, fill=1, stroke=0)
    c.setFillColor(ORANGE)
    c.rect(bx + 8 + 2 * step + step * 0.35, by + 16, step * 0.65 - 8, 6, fill=1, stroke=0)
    ptext(c, bx + 2.5 * step + 8, by + 44, "témoin d'usure", 7.4, "LSB", ORANGE, "c")
    ptext(c, bx + bw / 2, by - 14, "Profondeur minimale : AV 1,5 mm ; AR 2,0 mm", 7.6, "LSB", DARK, "c")


def fig_manometre(c, x, ytop, w, h):
    for i, (lab, val) in enumerate((("Avant", "200 kPa"), ("Arrière", "225 kPa"))):
        cx = x + w * (0.28 + 0.44 * i)
        cy = ytop - h / 2 + 6
        r = min(h / 2 - 22, 40)
        c.setFillColor(white)
        c.setStrokeColor(DARK)
        c.setLineWidth(1.4)
        c.circle(cx, cy, r, fill=1, stroke=1)
        for k in range(9):
            a = math.radians(210 - k * 30)
            c.setLineWidth(0.8)
            c.line(cx + math.cos(a) * r * 0.78, cy + math.sin(a) * r * 0.78, cx + math.cos(a) * r * 0.92, cy + math.sin(a) * r * 0.92)
        a = math.radians(210 - (5.5 if i else 4.8) * 30)
        c.setStrokeColor(RED)
        c.setLineWidth(1.6)
        c.line(cx, cy, cx + math.cos(a) * r * 0.7, cy + math.sin(a) * r * 0.7)
        ptext(c, cx, cy - r - 12, "%s : %s" % (lab, val), 7.8, "LSB", DARK, "c")
    ptext(c, x + w / 2, ytop - 12, "pression à froid, pilote seul ou avec passager", 7, "LSI", GREY_D, "c")


def fig_batterie(c, x, ytop, w, h):
    bw, bh = 96, 64
    bx, by = x + 16, ytop - h / 2 - bh / 2
    c.setFillColor(DARK)
    c.roundRect(bx, by, bw, bh, 4, fill=1, stroke=0)
    for k, (sx, lab, col) in enumerate(((bx + 22, "-", GREY_D), (bx + bw - 22, "+", RED))):
        c.setFillColor(col)
        c.rect(sx - 8, by + bh, 16, 9, fill=1, stroke=0)
        ptext(c, sx, by + bh + 14, lab, 12, "LSB", col, "c")
    ptext(c, bx + bw / 2, by + bh / 2 + 2, "YTZ8V", 11, "LSB", white, "c")
    ptext(c, bx + bw / 2, by + bh / 2 - 12, "12 V - 7,0 Ah", 7.6, "LS", white, "c")
    tx = bx + bw + 14
    ptext(c, tx, by + bh - 6, "Débrancher : (-) en premier", 7, "LSB", DARK)
    ptext(c, tx, by + bh - 19, "Rebrancher : (+) en premier", 7, "LSB", DARK)
    ptext(c, tx, by + 10, "Démarreur : 5 s maximum,", 7, "LS", DARK)
    ptext(c, tx, by - 2, "puis Off et 10 s d'attente", 7, "LS", DARK)


def fig_fusibles(c, x, ytop, w, h):
    fus = [("20 A", "principal"), ("30 A", ""), ("15 A", ""), ("10 A", ""), ("7,5 A", "")]
    fw = 42
    x0 = x + (w - len(fus) * (fw + 12)) / 2
    yb = ytop - h / 2 - 20
    for i, (a, t) in enumerate(fus):
        fx = x0 + i * (fw + 12)
        c.setFillColor(HexColor("#f2c14e") if i == 0 else HexColor("#d9dde3"))
        c.setStrokeColor(DARK)
        c.roundRect(fx, yb, fw, 40, 4, fill=1, stroke=1)
        c.setFillColor(GREY_D)
        c.rect(fx + 8, yb - 10, 6, 10, fill=1, stroke=0)
        c.rect(fx + fw - 14, yb - 10, 6, 10, fill=1, stroke=0)
        ptext(c, fx + fw / 2, yb + 16, a, 9, "LSB", DARK, "c")
        if t:
            ptext(c, fx + fw / 2, yb + 48, t, 7, "LSB", DARK, "c")
    ptext(c, x + w / 2, yb - 26, "Fusible grillé : filament coupé. Remplacer par le même calibre, jamais plus fort.", 7.2, "LSI", GREY_D, "c")


def fig_plaquettes(c, x, ytop, w, h):
    cx, cy = x + w * 0.3, ytop - h / 2
    c.setFillColor(HexColor("#b8bdc4"))
    c.setStrokeColor(DARK)
    c.circle(cx, cy, 44, fill=1, stroke=1)
    c.setFillColor(GREY_L)
    c.circle(cx, cy, 16, fill=1, stroke=1)
    c.setFillColor(DARK)
    c.roundRect(cx + 26, cy - 22, 30, 44, 5, fill=1, stroke=0)
    tx = x + w * 0.58
    for i, (lab, th, col) in enumerate((("plaquette correcte", 10, GREEN), ("plaquette usée", 3, RED))):
        yy = cy + 16 - i * 40
        c.setFillColor(GREY_D)
        c.rect(tx, yy, 60, 6, fill=1, stroke=0)
        c.setFillColor(col)
        c.rect(tx, yy - th, 60, th, fill=1, stroke=0)
        ptext(c, tx + 68, yy - 4, lab, 7.4, "LSB", col)


def fig_reservoir_frein(c, x, ytop, w, h):
    bw, bh = 90, h - 50
    bx, by = x + w / 2 - bw / 2 - 30, ytop - h + 22
    c.setFillColor(HexColor("#d9dde3"))
    c.setStrokeColor(DARK)
    c.roundRect(bx, by, bw, bh, 6, fill=1, stroke=1)
    c.setFillColor(white)
    c.rect(bx + 30, by + 8, 30, bh - 16, fill=1, stroke=1)
    c.setFillColor(HexColor("#e9c46a"))
    c.rect(bx + 31, by + 9, 28, (bh - 18) * 0.25, fill=1, stroke=0)
    c.setStrokeColor(DARK)
    c.line(bx + 26, by + 8 + (bh - 16) * 0.4, bx + 64, by + 8 + (bh - 16) * 0.4)
    ptext(c, bx + bw + 10, by + 8 + (bh - 16) * 0.4 - 3, "repère LOWER", 7.4, "LSB", DARK)
    ptext(c, bx + bw + 10, by + 12, "liquide sous le repère", 7.4, "LSB", RED)
    ptext(c, bx + bw / 2, by + bh + 8, "réservoir au guidon (schéma)", 7, "LSI", GREY_D, "c")


def fig_lcd_entretien(c, x, ytop, w, h):
    lw, lh = 200, 74
    lx, ly = x + (w - lw) / 2, ytop - h / 2 - lh / 2
    c.setFillColor(DARK)
    c.roundRect(lx - 8, ly - 8, lw + 16, lh + 16, 8, fill=1, stroke=0)
    c.setFillColor(HexColor("#b9c7b0"))
    c.roundRect(lx, ly, lw, lh, 4, fill=1, stroke=0)
    icon(c, "cle", lx + 30, ly + lh / 2, 22, DARK)
    ptext(c, lx + 60, ly + lh / 2 + 6, "ENTRETIEN", 11, "LSB", DARK)
    ptext(c, lx + 60, ly + lh / 2 - 10, "dans 0 km", 9, "LS", DARK)
    ptext(c, x + w / 2, ly - 22, "Affichage schématique : indicateur d'entretien et distance restante", 7, "LSI", GREY_D, "c")


def fig_intervalles(bars):
    def f(c, x, ytop, w, h):
        maxv = max(v for _, v, _ in bars)
        by = ytop - 22
        bwmax = w - 190
        for lbl, v, col in bars:
            ptext(c, x + 10, by - 3, lbl, 7.2, "LSB", DARK)
            c.setFillColor(col)
            c.rect(x + 110, by - 6, bwmax * v / maxv, 11, fill=1, stroke=0)
            ptext(c, x + 114 + bwmax * v / maxv, by - 3, "%s km" % format(v, ",").replace(",", " "), 7, "LS", DARK)
            by -= 20
    return f


def fig_idling(c, x, ytop, w, h):
    labels = [("prêt", "on"), ("arrêt au feu", "blink"), ("redémarrage", "on")]
    bw = (w - 60) / 3
    for i, (t, st) in enumerate(labels):
        bx = x + 20 + i * (bw + 10)
        c.setFillColor(DARK)
        c.roundRect(bx + bw / 2 - 22, ytop - h / 2 - 8, 44, 40, 6, fill=1, stroke=0)
        pic(c, "idling", bx + bw / 2, ytop - h / 2 + 12, 22, GREEN)
        if st == "blink":
            _rays(c, bx + bw / 2, ytop - h / 2 + 12, 14, GREEN)
        ptext(c, bx + bw / 2, ytop - h / 2 - 22, t, 7.6, "LSB", DARK, "c")
        ptext(c, bx + bw / 2, ytop - h / 2 - 34, "témoin " + ("clignotant" if st == "blink" else "allumé"), 7, "LS", GREY_D, "c")
        if i < 2:
            arrow(c, bx + bw - 6, ytop - h / 2 + 12, bx + bw + 14, ytop - h / 2 + 12, ORANGE, 1.2)


# ------------------------------------------------------------------ mise en page
class Doc:
    def __init__(self, c, spec, n, total):
        self.c, self.s, self.n, self.total = c, spec, n, total
        self.page = 0
        self.fig = 0
        self.y = 0

    def header(self):
        c = self.c
        c.setFillColor(DARK)
        c.rect(0, H - 24, W, 24, fill=1, stroke=0)
        c.setFillColor(ORANGE)
        c.rect(0, H - 26, W, 2, fill=1, stroke=0)
        ptext(c, M, H - 16, "MaintiDoc  |  %s" % self.s["id"], 8.5, "LSB", white)
        ptext(c, W - M, H - 16, "%s  |  %s  |  fiche-problème %02d/20" % (MODEL, EQ, self.n), 6.8, "LS", white, "r")
        if self.page == 1:
            c.setFillColor(COLM)
            c.roundRect(M, H - 62, 78, 18, 3, fill=1, stroke=0)
            ptext(c, M + 39, H - 56, "PROBLÈME %02d" % self.n, 8, "LSB", white, "c")
            ptext(c, M + 88, H - 58, self.s["titre"], 13.5, "LSB", DARK)
            ptext(c, M, H - 80, "Un seul problème par fiche. Valeurs : manuel du propriétaire Jeep Wrangler 2026, page citée (OM p. N).", 7.4, "LSI", GREY_D)
            c.setStrokeColor(GREY_M)
            c.setLineWidth(0.6)
            c.line(M, H - 88, W - M, H - 88)
            self.y = H - 98
        else:
            ptext(c, M, H - 46, "%s (suite)" % self.s["titre"], 10.5, "LSB", DARK)
            c.setStrokeColor(GREY_M)
            c.line(M, H - 54, W - M, H - 54)
            self.y = H - 64

    def footer(self):
        c = self.c
        c.setStrokeColor(GREY_M)
        c.setLineWidth(0.5)
        c.line(M, 36, W - M, 36)
        ptext(c, M, 27, "%s  |  version %s  |  OM p. N = manuel du propriétaire Jeep Wrangler 2026 (105655_26_JL_OM_EN_USC, E2), page imprimée N" % (self.s["id"], VERS),
              6.2, "LS", GREY_D)
        ptext(c, W - M, 27, "Page %d / %s" % (self.page, self.total), 7, "LSB", DARK, "r")
        ptext(c, W / 2, 16, "Synthèse rédigée par l'équipe MaintiDoc avec assistance IA. Non affiliée à Jeep / Stellantis ; le manuel Jeep fait foi.", 5.8, "LSI", GREY, "c")

    def new_page(self):
        if self.page:
            self.footer()
            self.c.showPage()
        self.page += 1
        self.header()

    def measure(self, fn):
        scratch = canvas.Canvas(io.BytesIO(), pagesize=A4)
        return fn(scratch, H - 100)

    def put(self, fn, gap=8, keep=0):
        h = self.measure(fn)
        if self.y - h - keep < BOTTOM:
            self.new_page()
        used = fn(self.c, self.y)
        self.y -= used + gap

    def photo(self, key, brief, cap, fh=230):
        self.fig += 1
        num = self.fig
        f = photo_file(key)
        if f:
            cr = CREDITS[key]
            cap = cap + " Source : %s, %s. Licence : %s." % (cr["auteur"], cr["url"], cr["licence"])
            from PIL import Image as _I
            iw, ih = _I.open(f).size
            fh = min(fh, (CW - 12) * ih / iw + 12, 112 if iw / ih > 2 else fh)

        def fn(c, y):
            photo_slot(c, M, y, CW, fh, key, brief)
            return fh + 4 + caption(c, M, y - fh - 4, CW, str(num), cap)
        self.put(fn)

    def figure(self, draw, cap, fh=150, photo=None):
        self.fig += 1
        num = self.fig

        def fn(c, y):
            if photo:
                hw = (CW - 12) / 2
                frame(c, M, y, hw, fh, white)
                draw(c, M, y, hw, fh)
                photo_slot(c, M + hw + 12, y, hw, fh, *photo)
            else:
                frame(c, M, y, CW, fh, white)
                draw(c, M, y, CW, fh)
            return fh + 4 + caption(c, M, y - fh - 4, CW, str(num), cap)
        self.put(fn)

    def section(self, t):
        self.put(lambda c, y: section(c, M, y, t), gap=4, keep=60)


def photo_slot(c, x, ytop, w, h, key, brief):
    f = photo_file(key)
    if f:
        img = ImageReader(f)
        iw, ih = img.getSize()
        sc = min((w - 12) / iw, (h - 12) / ih)
        dw, dh = iw * sc, ih * sc
        frame(c, x, ytop, w, h, GREY_L)
        c.drawImage(img, x + (w - dw) / 2, ytop - h + (h - dh) / 2, dw, dh)
        return
    c.setFillColor(GREY_L)
    c.setStrokeColor(ORANGE)
    c.setDash(4, 3)
    c.roundRect(x, ytop - h, w, h, 3, fill=1, stroke=1)
    c.setDash()
    cx, cy = x + w / 2, ytop - h / 2 + 22
    c.setFillColor(GREY_D)
    c.roundRect(cx - 20, cy - 13, 40, 26, 4, fill=1, stroke=0)
    c.setFillColor(GREY_L)
    c.circle(cx, cy, 8, fill=1, stroke=0)
    c.setFillColor(GREY_D)
    c.rect(cx - 8, cy + 13, 14, 5, fill=1, stroke=0)
    ptext(c, cx, cy - 28, "PHOTO RÉELLE À AJOUTER", 8, "LSB", ORANGE, "c")
    para(c, "<b>À photographier :</b> " + brief + "<br/>Fichier : <b>%s.jpg</b> (photo de l'équipe ou Wikimedia Commons, licence notée)." % key,
         x + 10, cy - 36, w - 20, "pxs")


def card(title, text, col=ORANGE):
    def fn(c, y):
        p = P(text, "ps")
        _, ph = p.wrap(CW - 30, 1000)
        h = ph + 30
        c.setFillColor(white)
        c.setStrokeColor(GREY_M)
        c.rect(M, y - h, CW, h, fill=1, stroke=1)
        c.setFillColor(col)
        c.rect(M, y - h, 4, h, fill=1, stroke=0)
        ptext(c, M + 14, y - 14, title, 8.6, "LSB", col)
        p.drawOn(c, M + 14, y - 20 - ph)
        return h
    return fn


def build(spec, n, path):
    for total in ("?", None):
        buf = io.BytesIO() if total == "?" else path
        c = canvas.Canvas(buf, pagesize=A4)
        c.setTitle("%s - %s" % (spec["id"], spec["titre"]))
        c.setAuthor("Équipe MaintiDoc")
        c.setSubject("Fiche-problème Jeep Wrangler JL 2026, synthèse non officielle")
        d = Doc(c, spec, n, total if total else str(pages))
        d.new_page()
        grav = [r[2] for r in spec["sens"]]
        order = ["aucune", "faible", "moyenne", "contrôle rapide", "élevée", "arrêt"]
        g = max(grav, key=lambda v: order.index(v) if v in order else 0)
        d.put(lambda c, y: table(c, [["Famille", "voiture (4x4)", "Équipement", "Jeep Wrangler JL 2026 (%s)" % EQ],
                                     ["Problème", spec["titre"], "Gravité maximale", g]], M, y, [70, CW / 2 - 70, 90, CW / 2 - 90], head=False))
        d.put(card("Symptôme signalé", spec["symptome"], COLM))
        d.photo(spec["id"], spec["photo_brief"], "photo réelle : " + spec["photo_desc"] + ".")
        d.figure(spec["fig"], "schéma de l'équipe : " + spec["fig_cap"], spec.get("fig_h", 130))
        d.section("Signification et gravité")
        d.put(lambda c, y: table(c, [["Constat", "Signification", "Gravité", "Source"]] + spec["sens"], M, y, [130, CW - 260, 70, 60]))
        sk, st, stx = spec["securite"]
        d.put(lambda c, y: callout(c, sk, M, y, CW, st, stx))
        d.section("Diagnostic pas à pas")
        d.put(lambda c, y: flow(c, spec["flow"], M, y, CW, 38, hl=spec.get("flow_hl", (0,))) + 4
              + caption(c, M, y - 42, CW, str(d.fig + 1), spec["flow_cap"]), gap=10)
        d.fig += 1
        d.section("Procédure")
        d.put(lambda c, y: steps(c, spec["steps"], M, y, CW, gap=4, st="ps"))
        if spec.get("fig2"):
            d.figure(spec["fig2"], spec["fig2_cap"], spec.get("fig2_h", 120))
        d.section("Valeurs de référence (Wrangler JL 2026)")
        d.put(lambda c, y: table(c, [["Élément", "Valeur", "Source"]] + spec["valeurs"], M, y, [170, CW - 240, 70]))
        if spec.get("negatif"):
            d.put(lambda c, y: callout(c, "attention", M, y, CW, "Négatif difficile (ne pas confondre)", spec["negatif"]))
        d.put(lambda c, y: callout(c, "info", M, y, CW, "Ce que cette fiche ne contient pas", spec["absent"]))
        d.section("Sources et traçabilité")
        d.put(lambda c, y: table(c, [["Élément", "Valeur"],
                                      ["Source", "Manuel du propriétaire Jeep Wrangler 2026, réf. 105655_26_JL_OM_EN_USC (E2), pages imprimées " + spec["pages"]
                                       + ". Fourni par l'équipe (publication FCA US LLC), non versé au corpus."],
                                      ["Rédaction", "Équipe MaintiDoc avec assistance IA (Claude Opus 5.5), prompt P16 ; schémas originaux CC BY 4.0"],
                                      ["Fiches liées", spec["liens"]],
                                      ["Vérification", "À relire par un membre de l'équipe : chaque valeur contre la page OM citée"]], M, y, [90, CW - 90]))
        d.footer()
        c.save()
        if total == "?":
            pages = d.page
    return pages


from specs_jeep import SPECS  # noqa: E402


def main():
    os.makedirs(OUTDIR, exist_ok=True)
    assert len(SPECS) == 20 and len({s["id"] for s in SPECS}) == 20
    for i, s in enumerate(SPECS):
        n = build(s, i + 1, os.path.join(OUTDIR, s["id"] + ".pdf"))
        print("%-42s %d pages" % (s["id"], n))


if __name__ == "__main__":
    main()
