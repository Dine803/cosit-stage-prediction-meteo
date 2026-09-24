"""
src/model.py
-------------
Entraîne et évalue un modèle de classification simple :
prédire si un jour sera pluvieux (precipitation > 1 mm) ou non,
à partir de la température, l'humidité et le vent.
"""
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
import joblib


def preparer_donnees_modele(df: pd.DataFrame):
    """Construit les variables explicatives (X) et la cible (y)."""
    df = df.copy()
    df["jour_pluvieux"] = (df["precipitation"] > 1).astype(int) # cible binaire

    X = df[["temperature", "humidite", "vent"]]
    y = df["jour_pluvieux"]
    return X, y


def entrainer_modele(X, y):
    """Sépare les données en train/test, entraîne un RandomForest et l'évalue."""
    X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
    )

    modele = RandomForestClassifier(n_estimators=200, random_state=42)
    modele.fit(X_train, y_train)

    predictions = modele.predict(X_test)
    rapport = {
    "accuracy": round(accuracy_score(y_test, predictions), 3),
    "detail": classification_report(y_test, predictions, output_dict=True),
    }
    return modele, rapport


def sauvegarder_modele(modele, chemin="src/modele_pluie.joblib"):
    """Sauvegarde le modèle entraîné pour réutilisation sans ré-entraînement."""
    joblib.dump(modele, chemin)


def charger_modele(chemin="src/modele_pluie.joblib"):
    """Charge un modèle déjà entraîné."""
    return joblib.load(chemin)


def predire_pluie(modele, temperature: float, humidite: float, vent: float) -> str:
    """Retourne une prédiction lisible à partir de 3 valeurs saisies par l'utilisateur."""
    prediction = modele.predict([[temperature, humidite, vent]])[0]
    return "Jour pluvieux probable" if prediction == 1 else "Jour sec probable"