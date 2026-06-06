import logging

import pandas as pd
from fastapi import HTTPException, status

from app.services.model_loader import MODELS
from app.services.metadata_loader import CHALEUR_METADATA

logger = logging.getLogger(__name__)

# Seuils par horizon — fallback sur seuil_optimal_j0 tant que les autres
# ne sont pas calculés dans le notebook.
# TODO: ajouter seuil_optimal_j3/j7/j14/j30 dans metadata.json
#       après ré-entraînement et remplacer ce dict.
_SEUILS: dict[str, float] = {
    horizon: CHALEUR_METADATA.get(f"seuil_optimal_{horizon}", CHALEUR_METADATA["seuil_optimal_j0"])
    for horizon in ["j0", "j3", "j7", "j14", "j30"]
}


def predict_chaleur(features: dict, horizon: str) -> dict:
    """
    Prédit la probabilité de vague de chaleur pour un horizon donné.

    Args:
        features: dictionnaire des features (issu de request.model_dump())
        horizon:  horizon de prévision (j0, j3, j7, j14, j30)

    Returns:
        dict avec probabilite, alerte et seuil_utilise
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