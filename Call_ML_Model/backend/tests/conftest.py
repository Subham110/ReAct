"""Shared test fixtures for Call_ML_Model backend."""

import sys
from pathlib import Path

# Ensure backend root is on sys.path
sys.path.insert(0, str(Path(__file__).parent.parent))

import pytest
from unittest.mock import AsyncMock, patch
from fastapi.testclient import TestClient
from app.main import app
from app.schemas.response_schemas import VisualizationData


@pytest.fixture
def mock_iris_data():
    return VisualizationData(
        domain="iris",
        prediction={"species": "setosa", "confidence": 0.98},
        probabilities=[
            {"species": "setosa", "probability": 0.98},
            {"species": "versicolor", "probability": 0.02},
            {"species": "virginica", "probability": 0.0},
        ],
        feature_comparison=[
            {"feature": "Sepal Length", "input_value": 5.1, "setosa_avg": 5.01, "versicolor_avg": 5.94, "virginica_avg": 6.59},
            {"feature": "Sepal Width", "input_value": 3.5, "setosa_avg": 3.42, "versicolor_avg": 2.77, "virginica_avg": 2.97},
            {"feature": "Petal Length", "input_value": 1.4, "setosa_avg": 1.46, "versicolor_avg": 4.26, "virginica_avg": 5.55},
            {"feature": "Petal Width", "input_value": 0.2, "setosa_avg": 0.24, "versicolor_avg": 1.33, "virginica_avg": 2.03},
        ],
        analysis="The measurements strongly align with Iris Setosa due to very small petal length and width.",
        visualization_hints={"chart_type": "radar", "highlight_species": "setosa"},
    )


@pytest.fixture
def mock_titanic_data():
    return VisualizationData(
        domain="titanic",
        survived=True,
        survival_probability=0.92,
        confidence=0.92,
        risk_factors={"sex": "positive — female passengers had priority", "pclass": "positive — 1st class higher survival"},
        passenger_profile={"title": "Mrs", "class": 1, "age": 30.0, "sex": "female", "family_size": 1, "is_alone": False, "has_cabin": True, "embarked": "S", "fare": 80.0},
        analysis="First-class female passenger with high survival likelihood.",
        visualization_hints={"chart_type": "survival_gauge", "outcome": "survived"},
    )


@pytest.fixture
def mock_loan_data():
    return VisualizationData(
        domain="loan",
        approved=True,
        approval_probability=0.96,
        cibil_rating="Excellent",
        risk_factors={"cibil_score": "positive — excellent credit history (780)"},
        financial_summary={
            "total_assets": 11000000.0,
            "asset_coverage_ratio": 1.1,
            "loan_to_income_ratio": 1.67,
            "annual_income": 6000000.0,
            "loan_amount": 10000000.0,
            "loan_term_years": 10,
        },
        feature_importance={"cibil_score": 0.847, "loan_term": 0.05},
        input_features={
            "no_of_dependents": 2,
            "education": "Graduate",
            "self_employed": "No",
            "income_annum": 6000000.0,
            "loan_amount": 10000000.0,
            "loan_term": 10,
            "cibil_score": 780,
            "residential_assets_value": 8000000.0,
            "commercial_assets_value": 0.0,
            "luxury_assets_value": 1000000.0,
            "bank_asset_value": 2000000.0,
        },
        analysis="Application approved primarily due to high CIBIL score of 780 and sufficient asset collateral.",
        visualization_hints={"chart_type": "approval_gauge", "outcome": "approved"},
    )


@pytest.fixture
def client():
    """Test client with lifespan context to manage knn_client."""
    with patch("app.tools.knn_client.knn_client.startup", new_callable=AsyncMock), \
         patch("app.tools.knn_client.knn_client.shutdown", new_callable=AsyncMock):
        with TestClient(app) as c:
            yield c
