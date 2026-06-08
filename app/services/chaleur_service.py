import logging

import pandas as pd
from fastapi import HTTPException, status

from app.services.model_loader import MODELS
from app.services.metadata_loader import CHALEUR_METADATA

logger = logging.getLogger(__name__)

# Seuils par horizon — fallback sur seuil_optimal_j0
_SEUILS: dict[str, float] = {
    horizon: CHALEUR_METADATA.get(f"seuil_optimal_{horizon}", CHALEUR_METADATA["seuil_optimal_j0"])
    for horizon in ["j0", "j3", "j7", "j14", "j30"]
}


def predict_chaleur(features: dict, horizon: str) -> dict:
    """
    Prédit la probabilité de vague de chaleur pour un horizon donné.
    """
    model = MODELS["chaleur"].get(horizon)

    if model is None:
        logger.error("Modèle chaleur/%s non chargé.", horizon)
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Modèle chaleur/{horizon} indisponible. Vérifiez les fichiers .ubj.",
        )

    feature_order = CHALEUR_METADATA["features_clf"]

    try:
        X = pd.DataFrame(
            [[features[col] for col in feature_order]],
            columns=feature_order,
        )
    except KeyError as e:
        logger.error("Feature manquante dans la requête : %s", e)
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Feature manquante : {e}",
        )

    proba = float(model.predict_proba(X)[0, 1])
    seuil = _SEUILS[horizon]

    return {
        "probabilite": round(proba, 4),
        "alerte": proba >= seuil,
        "seuil_utilise": seuil,
    }


def predict_regression_chaleur(features: dict) -> dict:
    """
    Prédit la température maximale via le modèle de régression.

    Args:
        features: dictionnaire des features_reg (issu de request.model_dump())

    Returns:
        dict avec tmax_prevu, unite, modele
    """
    model = MODELS["regression"].get("chaleur")

    if model is None:
        logger.error("Modèle regression/chaleur non chargé.")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Modèle regression/chaleur indisponible. Vérifiez xgb_regression_tmax.ubj.",
        )

    feature_order = CHALEUR_METADATA["features_reg"]

    try:
        X = pd.DataFrame(
            [[features[col] for col in feature_order]],
            columns=feature_order,
        )
    except KeyError as e:
        logger.error("Feature manquante pour la régression chaleur : %s", e)
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Feature manquante : {e}",
        )

    tmax_prevu = float(model.predict(X)[0])

    return {
        "tmax_prevu": round(tmax_prevu, 2),
        "unite": "°C",
        "modele": "XGBoost Regression",
    }