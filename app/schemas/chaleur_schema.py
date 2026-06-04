from pydantic import BaseModel
from typing import Literal

class ChaleurPredictionRequest(BaseModel):
    horizon: Literal["j0", "j3", "j7", "j14", "j30"]

    temp_max: float
    temp_min: float
    temp_moy: float

    humidite_rel: float
    pression_moy: float

    amplitude_thermique: float
    heat_index: float
    anomalie_temp: float
    EHF: float


class PredictionResponse(BaseModel):
    horizon: str
    probabilite: float
    alerte: bool