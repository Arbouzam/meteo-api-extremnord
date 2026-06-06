"""Tests du endpoint /pluies-intenses/predict."""
import pytest


def test_predict_pluie_j0(client, headers, pluie_payload):
    """Prédiction valide J0 — vérifie la structure de la réponse."""
    response = client.post(
        "/pluies-intenses/predict", json=pluie_payload, headers=headers
    )
    assert response.status_code == 200
    data = response.json()
    assert "horizon" in data
    assert "probabilite" in data
    assert "alerte" in data
    assert "seuil_utilise" in data
    assert data["horizon"] == "j0"
    assert 0.0 <= data["probabilite"] <= 1.0
    assert isinstance(data["alerte"], bool)
    assert data["seuil_utilise"] > 0


@pytest.mark.parametrize("horizon", ["j0", "j3", "j7", "j14", "j30"])
def test_predict_pluie_tous_horizons(client, headers, pluie_payload, horizon):
    """Tous les horizons doivent retourner une réponse valide."""
    pluie_payload["horizon"] = horizon
    response = client.post(
        "/pluies-intenses/predict", json=pluie_payload, headers=headers
    )
    assert response.status_code == 200
    assert response.json()["horizon"] == horizon


def test_predict_pluie_horizon_invalide(client, headers, pluie_payload):
    """Horizon inconnu → 422."""
    pluie_payload["horizon"] = "j99"
    response = client.post(
        "/pluies-intenses/predict", json=pluie_payload, headers=headers
    )
    assert response.status_code == 422


def test_predict_pluie_champ_manquant(client, headers, pluie_payload):
    """Champ obligatoire manquant → 422."""
    del pluie_payload["PW_d1"]
    response = client.post(
        "/pluies-intenses/predict", json=pluie_payload, headers=headers
    )
    assert response.status_code == 422


def test_predict_pluie_valeur_hors_bornes(client, headers, pluie_payload):
    """Valeur hors plage Pydantic → 422."""
    pluie_payload["HR_850_d1"] = 999.0  # max autorisé : 100
    response = client.post(
        "/pluies-intenses/predict", json=pluie_payload, headers=headers
    )
    assert response.status_code == 422