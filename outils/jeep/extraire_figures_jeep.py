# -*- coding: utf-8 -*-
"""Extrait du manuel du propriétaire Jeep Wrangler 2026 (105655_26_JL_OM_EN_USC, édition E2) l'image utilisée par chaque fiche.
Usage : python extraire_figures_jeep.py <manuel.pdf> <dossier>   ->  <cle>.jpg + credits.csv
Page imprimée = page PDF - 2."""
import csv, os, sys
import pymupdf as fitz

def tt(p, x0, y0):  # bloc témoin : pictogramme + titre + début de description, dans une colonne
    return (p, [x0 - 3, y0 - 4, x0 + 168, min(y0 + 60, 346)])

FIG = {
 "jl_temoin_moteur_mil":            tt(141, 36, 221) + ("témoin Engine Check / MIL et sa description",),
 "jl_temoin_temperature_moteur":    tt(138, 215, 270) + ("témoin de température du liquide de refroidissement",),
 "jl_temoin_pression_huile":        tt(138, 393, 281) + ("témoin de pression d'huile",),
 "jl_temoin_charge_batterie":       tt(138, 36, 36) + ("témoin de charge de la batterie",),
 "jl_batterie_dechargee":           (247, [212, 51, 382, 152], "borne positive (+) de la batterie, compartiment moteur"),
 "jl_moteur_ne_demarre_pas":        (160, [405, 66, 561, 166], "bouton Start (OFF, ACC, RUN)"),
 "jl_temoin_frein":                 tt(137, 215, 91) + ("témoin de frein (rouge)",),
 "jl_temoin_abs":                   tt(140, 215, 54) + ("témoin ABS (jaune)",),
 "jl_temoin_tpms":                  tt(142, 36, 82) + ("témoin de surveillance de pression des pneus (TPMS)",),
 "jl_crevaison_roue_secours":       (244, [226, 30, 382, 128], "dépose de la roue de secours"),
 "jl_usure_pneus":                  (313, [390, 170, 561, 273], "témoins d'usure de la bande de roulement"),
 "jl_vidange_huile":                (268, [114, 44, 480, 236], "compartiment moteur 3.6L : jauge d'huile (repère 3) et bouchon de remplissage (repère 4)"),
 "jl_filtre_air":                   (272, [405, 30, 561, 140], "couvercle du filtre à air moteur"),
 "jl_niveau_liquide_refroidissement": (266, [114, 72, 480, 262], "compartiment moteur 2.0L : réservoir de liquide de refroidissement (repère 4)"),
 "jl_fusible_grille":               (286, [33, 30, 204, 126], "emplacement du boîtier de distribution (Power Distribution Center)"),
 "jl_temoin_esc":                   tt(140, 215, 277) + ("témoin ESC actif",),
 "jl_4x4_ne_s_engage_pas":          (177, [390, 32, 561, 134], "levier de boîte de transfert"),
 "jl_temoin_airbag":                tt(137, 36, 285) + ("témoin d'airbag",),
 "jl_temoin_temperature_transmission": tt(139, 393, 187) + ("témoin de température de transmission",),
 "jl_niveau_liquide_frein":         (268, [114, 44, 480, 236], "compartiment moteur 3.6L : réservoir de liquide de frein (repère 6)"),
}

def main(manual, out):
    os.makedirs(out, exist_ok=True)
    d = fitz.open(manual)
    rows = []
    for key, (p, box, desc) in FIG.items():
        d[p - 1].get_pixmap(dpi=240, clip=fitz.Rect(*box)).save(os.path.join(out, key + ".jpg"), jpg_quality=88)
        rows.append(dict(cle=key, auteur="FCA US LLC (Stellantis)",
                         licence="© FCA US LLC, tous droits réservés ; extrait cité à des fins pédagogiques, usage interne, à valider par l'enseignante",
                         url="manuel du propriétaire Jeep Wrangler 2026 (105655_26_JL_OM_EN_USC, E2), page imprimée %d (page PDF %d) : %s" % (p - 2, p, desc)))
    with open(os.path.join(out, "credits.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["cle", "auteur", "licence", "url"]); w.writeheader(); w.writerows(rows)
    print(len(rows), "figures")

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
