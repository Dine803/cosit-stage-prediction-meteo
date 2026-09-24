"""
src/analysis.py
-----------------
Analyses statistiques sur les données météo (station unique : Porto-Novo).
Suppose que df a déjà été préparé par charger_donnees() + preparer_features(),
et contient donc les colonnes : time, mois, temperature, precipitation,
humidite, vent, vent_rafales, pression, nuages, sunshine_duration_heures.
"""

import pandas as pd
from scipy import stats


def statistiques_descriptives(df: pd.DataFrame) -> pd.DataFrame:
    """Retourne moyenne, écart-type, min et max des variables climatiques.

    Une seule station dans ce jeu de données : pas de groupby par station,
    on calcule les statistiques sur l'ensemble des relevés.
    """
    return df[["temperature", "precipitation", "humidite", "vent"]].agg(
        ["mean", "std", "min", "max"]
    )


def temperature_moyenne_mensuelle(df: pd.DataFrame) -> pd.Series:
    """Agrège la température moyenne par mois, tous relevés confondus."""
    df = df.copy()
    return df.groupby("mois")["temperature"].mean()


def matrice_correlation(df: pd.DataFrame) -> pd.DataFrame:
    """Calcule la matrice de corrélation entre les variables climatiques."""
    return df[["temperature", "precipitation", "humidite", "vent"]].corr()


def test_saison_seche_vs_pluvieuse(df: pd.DataFrame) -> dict:
    """
    Test statistique (t-test de Student) comparant la température moyenne
    de la saison sèche (nov.-mars) et de la saison pluvieuse (avril-oct.)
    au Bénin.

    Hypothèse nulle H0 : les moyennes des deux saisons sont égales.
    """
    df = df.copy()
    df["saison"] = df["mois"].apply(
        lambda m: "seche" if m in [11, 12, 1, 2, 3] else "pluvieuse"
    )

    temp_seche = df.loc[df["saison"] == "seche", "temperature"]
    temp_pluvieuse = df.loc[df["saison"] == "pluvieuse", "temperature"]

    t_stat, p_value = stats.ttest_ind(temp_seche, temp_pluvieuse, equal_var=False)

    return {
        "t_statistique": round(float(t_stat), 4),
        "p_value": round(float(p_value), 6),
        "moyenne_saison_seche": round(float(temp_seche.mean()), 2),
        "moyenne_saison_pluvieuse": round(float(temp_pluvieuse.mean()), 2),
        "conclusion": (
            "Différence significative (on rejette H0)"
            if p_value < 0.05
            else "Pas de différence significative (on ne rejette pas H0)"
        ),
    }
