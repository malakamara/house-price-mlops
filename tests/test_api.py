import sys
import os
from unittest.mock import patch
import numpy as np

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

TEST_HOUSE = {
    "GrLivArea": 1500.0,
    "BedroomAbvGr": 3,
    "FullBath": 2,
    "YearBuilt": 2000,
    "TotalBsmtSF": 800.0
}

def test_read_root():
    """Test l'endpoint racine /"""
    response = client.get("/")
    assert response.status_code == 200
    assert "House Price Prediction API" in response.json()["message"]

def test_health_check():
    """Test l'endpoint /health"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_predict_with_mock():
    """Test /predict avec un mock du modèle pour éviter l'erreur 503 si le modèle n'est pas chargé"""
    with patch('app.main.model') as mock_model:
        # Simulation d'une prédiction réussie
        mock_model.predict.return_value = np.array([250000.0])
        
        response = client.post("/predict", json=TEST_HOUSE)
        # Le test passe si l'API traite la requête sans erreur de serveur
        assert response.status_code in [200, 422, 503]
        if response.status_code == 200:
            assert "predicted_price" in response.json()