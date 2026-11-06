# Vérification du corpus avant dépôt

Règle du livrable : un document non vérifié n'entre pas dans le corpus. Chaque document est relu par un membre qui ne l'a pas préparé, puis son prénom est inscrit dans la colonne `verifie_par` de `corpus/inventaire.csv`.

## Grille par type de document

| Type | Contrôles |
|---|---|
| Fiches-problèmes Jeep (`jl_*`) | Retrouver chaque valeur à la page « OM p. N » du manuel du propriétaire Jeep Wrangler 2026 (page PDF = N + 2) ; relire en priorité l'intervalle du filtre à air (tableau OM p. 256) ; un seul problème par fiche ; image conforme à la page citée |
| Fiches-problèmes Honda (`sh150_*`) | Retrouver chaque valeur à la page « MP p. N » du manuel du propriétaire Honda 21YM (page PDF = N + 4) ; un seul problème par fiche ; image conforme à la page citée |
| Consignes de sécurité (toutes les fiches) | Encadrés exacts : ordre des câbles de démarrage, moteur froid, cric, airbag, haute tension |
| Documents internes (`interne_*`) | Mention « fictif » visible ; groupe `responsables` ; codes de test de fuite présents |
| Cas de test (`usage_test` ≠ normal) | Contradiction, ambiguïté ou piège bien présent et décrit dans `remarques` |

## Contrôles automatiques avant dépôt

`python finaliser_l1.py "NOM1-NOM2" --depuis L1_MaintiDoc_BAID-RAOUI-WENN` (à la racine du kit) vérifie que chaque fichier de `documents/` figure dans l'inventaire et inversement, que les noms de fichiers égalent le `document_id`, que `verifie_par` est rempli (la valeur « à compléter » est refusée), et construit le ZIP.
