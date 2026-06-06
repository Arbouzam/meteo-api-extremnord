from pydantic import BaseModel, Field
from typing import Literal

from app.schemas.common import PredictionResponse  # noqa: F401  (réexporté)


class ChaleurPredictionRequest(BaseModel):

    horizon: Literal["j0", "j3", "j7", "j14", "j30"]

    # --- Variables météo de base ---
    temp_max: float = Field(ge=15, le=55, description="Température maximale (°C)")
    temp_moy: float = Field(ge=10, le=50, description="Température moyenne (°C)")
    temp_min: float = Field(ge=5, le=45, description="Température minimale (°C)")
    humidite_rel: float = Field(ge=0, le=100, description="Humidité relative (%)")
    pression_moy: float = Field(ge=900, le=1050, description="Pression moyenne (hPa)")

    # --- Indices dérivés ---
    amplitude_thermique: float = Field(ge=0, le=30, description="Tmax - Tmin (°C)")
    heat_index: float = Field(ge=20, le=80, description="Indice de chaleur ressenti (°C)")
    anomalie_temp: float = Field(ge=-15, le=15, description="Anomalie Tmax vs climatologie (°C)")
    EHF: float = Field(description="Excess Heat Factor")

    # --- Features temporelles ---
    mois_sin: float = Field(ge=-1, le=1)
    mois_cos: float = Field(ge=-1, le=1)
    jour_sin: float = Field(ge=-1, le=1)
    jour_cos: float = Field(ge=-1, le=1)

    # --- Lags Tmax ---
    temp_max_lag1: float = Field(ge=15, le=55)
    temp_max_lag3: float = Field(ge=15, le=55)
    temp_max_lag7: float = Field(ge=15, le=55)

    # --- Rolling Tmax ---
    temp_max_mean3: float = Field(ge=15, le=55)
    temp_max_mean7: float = Field(ge=15, le=55)
    temp_max_mean14: float = Field(ge=15, le=55)
    temp_max_max3: float = Field(ge=15, le=55)
    temp_max_max7: float = Field(ge=15, le=55)
    temp_max_std7: float = Field(ge=0, le=10)

    # --- Rolling Heat Index ---
    heat_index_mean7: float = Field(ge=20, le=80)

    # --- Seuils climatologiques ---
    q90_tmax: float = Field(ge=25, le=55, description="Q90 Tmax mensuel (°C)")
    q90_tmin: float = Field(ge=10, le=40, description="Q90 Tmin mensuel (°C)")

    # --- Calendrier ---
    mois: int = Field(ge=1, le=12)
    saison: int = Field(ge=1, le=4)