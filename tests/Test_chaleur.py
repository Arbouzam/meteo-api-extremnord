"""Tests du endpoint /vagues-chaleur/predict."""
import pytest


def test_predict_chaleur_j0(client, headers, chaleur_payload):
    """Prédiction valide J0 — vérifie la structure de la réponse."""
    response = client.post(
        "/vagues-chaleur/predict", json=chaleur_payload, headers=headers
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


@pytest.mark.parametrize("horizon", ["j0", "j3", "j7", "j14", "j30"])
def test_predict_chaleur_tous_horizons(client, headers, chaleur_payload, horizon):
    """Tous les horizons doivent retourner une réponse valide."""
    chaleur_payload["horizon"] = horizon
    response = client.post(
        "/vagues-chaleur/predict", json=chaleur_payload, headers=headers
    )
    assert response.status_code == 200
    assert response.json()["horizon"] == horizon


def test_predict_chaleur_horizon_invalide(client, headers, chaleur_payload):
    """Horizon inconnu → 422."""
    chaleur_payload["horizon"] = "j999"
    response = client.post(
        "/vagues-chaleur/predict", json=chaleur_payload, headers=headers
    )
    assert response.status_code == 422


def test_predict_chaleur_champ_manquant(client, headers, chaleur_payload):
    """Champ obligatoire manquant → 422."""
    del chaleur_payload["temp_max"]
    response = client.post(
        "/vagues-chaleur/predict", json=chaleur_payload, headers=headers
    )
    assert response.status_code == 422


def test_predict_chaleur_valeur_hors_bornes(client, headers, chaleur_payload):
    """Température impossible → 422."""
    chaleur_payload["temp_max"] = 9999.0  # max autorisé : 55
    response = client.post(
        "/vagues-chaleur/predict", json=chaleur_payload, headers=headers
    )
    assert response.status_code == 422