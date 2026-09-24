"""
Fonction de chargement partagée, pour que les deux notebooks
lisent les données exactement de la même façon. 
import pandas as pd


#def charger_donnees(chemin_csv, skip_rows=3):

    #"""Charge le CSV Open-Meteo et prépare les colonnes de base."""
    
    #df = pd.read_csv(chemin_csv, skiprows=skip_rows)
    #df["time"] = pd.to_datetime(df["time"])
    #df["mois"] = df["time"].dt.month
    #return df 



def charger_donnees(chemin_csv="data/data_OPEN_METEO.csv", skip_rows=3):

    """Charge le CSV Open-Meteo et prépare les colonnes de base."""
    
   # df = pd.read_csv(chemin_csv, skiprows=skip_row)
    df["time"] = pd.to_datetime(df["time"])
    df["mois"] = df["time"].dt.month
    return df

