from pydantic import BaseModel, Field
from typing import Literal

from app.schemas.common import PredictionResponse  # noqa: F401  (réexporté)


class PluiePredictionRequest(BaseModel):

    horizon: Literal["j0", "j3", "j7", "j14", "j30"]

    # --- Variables ERA5 J-1 ---
    PW_d1: float = Field(ge=0, le=100, description="Eau précipitable J-1 (mm)")
    HR_850_d1: float = Field(ge=0, le=100, description="Humidité relative 850 hPa J-1 (%)")
    SST_GG_d1: float = Field(ge=270, le=320, description="Température surface mer J-1 (K)")
    CAPE_d1: float = Field(ge=0, le=6000, description="CAPE J-1 (J/kg)")
    Tmax_d1: float = Field(ge=15, le=55, description="Température max J-1 (°C)")
    v850_d1: float = Field(ge=-30, le=30, description="Vent méridional 850 hPa J-1 (m/s)")
    u600_d1: float = Field(ge=-30, le=30, description="Vent zonal 600 hPa J-1 (m/s)")
    Cisaillement_d1: float = Field(description="Cisaillement vertical J-1 (m/s)")
    FIT_lat_d1: float = Field(ge=-20, le=30, description="Latitude FIT J-1 (°N)")
    OLR_d1: float = Field(ge=100, le=350, description="Rayonnement LW sortant J-1 (W/m²)")

    # --- Variables ERA5 J-2, J-3 ---
    PW_d2: float = Field(ge=0, le=100)
    PW_d3: float = Field(ge=0, le=100)
    CAPE_d2: float = Field(ge=0, le=6000)
    CAPE_d3: float = Field(ge=0, le=6000)
    HR850_d2: float = Field(ge=0, le=100)
    HR850_d3: float = Field(ge=0, le=100)
    OLR_d2: float = Field(ge=100, le=350)
    OLR_d3: float = Field(ge=100, le=350)
    v850_d2: float = Field(ge=-30, le=30)
    v850_d3: float = Field(ge=-30, le=30)

    # --- Features rolling ---
    PW_mean3: float = Field(ge=0, le=100)
    PW_mean7: float = Field(ge=0, le=100)
    PW_max7: float = Field(ge=0, le=100)
    CAPE_mean3: float = Field(ge=0, le=6000)
    CAPE_mean7: float = Field(ge=0, le=6000)
    CAPE_max7: float = Field(ge=0, le=6000)
    OLR_mean7: float = Field(ge=100, le=350)
    v850_mean3: float = Field(ge=-30, le=30)
    v850_mean7: float = Field(ge=-30, le=30)
    anomalie_PW: float = Field(description="Anomalie eau précipitable vs climatologie (mm)")

    # --- Features temporelles ---
    mois_sin: float = Field(ge=-1, le=1)
    mois_cos: float = Field(ge=-1, le=1)
    jour_sin: float = Field(ge=-1, le=1)
    jour_cos: float = Field(ge=-1, le=1)
    saison: int = Field(ge=1, le=4)
    mois: int = Field(ge=1, le=12)