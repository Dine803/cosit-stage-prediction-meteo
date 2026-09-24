"""
src/visualization.py
----------------------
Génère les figures matplotlib/seaborn réutilisées par l'interface Streamlit.
Chaque fonction retourne un objet Figure (et non un graphique déjà affiché),
ce qui permet de l'utiliser aussi bien dans un notebook que dans app.py.

Suppose que df a déjà été préparé par charger_donnees() + preparer_features().
"""

import matplotlib.pyplot as plt
import seaborn as sns


def graphique_temperature_mensuelle(serie_mensuelle):
    """Courbe de l'évolution de la température moyenne mensuelle."""
    fig, ax = plt.subplots(figsize=(7, 4))
    serie_mensuelle.plot(ax=ax, marker="o")
    ax.set_title("Température moyenne mensuelle")
    ax.set_xlabel("Mois")
    ax.set_ylabel("Température (°C)")
    fig.tight_layout()
    return fig


def graphique_precipitations_par_mois(df):
    """Diagramme en barres du cumul de précipitations par mois.

    Remplace l'ancienne version 'par station' : ce jeu de données
    ne couvre qu'une seule station (Porto-Novo).
    """
    fig, ax = plt.subplots(figsize=(7, 4))
    df.groupby("mois")["precipitation"].sum().plot(kind="bar", ax=ax)
    ax.set_title("Précipitations cumulées par mois")
    ax.set_xlabel("Mois")
    ax.set_ylabel("Précipitations (mm)")
    fig.tight_layout()
    return fig


def heatmap_correlation(matrice_corr):
    """Heatmap de la matrice de corrélation entre variables climatiques."""
    fig, ax = plt.subplots(figsize=(5, 4))
    sns.heatmap(matrice_corr, annot=True, cmap="Greys", ax=ax)
    ax.set_title("Corrélation entre variables climatiques")
    fig.tight_layout()
    return fig


def boxplot_saisonnier(df):
    """Distribution des températures par saison (sèche / pluvieuse)."""
    df = df.copy()
    df["saison"] = df["mois"].apply(
        lambda m: "Sèche" if m in [11, 12, 1, 2, 3] else "Pluvieuse"
    )
    fig, ax = plt.subplots(figsize=(5, 4))
    sns.boxplot(data=df, x="saison", y="temperature", ax=ax)
    ax.set_title("Températures par saison")
    fig.tight_layout()
    return fig
