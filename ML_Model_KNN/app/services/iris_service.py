"""
Iris KNN Model Service — Singleton inference engine.

Loads the trained KNN pipeline from disk and provides
thread-safe prediction with probability estimation.
"""

import json
import os
import logging

import joblib
import numpy as np
import pandas as pd

from app.config import settings

logger = logging.getLogger("ml_api.iris")


class IrisModelService:
    """Manages the Iris KNN pipeline lifecycle and inference."""

    def __init__(self) -> None:
        self.model = None
        self.metadata: dict = {}

    def load_model(self) -> None:
        """Load the KNN pipeline and metadata from disk."""
        if not os.path.exists(settings.IRIS_MODEL_PATH):
            raise FileNotFoundError(
                f"Iris model not found at {settings.IRIS_MODEL_PATH}"
            )

        self.model = joblib.load(settings.IRIS_MODEL_PATH)

        if os.path.exists(settings.IRIS_METADATA_PATH):
            with open(settings.IRIS_METADATA_PATH, "r") as f:
                self.metadata = json.load(f)
        else:
            self.metadata = {"model_version": "unknown", "model_type": "KNN"}

        logger.info(
            "Iris model loaded — version=%s, accuracy=%.2f%%",
            self.metadata.get("model_version", "?"),
            self.metadata.get("accuracy", 0) * 100,
        )

    def is_ready(self) -> bool:
        """Check if the model is loaded and ready for inference."""
        return self.model is not None

    def predict(self, feature_dicts: list[dict]) -> list[dict]:
        """
        Run prediction on one or more samples.

        Args:
            feature_dicts: List of dicts with keys
                [sepal_length, sepal_width, petal_length, petal_width].

        Returns:
            List of prediction result dicts.
        """
        if not self.is_ready():
            raise RuntimeError("Iris model is not initialized.")

        df = pd.DataFrame(feature_dicts)

        predictions = self.model.predict(df)
        probabilities = self.model.predict_proba(df)
        classes = self.model.classes_

        results = []
        for i, (pred, prob_row) in enumerate(zip(predictions, probabilities)):
            prob_dict = {
                str(cls): round(float(prob), 4)
                for cls, prob in zip(classes, prob_row)
            }
            top_confidence = round(float(np.max(prob_row)), 4)
            results.append(
                {
                    "predicted_species": str(pred),
                    "confidence": top_confidence,
                    "probabilities": prob_dict,
                    "input_features": feature_dicts[i],
                }
            )
        return results


# Singleton instance — initialized during app lifespan
iris_service = IrisModelService()
