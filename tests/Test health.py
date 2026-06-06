"""Tests du endpoint /health."""


def test_health_ok(client):
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert data["version"] == "1.0.0"
    assert data["service"] == "phenomenes_extremes_api"


def test_health_no_auth_required(client):
    """Le endpoint health doit être accessible sans clé API."""
    response = client.get("/health", headers={})
    assert response.status_code == 200