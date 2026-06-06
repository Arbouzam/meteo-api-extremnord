from fastapi import APIRouter, Depends

from app.security import verify_api_key
from app.schemas.chaleur_schema import ChaleurPredictionRequest
from app.schemas.common import PredictionResponse
from app.services.chaleur_service import predict_chaleur

router = APIRouter(
    prefix="/vagues-chaleur",
    tags=["Vagues de Chaleur"],
)


@router.post("/predict", response_model=PredictionResponse)
async def predict(
    request: ChaleurPredictionRequest,
    api_key: str = Depends(verify_api_key),
) -> PredictionResponse:
    """Prédit la probabilité de vague de chaleur pour l'horizon demandé."""

    result = predict_chaleur(request.model_dump(), request.horizon)

    return PredictionResponse(
        horizon=request.horizon,
        probabilite=result["probabilite"],
        alerte=result["alerte"],
        seuil_utilise=result["seuil_utilise"],
    )