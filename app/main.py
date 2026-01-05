from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List
import joblib
import numpy as np
import logging
import os
import traceback

from opencensus.ext.azure.log_exporter import AzureLogHandler
from app.models import HouseFeatures, PredictionResponse, HealthResponse
#from app.drift_detect import detect_drift

# Logging & Application Insights
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("house-price-api")

APPINSIGHTS_CONN = os.getenv("APPLICATIONINSIGHTS_CONNECTION_STRING")
if APPINSIGHTS_CONN:
    logger.addHandler(AzureLogHandler(connection_string=APPINSIGHTS_CONN))
    logger.info("Application Insights connecté")
else:
    logger.warning("Application Insights non configuré")

# Initialisation FastAPI
app = FastAPI(
    title="House Price Prediction API",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Chargement du modèle
MODEL_PATH = os.getenv("MODEL_PATH", "model/house_price_model.pkl")
model = None

@app.on_event("startup")
async def load_model():
    global model
    try:
        model = joblib.load(MODEL_PATH)
        logger.info(f"Modèle chargé depuis {MODEL_PATH}")
    except Exception as e:
        logger.error(f"Erreur chargement modèle : {e}")
        model = None

@app.get("/", tags=["General"])
def root():
    return {
        "message": "House Price Prediction API",
        "version": "1.0.0",
        "status": "running",
        "docs": "/docs"
    }

@app.get("/health", response_model=HealthResponse)
def health():
    if model is None:
        raise HTTPException(status_code=503, detail="Modèle non chargé")
    return {"status": "healthy", "model_loaded": True}

@app.post("/predict", response_model=PredictionResponse)
def predict(features: HouseFeatures):
    if model is None:
        raise HTTPException(status_code=503, detail="Modèle indisponible")

    try:
        input_data = np.array([[
            features.GrLivArea,
            features.BedroomAbvGr,
            features.FullBath,
            features.YearBuilt,
            features.TotalBsmtSF
        ]])

        prediction = float(model.predict(input_data)[0])
        
        if prediction < 100000:
            price_range = "Low"
        elif prediction < 200000:
            price_range = "Medium"
        elif prediction < 300000:
            price_range = "High"
        else:
            price_range = "Very High"

        logger.info(
            "prediction",
            extra={
                "custom_dimensions": {
                    "event_type": "prediction",
                    "predicted_price": float(prediction),
                    "price_range": price_range
                }
            }
        )

        return {
            "predicted_price": round(float(prediction), 2),
            "price_range": price_range
        }

    except Exception as e:
        logger.error(f"Erreur prediction : {e}")
        raise HTTPException(status_code=500, detail=str(e))
"""
@app.post("/drift/check", tags=["Monitoring"])
def check_drift(threshold: float = 0.05):
    # ... tout le code de la fonction ...

@app.post("/drift/check", tags=["Monitoring"])
def check_drift(threshold: float = 0.05):
    try:
        results = detect_drift(
            reference_file="data/house_prices_clean.csv",
            production_file="data/production_data.csv",
            threshold=threshold
        )

        drifted = [f for f, r in results.items() if r["drift_detected"]]
        drift_pct = len(drifted) / len(results) * 100

        logger.info(
            "drift_detection",
            extra={
                "custom_dimensions": {
                    "event_type": "drift_detection",
                    "features_analyzed": len(results),
                    "features_drifted": len(drifted),
                    "drift_percentage": drift_pct,
                    "risk_level": "HIGH" if drift_pct > 50 else "MEDIUM" if drift_pct > 20 else "LOW"
                }
            }
        )

        return {
            "status": "success",
            "features_analyzed": len(results),
            "features_drifted": len(drifted)
        }

    except Exception:
        tb = traceback.format_exc()
        logger.error(tb)
        raise HTTPException(status_code=500, detail="Erreur drift detection")
        """