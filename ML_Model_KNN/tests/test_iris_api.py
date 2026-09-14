"""
Iris API endpoint tests.

Tests the /iris/predict, /iris/predict/batch, and /iris/metadata
endpoints against the loaded KNN model.
"""

import pytest


class TestIrisPredict:
    """Tests for POST /iris/predict."""

    def test_valid_prediction(self, client):
        """Standard Iris setosa input should return a valid prediction."""
        response = client.post("/iris/predict", json={
            "sepal_length": 5.1,
            "sepal_width": 3.5,
            "petal_length": 1.4,
            "petal_width": 0.2,
        })
        assert response.status_code == 200
        data = response.json()
        assert "predicted_species" in data
        assert data["predicted_species"] in ["setosa", "versicolor", "virginica"]
        assert 0.0 <= data["confidence"] <= 1.0
        assert len(data["probabilities"]) == 3
        assert "input_features" in data

    def test_versicolor_input(self, client):
        """Typical Iris versicolor measurements."""
        response = client.post("/iris/predict", json={
            "sepal_length": 6.0,
            "sepal_width": 2.7,
            "petal_length": 4.5,
            "petal_width": 1.5,
        })
        assert response.status_code == 200
        assert response.json()["predicted_species"] == "versicolor"

    def test_invalid_negative_value(self, client):
        """Negative measurements should be rejected by Pydantic validation."""
        response = client.post("/iris/predict", json={
            "sepal_length": -1.0,
            "sepal_width": 3.5,
            "petal_length": 1.4,
            "petal_width": 0.2,
        })
        assert response.status_code == 422

    def test_missing_field(self, client):
        """Missing required field should return 422."""
        response = client.post("/iris/predict", json={
            "sepal_length": 5.1,
            "sepal_width": 3.5,
        })
        assert response.status_code == 422


class TestIrisBatchPredict:
    """Tests for POST /iris/predict/batch."""

    def test_valid_batch(self, client):
        """Batch of 2 samples should return 2 predictions."""
        response = client.post("/iris/predict/batch", json={
            "samples": [
                {"sepal_length": 5.1, "sepal_width": 3.5, "petal_length": 1.4, "petal_width": 0.2},
                {"sepal_length": 6.7, "sepal_width": 3.0, "petal_length": 5.2, "petal_width": 2.3},
            ]
        })
        assert response.status_code == 200
        data = response.json()
        assert data["total_samples"] == 2
        assert len(data["predictions"]) == 2


class TestIrisMetadata:
    """Tests for GET /iris/metadata."""

    def test_metadata_returns(self, client):
        """Metadata endpoint should return model info."""
        response = client.get("/iris/metadata")
        assert response.status_code == 200
        data = response.json()
        assert "model_version" in data
        assert "accuracy" in data
