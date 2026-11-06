---
doc_id: proc_lecture_obd_v2
titre: Réception d'un véhicule en atelier - lecture des défauts OBD-II (version 2)
famille: voiture
modele: Jeep Wrangler JL 2026 (procédure générique)
type: procédure
version: 2.0 (2026-11)
licence: CC BY 4.0 (équipe MaintiDoc)
groupes: techniciens_auto ; responsables
---
# Principe

Les véhicules thermiques vendus depuis le début des années 2000 dans la plupart des marchés disposent d'une prise de diagnostic **OBD-II** à 16 broches (norme SAE J1962). Un lecteur permet de lire les **codes défaut normalisés** (codes P0xxx décrits dans codes_obd_p0300 à codes_obd_p0442) et les données en temps réel.

[FIG:obd|prise de diagnostic OBD-II à 16 broches.]

# Procédure

1. Contact coupé, brancher le lecteur sur la prise (généralement sous la planche de bord, côté conducteur).
2. Mettre le contact (moteur arrêté sauf indication du lecteur).
3. Lire et **noter tous les codes** avec leur statut (actif, en mémoire, en attente) avant toute action.
4. Enregistrer les « données figées » (freeze frame) associées si le lecteur les propose.
5. Rechercher chaque code dans les fiches OBD du corpus ; un code n'est pas un diagnostic, c'est un point de départ.
6. **Ne pas effacer** les codes avant d'avoir terminé le diagnostic et informé le client.
7. Après réparation, effacer, faire un essai routier et relire.

> ATTENTION: les codes commençant par P1, B, C ou U sont, pour une part, spécifiques au constructeur. Le corpus ne décrit que des codes génériques P0 : pour tout autre code, l'assistant répond que l'information n'est pas disponible et oriente vers l'outil constructeur.

> INFO: le voyant moteur (orange) allumé fixe signale un défaut enregistré ; clignotant, il signale souvent des ratés d'allumage sévères pouvant endommager le catalyseur : réduire la charge et faire contrôler rapidement (voir codes_obd_p0300).
