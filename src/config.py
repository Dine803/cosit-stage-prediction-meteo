"""
Constantes partagées entre les deux modèles.
Noms de colonnes exacts tels qu'ils apparaissent dans le CSV Open-Meteo.
"""

# Colonnes brutes du CSV (avec unités, telles que fournies par Open-Meteo)
COLONNE_HUMIDITE = "relative_humidity_2m_mean (%)"
COLONNE_PRESSION = "surface_pressure_mean (hPa)"
COLONNE_VENT_VITESSE = "wind_speed_10m_max (km/h)"
COLONNE_VENT_RAFALES = "wind_gusts_10m_max (km/h)"
COLONNE_NUAGES = "cloud_cover_mean (%)"
COLONNE_ENSOLEILLEMENT_BRUTE = "sunshine_duration (s)"  # en secondes dans le CSV
COLONNE_TEMPERATURE = "temperature_2m_mean (°C)"
COLONNE_PRECIPITATION = "precipitation_sum (mm)"

# Features communes utilisées par les DEUX modèles, une fois préparées
# (voir src/features.py pour la transformation sunshine_duration -> heures)
FEATURES_COMMUNES = [
    "humidite",
    "pression",
    "vent_vitesse",
    "vent_rafales",
    "nuages",
    "mois",
    "sunshine_duration_heures",
]

CIBLE_TEMPERATURE = "temperature"
CIBLE_PLUIE = "pluie"
SEUIL_PLUIE_MM = 1.0           # définit la cible à partir de l'historique
SEUIL_DECISION_PLUIE = 0.5     # seuil de décision sur la probabilité prédite

TAILLE_TEST = 0.2
NB_FOLDS_CV = 5
RANDOM_STATE = 42