# -*- coding: utf-8 -*-
"""Construit le corpus mono-famille Honda SH150i (20 fiches-problèmes avec image réelle).

Usage : python build_corpus_sh150.py <manuel_proprietaire_32K0RA000.pdf> <dossier_sortie>
Sortie : <dossier>/documents/famille_1/*.pdf, images/*.jpg, inventaire.csv, outils/photos_sources.csv
"""
import csv
import os
import shutil
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
MANUAL, OUT = sys.argv[1], Path(sys.argv[2])


def main():
    if OUT.exists():
        shutil.rmtree(OUT)
    for sub in ("documents/famille_1", "images", "outils"):
        (OUT / sub).mkdir(parents=True)
    tmp = Path("/tmp/sh150_figs")
    shutil.rmtree(tmp, ignore_errors=True)
    subprocess.run([sys.executable, str(HERE / "extraire_figures_honda.py"), MANUAL, str(tmp)], check=True, capture_output=True)
    sys.path.insert(0, str(HERE))
    from extraire_figures_honda import FIG
    figcred = {r["cle"]: r for r in csv.DictReader(open(tmp / "credits.csv", encoding="utf-8"))}

    sys.argv = ["x", str(OUT / "documents/famille_1"), str(OUT / "images"), str(OUT / "outils/photos_sources.csv")]
    import build_sh150_20 as B
    srcrows = []
    for s in B.SPECS:
        key = s["photo"]
        page, _, desc = FIG[key]
        shutil.copy(tmp / (key + ".jpg"), OUT / "images" / (s["id"] + ".jpg"))
        cr = figcred[key]
        srcrows.append(dict(document_id=s["id"], auteur=cr["auteur"], licence=cr["licence"], url=cr["url"]))
        s["photo_desc"] = "%s (Honda SH150i 2020-2024, manuel du propriétaire, page imprimée %d)" % (desc, page - 4)
    with open(OUT / "outils/photos_sources.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["document_id", "auteur", "licence", "url"])
        w.writeheader()
        w.writerows(srcrows)
    B.CREDITS = B.load_credits()

    rows = []
    for i, s in enumerate(B.SPECS):
        dest = OUT / "documents/famille_1" / (s["id"] + ".pdf")
        n = B.build(s, i + 1, str(dest))
        vis = "photo réelle p.1 (fig 1) ; schéma p.1 (fig 2) ; schéma de diagnostic (fig 3)"
        if s.get("fig2"):
            vis += " ; schéma (fig 4)"
        vis += " ; tableaux"
        page = FIG[s["photo"]][0] - 4
        rem = "Photo : figure du manuel du propriétaire Honda, page imprimée %d (images/%s.jpg)" % (page, s["id"])
        if s["usage"] == "ambigu":
            rem = "cas ambigu : « le moteur cale » peut décrire l'Idling Stop (normal) ou une panne ; l'assistant doit demander ; " + rem
        rows.append(dict(document_id=s["id"], fichier="documents/famille_1/%s.pdf" % s["id"], titre="%s (Honda SH150i 2020-2024)" % s["titre"],
                         famille_equipement="deux_roues", equipement_id=B.EQ, type_document="procedure", version="v1.0 (2026-11)",
                         nb_pages=n, langue="fr", format="pdf_texte", elements_visuels=vis,
                         provenance="synthetique ; valeurs et photo issues de : Honda, manuel du propriétaire SH125/SH150 21YM réf. 32K0RA000, pages imprimées %s et %d, fourni par l'équipe" % (s["pages"], page),
                         licence="texte et schémas : CC BY 4.0 (équipe) ; photo : © Honda, extrait cité à des fins pédagogiques, à valider par l'enseignante",
                         genere_par_ia="oui", outil_ia="Claude Opus 5.5 (prompt P16)", verifie_par="à compléter",
                         corrections="aucune (relecture équipe à faire)", groupe_acces="techniciens_moto ; responsables",
                         usage_test=s["usage"], remarques=rem))
    cols = ["document_id", "fichier", "titre", "famille_equipement", "equipement_id", "type_document", "version", "nb_pages", "langue", "format",
            "elements_visuels", "provenance", "licence", "genere_par_ia", "outil_ia", "verifie_par", "corrections", "groupe_acces", "usage_test", "remarques"]
    with open(OUT / "inventaire.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader()
        w.writerows(rows)
    for f in ("build_corpus_sh150.py", "build_sh150_20.py", "extraire_figures_honda.py", "dessin.py", "build_manuel_2021.py"):
        shutil.copy(HERE / f, OUT / "outils" / f)
    print(len(rows), "fiches", sorted({r["nb_pages"] for r in rows}))


if __name__ == "__main__":
    main()
