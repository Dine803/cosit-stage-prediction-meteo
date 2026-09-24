"""
Point d'entrée du site de déploiement.
TODO : à écrire une fois les deux modèles (.pkl) disponibles et
la technologie (Streamlit ou Flask) choisie en équipe.
"""

import streamlit as st        


from data_loading import charger_donnees
from features import preparer_features
from analysis import (
statistiques_descriptives,
temperature_moyenne_mensuelle,
matrice_correlation,
test_saison_seche_vs_pluvieuse,
)
from visualization import (
graphique_temperature_mensuelle,
#graphique_precipitations_par_station,
heatmap_correlation,
boxplot_saisonnier,
)
from model import (
preparer_donnees_modele,
entrainer_modele,
predire_pluie,
)

st.set_page_config(page_title="MétéoAnalysis", layout="wide")

# 1. Initialisation de la base au premier lancement (ne recrée rien si elle existe déjà)
#initialiser_base()

# Chargement des données 
df= charger_donnees()
df= preparer_features(df)



st.title("MétéoAnalysis  Tableau de bord climatique du Bénin")

# --- Barre latérale de navigation ---
page = st.sidebar.radio(
"Navigation",
["Vue d'ensemble", "Analyse statistique", "Visualisations", "Modèle IA"],
)

if page == "Vue d'ensemble":
    col1, col2, col3 = st.columns(3)
    col1.metric("Température moyenne", f"{ df['temperature'].mean(): .1f} °C")
    col2.metric("Précipitations cumulées", f"{ df['precipitation'].sum(): .0f} mm")
    #col3.metric("Stations suivies", df["nom_station"].nunique())
    st.dataframe(df.tail(20))

elif page == "Analyse statistique":
    st.subheader("Statistiques descriptives par station")
    st.dataframe(statistiques_descriptives(df))
    st.subheader("Test statistique : saison sèche vs saison pluvieuse")
    resultat = test_saison_seche_vs_pluvieuse(df)
    st.json(resultat)

elif page == "Visualisations":
    col1, col2 = st.columns(2)
    with col1:
        st.pyplot(graphique_temperature_mensuelle(temperature_moyenne_mensuelle(df)))
        st.pyplot(heatmap_correlation(matrice_correlation(df)))
    with col2:
        #st.pyplot(graphique_precipitations_par_station(df))
        st.pyplot(boxplot_saisonnier(df))

elif page == "Modèle IA":
   st.subheader("Prédiction : jour pluvieux ou sec ?")
   X, y = preparer_donnees_modele(df)
   modele, rapport = entrainer_modele(X, y)
   st.write(f"Précision du modèle sur les données de test : **{ rapport['accuracy']*100: .1f} %**")

   temperature = st.slider("Température (°C)", 15.0, 40.0, 27.0)
   humidite = st.slider("Humidité (%)", 20.0, 100.0, 70.0)
   vent = st.slider("Vent (km/h)", 0.0, 60.0, 12.0)
if st.button("Prédire"):
  resultat = predire_pluie(modele, temperature, humidite, vent)
  st.success(resultat)
