from pydantic import BaseModel

class HouseFeatures(BaseModel):
    GrLivArea: float  # Surface habitable
    BedroomAbvGr: int  # Nombre de chambres
    FullBath: int  # Nombre de salles de bain complètes
    YearBuilt: int  # Année de construction
    TotalBsmtSF: float  # Surface du sous-sol

class PredictionResponse(BaseModel):
    predicted_price: float
    price_range: str

class HealthResponse(BaseModel):
    status: str
    model_loaded: bool