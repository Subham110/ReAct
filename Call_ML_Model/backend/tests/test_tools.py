"""Unit tests for LangChain tools in app.tools.botanical_tools."""

import json
from unittest.mock import MagicMock, patch
from app.tools.botanical_tools import (
    predict_iris_species,
    predict_titanic_survival,
    predict_loan_approval,
    get_model_info,
)


def test_predict_iris_tool_success():
    mock_resp = MagicMock()
    mock_resp.json.return_value = {
        "predicted_species": "setosa",
        "confidence": 0.98,
        "probabilities": {"setosa": 0.98, "versicolor": 0.02, "virginica": 0.0},
    }
    mock_resp.raise_for_status = MagicMock()

    with patch("httpx.Client.post", return_value=mock_resp):
        res = predict_iris_species.invoke({
            "sepal_length": 5.1,
            "sepal_width": 3.5,
            "petal_length": 1.4,
            "petal_width": 0.2,
        })
        data = json.loads(res)
        assert data["predicted_species"] == "setosa"
        assert data["confidence"] == 0.98


def test_predict_titanic_tool_success():
    mock_resp = MagicMock()
    mock_resp.json.return_value = {
        "survived": True,
        "survival_probability": 0.95,
        "confidence": 0.95,
    }
    mock_resp.raise_for_status = MagicMock()

    with patch("httpx.Client.post", return_value=mock_resp):
        res = predict_titanic_survival.invoke({
            "Pclass": 1,
            "Name": "Astor, Mrs. John Jacob",
            "Sex": "female",
            "Age": 28.0,
            "Fare": 100.0,
        })
        data = json.loads(res)
        assert data["survived"] is True


def test_predict_loan_tool_success():
    mock_resp = MagicMock()
    mock_resp.json.return_value = {
        "approved": True,
        "approval_probability": 0.97,
        "cibil_rating": "Excellent",
    }
    mock_resp.raise_for_status = MagicMock()

    with patch("httpx.Client.post", return_value=mock_resp):
        res = predict_loan_approval.invoke({
            "no_of_dependents": 2,
            "education": "Graduate",
            "self_employed": "No",
            "income_annum": 6000000.0,
            "loan_amount": 10000000.0,
            "loan_term": 10,
            "cibil_score": 780,
            "residential_assets_value": 8000000.0,
        })
        data = json.loads(res)
        assert data["approved"] is True
        assert data["cibil_rating"] == "Excellent"


def test_tool_failure_returns_error_json():
    with patch("httpx.Client.post", side_effect=Exception("Connection refused")):
        res = predict_loan_approval.invoke({
            "no_of_dependents": 2,
            "education": "Graduate",
            "self_employed": "No",
            "income_annum": 6000000.0,
            "loan_amount": 10000000.0,
            "loan_term": 10,
            "cibil_score": 780,
        })
        data = json.loads(res)
        assert "error" in data
        assert "Connection refused" in data["error"]

