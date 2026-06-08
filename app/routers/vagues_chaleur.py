from fastapi import APIRouter, Depends

from app.security import verify_api_key
from app.schemas.chaleur_schema import ChaleurPredictionRequest, ChaleurRegressionRequest
from app.schemas.common import PredictionResponse, RegressionChaleurResponse
from app.services.chaleur_service import predict_chaleur, predict_regression_chaleur

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


@router.post("/regression", response_model=RegressionChaleurResponse)
async def regression(
    request: ChaleurRegressionRequest,
    api_key: str = Depends(verify_api_key),
) -> RegressionChaleurResponse:
    """Prédit la température maximale (Tmax) via le modèle de régression XGBoost."""
    result = predict_regression_chaleur(request.model_dump())
    return RegressionChaleurResponse(
        tmax_prevu=result["tmax_prevu"],
        unite=result["unite"],
        modele=result["modele"],
    )