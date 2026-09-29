"""
Test du modèle de température sur les données réelles d'une journée récente
(ex: hier), récupérées via l'API Forecast d'Open-Meteo (paramètre past_days).

Utilisation :
    python tester_journee_reelle.py chemin_vers_le_csv_recent.csv
"""

import sys
import joblib
import pandas as pd

CHEMIN_CSV = sys.argv[1] if len(sys.argv) > 1 else "donnees_recentes.csv"
CHEMIN_MODELE = "models/model_temperature.pkl"

# Le CSV de l'API Forecast a le même style de métadonnées en en-tête
# que l'API Archive (latitude, longitude, elevation...)
df = pd.read_csv(CHEMIN_CSV, skiprows=3)
df["time"] = pd.to_datetime(df["time"])

# Sélectionne la ligne correspondant à hier
hier = pd.Timestamp.now().normalize() - pd.Timedelta(days=1)
ligne_hier = df[df["time"] == hier]

if ligne_hier.empty:
    print("Date d'hier introuvable dans le CSV — vérifie past_days et le fuseau horaire.")
    print("Dates disponibles :", df["time"].tolist())
    sys.exit(1)

ligne_hier = ligne_hier.iloc[0]

# Préparation des features dans le même format que src/features.py
caracteristiques = pd.DataFrame([{
    "humidite": ligne_hier["relative_humidity_2m_mean (%)"],
    "pression": ligne_hier["surface_pressure_mean (hPa)"],
    "vent_vitesse": ligne_hier["wind_speed_10m_max (km/h)"],
    "vent_rafales": ligne_hier["wind_gusts_10m_max (km/h)"],
    "nuages": ligne_hier["cloud_cover_mean (%)"],
    "mois": hier.month,
    "sunshine_duration_heures": ligne_hier["sunshine_duration (s)"] / 3600,
}])

print("Caractéristiques utilisées pour hier :")
print(caracteristiques.to_string(index=False))

modele = joblib.load(CHEMIN_MODELE)
prediction = modele.predict(caracteristiques)[0]

print(f"\nTempérature prédite pour hier : {prediction:.1f} °C")
print("Compare ce résultat à la température réellement observée hier "
      "(ex: via un relevé météo local ou Google) pour évaluer la pertinence.")
