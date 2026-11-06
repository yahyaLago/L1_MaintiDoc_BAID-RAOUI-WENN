# MaintiDoc - dépôt de l'équipe BAID-RAOUI-WENN

## Membres de l'équipe

| Membre | Rôle |
|---|---|
| Yahya BAID | Famille 2 : moto Honda SH150i (fiches `sh150_*`, images, valeurs du manuel Honda) |
| Ahmed RAOUI | Combinaison des deux familles : inventaire, documents de test, architecture, agent et serveur MCP |
| Wenn BOUKA | Famille 1 : voiture Jeep Wrangler JL 2026 (fiches `jl_*`, images, valeurs du manuel Jeep) |

## Objectif du projet

MaintiDoc est un assistant documentaire multimodal et agentique pour la maintenance. Le technicien pose une question en français, avec une photo s'il le souhaite. L'assistant répond en citant le document, la page et la figure, ou s'abstient ; il consulte l'historique de l'équipement par un outil MCP et prépare un ticket d'intervention soumis à validation humaine. Deux familles, un modèle chacune : **Jeep Wrangler JL 2026** (voiture) et **Honda SH150i 2020-2024** (moto).

## Contenu du ZIP

| Élément | Contenu |
|---|---|
| `L1_MaintiDoc_BAID-RAOUI-WENN_Rapport.pdf` | Rapport complet (parties 2.1 à 2.6) |
| `L1_MaintiDoc_BAID-RAOUI-WENN_LienGitHub.txt` | URL du dépôt GitHub de l'équipe |
| `README.md` | Ce fichier |
| `L1_MaintiDoc_BAID-RAOUI-WENN_Corpus/` | `inventaire.csv` (46 lignes), `prompts_corpus.md`, `documents/famille_1/` (24 PDF voiture), `documents/famille_2/` (22 PDF moto), `images/` (40 images) |

Chaque fichier est nommé `<document_id>.<extension>`, avec le même `document_id` que dans l'inventaire. Les 40 fiches-problèmes font 2 pages et contiennent une image réelle tirée du manuel du propriétaire (page citée). Cas de test : 2 contradictoires, 2 ambigus, 2 injections, 1 scan, 2 documents à accès restreint.

## Structure du dépôt

```
maintidoc/
├── README.md
├── .gitignore
├── docs/
│   └── diagrammes/        architecture (Graphviz .dot et image)
├── corpus/
│   ├── inventaire.csv
│   ├── prompts_corpus.md
│   ├── documents/famille_1/, famille_2/
│   └── images/
└── outils/                scripts de génération du corpus et de contrôle avant dépôt
```
