from pydantic import BaseModel, Field


class PredictionResponse(BaseModel):
    """Réponse commune aux deux modules de prédiction."""

    horizon: str = Field(description="Horizon de prévision (j0, j3, j7, j14, j30)")
    probabilite: float = Field(description="Probabilité prédite par le modèle [0, 1]")
    alerte: bool = Field(description="True si probabilité ≥ seuil optimal")
    seuil_utilise: float = Field(description="Seuil de décision appliqué")