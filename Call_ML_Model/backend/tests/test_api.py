"""
Integration and schema tests for Call_ML_Model AI agent backend.
"""

import pytest
from unittest.mock import AsyncMock, patch
from app.schemas.response_schemas import (
    VisualizationData,
    PredictionDetail,
    ProbabilityEntry,
    FeatureComparison,
    AnalyzeResponse,
)
from app.agents.botanical_agent import botanical_agent
from app.tools.botanical_tools import predict_iris_species, predict_titanic_survival


class TestHealthEndpoints:
    """Tests for system health endpoints."""

    def test_liveness(self, client):
        response = client.get("/health/live")
        assert response.status_code == 200
        assert response.json() == {"status": "alive"}


class TestRequestValidation:
    """Tests for request payload validation on /api/v1/analyze."""

    def test_empty_query_rejected(self, client):
        response = client.post("/api/v1/analyze", json={"query": ""})
        assert response.status_code == 422

    def test_missing_query_rejected(self, client):
        response = client.post("/api/v1/analyze", json={})
        assert response.status_code == 422


class TestResponseSchemas:
    """Tests for polymorphic VisualizationData schemas."""

    def test_iris_schema_validation(self):
        data = VisualizationData(
            domain="iris",
            prediction=PredictionDetail(species="setosa", confidence=0.98),
            probabilities=[
                ProbabilityEntry(species="setosa", probability=0.98),
                ProbabilityEntry(species="versicolor", probability=0.01),
                ProbabilityEntry(species="virginica", probability=0.01),
            ],
            feature_comparison=[
                FeatureComparison(
                    feature="Sepal Length",
                    input_value=5.1,
                    setosa_avg=5.01,
                    versicolor_avg=5.94,
                    virginica_avg=6.59,
                ),
            ],
            analysis="Strong setosa indicators.",
            visualization_hints={"chart_type": "radar", "highlight_species": "setosa"},
        )
        assert data.domain == "iris"
        assert data.prediction.species == "setosa"
        assert len(data.probabilities) == 3

    def test_titanic_schema_validation(self):
        data = VisualizationData(
            domain="titanic",
            survived=True,
            survival_probability=0.82,
            confidence=0.82,
            risk_factors={"sex": "positive — female"},
            passenger_profile={
                "title": "Miss",
                "class": 1,
                "age": 17.0,
                "sex": "female",
                "family_size": 1,
                "is_alone": True,
                "has_cabin": True,
                "embarked": "S",
                "fare": 512.0,
            },
            analysis="Rose had high survival likelihood.",
            visualization_hints={"chart_type": "survival_gauge", "outcome": "survived"},
        )
        assert data.domain == "titanic"
        assert data.survived is True
        assert data.survival_probability == 0.82
        assert data.passenger_profile["class"] == 1


class TestToolRegistrations:
    """Verify tool bindings on the agent."""

    def test_tools_registered(self):
        tool_names = [t.name for t in botanical_agent.tools]
        assert "predict_iris_species" in tool_names
        assert "predict_titanic_survival" in tool_names
        assert "get_model_info" in tool_names


class TestMockedAnalyzeEndpoint:
    """Verify the /api/v1/analyze endpoint envelope with mocked agent responses."""

    def test_analyze_iris_flow(self, client):
        mock_data = VisualizationData(
            domain="iris",
            prediction=PredictionDetail(species="setosa", confidence=0.95),
            probabilities=[
                ProbabilityEntry(species="setosa", probability=0.95),
                ProbabilityEntry(species="versicolor", probability=0.03),
                ProbabilityEntry(species="virginica", probability=0.02),
            ],
            feature_comparison=[
                FeatureComparison(
                    feature="Petal Length",
                    input_value=1.4,
                    setosa_avg=1.46,
                    versicolor_avg=4.26,
                    virginica_avg=5.55,
                )
            ],
            analysis="Iris setosa prediction confirmed.",
            visualization_hints={"chart_type": "radar"},
        )

        with patch.object(botanical_agent, "analyze", new_callable=AsyncMock) as mock_analyze:
            mock_analyze.return_value = mock_data
            response = client.post(
                "/api/v1/analyze",
                json={"query": "Classify: sepal 5.1, 3.5, petal 1.4, 0.2"},
            )
            assert response.status_code == 200
            json_resp = response.json()
            assert json_resp["success"] is True
            assert json_resp["data"]["domain"] == "iris"
            assert json_resp["data"]["prediction"]["species"] == "setosa"
            assert json_resp["processing_time_ms"] >= 0

    def test_analyze_titanic_flow(self, client):
        mock_data = VisualizationData(
            domain="titanic",
            survived=True,
            survival_probability=0.85,
            confidence=0.85,
            risk_factors={"class": "positive — 1st class"},
            passenger_profile={
                "title": "Miss",
                "class": 1,
                "age": 17.0,
                "sex": "female",
                "family_size": 2,
                "is_alone": False,
                "has_cabin": True,
                "embarked": "S",
                "fare": 512.0,
            },
            analysis="Passenger Rose was predicted to survive.",
            visualization_hints={"chart_type": "survival_gauge", "outcome": "survived"},
        )

        with patch.object(botanical_agent, "analyze", new_callable=AsyncMock) as mock_analyze:
            mock_analyze.return_value = mock_data
            response = client.post(
                "/api/v1/analyze",
                json={"query": "Would Rose survive? 1st class, female, age 17"},
            )
            assert response.status_code == 200
            json_resp = response.json()
            assert json_resp["success"] is True
            assert json_resp["data"]["domain"] == "titanic"
            assert json_resp["data"]["survived"] is True
            assert json_resp["data"]["passenger_profile"]["title"] == "Miss"
