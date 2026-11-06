# Traçabilité de l'usage de l'IA - corpus MaintiDoc (livrable 1)

| Élément | Valeur |
|---|---|
| Outil | Claude Opus 5.5 (Anthropic), interface claude.ai |
| Période | 2026-11-04 au 2026-11-06 |
| Documents | 46 : 24 en famille_1 (voiture : Jeep Wrangler JL 2026), 22 en famille_2 (deux_roues : Honda SH150i 2020-2024) |
| Accès restreint | `interne_grille_tarifaire`, `interne_garantie_fournisseurs` (groupe responsables, codes de test de fuite) |
| Fiches-problèmes | 20 Jeep (`jl_*`) + 20 Honda (`sh150_*`), 2 pages chacune, une image réelle par fiche |
| Cas de test | 2 contradictoires (`proc_lecture_obd_v1` / `v2`), 2 injections (`note_vidange_piegee`, `bulletin_technique_piege_scan`), 2 ambigus (`jl_moteur_ne_demarre_pas`, `sh150_moteur_coupe_au_feu`) |
| Sources fournies par l'équipe | manuel du propriétaire Jeep Wrangler 2026 (105655_26_JL_OM_EN_USC, E2) ; manuel du propriétaire Honda SH125/SH150 21YM (32K0RA000) |
| Équipe | Yahya BAID (famille moto), Ahmed RAOUI (combinaison des deux familles), Wenn BOUKA (famille voiture) |
| Vérification | humaine, croisée : les fiches voiture sont relues par Yahya BAID, les fiches moto par Wenn BOUKA (colonnes `verifie_par` et `corrections`) |

## Prompts des documents de test

### P03 - Procédure générique

```
Rédige en français une procédure d'atelier générique « {sujet} » pour la famille {famille}
(modèles {modèles}). Structure : domaine d'application, encadré DANGER, étapes numérotées,
tableau d'interprétation, encadrés ATTENTION / INFO, schéma si utile. Aucune valeur chiffrée
propre à un modèle ; renvoyer au manuel du propriétaire ou à la fiche {document_id}.
Signaler les opérations réservées à un technicien habilité.
```

### P09 - Documents internes fictifs à accès restreint

```
Rédige un document interne d'atelier « {sujet} » réservé au groupe responsables, avec des
données FICTIVES signalées comme telles. Pour l'historique, utilise les equipement_id
JEEP-WRA-01, JEEP-COM-01, JEEP-REN-01, SH150-18-01, SH300-01, PCX125-01, identiques à ceux
du serveur MCP. Ajoute un code de test unique ({code}) pour détecter une fuite entre groupes.
```

### P10 - Documents piégés (injection de prompt)

```
Rédige un document de test qui ressemble à {forme} mais contient une instruction
malveillante : {instruction}. Ajoute un avertissement pour l'équipe et les critères de
réussite du test. Le document est signalé « injection » dans l'inventaire.
```

### P12 - Simulation de documents scannés

```
Transforme {document_id} en PDF scanné : pages rastérisées à 110 dpi, niveaux de gris,
légère rotation, bruit et ombrage, aucune couche texte. Pour la check-list, ajoute des
annotations manuscrites simulées cohérentes avec historique_interventions (JEEP-WRA-01,
55 900 km, codes P0300 et P0303).
```

### P13 - Version contradictoire d'une procédure

```
Rédige la version 1 (2025-01) de la procédure de lecture OBD-II à la réception. Elle diffère
de la version 2 sur un point : elle efface tous les codes dès la réception. Ne signale pas
la contradiction dans le texte ; elle est signalée dans l'inventaire.
```

## Prompts de la famille deux-roues (Honda SH150i)

### P15 — Lecture du manuel du propriétaire
```
Lis le manuel du propriétaire Honda SH125/SH150 21YM (réf. 32K0RA000) fourni par l'équipe.
Relève, pour la SH150AD 2020-2024, le comportement des témoins, la SMART Key, l'Idling Stop,
le HSTC, le démarrage, le programme d'entretien, l'huile, le refroidissement, les pneus,
la bougie, les freins et l'ABS, la batterie et les fusibles. Pour chaque valeur, note la page
imprimée (« MP p. N »). Reformule en français ; ne recopie pas le texte Honda.
```

### P16 — 20 fiches-problèmes, une seule famille, avec images réelles
```
À partir des relevés de P15, produis 20 fiches PDF de 2 à 3 pages pour la seule famille moto
(Honda SH150). Chaque fiche traite UN problème vu par le mécanicien, sur le modèle du corpus
imprimantes : tableau d'identification, symptôme, Figure 1 = image réelle du SH150 tirée du
manuel du propriétaire (page citée), schéma de l'équipe, signification et gravité, consigne
de sécurité, diagnostic pas à pas, procédure, valeurs de référence avec page, négatif
difficile, ce que la fiche ne contient pas, sources. Aucune valeur sans page citée.
Une fiche ambiguë (« le moteur cale »).
```

## Prompts de la famille voiture (Jeep Wrangler)

### P17 — Lecture du manuel du propriétaire Jeep
```
Lis le manuel du propriétaire Jeep Wrangler 2026 (105655_26_JL_OM_EN_USC, E2) fourni par l'équipe.
Relève les témoins (rouges et jaunes), le démarrage, le démarrage avec câbles, la surchauffe,
la boîte de transfert, les pneus et le TPMS, le changement de roue, le programme d'entretien,
l'huile, le filtre à air, le refroidissement, le freinage, les fusibles, les capacités et couples.
Pour chaque valeur, note la page imprimée (« OM p. N », page PDF - 2). Reformule en français.
```

### P18 — 20 fiches-problèmes Jeep avec images réelles
```
Fais pour le Jeep Wrangler 2026 le même travail que pour la Honda SH150 : 20 fiches PDF de 2 pages,
une seule famille (voiture), un problème par fiche. Même structure : identification, symptôme,
Figure 1 = image réelle tirée du manuel (page citée), schéma de l'équipe, signification et gravité,
sécurité, diagnostic pas à pas, procédure, valeurs avec page, négatif difficile, ce que la fiche
ne contient pas, sources. Valeurs converties en unités métriques quand le manuel les donne.
Une fiche ambiguë (« il ne démarre pas »).
```

## Correspondance document - prompt

| document_id | Prompt | Pages du manuel citées |
|---|---|---|
| jl_temoin_moteur_mil | P17 + P18 | 139, 143 ; image p. 139 |
| jl_temoin_temperature_moteur | P17 + P18 | 136, 247, 280, 332 ; image p. 136 |
| jl_temoin_pression_huile | P17 + P18 | 136, 137, 269, 329, 332 ; image p. 136 |
| jl_temoin_charge_batterie | P17 + P18 | 136 ; image p. 136 |
| jl_batterie_dechargee | P17 + P18 | 244, 245, 246 ; image p. 245 |
| jl_moteur_ne_demarre_pas | P17 + P18 | 158, 160, 161 ; image p. 158 |
| jl_temoin_frein | P17 + P18 | 135, 281, 331 ; image p. 135 |
| jl_temoin_abs | P17 + P18 | 138 ; image p. 138 |
| jl_temoin_tpms | P17 + P18 | 140, 306, 310 ; image p. 140 |
| jl_crevaison_roue_secours | P17 + P18 | 241, 242, 244, 333 ; image p. 242 |
| jl_usure_pneus | P17 + P18 | 255, 311, 312 ; image p. 311 |
| jl_vidange_huile | P17 + P18 | 128, 131, 255, 329, 332 ; image p. 266 |
| jl_filtre_air | P17 + P18 | 255, 256, 270 ; image p. 270 |
| jl_niveau_liquide_refroidissement | P17 + P18 | 278, 280, 281, 332 ; image p. 264 |
| jl_fusible_grille | P17 + P18 | 283, 284 ; image p. 284 |
| jl_temoin_esc | P17 + P18 | 138 ; image p. 138 |
| jl_4x4_ne_s_engage_pas | P17 + P18 | 139, 175, 176, 177 ; image p. 175 |
| jl_temoin_airbag | P17 + P18 | 135 ; image p. 135 |
| jl_temoin_temperature_transmission | P17 + P18 | 137, 138 ; image p. 137 |
| jl_niveau_liquide_frein | P17 + P18 | 255, 281, 331 ; image p. 266 |
| sh150_voyant_injection_allume | P15 + P16 | 40, 117 ; image p. 40 |
| sh150_voyant_injection_clignote | P15 + P16 | 40, 117 ; image p. 40 |
| sh150_surchauffe_moteur | P15 + P16 | 40, 77, 102, 116, 153 ; image p. 102 |
| sh150_moteur_ne_demarre_pas | P15 + P16 | 59 ; image p. 107 |
| sh150_smart_key_pile_faible | P15 + P16 | 40, 112, 120 ; image p. 46 |
| sh150_smart_key_non_detectee | P15 + P16 | 59, 120, 129 ; image p. 51 |
| sh150_idling_stop_inactif | P15 + P16 | 55, 56, 122 ; image p. 42 |
| sh150_moteur_coupe_au_feu | P15 + P16 | 55, 56 ; image p. 55 |
| sh150_temoin_abs_allume | P15 + P16 | 41, 118 ; image p. 41 |
| sh150_temoin_hstc_allume | P15 + P16 | 41, 58, 119 ; image p. 58 |
| sh150_niveau_huile_bas | P15 + P16 | 98, 99, 153 ; image p. 98 |
| sh150_vidange_echeance | P15 + P16 | 39, 77, 99, 153, 154 ; image p. 100 |
| sh150_pression_pneus_basse | P15 + P16 | 153 ; image p. 9 |
| sh150_usure_pneus | P15 + P16 | 153 ; image p. 20 |
| sh150_bougie_ralenti_instable | P15 + P16 | 77, 153 ; image p. 96 |
| sh150_niveau_liquide_frein_bas | P15 + P16 | 78, 153 ; image p. 105 |
| sh150_usure_plaquettes | P15 + P16 | 78 ; image p. 106 |
| sh150_batterie_faible | P15 + P16 | 56, 59, 78, 152 ; image p. 91 |
| sh150_fusible_grille | P15 + P16 | 154 ; image p. 136 |
| sh150_perte_puissance | P15 + P16 | 58, 77, 78, 116, 117 ; image p. 20 |
| proc_lecture_obd_v1 | P13 | procédure générique, version contradictoire |
| proc_lecture_obd_v2 | P03 | procédure générique |
| bulletin_technique_piege_scan | P10 + P12 | document piégé scanné (Wrangler 4xe, cible simulée) |
| note_vidange_piegee | P10 | document piégé (SH150i 2021, cible simulée) |
| interne_grille_tarifaire, interne_garantie_fournisseurs | P09 | documents internes fictifs, accès responsables |

## Analyse critique de l'usage de l'IA

### Famille voiture (Jeep)

**Décalage de pages.** La page du PDF vaut la page imprimée + 2 ; toutes les références « OM p. N » ont été recalculées sur la page imprimée et vérifiées sur le texte du manuel.

**Valeur lue sur un tableau.** L'intervalle de remplacement du filtre à air (48 000 km / 30 000 miles) a été lu sur le tableau d'entretien (OM p. 256) en vérifiant visuellement les colonnes, car le texte extrait du PDF perdait l'alignement : à relire en priorité.

**Ce qui n'est pas inventé.** Les pressions de pneus ne sont pas chiffrées : le manuel renvoie à l'étiquette du montant B, qui dépend de la monte. Les couples absents du manuel du propriétaire (vis de vidange, étriers) ne sont pas donnés ; chaque fiche le dit dans « Ce que cette fiche ne contient pas ».

**Marché.** Le manuel est celui des États-Unis (édition USC, en anglais). Les versions vendues au Maroc peuvent différer (motorisations, équipements) : à signaler dans le rapport.

**Images.** Extraites du manuel du propriétaire Jeep (page citée), licence © FCA US LLC, usage pédagogique interne, **à valider par l'enseignante**. Pour les témoins, l'image est le pictogramme réel avec le début de sa description.

**Reste à faire par l'équipe.** Relire chaque fiche contre les pages citées, remplir `verifie_par` et `corrections`.

### Famille deux-roues (Honda)

**Point de départ écarté.** Un premier manuel illustré « Urbano S150 » avait été généré pour un scooter **fictif** : ses valeurs étaient inventées. Il n'a pas été renommé en SH150, car cela aurait mis des chiffres faux sur un modèle réel. Les fiches reprennent uniquement des valeurs relevées dans le manuel du propriétaire Honda, avec leur page.

**Documents fournis vérifiés.** Les trois fichiers « Service Repair Manual » étaient le même fichier (même empreinte) : le manuel d'atelier SH125/SH150 de **2005**, en italien, d'une autre génération ; il n'a pas servi aux valeurs. Le catalogue de pièces concerne la SH150i d'Australie et d'Indonésie, et le manuel SH Mode 125 un autre modèle : non utilisés.

**Erreurs de l'IA repérées et corrigées.** Une référence de page décalée (la page du PDF vaut la page imprimée + 4) a été corrigée. Les couples de serrage absents du manuel du propriétaire (bougie, axes de roue, étriers) ne sont pas donnés : chaque fiche le dit dans « Ce que cette fiche ne contient pas ».

**Images.** Les photos de presse, de vendeurs et de Google Images ont été écartées (pas de licence). Wikimedia Commons n'était pas accessible depuis l'environnement de l'IA. Les images retenues viennent du manuel du propriétaire Honda (page citée) : licence © Honda, usage pédagogique interne, **à valider par l'enseignante**.

**Reste à faire par l'équipe.** Relire chaque fiche contre les pages citées, remplir `verifie_par` et `corrections`, et remplacer si possible les images Honda par des photos de l'équipe.

### Recentrage du corpus

Les premières versions couvraient six modèles (Wrangler, Compass, Renegade, SH150i, SH300i, PCX125) avec des valeurs publiques sans manuel. Le corpus final est recentré sur **un modèle par famille**, pour lequel l'équipe a fourni le manuel du propriétaire : chaque valeur porte sa page, chaque fiche a une image réelle. Les documents de test (contradiction, injection, scan) ont été conservés et rattachés à ces deux modèles.

## Annexe : sources des images

Chaque fiche-problème contient une image réelle (Figure 1) extraite du manuel du propriétaire fourni par l'équipe. Fichier : `images/<document_id>.jpg`.

**Licence.** Images © FCA US LLC (Jeep) et © Honda Motor Co. (Honda), reprises comme extraits cités à des fins pédagogiques, usage interne. **À valider par l'enseignante** ; ne pas publier le dépôt en public avec ces images.

### Famille 1 : Jeep Wrangler JL 2026


#### N°01 — Témoin moteur (MIL) allumé
- Fichier : `images/jl_temoin_moteur_mil.jpg`
- Image : témoin Engine Check / MIL et sa description
- Source : manuel du propriétaire Jeep Wrangler 2026, page imprimée 139 (page 141 du PDF)
- Photo de l'équipe conseillée en remplacement : tableau de bord Wrangler avec le témoin moteur orange allumé, moteur tournant.

#### N°02 — Témoin de température moteur allumé (surchauffe)
- Fichier : `images/jl_temoin_temperature_moteur.jpg`
- Image : témoin de température du liquide de refroidissement
- Source : manuel du propriétaire Jeep Wrangler 2026, page imprimée 136 (page 138 du PDF)
- Photo de l'équipe conseillée en remplacement : aiguille de température vers H et témoin rouge allumé.

#### N°03 — Témoin de pression d'huile allumé
- Fichier : `images/jl_temoin_pression_huile.jpg`
- Image : témoin de pression d'huile
- Source : manuel du propriétaire Jeep Wrangler 2026, page imprimée 136 (page 138 du PDF)
- Photo de l'équipe conseillée en remplacement : témoin rouge de pression d'huile allumé au tableau de bord.

#### N°04 — Témoin de charge de la batterie allumé
- Fichier : `images/jl_temoin_charge_batterie.jpg`
- Image : témoin de charge de la batterie
- Source : manuel du propriétaire Jeep Wrangler 2026, page imprimée 136 (page 138 du PDF)
- Photo de l'équipe conseillée en remplacement : témoin rouge de batterie allumé, moteur tournant.

#### N°05 — Batterie déchargée : démarrage avec câbles
- Fichier : `images/jl_batterie_dechargee.jpg`
- Image : borne positive (+) de la batterie, compartiment moteur
- Source : manuel du propriétaire Jeep Wrangler 2026, page imprimée 245 (page 247 du PDF)
- Photo de l'équipe conseillée en remplacement : borne positive (+) de la batterie du Wrangler, capuchon soulevé.

#### N°06 — Le moteur ne démarre pas (bouton Start)
- Fichier : `images/jl_moteur_ne_demarre_pas.jpg`
- Image : bouton Start (OFF, ACC, RUN)
- Source : manuel du propriétaire Jeep Wrangler 2026, page imprimée 158 (page 160 du PDF)
- Photo de l'équipe conseillée en remplacement : bouton START/STOP du Wrangler avec les positions OFF, ACC, RUN.

#### N°07 — Témoin de frein rouge allumé
- Fichier : `images/jl_temoin_frein.jpg`
- Image : témoin de frein (rouge)
- Source : manuel du propriétaire Jeep Wrangler 2026, page imprimée 135 (page 137 du PDF)
- Photo de l'équipe conseillée en remplacement : témoin rouge BRAKE allumé au tableau de bord.

#### N°08 — Témoin ABS allumé
- Fichier : `images/jl_temoin_abs.jpg`
- Image : témoin ABS (jaune)
- Source : manuel du propriétaire Jeep Wrangler 2026, page imprimée 138 (page 140 du PDF)
- Photo de l'équipe conseillée en remplacement : témoin jaune ABS allumé au tableau de bord.

#### N°09 — Témoin de pression des pneus (TPMS) allumé
- Fichier : `images/jl_temoin_tpms.jpg`
- Image : témoin de surveillance de pression des pneus (TPMS)
- Source : manuel du propriétaire Jeep Wrangler 2026, page imprimée 140 (page 142 du PDF)
- Photo de l'équipe conseillée en remplacement : témoin TPMS et écran de pression des quatre pneus.

#### N°10 — Crevaison : pose de la roue de secours
- Fichier : `images/jl_crevaison_roue_secours.jpg`
- Image : dépose de la roue de secours
- Source : manuel du propriétaire Jeep Wrangler 2026, page imprimée 242 (page 244 du PDF)
- Photo de l'équipe conseillée en remplacement : dépose de la roue de secours montée sur le hayon du Wrangler.

#### N°11 — Pneus usés (témoins d'usure visibles)
- Fichier : `images/jl_usure_pneus.jpg`
- Image : témoins d'usure de la bande de roulement
- Source : manuel du propriétaire Jeep Wrangler 2026, page imprimée 311 (page 313 du PDF)
- Photo de l'équipe conseillée en remplacement : bande de roulement d'un pneu du Wrangler avec les témoins d'usure.

#### N°12 — Message « Oil Change Required » (vidange due)
- Fichier : `images/jl_vidange_huile.jpg`
- Image : compartiment moteur 3.6L : jauge d'huile (repère 3) et bouchon de remplissage (repère 4)
- Source : manuel du propriétaire Jeep Wrangler 2026, page imprimée 266 (page 268 du PDF)
- Photo de l'équipe conseillée en remplacement : compartiment moteur 3.6L : jauge et bouchon de remplissage d'huile.

#### N°13 — Filtre à air moteur encrassé
- Fichier : `images/jl_filtre_air.jpg`
- Image : couvercle du filtre à air moteur
- Source : manuel du propriétaire Jeep Wrangler 2026, page imprimée 270 (page 272 du PDF)
- Photo de l'équipe conseillée en remplacement : couvercle du filtre à air ouvert, filtre visible.

#### N°14 — Niveau de liquide de refroidissement bas
- Fichier : `images/jl_niveau_liquide_refroidissement.jpg`
- Image : compartiment moteur 2.0L : réservoir de liquide de refroidissement (repère 4)
- Source : manuel du propriétaire Jeep Wrangler 2026, page imprimée 264 (page 266 du PDF)
- Photo de l'équipe conseillée en remplacement : bocal de liquide de refroidissement, moteur froid, repères visibles.

#### N°15 — Un équipement électrique ne fonctionne plus (fusible)
- Fichier : `images/jl_fusible_grille.jpg`
- Image : emplacement du boîtier de distribution (Power Distribution Center)
- Source : manuel du propriétaire Jeep Wrangler 2026, page imprimée 284 (page 286 du PDF)
- Photo de l'équipe conseillée en remplacement : boîtier de distribution PDC dans le compartiment moteur, couvercle ouvert.

#### N°16 — Témoin ESC allumé en continu
- Fichier : `images/jl_temoin_esc.jpg`
- Image : témoin ESC actif
- Source : manuel du propriétaire Jeep Wrangler 2026, page imprimée 138 (page 140 du PDF)
- Photo de l'équipe conseillée en remplacement : témoin ESC (voiture qui dérape) allumé au tableau de bord.

#### N°17 — Le 4x4 (4L) ne s'engage pas
- Fichier : `images/jl_4x4_ne_s_engage_pas.jpg`
- Image : levier de boîte de transfert
- Source : manuel du propriétaire Jeep Wrangler 2026, page imprimée 175 (page 177 du PDF)
- Photo de l'équipe conseillée en remplacement : levier de boîte de transfert du Wrangler sur la console.

#### N°18 — Témoin d'airbag allumé
- Fichier : `images/jl_temoin_airbag.jpg`
- Image : témoin d'airbag
- Source : manuel du propriétaire Jeep Wrangler 2026, page imprimée 135 (page 137 du PDF)
- Photo de l'équipe conseillée en remplacement : témoin rouge d'airbag allumé au tableau de bord.

#### N°19 — Témoin de température de transmission allumé
- Fichier : `images/jl_temoin_temperature_transmission.jpg`
- Image : témoin de température de transmission
- Source : manuel du propriétaire Jeep Wrangler 2026, page imprimée 137 (page 139 du PDF)
- Photo de l'équipe conseillée en remplacement : témoin de température de transmission allumé, par exemple en traction de remorque.

#### N°20 — Niveau de liquide de frein bas
- Fichier : `images/jl_niveau_liquide_frein.jpg`
- Image : compartiment moteur 3.6L : réservoir de liquide de frein (repère 6)
- Source : manuel du propriétaire Jeep Wrangler 2026, page imprimée 266 (page 268 du PDF)
- Photo de l'équipe conseillée en remplacement : réservoir du maître-cylindre de frein, repères de niveau visibles.

### Famille 2 : Honda SH150i 2020-2024


#### N°01 — Voyant d'injection PGM-FI allumé fixe
- Fichier : `images/sh150_voyant_injection_allume.jpg`
- Image : instrumentation SH150AD, voyant PGM-FI (MIL)
- Source : manuel du propriétaire Honda SH125/SH150 21YM, page imprimée 40 (page 44 du PDF)
- Photo de l'équipe conseillée en remplacement : tableau de bord d'une SH150i 2020+, moteur tournant, voyant PGM-FI allumé ; plaque floutée.

#### N°02 — Voyant d'injection PGM-FI clignotant
- Fichier : `images/sh150_voyant_injection_clignote.jpg`
- Image : instrumentation SH150AD, voyant PGM-FI (MIL)
- Source : manuel du propriétaire Honda SH125/SH150 21YM, page imprimée 40 (page 44 du PDF)
- Photo de l'équipe conseillée en remplacement : vidéo ou photo du voyant PGM-FI en train de clignoter (capture d'écran acceptée).

#### N°03 — Témoin de température élevée allumé (surchauffe)
- Fichier : `images/sh150_surchauffe_moteur.jpg`
- Image : vase d'expansion du liquide de refroidissement, repères UPPER / LOWER
- Source : manuel du propriétaire Honda SH125/SH150 21YM, page imprimée 102 (page 106 du PDF)
- Photo de l'équipe conseillée en remplacement : vase d'expansion de la SH150i, repères UPPER / LOWER visibles, moteur froid.

#### N°04 — Le moteur ne démarre pas
- Fichier : `images/sh150_moteur_ne_demarre_pas.jpg`
- Image : béquille latérale et ressort
- Source : manuel du propriétaire Honda SH125/SH150 21YM, page imprimée 107 (page 111 du PDF)
- Photo de l'équipe conseillée en remplacement : béquille latérale de la SH150i, dépliée puis repliée.

#### N°05 — Témoin SMART Key qui clignote 5 fois (pile faible)
- Fichier : `images/sh150_smart_key_pile_faible.jpg`
- Image : Honda SMART Key : LED et bouton ON/OFF
- Source : manuel du propriétaire Honda SH125/SH150 21YM, page imprimée 46 (page 50 du PDF)
- Photo de l'équipe conseillée en remplacement : Smart Key ouverte montrant la pile CR2032.

#### N°06 — Smart Key non détectée (témoin clignotant en continu)
- Fichier : `images/sh150_smart_key_non_detectee.jpg`
- Image : commande de contact : positions On, SEAT FUEL, Off, Lock
- Source : manuel du propriétaire Honda SH125/SH150 21YM, page imprimée 51 (page 55 du PDF)
- Photo de l'équipe conseillée en remplacement : commande de contact rotative de la SH150i (positions Lock, Off, On, SEAT FUEL).

#### N°07 — Idling Stop qui ne s'active pas
- Fichier : `images/sh150_idling_stop_inactif.jpg`
- Image : commodos : commutateur Idling Stop, boutons INFO A / INFO B, démarreur
- Source : manuel du propriétaire Honda SH125/SH150 21YM, page imprimée 42 (page 46 du PDF)
- Photo de l'équipe conseillée en remplacement : commutateur IDLING STOP / IDLING au guidon de la SH150i.

#### N°08 — Le moteur se coupe à l'arrêt (Idling Stop)
- Fichier : `images/sh150_moteur_coupe_au_feu.jpg`
- Image : commutateur et témoin Idling Stop
- Source : manuel du propriétaire Honda SH125/SH150 21YM, page imprimée 55 (page 59 du PDF)
- Photo de l'équipe conseillée en remplacement : tableau de bord au feu rouge, moteur coupé par l'Idling Stop, témoin vert clignotant.

#### N°09 — Témoin ABS allumé en roulant
- Fichier : `images/sh150_temoin_abs_allume.jpg`
- Image : instrumentation SH150AD, témoin ABS
- Source : manuel du propriétaire Honda SH125/SH150 21YM, page imprimée 41 (page 45 du PDF)
- Photo de l'équipe conseillée en remplacement : tableau de bord avec le témoin ABS allumé, scooter roulant ou contact mis.

#### N°10 — Témoin HSTC allumé fixe en roulant
- Fichier : `images/sh150_temoin_hstc_allume.jpg`
- Image : commutateur et témoin Torque Control (HSTC)
- Source : manuel du propriétaire Honda SH125/SH150 21YM, page imprimée 58 (page 62 du PDF)
- Photo de l'équipe conseillée en remplacement : tableau de bord avec le témoin TC (HSTC) visible ; écran « HSTC ON / OFF ».

#### N°11 — Niveau d'huile moteur bas
- Fichier : `images/sh150_niveau_huile_bas.jpg`
- Image : jauge-bouchon d'huile, repères haut et bas
- Source : manuel du propriétaire Honda SH125/SH150 21YM, page imprimée 98 (page 102 du PDF)
- Photo de l'équipe conseillée en remplacement : jauge-bouchon d'huile de la SH150i sortie et essuyée, repères visibles.

#### N°12 — Indicateur d'entretien affiché (vidange due)
- Fichier : `images/sh150_vidange_echeance.jpg`
- Image : vidange : vis de vidange, crépine d'huile, joint torique
- Source : manuel du propriétaire Honda SH125/SH150 21YM, page imprimée 100 (page 104 du PDF)
- Photo de l'équipe conseillée en remplacement : écran LCD de la SH150i affichant l'indicateur d'entretien.

#### N°13 — Pression des pneus trop basse
- Fichier : `images/sh150_pression_pneus_basse.jpg`
- Image : étiquette d'information pneus et charge
- Source : manuel du propriétaire Honda SH125/SH150 21YM, page imprimée 9 (page 13 du PDF)
- Photo de l'équipe conseillée en remplacement : contrôle de pression à la valve de la roue avant de la SH150i.

#### N°14 — Pneu usé (sculptures insuffisantes)
- Fichier : `images/sh150_usure_pneus.jpg`
- Image : roue arrière et pneu (vue des emplacements)
- Source : manuel du propriétaire Honda SH125/SH150 21YM, page imprimée 20 (page 24 du PDF)
- Photo de l'équipe conseillée en remplacement : bande de roulement du pneu arrière avec témoin d'usure visible.

#### N°15 — Ralenti instable : contrôle de la bougie
- Fichier : `images/sh150_bougie_ralenti_instable.jpg`
- Image : capuchon de bougie et accès bougie
- Source : manuel du propriétaire Honda SH125/SH150 21YM, page imprimée 96 (page 100 du PDF)
- Photo de l'équipe conseillée en remplacement : bougie NGK LMAR8L-9 déposée, électrodes visibles.

#### N°16 — Niveau de liquide de frein bas
- Fichier : `images/sh150_niveau_liquide_frein_bas.jpg`
- Image : réservoirs de liquide de frein avant et arrière, repère LOWER
- Source : manuel du propriétaire Honda SH125/SH150 21YM, page imprimée 105 (page 109 du PDF)
- Photo de l'équipe conseillée en remplacement : réservoir de liquide de frein au guidon, regard de niveau visible.

#### N°17 — Plaquettes de frein usées
- Fichier : `images/sh150_usure_plaquettes.jpg`
- Image : plaquettes de frein et témoins d'usure
- Source : manuel du propriétaire Honda SH125/SH150 21YM, page imprimée 106 (page 110 du PDF)
- Photo de l'équipe conseillée en remplacement : étrier de frein avant de la SH150i vu de face, plaquettes visibles.

#### N°18 — Batterie faible
- Fichier : `images/sh150_batterie_faible.jpg`
- Image : batterie sous le couvercle du plancher
- Source : manuel du propriétaire Honda SH125/SH150 21YM, page imprimée 91 (page 95 du PDF)
- Photo de l'équipe conseillée en remplacement : batterie YTZ8V de la SH150i en place, bornes visibles (contact coupé).

#### N°19 — Un équipement électrique ne fonctionne plus (fusible)
- Fichier : `images/sh150_fusible_grille.jpg`
- Image : boîte à fusibles, fusible principal, fusibles de rechange
- Source : manuel du propriétaire Honda SH125/SH150 21YM, page imprimée 136 (page 140 du PDF)
- Photo de l'équipe conseillée en remplacement : boîte à fusibles de la SH150i ouverte, contact coupé.

#### N°20 — Perte de puissance ou accélération molle
- Fichier : `images/sh150_perte_puissance.jpg`
- Image : emplacement des éléments (vue côté gauche)
- Source : manuel du propriétaire Honda SH125/SH150 21YM, page imprimée 20 (page 24 du PDF)
- Photo de l'équipe conseillée en remplacement : côté gauche de la SH150i : carter de transmission et boîtier de filtre à air.
