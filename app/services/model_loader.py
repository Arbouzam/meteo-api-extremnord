import logging
import os

import xgboost as xgb

logger = logging.getLogger(__name__)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

MODELS: dict = {
    "pluie": {},
    "chaleur": {},
    "regression": {},
}

HORIZONS = ["j0", "j3", "j7", "j14", "j30"]


def load_xgb_classifier(path: str) -> xgb.XGBClassifier:
    """Charge un modèle XGBoost de classification (.ubj)."""
    model = xgb.XGBClassifier()
    model.load_model(path)
    return model


def load_xgb_regressor(path: str) -> xgb.XGBRegressor:
    """Charge un modèle XGBoost de régression (.ubj)."""
    model = xgb.XGBRegressor()
    model.load_model(path)
    return model


def _load_or_warn(load_fn, path: str, label: str):
    """Tente de charger un modèle — log un warning si le fichier est absent."""
    if not os.path.exists(path):
        logger.warning("Modèle introuvable, ignoré : %s (%s)", path, label)
        return None
    model = load_fn(path)
    logger.info("Modèle chargé : %s", label)
    return model


def load_models() -> None:
    """Charge tous les modèles ML au démarrage de l'API."""

    # --- Modèles pluies intenses (classification) ---
    pluie_dir = os.path.join(BASE_DIR, "models", "pluie")
    for horizon in HORIZONS:
        path = os.path.join(pluie_dir, f"xgb_{horizon}.ubj")
        MODELS["pluie"][horizon] = _load_or_warn(
            load_xgb_classifier, path, f"pluie/{horizon}"
        )

    # --- Modèles vagues de chaleur (classification) ---
    chaleur_dir = os.path.join(BASE_DIR, "models", "chaleur")
    for horizon in HORIZONS:
        path = os.path.join(chaleur_dir, f"xgb_{horizon}.ubj")
        MODELS["chaleur"][horizon] = _load_or_warn(
            load_xgb_classifier, path, f"chaleur/{horizon}"
        )

    # --- Modèles de régression ---
    MODELS["regression"]["pluie"] = _load_or_warn(
        load_xgb_regressor,
        os.path.join(pluie_dir, "xgb_regression_pluie.ubj"),
        "regression/pluie",
    )
    MODELS["regression"]["chaleur"] = _load_or_warn(
        load_xgb_regressor,
        os.path.join(chaleur_dir, "xgb_regression_tmax.ubj"),
        "regression/chaleur",
    )

    logger.info("Chargement des modèles terminé.")