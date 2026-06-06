from fastapi import APIRouter, Depends

from app.security import verify_api_key
from app.schemas.pluie_schema import PluiePredictionRequest
from app.schemas.common import PredictionResponse
from app.services.pluie_service import predict_pluie

router = APIRouter(
    prefix="/pluies-intenses",
    tags=["Pluies Intenses"],
)


@router.post("/predict", response_model=PredictionResponse)
async def predict(
    request: PluiePredictionRequest,
    api_key: str = Depends(verify_api_key),
) -> PredictionResponse:
    """Prédit la probabilité de pluie intense pour l'horizon demandé."""

    result = predict_pluie(request.model_dump(), request.horizon)

    return PredictionResponse(
        horizon=request.horizon,
        probabilite=result["probabilite"],
        alerte=result["alerte"],
        seuil_utilise=result["seuil_utilise"],
    )