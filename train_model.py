import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
import joblib
import mlflow
import mlflow.sklearn
import matplotlib.pyplot as plt
import seaborn as sns

# Configuration MLflow
mlflow.set_tracking_uri("./mlruns")
mlflow.set_experiment("house-price-prediction")

print("Chargement des données...")
df = pd.read_csv("data/house_prices_clean.csv")

print(f"Dataset : {len(df)} lignes, {len(df.columns)} colonnes")

# Séparation features/target
features = ['GrLivArea', 'BedroomAbvGr', 'FullBath', 'YearBuilt', 'TotalBsmtSF']
X = df[features]
y = df['SalePrice']

# Split train/test (80/20)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

print(f"\nTrain : {len(X_train)} lignes")
print(f"Test : {len(X_test)} lignes")

# Entraînement avec MLflow tracking
print("\nEntraînement du modèle...")
with mlflow.start_run(run_name="random-forest-v1"):
    
    # Paramètres du modèle
    params = {
        'n_estimators': 100,
        'max_depth': 10,
        'min_samples_split': 5,
        'random_state': 42
    }
    
    # Entraînement
    model = RandomForestRegressor(**params)
    model.fit(X_train, y_train)
    
    # Prédictions
    y_pred = model.predict(X_test)
    
    # Calcul des métriques
    mse = mean_squared_error(y_test, y_pred)
    rmse = np.sqrt(mse)
    r2 = r2_score(y_test, y_pred)
    
    # Log des paramètres et métriques dans MLflow
    mlflow.log_params(params)
    mlflow.log_metrics({
        "mse": mse,
        "rmse": rmse,
        "r2": r2
    })
    
    # Graphique de prédiction vs réel
    plt.figure(figsize=(10, 6))
    plt.scatter(y_test, y_pred, alpha=0.5)
    plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'k--', lw=2)
    plt.xlabel('Prix réel')
    plt.ylabel('Prix prédit')
    plt.title('Prix réel vs Prix prédit')
    plt.savefig('prediction_vs_actual.png')
    mlflow.log_artifact('prediction_vs_actual.png')
    plt.close()
    
    # Feature importance
    feature_importance = pd.DataFrame({
        'feature': features,
        'importance': model.feature_importances_
    }).sort_values('importance', ascending=False)
    
    plt.figure(figsize=(10, 6))
    plt.barh(feature_importance['feature'], feature_importance['importance'])
    plt.xlabel('Importance')
    plt.title('Feature Importance')
    plt.tight_layout()
    plt.savefig('feature_importance.png')
    mlflow.log_artifact('feature_importance.png')
    plt.close()
    
    # Enregistrement du modèle dans MLflow
    mlflow.sklearn.log_model(
        model,
        "model",
        registered_model_name="house-price-regressor"
    )
    
    # Sauvegarde locale du modèle
    joblib.dump(model, "model/house_price_model.pkl")
    
    # Tags
    mlflow.set_tags({
        "environment": "development",
        "model_type": "RandomForest",
        "task": "regression"
    })
    
    # Affichage des résultats
    print("\n" + "="*50)
    print("RÉSULTATS DE L'ENTRAÎNEMENT")
    print("="*50)
    print(f"RMSE : ${rmse:.2f}")
    print(f"R²   : {r2:.4f}")
    print("="*50)
    
    print(f"\nModèle sauvegardé dans : model/house_price_model.pkl")
    print(f"MLflow UI : mlflow ui --port 5000")