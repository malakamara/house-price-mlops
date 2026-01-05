import pandas as pd
import numpy as np
import os

def prepare_data():
    """
    Prépare les données pour le projet.
    1. Charge le fichier CSV original.
    2. Sélectionne et renomme les colonnes clés.
    3. Nettoie les données en supprimant les valeurs manquantes.
    4. Sauvegarde le fichier nettoyé.
    """
    print("Début de la préparation des données...")
    
    # Vérifier si le fichier source existe
    source_file = 'data/house_prices.csv'
    if not os.path.exists(source_file):
        print(f"ERREUR: Le fichier {source_file} n'a pas été trouvé. Assurez-vous de l'avoir téléchargé et renommé.")
        return

    # Charger les données
    df = pd.read_csv(source_file)
    print(f"Fichier original chargé : {len(df)} lignes, {len(df.columns)} colonnes")

    # Dictionnaire pour renommer les colonnes (on enlève les espaces)
    column_mapping = {
        'Gr Liv Area': 'GrLivArea',
        'Bedroom AbvGr': 'BedroomAbvGr',
        'Full Bath': 'FullBath',
        'Year Built': 'YearBuilt',
        'Total Bsmt SF': 'TotalBsmtSF',
        'SalePrice': 'SalePrice'
    }

    # Sélectionner les colonnes pertinentes et les renommer
    features_original = list(column_mapping.keys())
    df = df[features_original].copy()
    df.rename(columns=column_mapping, inplace=True)

    print("Colonnes sélectionnées et renommées :")
    print(df.columns.tolist())

    # Supprimer les lignes avec des valeurs manquantes pour les features choisies
    df_cleaned = df.dropna()
    
    print(f"\nNettoyage des valeurs manquantes...")
    print(f"Lignes avant nettoyage : {len(df)}")
    print(f"Lignes après nettoyage : {len(df_cleaned)}")
    
    # Sauvegarder les données préparées
    output_file = 'data/house_prices_clean.csv'
    df_cleaned.to_csv(output_file, index=False)
    
    print(f"\n✅ Données préparées avec succès !")
    print(f"📁 Fichier sauvegardé dans : {output_file}")
    print(f"📊 Prix moyen des maisons : ${df_cleaned['SalePrice'].mean():.2f}")
    
    return df_cleaned

if __name__ == "__main__":
    prepare_data()