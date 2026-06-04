from fastapi import APIRouter, Depends

from app.security import verify_api_key
from app.schemas.pluie_schema import (
    PluiePredictionRequest,
    PredictionResponse
)


router = APIRouter(prefix="/pluies-intenses", tags=["Pluies Intenses"])

@router.post("/predict", response_model=PredictionResponse)
def predict(
    request: PluiePredictionRequest,
    api_key: str = Depends(verify_api_key)
):
    return {
        "horizon": request.horizon,
        "probabilite": 0.75,
        "alerte": True
    }