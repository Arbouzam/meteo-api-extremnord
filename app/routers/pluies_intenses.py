from fastapi import APIRouter, Depends

from app.security import verify_api_key
from app.schemas.pluie_schema import PluiePredictionRequest, PluieRegressionRequest
from app.schemas.common import PredictionResponse, RegressionPluieResponse
from app.services.pluie_service import predict_pluie, predict_regression_pluie

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


@router.post("/regression", response_model=RegressionPluieResponse)
async def regression(
    request: PluieRegressionRequest,
    api_key: str = Depends(verify_api_key),
) -> RegressionPluieResponse:
    """Prédit la quantité de pluie (mm) via le modèle de régression XGBoost."""
    result = predict_regression_pluie(request.model_dump())
    return RegressionPluieResponse(
        pluie_prevue_mm=result["pluie_prevue_mm"],
        unite=result["unite"],
        modele=result["modele"],
    )