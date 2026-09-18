# Prédiction Météorologique — Cotonou

Projet de stage réalisé chez **COSIT Bénin**, dans le cadre du programme de stage en Analyse de Données / Intelligence Artificielle / Machine Learning.

## Objectif

Construire deux modèles complémentaires qui, à partir d'un ensemble de caractéristiques météorologiques données en entrée (humidité, pression, vent, couverture nuageuse, mois, etc.), estiment :

- **Régression** : la température correspondant à ces conditions
- **Classification** : la probabilité de pluie (pluie / pas de pluie) correspondant à ces conditions

Contrairement à une prévision classique qui utiliserait l'historique récent pour anticiper le jour suivant, les modèles ici apprennent la relation entre un ensemble de caractéristiques et un résultat observé le même jour, à partir des données historiques de Cotonou.

## Données

- **Source principale** : [Open-Meteo](https://open-meteo.com/) (réanalyse ERA5), coordonnées de Cotonou (6.362°N, 2.412°E), période 2015-2024
- **Source de validation** : [NASA POWER](https://power.larc.nasa.gov/) (modèle MERRA-2), utilisée pour vérifier la représentativité des données Open-Meteo par recoupement des moyennes mensuelles

## Équipe

- SYLLA IMOROU Izou Dine — modèle de [régression/classification, à préciser]
- DASSI Mari Pascal — modèle de [régression/classification, à préciser]
- ADOGOUN Déo Gracias Mahugnon — déploiement (site web)
- Tuteur de stage : Mr Winceslas ADJIHANOU

## Plan du projet (4 semaines)

| Semaine | Contenu |
|---|---|
| S1 | Collecte et structuration des données (SQL) |
| S2 | Nettoyage et visualisation |
| S3 | Modèles supervisés (régression + classification) |
| S4 | Méthodes ensemblistes, comparaison des modèles, déploiement, rapport final |

## Structure du dépôt

```
├── data/                    # Données brutes et nettoyées (CSV)
├── notebooks/
│   ├── modele_temperature.ipynb
│   └── modele_pluie.ipynb
├── models/                  # Modèles entraînés sauvegardés (.pkl)
│   ├── model_temperature.pkl
│   └── model_pluie.pkl
├── app/                     # Code du site web de déploiement
├── src/                     # Fonctions Python partagées (nettoyage, features)
├── reports/                 # Rapport de stage, présentations
└── README.md
```
