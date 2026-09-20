"""Tests for Health endpoints in Call_ML_Model backend."""

from unittest.mock import AsyncMock, patch
from app.schemas.ml_contract import KNNHealthResponse, ModelStatusDetail
from app.core.exceptions import KNNServiceUnavailable


def test_liveness_probe(client):
    response = client.get("/health/live")
    assert response.status_code == 200
    assert response.json() == {"status": "alive"}


def test_readiness_probe_healthy(client):
    mock_health = KNNHealthResponse(
        status="ready",
        models={
            "iris": ModelStatusDetail(loaded=True, version="1.4.0", model_type="KNeighborsClassifier"),
            "titanic": ModelStatusDetail(loaded=True, version="1.0.3", model_type="LinearSVC"),
            "loan": ModelStatusDetail(loaded=True, version="1.0.0", model_type="RandomForestClassifier"),
        }
    )

    with patch("app.api.v1.health.knn_client.health_check", new_callable=AsyncMock) as mock_check:
        mock_check.return_value = mock_health
        response = client.get("/health/ready")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "ready"
        assert data["agent"] is True
        assert "loan" in data["knn_service"]["models"]


def test_readiness_probe_unhealthy(client):
    with patch("app.api.v1.health.knn_client.health_check", new_callable=AsyncMock) as mock_check:
        mock_check.side_effect = KNNServiceUnavailable("Connection refused")
        response = client.get("/health/ready")
        assert response.status_code == 503
        assert response.json()["detail"] == "KNN service unavailable"

