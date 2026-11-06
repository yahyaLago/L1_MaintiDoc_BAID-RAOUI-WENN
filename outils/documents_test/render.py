# -*- coding: utf-8 -*-
"""Rend les sources markdown du corpus MaintiDoc en PDF homogènes.

Syntaxe prise en charge :
  front-matter ---  clé: valeur ---  (doc_id, titre, famille, modele, type, version, groupes, licence, sources: url | libellé ; ...)
  # titre de section, ## sous-section
  paragraphe (texte libre, **gras**)
  - puce        1. étape numérotée
  | tableau | (première ligne = en-tête ; ligne |---| ignorée)
  > DANGER: texte   > ATTENTION: texte   > INFO: texte
  [FIG:nom|légende]  figure vectorielle dessinée par figures.py
"""
import re
import sys
from pathlib import Path

from reportlab.lib.colors import HexColor, white
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.pdfmetrics import registerFontFamily
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas as rl_canvas
from reportlab.platypus import (Flowable, KeepTogether, ListFlowable, ListItem, Paragraph, SimpleDocTemplate, Spacer, Table,
                                TableStyle)

FD = "/usr/share/fonts/truetype/liberation/"
for n, f in [("LS", "Regular"), ("LSB", "Bold"), ("LSI", "Italic"), ("LSBI", "BoldItalic")]:
    pdfmetrics.registerFont(TTFont(n, FD + "LiberationSans-%s.ttf" % f))
registerFontFamily("LS", normal="LS", bold="LSB", italic="LSI", boldItalic="LSBI")

DARK = HexColor("#262a31")
GREY = HexColor("#6b717a")
GREY_L = HexColor("#f1f2f4")
GREY_M = HexColor("#d5d8dd")
FAM_COL = {"voiture": HexColor("#2f6fd6"), "deux-roues": HexColor("#f08a00"), "commun": HexColor("#5b6b7a"), "test": HexColor("#9b2fd6")}
CALL = {"DANGER": (HexColor("#fbe3e3"), HexColor("#d7262e")), "ATTENTION": (HexColor("#fdf0dc"), HexColor("#f08a00")),
        "INFO": (HexColor("#eef2f7"), HexColor("#5b6b7a"))}

W, H = A4
M = 22 * mm

S = {
    "h1": ParagraphStyle("h1", fontName="LSB", fontSize=12.5, leading=16, spaceBefore=10, spaceAfter=5, textColor=DARK),
    "h2": ParagraphStyle("h2", fontName="LSB", fontSize=10, leading=13, spaceBefore=7, spaceAfter=3, textColor=DARK),
    "p": ParagraphStyle("p", fontName="LS", fontSize=9, leading=12.6, spaceAfter=5, textColor=DARK),
    "li": ParagraphStyle("li", fontName="LS", fontSize=9, leading=12.4, textColor=DARK),
    "th": ParagraphStyle("th", fontName="LSB", fontSize=8, leading=10, textColor=white),
    "td": ParagraphStyle("td", fontName="LS", fontSize=8, leading=10, textColor=DARK),
    "cap": ParagraphStyle("cap", fontName="LSI", fontSize=7.6, leading=9.6, textColor=GREY, spaceAfter=6),
    "call": ParagraphStyle("call", fontName="LS", fontSize=8.6, leading=11.4, textColor=DARK),
    "src": ParagraphStyle("src", fontName="LS", fontSize=7.6, leading=9.8, textColor=DARK),
    "title": ParagraphStyle("title", fontName="LSB", fontSize=17, leading=21, textColor=DARK, spaceAfter=4),
    "meta": ParagraphStyle("meta", fontName="LS", fontSize=8, leading=10.5, textColor=GREY),
}


def inline(t):
    t = t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    t = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", t)
    t = re.sub(r"(?<![\w*])\*(?!\s)(.+?)(?<!\s)\*(?![\w*])", r"<i>\1</i>", t)
    t = re.sub(r"`(.+?)`", r"<font face='Courier'>\1</font>", t)
    return t


class Callout(Flowable):
    def __init__(self, kind, text, width):
        super().__init__()
        self.kind, self.width_ = kind, width
        bg, col = CALL[kind]
        self.bg, self.col = bg, col
        self.p = Paragraph("<b><font color='%s'>%s</font></b> : %s" % (col.hexval().replace("0x", "#"), kind, inline(text)), S["call"])

    def wrap(self, aw, ah):
        _, h = self.p.wrap(self.width_ - 18, ah)
        self.h = h + 12
        return self.width_, self.h

    def draw(self):
        c = self.canv
        c.setFillColor(self.bg)
        c.rect(0, 0, self.width_, self.h, fill=1, stroke=0)
        c.setFillColor(self.col)
        c.rect(0, 0, 3, self.h, fill=1, stroke=0)
        self.p.drawOn(c, 12, 6)


class Fig(Flowable):
    def __init__(self, name, width, height, fn):
        super().__init__()
        self.name, self.w, self.h, self.fn = name, width, height, fn

    def wrap(self, aw, ah):
        return self.w, self.h

    def draw(self):
        c = self.canv
        c.setFillColor(GREY_L)
        c.setStrokeColor(GREY_M)
        c.roundRect(0, 0, self.w, self.h, 4, fill=1, stroke=1)
        self.fn(c, self.w, self.h)


def parse(md):
    m = re.match(r"---\n(.*?)\n---\n(.*)", md, re.S)
    meta = {}
    for line in m.group(1).splitlines():
        k, _, v = line.partition(":")
        meta[k.strip()] = v.strip()
    return meta, m.group(2)


def build_story(body, meta, width):
    import figures
    story = []
    lines = body.splitlines()
    i = 0
    fig_count = {"n": 0}
    while i < len(lines):
        ln = lines[i].rstrip()
        if not ln.strip():
            i += 1
            continue
        if ln.startswith("## "):
            story.append(Paragraph(inline(ln[3:]), S["h2"]))
            i += 1
        elif ln.startswith("# "):
            story.append(Paragraph(inline(ln[2:]), S["h1"]))
            i += 1
        elif ln.startswith("> "):
            kind, _, txt = ln[2:].partition(":")
            story.append(Spacer(1, 2))
            story.append(Callout(kind.strip(), txt.strip(), width))
            story.append(Spacer(1, 6))
            i += 1
        elif ln.startswith("[FIG:"):
            name, _, cap = ln[5:-1].partition("|")
            fig_count["n"] += 1
            fn, h = figures.FIGS[name.strip()]
            story.append(KeepTogether([Fig(name, width, h, fn),
                                       Paragraph("<b>Figure %d</b> : %s" % (fig_count["n"], inline(cap.strip())), S["cap"])]))
            i += 1
        elif ln.startswith("|"):
            rows = []
            while i < len(lines) and lines[i].startswith("|"):
                cells = [x.strip() for x in lines[i].strip().strip("|").split("|")]
                if not all(re.fullmatch(r":?-{2,}:?", x) for x in cells):
                    rows.append(cells)
                i += 1
            ncol = len(rows[0])
            data = [[Paragraph(inline(x), S["th"] if r == 0 else S["td"]) for x in row + [""] * (ncol - len(row))] for r, row in enumerate(rows)]
            lens = [max(len(row[k]) if k < len(row) else 0 for row in rows) + 4 for k in range(ncol)]
            tot = sum(lens)
            cw = [max(width * l / tot, 45) for l in lens]
            sc = width / sum(cw)
            cw = [x * sc for x in cw]
            t = Table(data, colWidths=cw, repeatRows=1)
            sty = [("GRID", (0, 0), (-1, -1), 0.4, GREY_M), ("BACKGROUND", (0, 0), (-1, 0), DARK), ("VALIGN", (0, 0), (-1, -1), "TOP"),
                   ("TOPPADDING", (0, 0), (-1, -1), 2.5), ("BOTTOMPADDING", (0, 0), (-1, -1), 2.5)]
            for r in range(2, len(data), 2):
                sty.append(("BACKGROUND", (0, r), (-1, r), GREY_L))
            t.setStyle(TableStyle(sty))
            story.append(t)
            story.append(Spacer(1, 7))
        elif re.match(r"^(- |\d+\. )", ln):
            numbered = bool(re.match(r"^\d+\. ", ln))
            items = []
            while i < len(lines) and re.match(r"^(- |\d+\. )", lines[i]):
                txt = re.sub(r"^(- |\d+\. )", "", lines[i].rstrip())
                items.append(ListItem(Paragraph(inline(txt), S["li"]), leftIndent=14))
                i += 1
            story.append(ListFlowable(items, bulletType="1" if numbered else "bullet", start="1" if numbered else None,
                                      bulletFontName="LSB" if numbered else "LS", bulletFontSize=8.5, leftIndent=14,
                                      bulletColor=DARK))
            story.append(Spacer(1, 5))
        else:
            buf = [ln]
            i += 1
            while i < len(lines) and lines[i].strip() and not re.match(r"^(#|>|\||- |\d+\. |\[FIG:)", lines[i]):
                buf.append(lines[i].rstrip())
                i += 1
            story.append(Paragraph(inline(" ".join(buf)), S["p"]))
    return story


def make_canvas(meta):
    fam = meta.get("famille", "commun")
    col = FAM_COL.get(fam, DARK)

    class NC(rl_canvas.Canvas):
        def __init__(self, *a, **k):
            super().__init__(*a, **k)
            self._pages = []

        def showPage(self):
            self._pages.append(dict(self.__dict__))
            self._startPage()

        def save(self):
            n = len(self._pages)
            for st in self._pages:
                self.__dict__.update(st)
                self.deco(n)
                super().showPage()
            super().save()

        def deco(self, total):
            self.setFillColor(DARK)
            self.rect(0, H - 20, W, 20, fill=1, stroke=0)
            self.setFillColor(col)
            self.rect(0, H - 22, W, 2, fill=1, stroke=0)
            self.setFillColor(white)
            self.setFont("LSB", 8)
            self.drawString(M, H - 13.5, "MaintiDoc  |  %s" % meta["doc_id"])
            self.setFont("LS", 7)
            self.drawRightString(W - M, H - 13.5, "%s  |  %s  |  v%s" % (fam, meta.get("equip", meta.get("modele", "-")), meta.get("version", "1.0")))
            self.setStrokeColor(GREY_M)
            self.setLineWidth(0.5)
            self.line(M, 30, W - M, 30)
            self.setFillColor(GREY)
            self.setFont("LS", 6.6)
            self.drawString(M, 21, "Corpus MaintiDoc - document de travail. %s" % meta.get("pied", "Rédigé avec assistance IA, vérifié par l'équipe (voir inventaire.csv)."))
            self.setFillColor(DARK)
            self.setFont("LSB", 7.2)
            self.drawRightString(W - M, 21, "Page %d / %d" % (self._pageNumber, total))
    return NC


def render(md_path, out_dir):
    md = Path(md_path).read_text(encoding="utf-8")
    meta, body = parse(md)
    out = Path(out_dir) / ("%s.pdf" % meta["doc_id"])
    doc = SimpleDocTemplate(str(out), pagesize=A4, leftMargin=M, rightMargin=M, topMargin=30 * mm, bottomMargin=17 * mm,
                            title="%s - %s" % (meta["doc_id"], meta["titre"]), author="Équipe MaintiDoc",
                            subject=meta.get("type", ""), creator="MaintiDoc corpus builder")
    width = W - 2 * M
    story = [Paragraph(inline(meta["titre"]), S["title"])]
    story.append(Paragraph("<b>%s</b>  |  Type : %s  |  Famille : %s  |  Modèle(s) : %s  |  Langue : fr  |  Licence : %s" % (
        meta["doc_id"], meta.get("type", "-"), meta.get("famille", "-"), meta.get("modele", "-"), meta.get("licence", "-")), S["meta"]))
    story.append(Spacer(1, 8))
    story += build_story(body, meta, width)
    if meta.get("sources"):
        story.append(Paragraph("Sources", S["h1"]))
        rows = [[Paragraph("N°", S["th"]), Paragraph("Source", S["th"])]]
        for k, s in enumerate([x.strip() for x in meta["sources"].split(" ; ") if x.strip()]):
            rows.append([Paragraph("[%d]" % (k + 1), S["src"]), Paragraph(inline(s), S["src"])])
        t = Table(rows, colWidths=[28, width - 28])
        t.setStyle(TableStyle([("GRID", (0, 0), (-1, -1), 0.4, GREY_M), ("BACKGROUND", (0, 0), (-1, 0), DARK), ("VALIGN", (0, 0), (-1, -1), "TOP")]))
        story.append(t)
    doc.build(story, canvasmaker=make_canvas(meta))
    return meta, out


if __name__ == "__main__":
    for p in sys.argv[2:]:
        print(render(p, sys.argv[1])[1])
