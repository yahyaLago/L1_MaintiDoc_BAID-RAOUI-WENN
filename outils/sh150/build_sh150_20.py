# -*- coding: utf-8 -*-
"""20 fiches-problèmes Honda SH150i (SH150AD, 2020-2024), 2 à 3 pages chacune, un seul problème par fiche.

Valeurs relevées dans le manuel du propriétaire Honda SH125/SH150 21YM (réf. 32K0RA000), page imprimée citée
(« MP p. N »). Aucun texte ni figure Honda reproduit : rédaction et schémas originaux de l'équipe.
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
from build_manuel_2021 import pic, panel  # noqa: E402

OUTDIR = sys.argv[1] if len(sys.argv) > 1 else "documents/famille_1"
PHOTOS_DIR = sys.argv[2] if len(sys.argv) > 2 else "images"
CREDITS_CSV = sys.argv[3] if len(sys.argv) > 3 else "outils/photos_sources.csv"
MODEL = "Honda SH150i (SH150AD) 2020-2024"
EQ = "SH150-21-01"
VERS = "1.0 (2026-11)"
COLM = HexColor("#c8102e")
BOTTOM = 48


def ref(p):
    return "MP p. %d" % p


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
            ptext(c, M, H - 80, "Un seul problème par fiche. Valeurs : manuel du propriétaire Honda 21YM, page citée (MP p. N).", 7.4, "LSI", GREY_D)
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
        ptext(c, M, 27, "%s  |  version %s  |  MP p. N = manuel du propriétaire Honda SH125/SH150 21YM (réf. 32K0RA000), page imprimée N" % (self.s["id"], VERS),
              6.2, "LS", GREY_D)
        ptext(c, W - M, 27, "Page %d / %s" % (self.page, self.total), 7, "LSB", DARK, "r")
        ptext(c, W / 2, 16, "Synthèse rédigée par l'équipe MaintiDoc avec assistance IA. Non affiliée à Honda ; le manuel Honda fait foi.", 5.8, "LSI", GREY, "c")

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
            fh = min(fh, (CW - 12) * ih / iw + 12)

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
        c.setSubject("Fiche-problème Honda SH150i 2020-2024, synthèse non officielle")
        d = Doc(c, spec, n, total if total else str(pages))
        d.new_page()
        grav = [r[2] for r in spec["sens"]]
        order = ["aucune", "faible", "moyenne", "contrôle rapide", "élevée", "arrêt"]
        g = max(grav, key=lambda v: order.index(v) if v in order else 0)
        d.put(lambda c, y: table(c, [["Famille", "deux_roues (moto)", "Équipement", "Honda SH150i SH150AD (%s)" % EQ],
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
        d.section("Valeurs de référence (SH150AD 2020-2024)")
        d.put(lambda c, y: table(c, [["Élément", "Valeur", "Source"]] + spec["valeurs"], M, y, [170, CW - 240, 70]))
        if spec.get("negatif"):
            d.put(lambda c, y: callout(c, "attention", M, y, CW, "Négatif difficile (ne pas confondre)", spec["negatif"]))
        d.put(lambda c, y: callout(c, "info", M, y, CW, "Ce que cette fiche ne contient pas", spec["absent"]))
        d.section("Sources et traçabilité")
        d.put(lambda c, y: table(c, [["Élément", "Valeur"],
                                      ["Source", "Manuel du propriétaire Honda SH125/SH150 21YM, réf. 32K0RA000, pages imprimées " + spec["pages"]
                                       + ". Fourni par l'équipe, non redistribué, non versé au corpus."],
                                      ["Rédaction", "Équipe MaintiDoc avec assistance IA (Claude Opus 5.5), prompt P16 ; schémas originaux CC BY 4.0"],
                                      ["Fiches liées", spec["liens"]],
                                      ["Vérification", "À relire par un membre de l'équipe : chaque valeur contre la page MP citée"]], M, y, [90, CW - 90]))
        d.footer()
        c.save()
        if total == "?":
            pages = d.page
    return pages


# ------------------------------------------------------------------ les 20 fiches
SPECS = [
 dict(id="sh150_voyant_injection_allume", titre="Voyant d'injection PGM-FI allumé fixe", usage="normal", pages="40, 117",
      symptome="Moteur tournant, le voyant orange d'injection PGM-FI (MIL) reste allumé fixe. Le scooter roule, parfois sans différence ressentie.",
      fig=fig_panel({"moteur": "on"}), fig_cap="voyant PGM-FI allumé fixe (repère 1 de la disposition schématique de l'équipe).",
      photo="sh150_tableau_voyant_injection", photo_brief="tableau de bord d'une SH150i 2020+, moteur tournant, voyant PGM-FI allumé ; plaque floutée.",
      sens=[["Allumé 1 à 2 s au contact puis éteint", "Contrôle normal des témoins", "aucune", ref(40)],
            ["Allumé fixe moteur tournant", "Problème du système antipollution du moteur", "contrôle rapide", ref(117)],
            ["Clignotant", "Ratés d'allumage : autre fiche", "élevée", ref(117)]],
      securite=("attention", "Conduite à tenir", "Éviter les vitesses élevées et faire contrôler rapidement le scooter chez le concessionnaire (" + ref(117) + ")."),
      flow=["Contact sur On : voyant s'allume puis s'éteint ?", "Moteur tournant : allumé fixe ?", "Clignote ? voir sh150_voyant_injection_clignote",
            "Rouler modérément", "Diagnostic concessionnaire"], flow_cap="lecture du voyant PGM-FI.",
      steps=["Noter le kilométrage et les conditions d'apparition (démarrage à froid, après un plein, en charge).",
             "Couper puis remettre le contact : vérifier que le voyant s'allume brièvement puis s'éteint (" + ref(40) + ").",
             "Moteur tournant, observer si le voyant reste fixe ou clignote : le clignotement relève d'une autre fiche.",
             "Fixe : rouler sans vitesse élevée jusqu'au diagnostic (" + ref(117) + ").",
             "Consigner l'intervention dans l'historique de l'équipement " + EQ + "."],
      valeurs=[["Couleur du voyant", "Orange", ref(40)], ["Comportement normal", "S'allume au contact puis s'éteint", ref(40)],
               ["Allumé moteur tournant", "Éviter les vitesses élevées ; contrôle rapide", ref(117)]],
      negatif="Un voyant allumé seulement 1 à 2 secondes au contact est un autotest, pas une panne.",
      absent="Aucun code de défaut chiffré : le manuel du propriétaire 2020-2024 n'en donne pas. La lecture des codes relève du manuel d'atelier, absent du corpus.",
      liens="sh150_voyant_injection_clignote, sh150_perte_puissance"),
 dict(id="sh150_voyant_injection_clignote", titre="Voyant d'injection PGM-FI clignotant", usage="normal", pages="40, 117",
      symptome="Le voyant orange d'injection PGM-FI clignote moteur tournant ; le moteur peut tourner irrégulièrement.",
      fig=fig_panel({"moteur": "blink"}), fig_cap="voyant PGM-FI clignotant (rayons = clignotement).",
      photo="sh150_tableau_voyant_injection_clignotant", photo_brief="vidéo ou photo du voyant PGM-FI en train de clignoter (capture d'écran acceptée).",
      sens=[["Clignotant moteur tournant", "Ratés d'allumage détectés", "élevée", ref(117)],
            ["Clignote encore après 10 min d'arrêt", "Défaut persistant", "élevée", ref(117)]],
      securite=("danger", "Risque d'incendie", "Se garer loin de toute matière inflammable et arrêter le moteur au moins 10 minutes (" + ref(117) + ")."),
      flow=["Voyant clignote", "Se garer loin de matières inflammables", "Moteur arrêté 10 min", "Redémarrer : clignote encore ?", "Oui : 50 km/h max jusqu'au concessionnaire"],
      flow_hl=(1, 2), flow_cap="conduite à tenir en cas de clignotement (" + ref(117) + ").",
      steps=["S'arrêter dès que possible dans un lieu sûr, à l'écart de tout matériau inflammable.",
             "Couper le moteur et attendre au moins 10 minutes.",
             "Redémarrer et observer le voyant.",
             "S'il clignote encore : rouler à 50 km/h maximum jusqu'au concessionnaire le plus proche (" + ref(117) + ").",
             "Ne pas effacer ni ignorer le défaut : le signaler dans le ticket d'intervention."],
      valeurs=[["Temps d'arrêt minimal", "10 minutes", ref(117)], ["Vitesse maximale si le défaut persiste", "50 km/h", ref(117)]],
      negatif="Fixe et clignotant n'ont pas la même gravité : le clignotement signale des ratés et impose l'arrêt ; le fixe autorise une conduite modérée.",
      absent="Causes précises des ratés (bougie, injection, allumage) et codes de défaut : manuel d'atelier, absent du corpus.",
      liens="sh150_voyant_injection_allume, sh150_bougie_ralenti_instable"),
 dict(id="sh150_surchauffe_moteur", titre="Témoin de température élevée allumé (surchauffe)", usage="normal", pages="40, 77, 102, 116, 153",
      symptome="Le témoin rouge de température du liquide de refroidissement s'allume ; l'accélération devient molle.",
      fig=fig_panel({"temp": "on"}), fig_cap="témoin rouge de température élevée du liquide.",
      photo="sh150_vase_expansion", photo_brief="vase d'expansion de la SH150i, repères UPPER / LOWER visibles, moteur froid.",
      sens=[["Témoin rouge allumé", "Température du liquide au-dessus de la valeur prévue", "arrêt", ref(116)],
            ["Niveau sous LOWER", "Manque de liquide, fuite probable", "élevée", ref(102)]],
      securite=("danger", "Ne pas continuer à rouler", "Rouler moteur en surchauffe peut l'endommager gravement. En cas de fuite, ne pas redémarrer : transporter le scooter (" + ref(116) + ")."),
      flow=["Témoin allumé, accélération molle", "Arrêt en sécurité, contact Off", "Refroidissement contact coupé", "Durites : fuite ?", "Niveau du vase, appoint"],
      flow_hl=(1,), flow_cap="conduite à tenir en cas de surchauffe (" + ref(116) + ").",
      steps=["Arrêter le scooter en sécurité et couper le contact.", "Laisser refroidir moteur arrêté.",
             "Rechercher une fuite sur les durites et autour du moteur.",
             "Moteur froid, scooter sur béquille centrale : contrôler le niveau du vase d'expansion (" + ref(102) + ").",
             "Compléter si besoin avec le liquide préconisé ; si le niveau baisse vite ou si le vase est vide : concessionnaire.",
             "Si tout est normal, reprendre la route en surveillant le témoin (" + ref(116) + ")."],
      fig2=fig_vase, fig2_cap="vase d'expansion : niveau à maintenir entre UPPER et LOWER (schéma).",
      valeurs=[["Capacité du circuit", "0,47 L", ref(153)], ["Liquide", "Pro Honda HP Coolant", ref(153)],
               ["Remplacement du liquide", "Tous les 3 ans", ref(77)]],
      negatif="Un ralenti accéléré prolongé peut allumer le témoin sans fuite : si les contrôles sont normaux, la route peut reprendre (" + ref(116) + ").",
      absent="Couple des colliers, purge du circuit, contrôle du thermostat ou du ventilateur : manuel d'atelier, absent du corpus.",
      liens="sh150_perte_puissance"),
 dict(id="sh150_moteur_ne_demarre_pas", titre="Le moteur ne démarre pas", usage="normal", pages="59",
      symptome="Contact mis, le démarreur ne lance pas le moteur, ou le moteur tourne sans démarrer.",
      fig=fig_scooter("bequille_l", "batterie"), fig_cap="points à vérifier : (1) béquille latérale, (2) batterie (silhouette schématique).",
      photo="sh150_bequille_laterale", photo_brief="béquille latérale de la SH150i, dépliée puis repliée.",
      sens=[["Béquille latérale dépliée", "Coupe-circuit : démarrage impossible", "aucune", ref(59)],
            ["Démarreur faible", "Tension de batterie insuffisante", "moyenne", ref(59)],
            ["Témoin SMART Key clignotant", "Clé non reconnue", "moyenne", ref(120)]],
      securite=("attention", "Ne pas insister", "Si le moteur ne démarre pas en 5 secondes : contact sur Off et 10 secondes d'attente avant un nouvel essai (" + ref(59) + ")."),
      flow=["Béquille latérale repliée ?", "Smart Key sur soi ?", "Poignée de gaz fermée ?", "Démarreur 5 s max", "Off, 10 s, nouvel essai"],
      flow_cap="ordre de vérification avant de conclure à une panne.",
      steps=["Replier la béquille latérale (" + ref(59) + ").", "Garder la Smart Key sur soi et vérifier le témoin SMART Key.",
             "Contact sur On : les témoins doivent s'allumer brièvement.",
             "Poignée d'accélérateur fermée, actionner le démarreur 5 secondes au maximum.",
             "Échec : contact sur Off, attendre 10 secondes, recommencer ; si l'échec persiste, contrôler la batterie (fiche sh150_batterie_faible)."],
      valeurs=[["Durée maximale d'un essai", "5 secondes", ref(59)], ["Attente entre deux essais", "10 secondes, contact sur Off", ref(59)],
               ["Batterie", "YTZ8V, 12 V - 7,0 Ah", ref(152)]],
      negatif="Moteur coupé au feu rouge avec le témoin Idling Stop clignotant : ce n'est pas un non-démarrage (fiche sh150_moteur_coupe_au_feu).",
      absent="Contrôle du relais de démarreur, du coupe-circuit et de la pompe à essence : manuel d'atelier, absent du corpus.",
      liens="sh150_batterie_faible, sh150_smart_key_non_detectee, sh150_moteur_coupe_au_feu"),
 dict(id="sh150_smart_key_pile_faible", titre="Témoin SMART Key qui clignote 5 fois (pile faible)", usage="normal", pages="40, 112, 120",
      symptome="Au passage du contact sur On, le témoin vert SMART Key clignote cinq fois.",
      fig=fig_smartkey, fig_cap="Smart Key, pile CR2032 et commande de contact (schéma de l'équipe).",
      photo="sh150_smart_key_pile", photo_brief="Smart Key ouverte montrant la pile CR2032.",
      sens=[["5 clignotements au contact", "Pile de la Smart Key faible", "faible", ref(120)],
            ["Allumé fixe", "Clé reconnue (normal)", "aucune", ref(40)]],
      securite=("info", "Bon réflexe", "Remplacer la pile dès que possible : une pile vide empêche l'utilisation normale de la clé. Honda recommande le concessionnaire (" + ref(112) + ")."),
      flow=["Contact sur On", "5 clignotements ?", "Pile faible", "Remplacer la CR2032", "Contrôle : témoin fixe"], flow_cap="diagnostic du témoin SMART Key.",
      steps=["Vérifier que le témoin clignote bien cinq fois au passage sur On (" + ref(120) + ").",
             "Préparer une pile CR2032 neuve.", "Remplacer la pile selon le manuel ou chez le concessionnaire (" + ref(112) + ").",
             "Remettre le contact : le témoin SMART Key doit s'allumer sans clignoter."],
      valeurs=[["Pile", "CR2032", ref(112)], ["Signal de pile faible", "5 clignotements au contact", ref(120)]],
      negatif="Un témoin qui clignote en continu contact sur On signale une perte de communication, pas une pile faible (fiche sh150_smart_key_non_detectee).",
      absent="Programmation d'une nouvelle clé et remplacement de l'unité de commande : concessionnaire.",
      liens="sh150_smart_key_non_detectee"),
 dict(id="sh150_smart_key_non_detectee", titre="Smart Key non détectée (témoin clignotant en continu)", usage="normal", pages="59, 120, 129",
      symptome="Contact sur On, le témoin SMART Key clignote en continu ; la clé a pu être oubliée ou perdue en roulant.",
      fig=fig_panel({"smartkey": "blink"}), fig_cap="témoin SMART Key clignotant en continu.",
      photo="sh150_commande_contact", photo_brief="commande de contact rotative de la SH150i (positions Lock, Off, On, SEAT FUEL).",
      sens=[["Clignote contact sur On", "Communication interrompue : ondes radio fortes ou clé perdue", "moyenne", ref(120)],
            ["Clé absente", "Le scooter fonctionne jusqu'au verrouillage du contact", "moyenne", ref(120)]],
      securite=("attention", "Pendant une intervention", "Moteur arrêté contact sur On, l'authentification se désactive au bout d'un temps ou quand la clé s'éloigne (" + ref(59) + ")."),
      flow=["Témoin clignote en continu", "Clé sur le pilote ?", "Éloigner téléphones et émetteurs", "Appui > 2 s : verrouillage", "Clé perdue : méthode de secours"],
      flow_cap="perte de communication avec la Smart Key (" + ref(120) + ").",
      steps=["Vérifier que la Smart Key est bien sur le pilote.", "S'éloigner des sources d'ondes radio fortes.",
             "Pour arrêter le clignotement : maintenir la commande de contact appuyée plus de 2 secondes ; le contact se verrouille (" + ref(120) + ").",
             "En position SEAT FUEL, Off ou Lock pendant le clignotement : bague et témoin s'allument environ 20 s, puis le contact se verrouille.",
             "Clé introuvable : appliquer la méthode de déverrouillage de secours décrite au manuel (" + ref(129) + ")."],
      valeurs=[["Appui pour verrouiller", "Plus de 2 secondes", ref(120)], ["Allumage bague et témoin", "Environ 20 secondes", ref(120)]],
      negatif="Cinq clignotements seulement au passage sur On : pile faible (fiche sh150_smart_key_pile_faible).",
      absent="Détail de la méthode de secours (numéro d'identification) : non reproduit, voir le manuel Honda page " + "129.",
      liens="sh150_smart_key_pile_faible, sh150_moteur_ne_demarre_pas"),
 dict(id="sh150_idling_stop_inactif", titre="Idling Stop qui ne s'active pas", usage="normal", pages="55, 56, 122",
      symptome="Le moteur ne se coupe pas aux arrêts et le témoin vert Idling Stop ne s'allume jamais.",
      fig=fig_panel({"idling": "off"}), fig_cap="témoin Idling Stop éteint (repère 7, gris = éteint).",
      photo="sh150_commutateur_idling_stop", photo_brief="commutateur IDLING STOP / IDLING au guidon de la SH150i.",
      sens=[["Témoin jamais allumé", "Conditions d'activation non réunies", "faible", ref(55)],
            ["Commutateur sur IDLING", "Système désactivé volontairement", "aucune", ref(56)]],
      securite=("info", "Pas une panne moteur", "L'absence d'Idling Stop n'empêche pas de rouler ; c'est une fonction d'économie de carburant."),
      flow=["Commutateur sur IDLING STOP ?", "Démarré au démarreur ?", "Moteur chaud ?", "Vitesse > 10 km/h atteinte ?", "Toujours rien : dépannage MP p. 122"],
      flow_cap="conditions d'activation de l'Idling Stop (" + ref(55) + ").",
      steps=["Placer le commutateur sur IDLING STOP.", "Démarrer le moteur avec le bouton de démarreur.",
             "Rouler jusqu'à ce que le moteur soit chaud.", "Dépasser 10 km/h : le témoin Idling Stop doit s'allumer (" + ref(55) + ").",
             "Si le témoin ne s'allume toujours pas, suivre le tableau de dépannage du manuel (" + ref(122) + ") ou ouvrir un ticket."],
      fig2=fig_idling, fig2_cap="cycle normal : prêt, arrêt au feu, redémarrage à l'ouverture des gaz.", fig2_h=100,
      valeurs=[["Vitesse d'armement", "Plus de 10 km/h", ref(55)], ["Désactivation", "Commutateur sur IDLING", ref(56)]],
      negatif="Batterie faible ou moteur froid peuvent suffire à empêcher l'activation sans aucun défaut.",
      absent="Seuils de tension batterie et de température utilisés par le système : non publiés dans le manuel du propriétaire.",
      liens="sh150_moteur_coupe_au_feu, sh150_batterie_faible"),
 dict(id="sh150_moteur_coupe_au_feu", titre="Le moteur se coupe à l'arrêt (Idling Stop)", usage="ambigu", pages="55, 56",
      symptome="Le client signale que le moteur « cale » aux feux rouges : il repart dès qu'on tourne la poignée.",
      fig=fig_panel({"idling": "blink"}), fig_cap="témoin Idling Stop clignotant : moteur arrêté par le système.",
      photo="sh150_tableau_idling_stop", photo_brief="tableau de bord au feu rouge, moteur coupé par l'Idling Stop, témoin vert clignotant.",
      sens=[["Arrêt au feu, témoin clignotant", "Idling Stop actif : fonctionnement normal", "aucune", ref(55)],
            ["Arrêt en roulant", "Panne réelle", "élevée", "-"]],
      securite=("danger", "Ne pas s'éloigner", "Ne jamais quitter le scooter quand le témoin Idling Stop clignote : le moteur redémarre si la poignée est ouverte. Couper le contact (" + ref(56) + ")."),
      flow=["Moteur coupé", "À l'arrêt ou en roulant ?", "À l'arrêt + témoin clignote : normal", "En roulant : panne", "Diagnostic"], flow_hl=(1,),
      flow_cap="distinguer l'Idling Stop d'une vraie panne.",
      steps=["Demander au client si le moteur s'arrête à l'arrêt complet ou en roulant.",
             "À l'arrêt, avec le témoin Idling Stop qui clignote : expliquer le fonctionnement, aucun défaut.",
             "Si le client ne veut pas de la fonction : commutateur sur IDLING (" + ref(56) + ").",
             "En roulant : traiter comme une panne (fiches sh150_voyant_injection_clignote, sh150_moteur_ne_demarre_pas)."],
      fig2=fig_idling, fig2_cap="cycle Idling Stop.", fig2_h=100,
      valeurs=[["Redémarrage", "À l'ouverture des gaz", ref(56)], ["Arrêt prolongé", "Peut décharger la batterie", ref(56)]],
      negatif="Cas de test ambigu : « mon scooter cale » peut décrire l'Idling Stop ou une panne. L'assistant doit demander à l'arrêt ou en roulant.",
      absent="Aucune valeur de durée maximale d'arrêt automatique dans le manuel du propriétaire.",
      liens="sh150_idling_stop_inactif"),
 dict(id="sh150_temoin_abs_allume", titre="Témoin ABS allumé en roulant", usage="normal", pages="41, 118",
      symptome="Le témoin orange ABS reste allumé ou clignote au-dessus de 10 km/h.",
      fig=fig_panel({"abs": "on"}), fig_cap="témoin ABS allumé (repère 2).",
      photo="sh150_tableau_temoin_abs", photo_brief="tableau de bord avec le témoin ABS allumé, scooter roulant ou contact mis.",
      sens=[["Allumé au contact, éteint vers 10 km/h", "Autotest normal", "aucune", ref(41)],
            ["Allumé ou clignotant en roulant", "Problème possible de l'ABS", "élevée", ref(118)],
            ["Ne s'allume pas au contact", "Défaut du témoin ou du système", "élevée", ref(118)]],
      securite=("attention", "Freinage sans antiblocage", "Témoin allumé : le freinage reste conventionnel mais sans antiblocage. Réduire la vitesse et faire contrôler (" + ref(118) + ")."),
      flow=["Contact sur On : témoin allumé ?", "Éteint au-dessus de 10 km/h ?", "Roue AR tournée levée ?", "Couper puis remettre le contact", "Toujours allumé : contrôle"],
      flow_cap="lecture du témoin ABS (" + ref(118) + ").",
      steps=["Vérifier que le témoin s'allume au contact puis s'éteint vers 10 km/h (" + ref(41) + ").",
             "Si la roue arrière a été tournée scooter levé, couper puis remettre le contact (" + ref(118) + ").",
             "Le témoin doit s'éteindre au-dessus de 30 km/h dans ce cas.", "S'il reste allumé : rouler prudemment et ouvrir un ticket de contrôle ABS."],
      valeurs=[["Extinction normale", "Vers 10 km/h", ref(41)], ["Après rotation de la roue levée", "S'éteint au-dessus de 30 km/h", ref(118)]],
      negatif="Témoin allumé après un passage sur béquille avec roue arrière entraînée : souvent sans défaut.",
      absent="Diagnostic des capteurs de roue et du modulateur ABS : manuel d'atelier, absent du corpus.",
      liens="sh150_niveau_liquide_frein_bas, sh150_usure_plaquettes, sh150_temoin_hstc_allume"),
 dict(id="sh150_temoin_hstc_allume", titre="Témoin HSTC allumé fixe en roulant", usage="normal", pages="41, 58, 119",
      symptome="Le témoin orange de contrôle de couple (HSTC) reste allumé fixe en roulant.",
      fig=fig_panel({"tc": "on"}), fig_cap="témoin HSTC (repère 3) allumé fixe.",
      photo="sh150_tableau_temoin_hstc", photo_brief="tableau de bord avec le témoin TC (HSTC) visible ; écran « HSTC ON / OFF ».",
      sens=[["Allumé au contact, éteint vers 3 km/h", "Autotest normal", "aucune", ref(41)],
            ["Clignote brièvement", "Le système agit (perte d'adhérence)", "aucune", ref(41)],
            ["Allumé fixe en roulant", "Problème possible du HSTC", "moyenne", ref(119)]],
      securite=("attention", "Conduite sans HSTC", "La conduite reste normale mais sans contrôle de couple : réduire la vitesse et faire contrôler (" + ref(119) + ")."),
      flow=["Témoin HSTC fixe", "HSTC désactivé (OFF) ?", "Roue AR tournée levée ?", "Off puis On", "Toujours allumé : contrôle"],
      flow_cap="lecture du témoin HSTC.",
      steps=["Vérifier si le témoin « HSTC OFF » est allumé : le système a peut-être été coupé avec le bouton INFO B (" + ref(58) + ").",
             "Rappel : à chaque mise du contact, le HSTC revient sur ON.",
             "Si la roue arrière a tourné scooter levé : couper puis remettre le contact (" + ref(119) + ").",
             "Persistance : ouvrir un ticket de contrôle."],
      valeurs=[["Extinction normale", "Vers 3 km/h", ref(41)], ["Activation / désactivation", "Bouton INFO B, scooter arrêté", ref(58)]],
      negatif="Le HSTC n'existe pas sur la SH150i 2017-2019 : vérifier le millésime avant de répondre.",
      absent="Diagnostic électronique du HSTC : manuel d'atelier, absent du corpus.",
      liens="sh150_temoin_abs_allume"),
 dict(id="sh150_niveau_huile_bas", titre="Niveau d'huile moteur bas", usage="normal", pages="98, 99, 153",
      symptome="Au contrôle, l'huile est sous le repère bas de la jauge-bouchon.",
      fig=fig_jauge, fig_cap="jauge-bouchon : niveau sous le repère bas (schéma de principe).",
      photo="sh150_jauge_huile", photo_brief="jauge-bouchon d'huile de la SH150i sortie et essuyée, repères visibles.",
      sens=[["Entre les repères", "Niveau correct", "aucune", ref(98)], ["Sous le repère bas", "Appoint nécessaire", "moyenne", ref(99)]],
      securite=("arret", "Conditions de mesure", "Commutateur Idling Stop sur IDLING ; moteur chauffé 3 à 5 min puis contact Off 2 à 3 min ; béquille centrale sur sol plat (" + ref(98) + ")."),
      flow=["Préparer le scooter", "Sortir et essuyer la jauge", "Réinsérer sans visser", "Lire le niveau", "Appoint jusqu'au repère haut"],
      flow_cap="contrôle du niveau (" + ref(98) + ").",
      steps=["Mettre le scooter dans les conditions de mesure ci-dessus.", "Retirer la jauge-bouchon et l'essuyer.",
             "La réinsérer jusqu'en butée sans la visser, puis la retirer.", "Lire le niveau entre les repères haut et bas.",
             "Compléter avec l'huile préconisée sans dépasser le repère haut (" + ref(99) + ").", "Remettre la jauge-bouchon fermement."],
      valeurs=[["Huile", "Honda 4 temps, API SG ou plus, SAE 10W-30, JASO MB", ref(153)], ["Quantité après vidange", "0,8 L", ref(153)],
               ["Bouchon de remplissage", "20 N·m", ref(154)]],
      negatif="Ne pas mélanger des huiles de marques ou de grades différents (" + ref(99) + ").",
      absent="Consommation d'huile normale : non donnée par le manuel du propriétaire.",
      liens="sh150_vidange_echeance"),
 dict(id="sh150_vidange_echeance", titre="Indicateur d'entretien affiché (vidange due)", usage="normal", pages="39, 77, 99, 153, 154",
      symptome="L'écran affiche l'indicateur d'entretien : la vidange d'huile moteur arrive à échéance.",
      fig=fig_lcd_entretien, fig_cap="indicateur d'entretien (affichage schématique de l'équipe).",
      photo="sh150_ecran_entretien", photo_brief="écran LCD de la SH150i affichant l'indicateur d'entretien.",
      sens=[["Indicateur affiché", "Entretien périodique à faire", "faible", ref(39)]],
      securite=("attention", "Outils spéciaux", "Vidange et nettoyage de la crépine demandent des outils spéciaux : Honda recommande le concessionnaire (" + ref(99) + ")."),
      flow=["Indicateur affiché", "Vidange huile moteur", "Crépine si 12 000 km", "Contrôle du niveau", "Remise à zéro (INFO A)"],
      flow_cap="traitement de l'échéance d'entretien.",
      steps=["Contrôler le kilométrage par rapport au programme d'entretien (" + ref(77) + ").",
             "Vidanger l'huile moteur ; nettoyer la crépine aux échéances prévues.", "Serrer la vis de vidange à 24 N·m (" + ref(154) + ").",
             "Remplir avec 0,8 L (0,9 L si la crépine a été nettoyée) puis contrôler à la jauge.",
             "Remettre l'indicateur à zéro en maintenant INFO A dans le mode prévu (" + ref(39) + ")."],
      fig2=fig_intervalles([("Première vidange", 1000, COLM), ("Vidange", 6000, ORANGE), ("Crépine", 12000, GREY_D)]),
      fig2_cap="intervalles de vidange et de crépine (" + ref(77) + "), plus une vidange chaque année.", fig2_h=90,
      valeurs=[["Intervalle", "1 000 km, puis tous les 6 000 km et chaque année", ref(77)], ["Après vidange ; avec crépine", "0,8 L ; 0,9 L", ref(153)],
               ["Vis de vidange", "24 N·m", ref(154)], ["Huile", "SAE 10W-30, JASO MB", ref(153)]],
      negatif="Huile de transmission finale : autre circuit, remplacement tous les 2 ans (" + ref(78) + "), ne pas confondre avec l'huile moteur.",
      absent="Référence du joint de vis de vidange : catalogue de pièces, absent du corpus pour 2020-2024.",
      liens="sh150_niveau_huile_bas"),
 dict(id="sh150_pression_pneus_basse", titre="Pression des pneus trop basse", usage="normal", pages="153",
      symptome="Direction lourde, tenue de route floue ou pneu visiblement écrasé.",
      fig=fig_manometre, fig_cap="pressions à froid de la SH150AD.",
      photo="sh150_valve_pneu_avant", photo_brief="contrôle de pression à la valve de la roue avant de la SH150i.",
      sens=[["Pression sous la valeur", "Usure rapide, tenue de route dégradée", "moyenne", ref(153)]],
      securite=("attention", "Mesurer à froid", "La pression se mesure pneus froids ; une mesure à chaud surestime la pression."),
      flow=["Pneus froids", "Mesurer AV et AR", "Comparer aux valeurs", "Corriger", "Inspecter le pneu"], flow_cap="contrôle de la pression.",
      steps=["Scooter sur béquille centrale, pneus froids.", "Mesurer la pression avant puis arrière.",
             "Corriger : 200 kPa à l'avant, 225 kPa à l'arrière, seul ou avec passager (" + ref(153) + ").",
             "Rechercher une cause de fuite : clou, coupure, valve.", "Recontrôler le lendemain si une fuite lente est suspectée."],
      valeurs=[["Avant", "200 kPa (2,00 bar)", ref(153)], ["Arrière", "225 kPa (2,25 bar)", ref(153)], ["Avec passager", "Mêmes valeurs", ref(153)],
               ["Dimensions", "AV 100/80-16M/C 50P ; AR 120/80-16M/C 60P", ref(153)]],
      negatif="Sur la génération 2005, les pressions sont différentes : ne pas les appliquer à une 2020-2024.",
      absent="Réparation d'un pneu sans chambre : non décrite ; remplacer ou confier à un spécialiste.",
      liens="sh150_usure_pneus"),
 dict(id="sh150_usure_pneus", titre="Pneu usé (sculptures insuffisantes)", usage="normal", pages="153",
      symptome="Bande de roulement lisse ou témoin d'usure atteint.",
      fig=fig_pneu, fig_cap="témoin d'usure dans les sculptures (schéma).",
      photo="sh150_pneu_arriere_usure", photo_brief="bande de roulement du pneu arrière avec témoin d'usure visible.",
      sens=[["Sous 1,5 mm (AV) ou 2,0 mm (AR)", "Pneu à remplacer", "élevée", ref(153)], ["Coupure, hernie", "Pneu à remplacer", "élevée", "-"]],
      securite=("danger", "Adhérence", "Un pneu sous la profondeur minimale réduit fortement l'adhérence, surtout sur sol mouillé : ne pas laisser repartir le scooter."),
      flow=["Inspection visuelle", "Mesure de profondeur", "Comparer aux minima", "Remplacement", "Contrôle pression"], flow_cap="contrôle d'usure.",
      steps=["Inspecter flancs et bande de roulement : coupures, clous, déformations.", "Mesurer la profondeur au centre de la bande.",
             "Remplacer sous 1,5 mm à l'avant ou 2,0 mm à l'arrière (" + ref(153) + ").", "Monter la dimension d'origine.", "Régler la pression du pneu neuf."],
      valeurs=[["Profondeur minimale AV", "1,5 mm", ref(153)], ["Profondeur minimale AR", "2,0 mm", ref(153)],
               ["Pneus d'origine", "IRC SS-530F / SS-530R ou MICHELIN CITY GRIP", ref(153)]],
      negatif="La profondeur légale au Maroc peut différer de la valeur Honda : appliquer la plus exigeante (à vérifier).",
      absent="Couples des axes de roue : manuel d'atelier, absent du corpus.",
      liens="sh150_pression_pneus_basse"),
 dict(id="sh150_bougie_ralenti_instable", titre="Ralenti instable : contrôle de la bougie", usage="normal", pages="77, 153",
      symptome="Ralenti irrégulier, démarrage difficile à froid, petits ratés à l'accélération.",
      fig=fig_bougie, fig_cap="bougie standard et écartement (schéma non à l'échelle).",
      photo="sh150_bougie", photo_brief="bougie NGK LMAR8L-9 déposée, électrodes visibles.",
      sens=[["Électrodes usées ou encrassées", "Allumage dégradé", "moyenne", ref(77)], ["Ralenti hors plage", "Réglage ou défaut moteur", "moyenne", ref(153)]],
      securite=("arret", "Moteur froid", "Déposer la bougie uniquement moteur froid, contact sur Off."),
      flow=["Ralenti irrégulier", "Échéance bougie ?", "Dépose moteur froid", "Écartement 0,8-0,9 mm", "Remplacement si usée"], flow_cap="contrôle de la bougie.",
      steps=["Vérifier l'échéance : inspection tous les 6 000 km, remplacement tous les 12 000 km (" + ref(77) + ").",
             "Déposer la bougie moteur froid.", "Contrôler l'aspect des électrodes et mesurer l'écartement : 0,8 à 0,9 mm (" + ref(153) + ").",
             "Remplacer par une NGK LMAR8L-9 si besoin.", "Contrôler le ralenti : 1 700 ± 100 tr/min."],
      valeurs=[["Bougie", "NGK LMAR8L-9", ref(153)], ["Écartement", "0,8 à 0,9 mm", ref(153)], ["Ralenti", "1 700 ± 100 tr/min", ref(153)],
               ["Échéances", "I tous les 6 000 km ; R tous les 12 000 km", ref(77)]],
      negatif="La génération 2005 utilise une autre bougie : ne pas transposer la référence.",
      absent="Couple de serrage de la bougie : non donné par le manuel du propriétaire.",
      liens="sh150_voyant_injection_clignote, sh150_perte_puissance"),
 dict(id="sh150_niveau_liquide_frein_bas", titre="Niveau de liquide de frein bas", usage="normal", pages="78, 153",
      symptome="Le niveau du réservoir de liquide de frein est sous le repère inférieur ; le levier peut paraître spongieux.",
      fig=fig_reservoir_frein, fig_cap="réservoir de liquide de frein au guidon (schéma).",
      photo="sh150_reservoir_frein", photo_brief="réservoir de liquide de frein au guidon, regard de niveau visible.",
      sens=[["Niveau sous le repère", "Plaquettes usées ou fuite", "élevée", ref(78)], ["Levier spongieux", "Air ou fuite dans le circuit", "élevée", "-"]],
      securite=("danger", "Intervention réservée", "Remplacement et purge du liquide demandent des compétences mécaniques : concessionnaire ou technicien formé (" + ref(78) + ")."),
      flow=["Scooter droit, guidon droit", "Lire le niveau", "Contrôler les plaquettes", "Rechercher une fuite", "Ticket atelier"], flow_cap="contrôle du circuit de frein.",
      steps=["Scooter sur béquille centrale, guidon droit, réservoir horizontal.", "Lire le niveau dans le regard.",
             "Contrôler l'usure des plaquettes (fiche sh150_usure_plaquettes) : un niveau bas suit souvent leur usure.",
             "Rechercher une fuite aux raccords et à l'étrier.", "Ne compléter qu'avec du DOT 3 ou DOT 4 d'un récipient fermé (" + ref(153) + ")."],
      valeurs=[["Liquide", "Honda DOT 3 ou DOT 4", ref(153)], ["Remplacement", "Tous les 2 ans", ref(78)],
               ["Contrôle", "Avant départ, tous les 6 000 km et chaque année", ref(78)]],
      negatif="Un niveau qui baisse lentement avec l'usure des plaquettes est normal ; une baisse rapide signale une fuite.",
      absent="Procédure de purge et couples des raccords : manuel d'atelier, absent du corpus.",
      liens="sh150_usure_plaquettes, sh150_temoin_abs_allume"),
 dict(id="sh150_usure_plaquettes", titre="Plaquettes de frein usées", usage="normal", pages="78",
      symptome="Bruit de frottement métallique au freinage ou freinage moins efficace.",
      fig=fig_plaquettes, fig_cap="épaisseur de garniture : correcte et usée (schéma).",
      photo="sh150_etrier_plaquettes", photo_brief="étrier de frein avant de la SH150i vu de face, plaquettes visibles.",
      sens=[["Garniture mince", "Plaquettes à remplacer", "élevée", ref(78)], ["Bruit métallique", "Garniture épuisée, disque menacé", "élevée", "-"]],
      securite=("danger", "Intervention réservée", "Le remplacement des plaquettes relève du concessionnaire ou d'un technicien formé (" + ref(78) + ")."),
      flow=["Bruit ou freinage faible", "Inspection des plaquettes", "Garniture mince ?", "Remplacement par paire", "Essai de freinage"], flow_cap="contrôle des plaquettes.",
      steps=["Scooter sur béquille centrale.", "Inspecter l'épaisseur de garniture par l'arrière de l'étrier.",
             "Garniture mince : remplacer les plaquettes par paire.", "Contrôler le niveau de liquide après remplacement.",
             "Faire un essai de freinage à basse vitesse."],
      valeurs=[["Contrôle de l'usure", "Avant départ, tous les 6 000 km et chaque année", ref(78)], ["Liquide", "DOT 3 ou DOT 4", ref(153)]],
      negatif="Un léger bruit après la pluie peut venir de l'oxydation du disque, sans usure anormale.",
      absent="Épaisseur minimale chiffrée et références des plaquettes : manuel d'atelier et catalogue, absents du corpus.",
      liens="sh150_niveau_liquide_frein_bas"),
 dict(id="sh150_batterie_faible", titre="Batterie faible", usage="normal", pages="56, 59, 78, 152",
      symptome="Démarreur lent ou inopérant ; Idling Stop qui ne s'arme plus ; témoins faibles au contact.",
      fig=fig_batterie, fig_cap="batterie YTZ8V et ordre de branchement des bornes (schéma).",
      photo="sh150_batterie", photo_brief="batterie YTZ8V de la SH150i en place, bornes visibles (contact coupé).",
      sens=[["Démarreur lent", "Tension insuffisante", "moyenne", ref(59)], ["Arrêts Idling Stop prolongés", "Décharge possible", "faible", ref(56)]],
      securite=("danger", "Ordre des bornes", "Débrancher la borne négative (-) en premier et rebrancher la positive (+) en premier (règle d'atelier)."),
      flow=["Symptôme de batterie", "Essais 5 s / 10 s", "Bornes propres et serrées ?", "Charge ou test", "Remplacement YTZ8V"], flow_cap="diagnostic de la batterie.",
      steps=["Limiter chaque essai de démarreur à 5 secondes, puis contact Off et 10 secondes d'attente (" + ref(59) + ").",
             "Contrôler la propreté et le serrage des bornes.", "Recharger ou tester la batterie avec un appareil adapté.",
             "Remplacer par une YTZ8V si elle ne tient plus la charge (" + ref(152) + ").", "Rappeler au client l'effet des arrêts Idling Stop prolongés (" + ref(56) + ")."],
      valeurs=[["Type", "YTZ8V", ref(152)], ["Capacité", "12 V - 7,0 Ah (10 h)", ref(152)], ["Contrôle", "Tous les 6 000 km et chaque année", ref(78)]],
      negatif="Un démarreur qui ne tourne pas béquille latérale dépliée n'est pas une batterie faible (fiche sh150_moteur_ne_demarre_pas).",
      absent="Courant de charge et tension de seuil : non donnés par le manuel du propriétaire.",
      liens="sh150_moteur_ne_demarre_pas, sh150_idling_stop_inactif"),
 dict(id="sh150_fusible_grille", titre="Un équipement électrique ne fonctionne plus (fusible)", usage="normal", pages="154",
      symptome="Un équipement électrique ne fonctionne plus d'un coup (éclairage, prise, clignotants) alors que le reste fonctionne.",
      fig=fig_fusibles, fig_cap="calibres des fusibles de la SH150AD (schéma).", fig_h=130,
      photo="sh150_boite_fusibles", photo_brief="boîte à fusibles de la SH150i ouverte, contact coupé.",
      sens=[["Fusible au filament coupé", "Surcharge ou court-circuit", "moyenne", ref(154)], ["Fusible qui grille à nouveau", "Court-circuit à rechercher", "élevée", "-"]],
      securite=("danger", "Jamais de calibre supérieur", "Remplacer un fusible uniquement par un fusible de même calibre ; un calibre supérieur peut provoquer un incendie."),
      flow=["Équipement en panne", "Contact Off", "Contrôler le fusible", "Même calibre", "Regrille : atelier"], flow_cap="contrôle d'un fusible.",
      steps=["Couper le contact.", "Accéder à la boîte à fusibles et repérer le fusible du circuit concerné.",
             "Contrôler le filament.", "Remplacer par un fusible du même calibre.", "S'il grille à nouveau : rechercher un court-circuit en atelier."],
      valeurs=[["Fusible principal", "20 A", ref(154)], ["Autres fusibles", "30 A, 15 A, 10 A, 7,5 A", ref(154)], ["Éclairage", "LED", ref(154)]],
      negatif="Un feu à LED qui ne s'allume plus peut venir du bloc LED lui-même : il ne se remplace pas comme une ampoule.",
      absent="Affectation de chaque fusible à un circuit et emplacement exact de la boîte : à relever sur le scooter, absents de cette fiche.",
      liens="sh150_batterie_faible"),
 dict(id="sh150_perte_puissance", titre="Perte de puissance ou accélération molle", usage="normal", pages="58, 77, 78, 116, 117",
      symptome="Le scooter accélère mal ou plafonne en vitesse, sans témoin particulier ou avec un témoin allumé.",
      fig=fig_scooter("airbox", "cvt"), fig_cap="(1) boîtier de filtre à air, (2) transmission V-Matic (silhouette schématique).",
      photo="sh150_carter_transmission", photo_brief="côté gauche de la SH150i : carter de transmission et boîtier de filtre à air.",
      sens=[["Témoin température allumé", "Surchauffe : autre fiche", "élevée", ref(116)], ["Voyant PGM-FI", "Défaut moteur : autre fiche", "élevée", ref(117)],
            ["Filtre à air ancien", "Admission d'air réduite", "moyenne", ref(77)], ["Courroie usée", "Transmission qui patine", "moyenne", ref(78)]],
      securite=("info", "Commencer par les témoins", "Une perte de puissance avec un témoin allumé renvoie d'abord à la fiche du témoin concerné."),
      flow=["Témoin allumé ?", "Oui : fiche du témoin", "Non : filtre à air (18 000 km)", "Courroie (12 000 / 24 000 km)", "Ticket atelier"],
      flow_cap="démarche en cas de perte de puissance.",
      steps=["Vérifier les témoins : température (fiche sh150_surchauffe_moteur), PGM-FI (fiches sh150_voyant_injection_*).",
             "Le HSTC limite volontairement la puissance quand il agit : vérifier s'il clignote (" + ref(58) + ").",
             "Contrôler l'échéance du filtre à air : remplacement tous les 18 000 km (" + ref(77) + ").",
             "Contrôler l'échéance de la courroie : inspection à 12 000 km, remplacement à 24 000 km (" + ref(78) + ").",
             "Sans cause trouvée : ticket atelier pour contrôle de la transmission."],
      fig2=fig_intervalles([("Courroie : contrôle", 12000, GREY_D), ("Filtre à air", 18000, ORANGE), ("Courroie : remplacement", 24000, DARK)]),
      fig2_cap="échéances liées à la perte de puissance (" + ref(77) + ", " + ref(78) + ").", fig2_h=86,
      valeurs=[["Filtre à air", "Remplacer tous les 18 000 km", ref(77)], ["Courroie", "Inspecter à 12 000 km, remplacer à 24 000 km", ref(78)],
               ["Transmission", "V-Matic 2,68:1 à 0,82:1", ref(152)]],
      negatif="Le clignotement du témoin HSTC en accélération sur sol glissant est normal : le système réduit la puissance.",
      absent="Largeur limite de courroie et galets pour 2020-2024 : manuel d'atelier, absent du corpus.",
      liens="sh150_surchauffe_moteur, sh150_voyant_injection_allume, sh150_temoin_hstc_allume"),
]


def main():
    os.makedirs(OUTDIR, exist_ok=True)
    assert len(SPECS) == 20 and len({s["id"] for s in SPECS}) == 20
    for i, s in enumerate(SPECS):
        n = build(s, i + 1, os.path.join(OUTDIR, s["id"] + ".pdf"))
        print("%-42s %d pages" % (s["id"], n))


if __name__ == "__main__":
    main()
