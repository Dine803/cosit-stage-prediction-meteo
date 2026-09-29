"""
Application Streamlit — Prédiction météo Cotonou
Formulaire unique interrogeant simultanément les deux modèles
(température par régression, pluie par classification).
"""

import streamlit as st
import pandas as pd
import joblib
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.config import SEUIL_DECISION_PLUIE

CHEMIN_MODELE_TEMPERATURE = "models/model_temperature.pkl"
CHEMIN_MODELE_PLUIE = "models/model_pluie.pkl"


@st.cache_resource
def charger_modele(chemin):
    """Charge un modèle une seule fois, mis en cache entre les interactions."""
    if os.path.exists(chemin) and os.path.getsize(chemin) > 0:
        return joblib.load(chemin)
    return None


modele_temperature = charger_modele(CHEMIN_MODELE_TEMPERATURE)
modele_pluie = charger_modele(CHEMIN_MODELE_PLUIE)


# ------------------------------------------------------------------
# Configuration de la page et style
# ------------------------------------------------------------------
st.set_page_config(
    page_title="Prédiction météo Cotonou",
    page_icon="🌤️",
    layout="centered",
)

st.markdown("""
<style>
    .hero {
        background: linear-gradient(135deg, #0EA5E9 0%, #0369A1 100%);
        padding: 2rem 1.5rem;
        border-radius: 16px;
        color: white;
        margin-bottom: 1.5rem;
        text-align: center;
    }
    .hero h1 { margin: 0; font-size: 1.9rem; }
    .hero p { margin: 0.4rem 0 0 0; opacity: 0.92; font-size: 0.95rem; }

    .carte-resultat {
        border-radius: 16px;
        padding: 1.3rem;
        text-align: center;
        height: 100%;
    }
    .carte-temperature {
        background: #E0F2FE;
        border: 1px solid #7DD3FC;
    }
    .carte-pluie-oui {
        background: #FEE2E2;
        border: 1px solid #FCA5A5;
    }
    .carte-pluie-non {
        background: #DCFCE7;
        border: 1px solid #86EFAC;
    }
    .carte-resultat .valeur {
        font-size: 2.2rem;
        font-weight: 700;
        margin: 0.3rem 0;
    }
    .carte-resultat .libelle {
        font-size: 0.9rem;
        color: #475569;
        text-transform: uppercase;
        letter-spacing: 0.03em;
    }
    footer {visibility: hidden;}
    #MainMenu {visibility: hidden;}
</style>
""", unsafe_allow_html=True)


# ------------------------------------------------------------------
# Barre latérale — contexte du projet
# ------------------------------------------------------------------
with st.sidebar:
    st.markdown("### 🌦️ À propos")
    st.markdown(
        "Projet réalisé dans le cadre d'un stage chez **COSIT Bénin**, "
        "prédiction météo pour la ville de **Cotonou** à partir de "
        "modèles de Machine Learning entraînés sur 10 ans de données "
        "(2015-2024)."
    )
    st.markdown("---")
    st.markdown("**Modèles utilisés**")
    st.markdown("- 🌡️ Régression (Gradient Boosting)\n- 🌧️ Classification (Gradient Boosting)")
    st.markdown("---")
    st.markdown("**Équipe**")
    st.markdown("SYLLA IMOROU Izou Dine · Pascal DASSI · Déo Gracias ADOGOUN")
    st.markdown("[📂 Code source sur GitHub](https://github.com/Dine803/cosit-stage-prediction-meteo)")


# ------------------------------------------------------------------
# En-tête
# ------------------------------------------------------------------
st.markdown("""
<div class="hero">
    <h1>🌤️ Prédiction météo — Cotonou</h1>
    <p>Renseigne les conditions atmosphériques pour estimer la température et la probabilité de pluie</p>
</div>
""", unsafe_allow_html=True)


# ------------------------------------------------------------------
# Formulaire
# ------------------------------------------------------------------
with st.form("formulaire_meteo"):
    st.markdown("#### 🧭 Conditions atmosphériques")

    col_a, col_b = st.columns(2)
    with col_a:
        humidite = st.slider("💧 Humidité relative moyenne (%)", 0, 100, 70)
        vent_vitesse = st.number_input("🌬️ Vitesse maximale du vent (km/h)", value=15.0)
        couverture_nuageuse = st.slider("☁️ Couverture nuageuse moyenne (%)", 0, 100, 50)
        duree_ensoleillement = st.number_input("☀️ Durée d'ensoleillement (heures)", value=6.0)
    with col_b:
        pression = st.number_input("🎈 Pression atmosphérique moyenne (hPa)", value=1013.0)
        vent_rafales = st.number_input("💨 Rafales maximales de vent (km/h)", value=25.0)
        mois = st.selectbox(
            "📅 Mois", list(range(1, 13)), index=8,
            format_func=lambda m: [
                "Janvier", "Février", "Mars", "Avril", "Mai", "Juin",
                "Juillet", "Août", "Septembre", "Octobre", "Novembre", "Décembre",
            ][m - 1],
        )

    st.markdown("")
    valider = st.form_submit_button("🔮 Prédire", use_container_width=True)

if valider:
    caracteristiques = pd.DataFrame([{
        "humidite": humidite,
        "pression": pression,
        "vent_vitesse": vent_vitesse,
        "vent_rafales": vent_rafales,
        "nuages": couverture_nuageuse,
        "mois": mois,
        "sunshine_duration_heures": duree_ensoleillement,
    }])

    st.markdown("#### 📊 Résultats")
    col1, col2 = st.columns(2)

    with col1:
        if modele_temperature is not None:
            prediction_temperature = modele_temperature.predict(caracteristiques)[0]
            st.markdown(f"""
            <div class="carte-resultat carte-temperature">
                <div class="libelle">Température estimée</div>
                <div class="valeur">🌡️ {prediction_temperature:.1f} °C</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="carte-resultat carte-temperature">
                <div class="libelle">Température (démo)</div>
                <div class="valeur">🌡️ 27.5 °C</div>
            </div>
            """, unsafe_allow_html=True)

    with col2:
        if modele_pluie is not None:
            probabilite_pluie = modele_pluie.predict_proba(caracteristiques)[0][1]
            va_pleuvoir = probabilite_pluie >= SEUIL_DECISION_PLUIE
            classe_css = "carte-pluie-oui" if va_pleuvoir else "carte-pluie-non"
            icone = "☔" if va_pleuvoir else "☀️"
            texte = "Pluie probable" if va_pleuvoir else "Pas de pluie attendue"
            st.markdown(f"""
            <div class="carte-resultat {classe_css}">
                <div class="libelle">{texte}</div>
                <div class="valeur">{icone} {probabilite_pluie * 100:.0f} %</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="carte-resultat carte-pluie-non">
                <div class="libelle">Pas de pluie attendue (démo)</div>
                <div class="valeur">☀️ 40 %</div>
            </div>
            """, unsafe_allow_html=True)

st.markdown(
    "<p style='text-align:center; color:#94A3B8; font-size:0.8rem; margin-top:2rem;'>"
    "Stage COSIT Bénin · Modèles de prédiction météo"
    "</p>",
    unsafe_allow_html=True,
)
