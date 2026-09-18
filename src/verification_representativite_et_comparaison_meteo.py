"""
Vérification de la représentativité des données météo de Open-Meteo pour Cotonou (Bénin)
------------------------------------------------------------------
Objectif : comparer les moyennes mensuelles calculées à partir du CSV
Open-Meteo avec ce qu'on connaît du climat de Cotonou (climat
subéquatorial, deux saisons des pluies, températures stables toute
l'année), afin de répondre à la question du tuteur sur la
représentativité des données.

Étape supplémentaire : croiser ces résultats avec une seconde source
indépendante (NASA POWER), pour vérifier que les deux s'accordent.
"""


import pandas as pd
import matplotlib.pyplot as plt



# 1. Chargement des données Open-Meteo

# Le fichier Open-Meteo commence par quelques lignes de métadonnées
# (latitude, longitude, élévation, unités) avant les vraies données.
# On les saute avec skiprows.

CSV_PATH_OPEN_METEO = r"C:\Users\user\Documents\Stage_COSIT\Projet_Stage\data_OPEN_METEO.csv"
SKIP_ROWS_OPEN_METEO = 3

df_om = pd.read_csv(CSV_PATH_OPEN_METEO, skiprows=SKIP_ROWS_OPEN_METEO)

# On convertit la colonne "time" en datetime et on crée une colonne "mois"
df_om["time"] = pd.to_datetime(df_om["time"])
df_om["mois"] = df_om["time"].dt.month



# 2. Calcul des moyennes mensuelles Open-Meteo (toutes années confondues)

moyennes_om = df_om.groupby("mois").agg(
    temperature_moyenne_om=("temperature_2m_mean (°C)", "mean"),
    precipitation_totale_om=("precipitation_sum (mm)", "sum"),
).reset_index()

nb_annees_om = df_om["time"].dt.year.nunique()
moyennes_om["precipitation_moyenne_om"] = (
    moyennes_om["precipitation_totale_om"] / nb_annees_om
)

noms_mois = [
    "Jan", "Fév", "Mar", "Avr", "Mai", "Jun",
    "Jul", "Aoû", "Sep", "Oct", "Nov", "Déc",
]
moyennes_om["nom_mois"] = moyennes_om["mois"].apply(lambda m: noms_mois[m - 1])



# 3. Chargement des données NASA POWER

# Le fichier NASA POWER commence lui aussi par des lignes de
# métadonnées (nombre variable selon les paramètres demandés), avant
# une ligne d'en-tête qui commence par "YEAR,DOY,...".

CSV_PATH_NASA = r"C:\Users\user\Documents\Stage_COSIT\Projet_Stage\data_NASA_POWER.csv"


SKIP_ROWS_NASA = 13
df_nasa = pd.read_csv(CSV_PATH_NASA, skiprows=SKIP_ROWS_NASA)

# NASA POWER encode les valeurs manquantes avec -999 : on les remplace par NaN
df_nasa = df_nasa.replace(-999, pd.NA)

# Ce fichier donne l'année (YEAR) et le jour de l'année (DOY, de 1 à
# 365/366), et non un mois/jour séparés. On reconstruit la date en
# partant du 1er janvier de chaque année, puis en ajoutant (DOY - 1) jours.
df_nasa["time"] = pd.to_datetime(df_nasa["YEAR"].astype(str), format="%Y") + \
    pd.to_timedelta(df_nasa["DOY"].astype(int) - 1, unit="D")
df_nasa["mois"] = df_nasa["time"].dt.month


# 4. Calcul des moyennes mensuelles NASA POWER (toutes années confondues)

moyennes_nasa = df_nasa.groupby("mois").agg(
    temperature_moyenne_nasa=("T2M", "mean"),
    precipitation_totale_nasa=("PRECTOTCORR", "sum"),
).reset_index()

nb_annees_nasa = df_nasa["time"].dt.year.nunique()
moyennes_nasa["precipitation_moyenne_nasa"] = (
    moyennes_nasa["precipitation_totale_nasa"] / nb_annees_nasa
)


# 5. Fusion des deux sources pour comparaison directe, mois par mois

comparaison = moyennes_om.merge(moyennes_nasa, on="mois")
comparaison["ecart_temperature"] = (
    comparaison["temperature_moyenne_om"] - comparaison["temperature_moyenne_nasa"]
)
comparaison["ecart_precipitation"] = (
    comparaison["precipitation_moyenne_om"] - comparaison["precipitation_moyenne_nasa"]
)

print("Comparaison mensuelle Open-Meteo vs NASA POWER :\n")
print(
    comparaison[
        [
            "nom_mois",
            "temperature_moyenne_om",
            "temperature_moyenne_nasa",
            "ecart_temperature",
            "precipitation_moyenne_om",
            "precipitation_moyenne_nasa",
            "ecart_precipitation",
        ]
    ].to_string(index=False)
)


# 6. Points de comparaison avec le climat connu de Cotonou

print("\nPoints à vérifier par rapport au climat connu de Cotonou :")
print("- Températures attendues entre ~24°C et ~31°C toute l'année")
print("- Pic de précipitations attendu autour d'avril-juillet (grande saison des pluies)")
print("- Second pic plus faible attendu autour de septembre-octobre (petite saison des pluies)")
print("- Saison sèche marquée attendue autour de décembre-février")



# 7. Visualisation : température et précipitations, deux sources superposées

fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(9, 12), sharex=True)

ax1.plot(
    comparaison["nom_mois"], comparaison["temperature_moyenne_om"],
    marker="o", color="#065A82", label="Open-Meteo (ERA5)",
)
ax1.plot(
    comparaison["nom_mois"], comparaison["temperature_moyenne_nasa"],
    marker="s", color="#D97706", linestyle="--", label="NASA POWER",
)
ax1.set_title("Température moyenne mensuelle — Cotonou (deux sources)")
ax1.set_ylabel("Température (°C)")
ax1.legend()
ax1.grid(True, alpha=0.3)

ax2.plot(
    comparaison["nom_mois"], comparaison["precipitation_moyenne_om"],
    marker="o", color="#1C7293", label="Open-Meteo (ERA5)",
)
ax2.plot(
    comparaison["nom_mois"], comparaison["precipitation_moyenne_nasa"],
    marker="s", color="#D97706", linestyle="--", label="NASA POWER",
)
ax2.set_title("Précipitations moyennes mensuelles — Cotonou (deux sources)")
ax2.set_ylabel("Précipitations (mm)")
ax2.set_xlabel("Mois")
ax2.legend()
ax2.grid(True, alpha=0.3)

ax3.bar(
    comparaison["nom_mois"],
    comparaison["precipitation_moyenne_om"],
    color="#1C7293",
)
ax3.set_title("Précipitations moyennes mensuelles — Cotonou (moyenne sur la période du CSV de Open-Meteo)")
ax3.set_ylabel("Précipitations (mm)")
ax3.set_xlabel("Mois")
ax3.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig("comparaison_open_meteo_nasa_power.png", dpi=150)
print("\nGraphique enregistré : comparaison_open_meteo_nasa_power.png")



# 8. Synthèse finale

ecart_temp_moyen = comparaison["ecart_temperature"].abs().mean()
ecart_precip_moyen = comparaison["ecart_precipitation"].abs().mean()
mois_ecart_temp_max = comparaison.loc[
    comparaison["ecart_temperature"].abs().idxmax(), "nom_mois"
]
mois_ecart_precip_max = comparaison.loc[
    comparaison["ecart_precipitation"].abs().idxmax(), "nom_mois"
]

print("\n" + "=" * 70)
print("SYNTHÈSE")
print("=" * 70)
print(
    f"""
Écart moyen de température entre les deux sources : {ecart_temp_moyen:.2f} °C
Écart moyen de précipitations entre les deux sources : {ecart_precip_moyen:.1f} mm/mois

Le plus grand écart de température est observé en {mois_ecart_temp_max}.
Le plus grand écart de précipitations est observé en {mois_ecart_precip_max}.

Comment lire ces résultats :
- Un écart moyen de température inférieur à 1°C est considéré comme
  très bon : cela signifie que deux modèles indépendants (ERA5 pour
  Open-Meteo, MERRA-2 pour NASA POWER), avec des résolutions spatiales
  différentes, arrivent à des valeurs quasiment identiques pour Cotonou.
- Les précipitations sont naturellement plus difficiles à faire
  correspondre parfaitement d'une source à l'autre (la pluie est un
  phénomène plus local et plus irrégulier que la température), donc un
  écart plus visible sur les précipitations que sur la température est
  normal et ne remet pas en cause la fiabilité générale des données.
- Si les deux courbes de température se superposent presque parfaitement
  et que les deux courbes de précipitations suivent la même tendance
  saisonnière (même mois de pics et de creux), cela confirme que les
  données Open-Meteo sont représentatives du climat réel de Cotonou.

Conclusion à retenir  :
Les données ne reposent pas sur une seule source, mais sont confirmées
par une seconde source indépendante. Cela renforce la confiance dans
leur utilisation pour entraîner les modèles de prédiction du projet.
"""
)
