import os
import xgboost as xgb

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

MODELS = {
    "pluie": {},
    "chaleur": {}
}


def load_xgb_model(path):
    model = xgb.XGBClassifier()
    model.load_model(path)
    return model


def load_models():

    pluie_dir = os.path.join(BASE_DIR, "models", "pluie")

    for horizon in ["j0", "j3", "j7", "j14", "j30"]:

        model_path = os.path.join(
            pluie_dir,
            f"xgb_{horizon}.ubj"
        )

        MODELS["pluie"][horizon] = load_xgb_model(model_path)

    chaleur_dir = os.path.join(
        BASE_DIR,
        "models",
        "chaleur"
    )

    for horizon in ["j0", "j3", "j7", "j14", "j30"]:

        model_path = os.path.join(
            chaleur_dir,
            f"xgb_{horizon}.ubj"
        )

        MODELS["chaleur"][horizon] = load_xgb_model(model_path)

    print("✅ Tous les modèles chargés")