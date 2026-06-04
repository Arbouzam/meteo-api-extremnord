from pydantic import BaseModel
from typing import Literal

class PluiePredictionRequest(BaseModel):
    horizon: Literal["j0", "j3", "j7", "j14", "j30"]

    PW_d1: float
    HR_850_d1: float
    SST_GG_d1: float
    CAPE_d1: float
    Tmax_d1: float
    v850_d1: float
    u600_d1: float
    Cisaillement_d1: float
    FIT_lat_d1: float
    OLR_d1: float


class PredictionResponse(BaseModel):
    horizon: str
    probabilite: float
    alerte: bool