"""Tests de l'authentification par clé API."""


def test_predict_pluie_sans_cle(client, pluie_payload):
    """Sans clé API → 401."""
    response = client.post("/pluies-intenses/predict", json=pluie_payload)
    assert response.status_code == 401


def test_predict_pluie_cle_invalide(client, pluie_payload):
    """Clé API incorrecte → 401."""
    response = client.post(
        "/pluies-intenses/predict",
        json=pluie_payload,
        headers={"X-API-Key": "mauvaise_cle"},
    )
    assert response.status_code == 401


def test_predict_chaleur_sans_cle(client, chaleur_payload):
    """Sans clé API → 401."""
    response = client.post("/vagues-chaleur/predict", json=chaleur_payload)
    assert response.status_code == 401


def test_info_sans_cle(client):
    """L'endpoint /info exige aussi une clé API."""
    response = client.get("/info")
    assert response.status_code == 401