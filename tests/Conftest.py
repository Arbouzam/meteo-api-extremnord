"""
Fixtures partagées pour tous les tests.
Les modèles ML et metadata sont mockés — aucun fichier .ubj/.json requis.
"""
import os
import sys
import types
from unittest.mock import MagicMock, patch

import numpy as np
import pytest
from fastapi.testclient import TestClient

# Clé API de test
TEST_API_KEY = "test_key_ci_only"
os.environ["API_KEY"] = TEST_API_KEY

# ── Faux metadata ─────────────────────────────────────────────────────────────
FAKE_PLUIE_METADATA = {
    "version": "v2",
    "source_donnees": "ERA5",
    "periode_test": "2023-01-01 / 2025-12-31",
    "seuil_pluie_mm": 9.34,
    "seuil_optimal_j0": 0.109,
    "features_clf": [
        "PW_d1","HR_850_d1","SST_GG_d1","CAPE_d1","Tmax_d1",
        "v850_d1","u600_d1","Cisaillement_d1","FIT_lat_d1","OLR_d1",
        "PW_d2","PW_d3","CAPE_d2","CAPE_d3","HR850_d2","HR850_d3",
        "OLR_d2","OLR_d3","v850_d2","v850_d3",
        "PW_mean3","PW_mean7","PW_max7",
        "CAPE_mean3","CAPE_mean7","CAPE_max7",
        "OLR_mean7","v850_mean3","v850_mean7",
        "anomalie_PW","mois_sin","mois_cos","jour_sin","jour_cos",
        "saison","mois",
    ],
    "perf_test": {"auc_j0": 0.8865},
    "date_entrainement": "2026-06-01 00:56",
    "clim_pw_mensuelle": {str(i): 20.0 for i in range(1, 13)},
}

FAKE_CHALEUR_METADATA = {
    "quantile_omm": 0.9,
    "duree_min_jours": 3,
    "date_fin_val": "2022-12-31",
    "seuil_optimal_j0": 0.25,
    "features_clf": [
        "temp_max","temp_moy","temp_min","humidite_rel","pression_moy",
        "amplitude_thermique","heat_index","anomalie_temp","EHF",
        "mois_sin","mois_cos","jour_sin","jour_cos",
        "temp_max_lag1","temp_max_lag3","temp_max_lag7",
        "temp_max_mean3","temp_max_mean7","temp_max_mean14",
        "temp_max_max3","temp_max_max7","temp_max_std7",
        "heat_index_mean7","q90_tmax","q90_tmin","mois","saison",
    ],
    "perf_test": {"auc_j0": 0.9741},
    "date_entrainement": "2026-05-19 09:54",
}

# ── Injection du faux module metadata_loader dans sys.modules ────────────────
# Nécessaire pour que patch() fonctionne avant le premier import de app.main
_fake_meta_module = types.ModuleType("app.services.metadata_loader")
_fake_meta_module.PLUIE_METADATA = FAKE_PLUIE_METADATA
_fake_meta_module.CHALEUR_METADATA = FAKE_CHALEUR_METADATA
sys.modules["app.services.metadata_loader"] = _fake_meta_module


def _make_mock_classifier(proba: float = 0.72):
    mock = MagicMock()
    mock.predict_proba.return_value = np.array([[1 - proba, proba]])
    return mock


def _make_mock_regressor(value: float = 38.5):
    mock = MagicMock()
    mock.predict.return_value = np.array([value])
    return mock


@pytest.fixture(scope="session")
def client():
    """Client de test avec modèles ML et metadata mockés."""
    mock_models = {
        "pluie":   {h: _make_mock_classifier(0.65) for h in ["j0","j3","j7","j14","j30"]},
        "chaleur": {h: _make_mock_classifier(0.80) for h in ["j0","j3","j7","j14","j30"]},
        "regression": {
            "pluie":   _make_mock_regressor(12.3),
            "chaleur": _make_mock_regressor(38.5),
        },
    }

    with patch("app.services.model_loader.MODELS", mock_models), \
         patch("app.services.model_loader.load_models", return_value=None):
        from app.main import app
        with TestClient(app) as c:
            yield c


@pytest.fixture
def headers():
    return {"X-API-Key": TEST_API_KEY}


@pytest.fixture
def pluie_payload():
    return {
        "horizon": "j0",
        "PW_d1": 42.5, "HR_850_d1": 78.0, "SST_GG_d1": 299.5,
        "CAPE_d1": 1200.0, "Tmax_d1": 36.5, "v850_d1": 5.2,
        "u600_d1": -3.1, "Cisaillement_d1": 8.4, "FIT_lat_d1": 12.3,
        "OLR_d1": 220.0,
        "PW_d2": 40.1, "PW_d3": 38.7,
        "CAPE_d2": 950.0, "CAPE_d3": 800.0,
        "HR850_d2": 72.0, "HR850_d3": 68.0,
        "OLR_d2": 230.0, "OLR_d3": 240.0,
        "v850_d2": 4.8, "v850_d3": 3.9,
        "PW_mean3": 40.4, "PW_mean7": 38.2, "PW_max7": 44.1,
        "CAPE_mean3": 983.0, "CAPE_mean7": 920.0, "CAPE_max7": 1300.0,
        "OLR_mean7": 225.0, "v850_mean3": 4.6, "v850_mean7": 4.1,
        "anomalie_PW": 3.2,
        "mois_sin": 0.866, "mois_cos": 0.5,
        "jour_sin": 0.743, "jour_cos": 0.669,
        "saison": 1, "mois": 8,
    }


@pytest.fixture
def chaleur_payload():
    return {
        "horizon": "j0",
        "temp_max": 41.2, "temp_moy": 35.8, "temp_min": 28.4,
        "humidite_rel": 32.0, "pression_moy": 1008.5,
        "amplitude_thermique": 12.8, "heat_index": 45.3,
        "anomalie_temp": 3.1, "EHF": 2.4,
        "mois_sin": 0.5, "mois_cos": 0.866,
        "jour_sin": 0.743, "jour_cos": 0.669,
        "temp_max_lag1": 40.8, "temp_max_lag3": 39.5, "temp_max_lag7": 38.2,
        "temp_max_mean3": 40.5, "temp_max_mean7": 39.8, "temp_max_mean14": 39.1,
        "temp_max_max3": 41.2, "temp_max_max7": 42.0,
        "temp_max_std7": 1.3, "heat_index_mean7": 44.1,
        "q90_tmax": 41.2, "q90_tmin": 30.6,
        "mois": 4, "saison": 2,
    }