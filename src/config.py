"""
Constantes partagées entre les deux modèles.
"""

# TODO : liste définitive des features à valider avec les 2 modélisateurs
FEATURES = [
    # "relative_humidity_2m_mean",
    # "surface_pressure_mean",
    # "wind_speed_10m_max",
    # "cloud_cover_mean",
    # "mois",
]

CIBLE_TEMPERATURE = "temperature_2m_mean"
CIBLE_PLUIE = "pluie"

# TODO : seuil à partir duquel on considère qu'il "pleut" (en mm)
SEUIL_PLUIE_MM = None