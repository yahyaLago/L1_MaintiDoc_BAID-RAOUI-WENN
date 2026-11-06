# -*- coding: utf-8 -*-
"""Prépare le ZIP du livrable 1 au nommage exact des consignes et vérifie l'inventaire.

Usage :
    python finaliser_l1.py NOMEQUIPE --depuis <dossier L1_MaintiDoc_BAID-RAOUI-WENN> [--sans-verif]

NOMEQUIPE : noms de famille des membres, en majuscules, sans accents ni espaces,
ordre alphabétique, séparés par un tiret simple (ex. ALAMI-IDRISSI).
"""
import argparse
import csv
import re
import shutil
import sys
import unicodedata
from pathlib import Path


def norm_team(s):
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode()
    parts = sorted(p.strip().upper().replace(" ", "") for p in s.split("-") if p.strip())
    return "-".join(parts)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("equipe")
    ap.add_argument("--depuis", default="L1_MaintiDoc_BAID-RAOUI-WENN")
    ap.add_argument("--sans-verif", action="store_true", help="ne pas bloquer si verifie_par est vide")
    a = ap.parse_args()
    team = norm_team(a.equipe)
    src = Path(a.depuis)
    old = src.name.replace("L1_MaintiDoc_", "")
    root = Path("L1_MaintiDoc_%s" % team)
    if root.resolve() != src.resolve():
        if root.exists():
            shutil.rmtree(root)
        shutil.copytree(src, root)
    for p in sorted(root.rglob("*"), key=lambda x: -len(x.parts)):
        if old in p.name:
            p.rename(p.with_name(p.name.replace(old, team)))
    readme = root / "README.md"
    readme.write_text(readme.read_text(encoding="utf-8").replace(old, team), encoding="utf-8")
    corpus = root / ("L1_MaintiDoc_%s_Corpus" % team)
    errors, warnings = [], []
    rows = list(csv.DictReader(open(corpus / "inventaire.csv", encoding="utf-8")))
    listed = {r["fichier"] for r in rows}
    on_disk = {str(p.relative_to(corpus)).replace("\\", "/") for p in (corpus / "documents").rglob("*") if p.is_file()}
    ids = {r["document_id"] for r in rows}
    imgs = {p.stem for p in (corpus / "images").glob("*") if p.is_file() and p.name != ".gitkeep"}
    for im in sorted(imgs - ids):
        errors.append("image sans document correspondant (images/<document_id>.jpg) : " + im)
    for r in rows:
        if "images/%s." % r["document_id"] in r.get("remarques", "") and r["document_id"] not in imgs:
            errors.append("image annoncée mais absente : images/%s.jpg" % r["document_id"])
    for f in sorted(on_disk - listed):
        errors.append("fichier absent de l'inventaire : " + f)
    for f in sorted(listed - on_disk):
        errors.append("ligne d'inventaire sans fichier : " + f)
    for r in rows:
        if Path(r["fichier"]).stem != r["document_id"]:
            errors.append("nom de fichier différent du document_id : " + r["fichier"])
        if not re.fullmatch(r"[a-z0-9_]+", r["document_id"]):
            errors.append("document_id non conforme : " + r["document_id"])
        if not r["verifie_par"].strip() or r["verifie_par"].strip().lower().startswith(("à compléter", "a completer", "a compléter", "relecture en cours")):
            (warnings if a.sans_verif else errors).append("verifie_par vide : " + r["document_id"])
    rapport = root / ("L1_MaintiDoc_%s_Rapport.pdf" % team)
    if not rapport.exists():
        errors.append("rapport manquant : " + rapport.name)
    lien = (root / ("L1_MaintiDoc_%s_LienGitHub.txt" % team)).read_text(encoding="utf-8").strip()
    if "<compte>" in lien:
        errors.append("lien GitHub à remplacer dans " + "L1_MaintiDoc_%s_LienGitHub.txt" % team)
    for w in warnings:
        print("AVERTISSEMENT :", w)
    if errors:
        print("\n".join("ERREUR : " + e for e in errors))
        print("\n%d erreur(s) : corrige-les puis relance. Dossier préparé : %s" % (len(errors), root))
        sys.exit(1)
    shutil.make_archive(str(root), "zip", root_dir=".", base_dir=root.name)
    print("ZIP prêt :", root.name + ".zip")


if __name__ == "__main__":
    main()
