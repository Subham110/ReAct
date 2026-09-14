"""
Titanic API endpoint tests.

Tests the /titanic/predict and /titanic/metadata endpoints
against the loaded LinearSVC model.
"""

import pytest


class TestTitanicPredict:
    """Tests for POST /titanic/predict."""

    def test_1st_class_woman_survives(self, client):
        """1st class woman should have high survival probability."""
        response = client.post("/titanic/predict", json={
            "Pclass": 1,
            "Name": "DeWitt Bukater, Miss. Rose",
            "Sex": "female",
            "Age": 17,
            "SibSp": 0,
            "Parch": 1,
            "Fare": 512.0,
            "Cabin": "B20",
            "Embarked": "S",
        })
        assert response.status_code == 200
        data = response.json()
        assert data["survived"] is True
        assert data["survival_probability"] > 0.5
        assert "risk_factors" in data
        assert "passenger_profile" in data
        assert "input_features" in data

    def test_3rd_class_man_perishes(self, client):
        """3rd class man should have low survival probability."""
        response = client.post("/titanic/predict", json={
            "Pclass": 3,
            "Name": "Dawson, Mr. Jack",
            "Sex": "male",
            "Age": 20,
            "SibSp": 0,
            "Parch": 0,
            "Fare": 5.0,
            "Cabin": None,
            "Embarked": "S",
        })
        assert response.status_code == 200
        data = response.json()
        assert data["survived"] is False
        assert data["survival_probability"] < 0.5

    def test_missing_age_imputed(self, client):
        """Passenger with missing Age should still get a valid prediction."""
        response = client.post("/titanic/predict", json={
            "Pclass": 2,
            "Name": "Smith, Mrs. Mary",
            "Sex": "female",
            "Age": None,
            "SibSp": 1,
            "Parch": 0,
            "Fare": 26.0,
            "Embarked": "S",
        })
        assert response.status_code == 200
        data = response.json()
        assert "survived" in data
        assert data["passenger_profile"]["age"] > 0

    def test_missing_fare_and_embarked(self, client):
        """Passenger with missing Fare and Embarked should be imputed."""
        response = client.post("/titanic/predict", json={
            "Pclass": 3,
            "Name": "Brown, Mr. James",
            "Sex": "male",
            "Age": 30,
            "SibSp": 0,
            "Parch": 0,
            "Fare": None,
            "Cabin": None,
            "Embarked": None,
        })
        assert response.status_code == 200
        data = response.json()
        assert data["passenger_profile"]["embarked"] == "S"
        assert data["passenger_profile"]["fare"] > 0

    def test_child_passenger(self, client):
        """Young child should have risk factor noting child priority."""
        response = client.post("/titanic/predict", json={
            "Pclass": 2,
            "Name": "Johnson, Master. Billy",
            "Sex": "male",
            "Age": 4,
            "SibSp": 1,
            "Parch": 2,
            "Fare": 30.0,
            "Embarked": "C",
        })
        assert response.status_code == 200
        data = response.json()
        assert "positive" in data["risk_factors"]["age"]

    def test_invalid_sex_rejected(self, client):
        """Invalid Sex value should be rejected by Pydantic."""
        response = client.post("/titanic/predict", json={
            "Pclass": 1,
            "Name": "Test, Mr. Invalid",
            "Sex": "unknown",
            "Age": 30,
        })
        assert response.status_code == 422

    def test_invalid_pclass_rejected(self, client):
        """Pclass outside 1-3 range should be rejected."""
        response = client.post("/titanic/predict", json={
            "Pclass": 5,
            "Name": "Test, Mr. Invalid",
            "Sex": "male",
            "Age": 30,
        })
        assert response.status_code == 422

    def test_missing_name_rejected(self, client):
        """Name is required for title extraction."""
        response = client.post("/titanic/predict", json={
            "Pclass": 1,
            "Sex": "male",
            "Age": 30,
        })
        assert response.status_code == 422


class TestTitanicMetadata:
    """Tests for GET /titanic/metadata."""

    def test_metadata_returns(self, client):
        """Metadata endpoint should return model info."""
        response = client.get("/titanic/metadata")
        assert response.status_code == 200
        data = response.json()
        assert "model_version" in data
        assert "accuracy" in data
        assert "feature_columns" in data


class TestHealthEndpoints:
    """Tests for global health probes."""

    def test_liveness(self, client):
        response = client.get("/health/live")
        assert response.status_code == 200
        assert response.json()["status"] == "alive"

    def test_readiness(self, client):
        response = client.get("/health/ready")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "ready"
        assert "iris" in data["models"]
        assert "titanic" in data["models"]
        assert data["models"]["iris"]["loaded"] is True
        assert data["models"]["titanic"]["loaded"] is True
