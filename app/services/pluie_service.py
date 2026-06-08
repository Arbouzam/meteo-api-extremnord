import logging

import pandas as pd
from fastapi import HTTPException, status

from app.services.model_loader import MODELS
from app.services.metadata_loader import PLUIE_METADATA

logger = logging.getLogger(__name__)

# Seuils par horizon — fallback sur seuil_optimal_j0
_SEUILS: dict[str, float] = {
    horizon: PLUIE_METADATA.get(f"seuil_optimal_{horizon}", PLUIE_METADATA["seuil_optimal_j0"])
    for horizon in ["j0", "j3", "j7", "j14", "j30"]
}


def predict_pluie(features: dict, horizon: str) -> dict:
    """
    Prédit la probabilité de pluie intense pour un horizon donné.
    """
    model = MODELS["pluie"].get(horizon)

    if model is None:
        logger.error("Modèle pluie/%s non chargé.", horizon)
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Modèle pluie/{horizon} indisponible. Vérifiez les fichiers .ubj.",
        )

    feature_order = PLUIE_METADATA["features_clf"]

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


def predict_regression_pluie(features: dict) -> dict:
    """
    Prédit la quantité de pluie en mm via le modèle de régression.

    Args:
        features: dictionnaire des features_reg (issu de request.model_dump())

    Returns:
        dict avec pluie_prevue_mm, unite, modele
    """
    model = MODELS["regression"].get("pluie")

    if model is None:
        logger.error("Modèle regression/pluie non chargé.")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Modèle regression/pluie indisponible. Vérifiez xgb_regression_pluie.ubj.",
        )

    feature_order = PLUIE_METADATA["features_reg"]

    try:
        X = pd.DataFrame(
            [[features[col] for col in feature_order]],
            columns=feature_order,
        )
    except KeyError as e:
        logger.error("Feature manquante pour la régression pluie : %s", e)
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Feature manquante : {e}",
        )

    pluie_mm = float(model.predict(X)[0])
    # Clamp : la pluie ne peut pas être négative
    pluie_mm = max(0.0, pluie_mm)

    return {
        "pluie_prevue_mm": round(pluie_mm, 2),
        "unite": "mm",
        "modele": "XGBoost Regression",
    }