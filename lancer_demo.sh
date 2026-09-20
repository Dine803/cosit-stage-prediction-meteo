#!/bin/bash
# Active l'environnement virtuel et lance la démo Streamlit

# Se placer à la racine du projet (là où se trouve ce script),
# peu importe le dossier depuis lequel tu l'appelles
cd "$(dirname "$0")"

source venv/Scripts/activate
streamlit run app/app.py