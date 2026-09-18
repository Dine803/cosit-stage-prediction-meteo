"""
Préparation des features, commune aux deux modèles.
À COMPLÉTER une fois les features définitives choisies.
"""

from src.config import FEATURES


def preparer_features(df):
    """Sélectionne et prépare les colonnes utilisées comme features."""
    # TODO : ajouter ici l'encodage/normalisation si nécessaire
    return df[FEATURES]