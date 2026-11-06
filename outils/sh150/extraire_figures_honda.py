# -*- coding: utf-8 -*-
"""Extrait de la manuel du propriétaire Honda SH125/SH150 21YM (32K0RA000) la figure utilisée par chaque fiche SH150.
Usage : python extraire_figures_honda.py <manuel.pdf> <dossier_photos>
Écrit <cle>.jpg et credits.csv (page PDF et page imprimée = page PDF - 4)."""
import csv, os, sys
import pymupdf as fitz

# cle : (page PDF, zone [x0, y0, x1, y1] en points, description)
FIG = {
 "sh150_tableau_voyant_injection":  (44, [26, 60, 214, 184], "instrumentation SH150AD, voyant PGM-FI (MIL)"),
 "sh150_tableau_voyant_injection_clignotant": (44, [26, 60, 214, 184], "instrumentation SH150AD, voyant PGM-FI (MIL)"),
 "sh150_vase_expansion":            (106, [214, 32, 382, 157], "vase d'expansion du liquide de refroidissement, repères UPPER / LOWER"),
 "sh150_bequille_laterale":         (111, [28, 55, 198, 178], "béquille latérale et ressort"),
 "sh150_smart_key_pile":            (50, [212, 30, 340, 145], "Honda SMART Key : LED et bouton ON/OFF"),
 "sh150_commande_contact":          (55, [205, 62, 385, 160], "commande de contact : positions On, SEAT FUEL, Off, Lock"),
 "sh150_commutateur_idling_stop":   (46, [24, 40, 395, 158], "commodos : commutateur Idling Stop, boutons INFO A / INFO B, démarreur"),
 "sh150_tableau_idling_stop":       (59, [210, 182, 392, 280], "commutateur et témoin Idling Stop"),
 "sh150_tableau_temoin_abs":        (45, [28, 118, 220, 244], "instrumentation SH150AD, témoin ABS"),
 "sh150_tableau_temoin_hstc":       (62, [214, 64, 395, 178], "commutateur et témoin Torque Control (HSTC)"),
 "sh150_jauge_huile":               (102, [210, 32, 356, 147], "jauge-bouchon d'huile, repères haut et bas"),
 "sh150_ecran_entretien":           (104, [218, 31, 388, 265], "vidange : vis de vidange, crépine d'huile, joint torique"),
 "sh150_valve_pneu_avant":          (13, [45, 25, 410, 250], "étiquette d'information pneus et charge"),
 "sh150_pneu_arriere_usure":        (24, [22, 118, 145, 236], "roue arrière et pneu (vue des emplacements)"),
 "sh150_bougie":                    (100, [218, 44, 377, 176], "capuchon de bougie et accès bougie"),
 "sh150_reservoir_frein":           (109, [222, 34, 395, 251], "réservoirs de liquide de frein avant et arrière, repère LOWER"),
 "sh150_etrier_plaquettes":         (110, [30, 104, 207, 240], "plaquettes de frein et témoins d'usure"),
 "sh150_batterie":                  (95, [30, 62, 203, 193], "batterie sous le couvercle du plancher"),
 "sh150_boite_fusibles":            (140, [213, 50, 380, 214], "boîte à fusibles, fusible principal, fusibles de rechange"),
 "sh150_carter_transmission":       (24, [20, 30, 385, 265], "emplacement des éléments (vue côté gauche)"),
}

def main(manual, out):
    os.makedirs(out, exist_ok=True)
    d = fitz.open(manual)
    rows = []
    for key, (p, box, desc) in FIG.items():
        pg = d[p - 1]
        pix = pg.get_pixmap(dpi=220, clip=fitz.Rect(*box))
        pix.save(os.path.join(out, key + ".jpg"), jpg_quality=88)
        rows.append(dict(cle=key, auteur="Honda Motor Co., Ltd.",
                         licence="© Honda, tous droits réservés ; extrait cité à des fins pédagogiques, usage interne, à valider par l'enseignante",
                         url="manuel du propriétaire SH125/SH150 21YM réf. 32K0RA000, page imprimée %d (page PDF %d) : %s" % (p - 4, p, desc)))
    with open(os.path.join(out, "credits.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["cle", "auteur", "licence", "url"])
        w.writeheader(); w.writerows(rows)
    print(len(rows), "figures")

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
