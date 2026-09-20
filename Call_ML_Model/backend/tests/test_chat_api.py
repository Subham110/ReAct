"""Tests for /api/v1/analyze chat endpoint in Call_ML_Model backend."""

from unittest.mock import AsyncMock, patch
from app.core.exceptions import KNNServiceUnavailable, AgentExecutionError


def test_analyze_iris_query(client, mock_iris_data):
    with patch("app.api.v1.chat.botanical_agent.analyze", new_callable=AsyncMock) as mock_analyze:
        mock_analyze.return_value = mock_iris_data
        response = client.post(
            "/api/v1/analyze",
            json={"query": "Classify: sepal 5.1, 3.5, petal 1.4, 0.2"},
        )
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["data"]["domain"] == "iris"
        assert data["data"]["prediction"]["species"] == "setosa"
        assert data["processing_time_ms"] >= 0


def test_analyze_titanic_query(client, mock_titanic_data):
    with patch("app.api.v1.chat.botanical_agent.analyze", new_callable=AsyncMock) as mock_analyze:
        mock_analyze.return_value = mock_titanic_data
        response = client.post(
            "/api/v1/analyze",
            json={"query": "Would a 30 year old 1st class woman survive the Titanic?"},
        )
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["data"]["domain"] == "titanic"
        assert data["data"]["survived"] is True


def test_analyze_loan_query(client, mock_loan_data):
    with patch("app.api.v1.chat.botanical_agent.analyze", new_callable=AsyncMock) as mock_analyze:
        mock_analyze.return_value = mock_loan_data
        response = client.post(
            "/api/v1/analyze",
            json={"query": "Graduate earning 60L wants 1Cr loan for 10 years, CIBIL 780"},
        )
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["data"]["domain"] == "loan"
        assert data["data"]["approved"] is True
        assert data["data"]["cibil_rating"] == "Excellent"


def test_analyze_knn_service_down(client):
    with patch("app.api.v1.chat.botanical_agent.analyze", new_callable=AsyncMock) as mock_analyze:
        mock_analyze.side_effect = KNNServiceUnavailable("Cannot reach port 8000")
        response = client.post(
            "/api/v1/analyze",
            json={"query": "predict iris"},
        )
        assert response.status_code == 503
        assert "KNN Service Error" in response.json()["detail"]


def test_analyze_agent_execution_error(client):
    with patch("app.api.v1.chat.botanical_agent.analyze", new_callable=AsyncMock) as mock_analyze:
        mock_analyze.side_effect = AgentExecutionError("Failed to extract JSON")
        response = client.post(
            "/api/v1/analyze",
            json={"query": "random query"},
        )
        assert response.status_code == 500
        assert "Agent Error" in response.json()["detail"]


def test_analyze_empty_payload_rejected(client):
    response = client.post("/api/v1/analyze", json={})
    assert response.status_code == 422

