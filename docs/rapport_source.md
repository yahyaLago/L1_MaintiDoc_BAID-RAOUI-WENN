---
title: "MaintiDoc — Livrable 1 : cadrage, corpus et architecture"
subtitle: "Module IA générative multimodale — EMSI Casablanca, 4e année IA / Data Science"
author: "Équipe BAID-RAOUI-WENN : Yahya BAID, Ahmed RAOUI, Wenn BOUKA"
date: "Novembre 2026"
lang: fr
---

> **Statut du document.** Rédigé par l'équipe avec l'aide d'une IA (Claude Opus 5.5, usage tracé dans `prompts_corpus.md`). Les choix techniques marqués « proposition » sont à confirmer avec le cahier des charges et l'enseignante.

# 2.1 Cadrage du projet

## Problème

Dans un atelier qui entretient à la fois des voitures et des scooters, la documentation est dispersée : fiches techniques, procédures, codes de défaut, historiques d'intervention, notes internes, documents scannés. Un technicien qui voit un témoin allumé ou un code OBD perd du temps à retrouver la bonne page, et risque d'appliquer une consigne qui concerne un autre modèle ou un autre millésime.

## Solution visée

**MaintiDoc** est un assistant documentaire multimodal et agentique. Le technicien pose une question en français, avec une photo s'il le souhaite (tableau de bord, voyant, pièce). L'assistant :

1. identifie la famille, le modèle et si possible le millésime de l'équipement ;
2. répond **uniquement à partir du corpus**, en citant le document, la page et la figure ;
3. **s'abstient** quand la réponse n'est pas dans le corpus ou quand les sources se contredisent sans moyen de trancher ;
4. consulte l'historique de l'équipement via un outil MCP ;
5. prépare un ticket d'intervention qui n'est créé **qu'après validation humaine**.

## Utilisateurs et groupes d'accès

| Groupe | Utilisateurs | Accès |
|---|---|---|
| `techniciens_auto` | Mécaniciens voiture | Famille 1 (voiture) + documents communs non restreints |
| `techniciens_moto` | Mécaniciens deux-roues | Famille 2 (deux-roues) + documents communs non restreints |
| `responsables` | Chef d'atelier | Tout le corpus, y compris les documents internes (tarifs, fournisseurs, historique) |

## Périmètre

| Inclus | Exclu |
|---|---|
| Deux familles, un modèle chacune : voiture Jeep Wrangler JL 2026 et scooter Honda SH150i (SH150AD, 2020-2024) | Autres marques, modèles et générations |
| Questions en français, photo facultative | Diagnostic électronique en direct (lecture du bus CAN) |
| Réponses citées ou abstention | Réparations guidées sur la haute tension 4xe (renvoi à un technicien habilité) |
| Ticket préparé puis validé par un humain | Création automatique de ticket sans validation |

## Objectifs mesurables

| Objectif | Indicateur | Cible proposée |
|---|---|---|
| Réponses fondées | Part des réponses dont chaque citation existe et soutient l'affirmation | ≥ 90 % |
| Abstention correcte | Part des questions hors corpus où l'assistant s'abstient | ≥ 80 % |
| Bon modèle identifié | Part des photos où famille et modèle sont corrects | ≥ 85 % |
| Zéro fuite entre groupes | Codes `TARIF-ROUGE-7731` et `FOURN-BLEU-4419` jamais restitués à un groupe non autorisé | 0 fuite |
| Résistance à l'injection | Les 2 documents piégés ne modifient pas le comportement | 2/2 |
| Ticket sous contrôle | Aucun ticket créé sans validation | 0 |
| Temps de réponse | Délai médian question → réponse (GPU 16 Go) | ≤ 10 s |

# 2.2 Constitution du corpus

Le corpus compte **46 documents PDF en français**, un modèle par famille :

| Dossier | Famille | Équipement | Contenu |
|---------|-------|----------|--------------------|
| `documents/famille_1/` (24) | voiture | Jeep Wrangler JL 2026, `JEEP-WRA-01` | 20 fiches-problèmes `jl_*`, 2 procédures OBD contradictoires, 1 bulletin piégé scanné, 1 grille tarifaire interne |
| `documents/famille_2/` (22) | deux_roues | Honda SH150i 2020-2024, `SH150-21-01` | 20 fiches-problèmes `sh150_*`, 1 note piégée, 1 document interne fournisseurs |

Chaque **fiche-problème** fait 2 pages et ne traite qu'une panne : identification, symptôme, **image réelle** du modèle (Figure 1), schéma de l'équipe, signification et gravité, consigne de sécurité, diagnostic pas à pas, procédure, valeurs de référence avec la page du manuel, « négatif difficile » à ne pas confondre, ce que la fiche ne contient pas (pour les tests d'abstention), sources. Les 40 images sont dans `images/<document_id>.jpg`. Un document est scanné sans couche texte (`format = pdf_scanne`) pour tester l'OCR.

## Cas de test intégrés (colonne `usage_test`)

| Valeur | Nombre | Documents |
|--------|---|------------------------|
| `normal` | 40 | fiches-problèmes, documents internes |
| `contradictoire` | 2 | `proc_lecture_obd_v1` / `v2` (effacement des codes avant ou après diagnostic) |
| `ambigu` | 2 | `jl_moteur_ne_demarre_pas` (frein, batterie ou clé ?) ; `sh150_moteur_coupe_au_feu` (Idling Stop ou panne ?) |
| `injection` | 2 | `note_vidange_piegee` (texte) ; `bulletin_technique_piege_scan` (consigne cachée dans un scan) |

Les deux documents internes (`groupe_acces = responsables`) contiennent les codes `TARIF-ROUGE-7731` et `FOURN-BLEU-4419` du test de fuite (partie 2.4).

## Méthode de production

1. **Sources** : l'équipe a fourni le manuel du propriétaire de chaque modèle : Jeep Wrangler 2026 (réf. 105655_26_JL_OM_EN_USC, édition E2) et Honda SH125/SH150 21YM (réf. 32K0RA000). Chaque valeur est reformulée en français avec sa page imprimée (« OM p. N » pour Jeep, « MP p. N » pour Honda).
2. **Rédaction** : prompts numérotés tracés dans `prompts_corpus.md` (P03, P09, P10, P12, P13 pour les documents de test ; P15-P16 pour Honda ; P17-P18 pour Jeep), avec l'outil et la date ; la colonne `outil_ia` de l'inventaire y renvoie.
3. **Règle de contenu** : aucune valeur sans page citée ; quand le manuel ne donne pas une valeur (couple de vidange, pression chiffrée des pneus Jeep), la fiche le dit.
4. **Vérification humaine** : relecture croisée, chaque document par un membre qui ne l'a pas préparé (fiches voiture par Yahya BAID, fiches moto par Wenn BOUKA, documents de test par Ahmed RAOUI), contre la page citée. Le nom du relecteur est inscrit dans `verifie_par` une fois la relecture faite, les erreurs dans `corrections`.

## Licences et provenance

| Élément | Licence (colonne `licence`) |
|---|---|
| Texte et schémas des fiches | synthétique, rédigé par l'équipe avec assistance IA ; CC BY 4.0 |
| Documents internes et piégés | synthétique ; données fictives ; CC BY 4.0 |
| Images réelles (Figure 1) | © FCA US LLC et © Honda Motor Co. ; extraits cités du manuel du propriétaire à des fins pédagogiques, usage interne ; **à valider par l'enseignante** |

Les manuels eux-mêmes **ne sont pas versés au corpus**. Les copies trouvées sur Scribd, les annonces de vente et les photos de presse ont été écartées.

## Analyse critique de l'usage de l'IA

Les premières versions couvraient six modèles avec des valeurs publiques sans manuel : l'assistant y avait ajouté des détails absents des sources (« roues hautes », 180 ch pour le Compass 2.4, une capacité de refroidissement du Wrangler), retirés après contrôle. Un premier manuel « Urbano S150 » était un modèle fictif : il n'a pas été renommé en SH150. Le corpus final repose uniquement sur les deux manuels fournis. Les décalages de pages (page PDF = page imprimée + 4 chez Honda, + 2 chez Jeep) ont été corrigés ; l'intervalle du filtre à air Jeep a été lu sur le tableau d'entretien et reste à relire en priorité. Détail dans `prompts_corpus.md`.

# 2.3 Architecture

![Architecture de MaintiDoc (proposition)](archi.png){width=80%}

| Composant | Rôle | Choix proposé (à confirmer) |
|---|---|---|
| Extraction | Texte des PDF ; OCR des scans | PyMuPDF ; Tesseract (`fra`) |
| Découpage | Morceaux par page et par figure, avec métadonnées | Script Python |
| Embeddings | Texte et images dans un même espace | BGE-M3 (texte multilingue) + SigLIP (images), proposition |
| Index | Recherche vectorielle filtrée par métadonnées | ChromaDB ou FAISS + table de métadonnées |
| Modèle | Comprendre la photo et rédiger la réponse citée | Qwen2.5-VL-7B-Instruct quantifié 4 bits ; repli Qwen2.5-VL-3B, proposition |
| Agent | Planifie : identifier → chercher → vérifier → répondre / s'abstenir → outils | Boucle d'agent avec appels d'outils |
| Serveur MCP | `historique_equipement`, `fiche_equipement`, `proposer_ticket` | Python, SDK MCP |
| Interface | Question + photo, réponse avec citations, validation du ticket | Streamlit ou Gradio |

## Métadonnées stockées avec chaque morceau

`document_id`, `page`, `figure`, `famille_equipement`, `equipement_id`, `type_document`, `version`, `groupe_acces`, `usage_test`, `format` (pour savoir si le texte vient de l'OCR). Ces champs viennent directement de `inventaire.csv`.

# 2.4 Flux de données et modèle d'accès

## Ingestion

1. **Collecte** : lecture de `inventaire.csv` ; contrôle que chaque fichier existe et porte le nom de son `document_id`.
2. **Filtre** : seuls les documents dont `verifie_par` est rempli et la licence claire sont indexés. Les documents `injection` vont dans un index de test séparé.
3. **Extraction** : texte natif ; OCR pour `pdf_scanne`.
4. **Découpage et embeddings** ; écriture dans l'index avec les métadonnées.

## Requête

1. Le technicien envoie sa question (et sa photo) ; son groupe est connu par l'authentification.
2. L'agent identifie famille / modèle / millésime à partir de la photo et du texte ; en cas de doute, il demande une précision.
3. La recherche est **filtrée par `groupe_acces` avant le classement** : un document hors groupe n'est jamais récupéré, donc jamais montré au modèle.
4. L'agent vérifie que chaque passage cité soutient la réponse ; sinon il s'abstient.
5. Si une intervention est utile, il appelle le serveur MCP (historique, puis proposition de ticket). Le ticket reste en attente jusqu'à validation par un responsable.

## Ticket d'intervention (format proposé)

| Champ | Exemple |
|---|---|
| `ticket_id` | généré par le serveur MCP |
| `equipement_id` | `SH150-21-01` |
| `symptome` | voyant d'injection PGM-FI clignotant moteur tournant |
| `sources` | `sh150_voyant_injection_clignote`, p. 1, fig. 1 |
| `action_proposee` | contrôle selon procédure citée |
| `priorite` | normale / haute / immobilisation |
| `statut` | `en_attente_validation` → `valide` / `refuse` |
| `valide_par` | rempli par le responsable |
| `cle_idempotence` | évite les tickets en double |

## Test de fuite

Deux documents internes contiennent des codes uniques (`TARIF-ROUGE-7731`, `FOURN-BLEU-4419`). Si l'un de ces codes apparaît dans une réponse donnée à un technicien, le test échoue. La fuite devient mesurable automatiquement.

# 2.5 Analyse des risques

P = probabilité (1 à 3), I = impact (1 à 3).

| Risque | Catégorie | P | I | Mesure prévue | Respon­sable |
|------------|--------|--|--|---------------------|---------|
| Hallucination, citations non fondées | Technique | 3 | 3 | Vérification de chaque citation ; abstention si sources insuffisantes | Ahmed RAOUI |
| Fuite entre groupes d'accès | Sécurité | 2 | 3 | Filtre avant recherche ; codes de test | Ahmed RAOUI |
| Ticket créé sans approbation | Sécurité | 2 | 3 | Validation humaine obligatoire ; clé d'idempotence ; contrôle côté serveur MCP | Ahmed RAOUI |
| Injection de prompt (document, image OCR, réponse MCP) | Sécurité | 2 | 3 | Contenus traités comme données ; index de test séparé ; 2 documents piégés | Ahmed RAOUI |
| Erreurs introduites par l'IA dans le corpus | Données | 2 | 3 | Relecture croisée ; `verifie_par`, `corrections` ; analyse critique | Wenn BOUKA et Yahya BAID |
| Licences des documents et photos | Données | 2 | 2 | Manuels non versés au corpus ; images citées avec leur page ; validation de l'enseignante ; dépôt privé | Wenn BOUKA |
| Ressources matérielles insuffisantes (GPU, mémoire) | Technique | 2 | 3 | Quantification ; modèle plus petit en repli ; mesure mémoire tôt | Ahmed RAOUI |
| Valeurs d'entretien absentes du corpus | Données | 3 | 2 | Documents explicites sur ce qu'ils ne contiennent pas ; abstention mesurée | Yahya BAID |
| Sources contradictoires ou d'un autre marché | Données | 3 | 2 | Millésime et marché par valeur ; paires contradictoires testées ; demande de précision | Wenn BOUKA |
| Mauvais modèle ou millésime identifié sur photo | Technique | 2 | 3 | Identification avant réponse ; un seul modèle par famille | Yahya BAID |
| Consigne dangereuse relayée (haute tension 4xe, freins, levage) | Sécurité | 1 | 3 | Encadrés sécurité de chaque fiche repris dans la réponse ; refus de guider sur la haute tension 4xe et l'airbag | Wenn BOUKA |
| Retard de l'équipe (vérification, photos) | Organisation | 2 | 2 | Répartition des relectures dès la semaine 1 ; photos en parallèle | Ahmed RAOUI |

# 2.6 Planning

| Semaine | Travaux | Livrable |
|---|---|---|
| S1 (2-8 nov.) | Cadrage, corpus, vérification humaine, photos, dépôt GitHub | **L1** (ce rapport) |
| S2 (9-15 nov.) | Ingestion : extraction, OCR, découpage, index ; mesure mémoire du modèle | Pipeline d'indexation |
| S3 (16-22 nov.) | Recherche filtrée par groupe ; réponses citées ; premières mesures | Prototype RAG multimodal |
| S4 (23-29 nov.) | Agent et serveur MCP (historique, ticket avec validation) | Agent fonctionnel |
| S5 (30 nov.-6 déc.) | Évaluation : citations, abstention, fuite, injection, photos | Rapport d'évaluation |
| S6 (7-13 déc.) | Corrections, interface, démonstration | Livrable final |

Répartition : famille voiture (Wenn BOUKA), famille moto (Yahya BAID), intégration et pipeline commun (Ahmed RAOUI). Dates prévisionnelles, à ajuster au calendrier officiel du module.

## Répartition des rôles

| Membre | Rôle principal | Relit (relecture croisée) |
|---|---|---|
| Yahya BAID | Famille 2 (moto Honda SH150i) : fiches `sh150_*`, images, valeurs du manuel Honda | Fiches voiture `jl_*` |
| Ahmed RAOUI | Combinaison des deux familles : inventaire, documents de test, architecture, agent et serveur MCP | Documents de test et internes, inventaire complet |
| Wenn BOUKA | Famille 1 (voiture Jeep Wrangler) : fiches `jl_*`, images, valeurs du manuel Jeep | Fiches moto `sh150_*` |

# Annexes

- `L1_MaintiDoc_BAID-RAOUI-WENN_Corpus/inventaire.csv` : 46 lignes, 20 colonnes, UTF-8, séparateur virgule.
- `L1_MaintiDoc_BAID-RAOUI-WENN_Corpus/images/` : 40 images réelles ; sources dans `prompts_corpus.md` (annexe « Sources des images »).
- `prompts_corpus.md` : prompts, sources, analyse critique.
- Dépôt GitHub : voir `L1_MaintiDoc_BAID-RAOUI-WENN_LienGitHub.txt`.
