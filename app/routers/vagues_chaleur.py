from fastapi import APIRouter, Depends

from app.security import verify_api_key
from app.schemas.chaleur_schema import (
    ChaleurPredictionRequest,
    PredictionResponse
)

router = APIRouter(prefix="/vagues-chaleur", tags=["Vagues de Chaleur"])

@router.post("/predict", response_model=PredictionResponse)
def predict(
    request: ChaleurPredictionRequest,
    api_key: str = Depends(verify_api_key)
):
    return {
        "horizon": request.horizon,
        "probabilite": 0.82,
        "alerte": True
    }