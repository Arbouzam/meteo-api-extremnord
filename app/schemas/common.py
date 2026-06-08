from pydantic import BaseModel, Field


class PredictionResponse(BaseModel):
    """Réponse commune aux deux modules de prédiction."""
    horizon: str = Field(description="Horizon de prévision (j0, j3, j7, j14, j30)")
    probabilite: float = Field(description="Probabilité prédite par le modèle [0, 1]")
    alerte: bool = Field(description="True si probabilité ≥ seuil optimal")
    seuil_utilise: float = Field(description="Seuil de décision appliqué")


class RegressionChaleurResponse(BaseModel):
    """Réponse du modèle de régression vagues de chaleur."""
    tmax_prevu: float = Field(description="Température maximale prévue (°C)")
    unite: str = Field(default="°C", description="Unité de mesure")
    modele: str = Field(default="XGBoost Regression", description="Modèle utilisé")


class RegressionPluieResponse(BaseModel):
    """Réponse du modèle de régression pluies intenses."""
    pluie_prevue_mm: float = Field(description="Quantité de pluie prévue (mm)")
    unite: str = Field(default="mm", description="Unité de mesure")
    modele: str = Field(default="XGBoost Regression", description="Modèle utilisé")