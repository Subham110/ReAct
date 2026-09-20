"""Integration tests for the Loan Approval endpoint."""

import pytest

#Fixtures 

GOOD_APPLICANT = {
    "no_of_dependents": 2,
    "education": "Graduate",
    "self_employed": "No",
    "income_annum": 6000000,
    "loan_amount": 10000000,
    "loan_term": 10,
    "cibil_score": 780,
    "residential_assets_value": 8000000,
    "commercial_assets_value": 0,
    "luxury_assets_value": 1000000,
    "bank_asset_value": 2000000,
}

RISKY_APPLICANT = {
    "no_of_dependents": 4,
    "education": "Not Graduate",
    "self_employed": "Yes",
    "income_annum": 1500000,
    "loan_amount": 15000000,
    "loan_term": 20,
    "cibil_score": 450,
    "residential_assets_value": 0,
    "commercial_assets_value": 0,
    "luxury_assets_value": 0,
    "bank_asset_value": 0,
}


class TestLoanPredict:
    def test_good_applicant_approved(self, client):
        response = client.post("/loan/predict", json=GOOD_APPLICANT)
        assert response.status_code == 200
        data = response.json()
        assert "approved" in data
        assert "approval_probability" in data
        assert data["approved"] is True
        assert data["cibil_rating"] == "Excellent"

    def test_risky_applicant_rejected(self, client):
        response = client.post("/loan/predict", json=RISKY_APPLICANT)
        assert response.status_code == 200
        data = response.json()
        assert "approved" in data
        assert data["approved"] is False
        assert data["cibil_rating"] == "Poor"

    def test_response_schema_complete(self, client):
        response = client.post("/loan/predict", json=GOOD_APPLICANT)
        data = response.json()
        for field in ["approved", "approval_probability", "confidence",
                      "cibil_rating", "risk_factors", "financial_summary",
                      "feature_importance", "input_features"]:
            assert field in data, f"Missing field: {field}"

    def test_financial_summary_fields(self, client):
        response = client.post("/loan/predict", json=GOOD_APPLICANT)
        fs = response.json()["financial_summary"]
        assert "total_assets" in fs
        assert "asset_coverage_ratio" in fs
        assert "loan_to_income_ratio" in fs

    def test_cibil_boundaries(self, client):
        for score, expected_rating in [(780, "Excellent"), (700, "Good"), (600, "Fair"), (480, "Poor")]:
            body = {**GOOD_APPLICANT, "cibil_score": score}
            resp = client.post("/loan/predict", json=body)
            assert resp.status_code == 200
            assert resp.json()["cibil_rating"] == expected_rating

    def test_invalid_cibil_score_rejected(self, client):
        bad = {**GOOD_APPLICANT, "cibil_score": 100}
        response = client.post("/loan/predict", json=bad)
        assert response.status_code == 422

    def test_missing_required_field_rejected(self, client):
        body = {k: v for k, v in GOOD_APPLICANT.items() if k != "cibil_score"}
        response = client.post("/loan/predict", json=body)
        assert response.status_code == 422

    def test_input_features_echo(self, client):
        response = client.post("/loan/predict", json=GOOD_APPLICANT)
        echo = response.json()["input_features"]
        assert echo["cibil_score"] == GOOD_APPLICANT["cibil_score"]
        assert echo["income_annum"] == GOOD_APPLICANT["income_annum"]


class TestLoanMetadata:
    def test_metadata_returns(self, client):
        response = client.get("/loan/metadata")
        assert response.status_code == 200
        data = response.json()
        assert "model_type" in data
        assert data["model_type"] == "RandomForestClassifier"
        assert "accuracy" in data
        assert data["accuracy"] > 0.90
        assert "features" in data
        assert "feature_importance" in data

