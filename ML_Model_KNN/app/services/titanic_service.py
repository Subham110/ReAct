"""
Titanic LinearSVC Model Service — Singleton inference engine.

Loads the trained LinearSVC pipeline and applies the same feature
engineering used during training to produce survival predictions
with sigmoid-calibrated probabilities.
"""

import json
import os
import logging
import re

import joblib
import numpy as np
import pandas as pd

from app.config import settings

logger = logging.getLogger("ml_api.titanic")


class TitanicModelService:
    """Manages the Titanic LinearSVC pipeline lifecycle and inference."""

    def __init__(self) -> None:
        self.model = None
        self.metadata: dict = {}

    def load_model(self) -> None:
        """Load the Titanic pipeline and metadata from disk."""
        if not os.path.exists(settings.TITANIC_MODEL_PATH):
            raise FileNotFoundError(
                f"Titanic model not found at {settings.TITANIC_MODEL_PATH}"
            )

        self.model = joblib.load(settings.TITANIC_MODEL_PATH)

        if os.path.exists(settings.TITANIC_METADATA_PATH):
            with open(settings.TITANIC_METADATA_PATH, "r") as f:
                self.metadata = json.load(f)
        else:
            self.metadata = {"model_version": "unknown", "model_type": "LinearSVC"}

        logger.info(
            "Titanic model loaded — version=%s, accuracy=%.2f%%",
            self.metadata.get("model_version", "?"),
            self.metadata.get("accuracy", 0) * 100,
        )

    def is_ready(self) -> bool:
        """Check if the model is loaded and ready for inference."""
        return self.model is not None

    # ── Feature Engineering (mirrors train_titanic.py) ──────────

    @staticmethod
    def _extract_title(name: str) -> str:
        """Extract honorific title from passenger name."""
        match = re.search(r" ([A-Za-z]+)\.", name)
        title = match.group(1) if match else "Unknown"

        rare_titles = {
            "Lady", "Countess", "Capt", "Col", "Don", "Dr",
            "Major", "Rev", "Sir", "Jonkheer", "Dona",
        }
        replacements = {"Mlle": "Miss", "Ms": "Miss", "Mme": "Mrs"}

        if title in rare_titles:
            return "Rare"
        return replacements.get(title, title)

    def _engineer_features(self, raw: dict) -> pd.DataFrame:
        """
        Apply the same feature engineering as training.

        Steps:
            1. Title extraction from Name
            2. FamilySize, IsAlone, HasCabin derived features
            3. Age imputation using training medians
            4. Embarked imputation (default 'S')
            5. Fare imputation using training median
            6. One-hot encoding + column alignment
        """
        df = pd.DataFrame([raw])

        # Title
        df["Title"] = df["Name"].apply(self._extract_title)

        # Family
        df["FamilySize"] = df["SibSp"] + df["Parch"] + 1
        df["IsAlone"] = (df["FamilySize"] == 1).astype(int)

        # Cabin
        df["HasCabin"] = df["Cabin"].notnull().astype(int)

        # Impute Age using training medians stored in metadata
        age_medians = self.metadata.get("age_medians", {})
        if df["Age"].isna().any():
            title = df["Title"].iloc[0]
            pclass = str(df["Pclass"].iloc[0])
            key = f"{title}_{pclass}"
            median_age = age_medians.get(key, self.metadata.get("global_age_median", 28.0))
            df["Age"] = df["Age"].fillna(median_age)

        # Impute Embarked
        df["Embarked"] = df["Embarked"].fillna("S")

        # Impute Fare
        if df["Fare"].isna().any():
            df["Fare"] = df["Fare"].fillna(self.metadata.get("fare_median", 14.4542))

        # Select features for encoding
        feature_cols = ["Pclass", "Age", "SibSp", "Parch", "Fare",
                        "FamilySize", "IsAlone", "HasCabin",
                        "Sex", "Embarked", "Title"]
        df = df[feature_cols]

        # One-hot encode categorical columns
        df = pd.get_dummies(df, columns=["Sex", "Embarked", "Title"], drop_first=False)

        # Align columns to match training schema
        training_columns = self.metadata.get("feature_columns", [])
        df = df.reindex(columns=training_columns, fill_value=0)

        return df

    @staticmethod
    def _sigmoid(x: float) -> float:
        """Numerically stable sigmoid function."""
        if x >= 0:
            return 1.0 / (1.0 + np.exp(-x))
        exp_x = np.exp(x)
        return exp_x / (1.0 + exp_x)

    @staticmethod
    def _resolve_embarked(df: pd.DataFrame) -> str:
        """Resolve embarked port from one-hot columns in processed dataframe."""
        for port in ["C", "Q", "S"]:
            col = f"Embarked_{port}"
            if col in df.columns and df[col].iloc[0] == 1:
                return port
        return "S"

    def _analyze_risk_factors(self, profile: dict) -> dict[str, str]:
        """Identify positive and negative survival factors."""
        factors: dict[str, str] = {}

        # Class effect
        pclass = profile.get("Pclass", 3)
        if pclass == 1:
            factors["passenger_class"] = "positive — 1st class passengers had priority access to lifeboats"
        elif pclass == 2:
            factors["passenger_class"] = "neutral — 2nd class had moderate survival rates"
        else:
            factors["passenger_class"] = "negative — 3rd class had lowest survival rates"

        # Sex effect
        if profile.get("Sex_female", 0) == 1:
            factors["sex"] = "positive — women were prioritized under 'women and children first'"
        else:
            factors["sex"] = "negative — men had significantly lower survival rates"

        # Age effect
        age = profile.get("Age", 30)
        if age < 10:
            factors["age"] = "positive — children were prioritized for lifeboats"
        elif age > 60:
            factors["age"] = "negative — elderly passengers had lower survival rates"
        else:
            factors["age"] = f"neutral — age {age:.0f} had average survival rates"

        # Family effect
        family_size = profile.get("FamilySize", 1)
        if family_size == 1:
            factors["family"] = "negative — solo travelers had lower survival rates"
        elif family_size <= 4:
            factors["family"] = "positive — small families had higher survival rates"
        else:
            factors["family"] = "negative — large families had difficulty evacuating together"

        # Fare effect
        fare = profile.get("Fare", 0)
        if fare > 50:
            factors["fare"] = "positive — higher fare correlates with better cabin location"
        elif fare < 10:
            factors["fare"] = "negative — low fare indicates lower deck accommodations"

        return factors

    def predict_survival(self, raw_input: dict) -> dict:
        """
        Predict survival for a single passenger.

        Args:
            raw_input: Dict with keys matching TitanicInput schema.

        Returns:
            Dict with survived, survival_probability, confidence,
            risk_factors, passenger_profile, and input_features.
        """
        if not self.is_ready():
            raise RuntimeError("Titanic model is not initialized.")

        # Engineer features
        df = self._engineer_features(raw_input)

        # Predict
        prediction = self.model.predict(df)[0]
        survived = bool(prediction == 1)

        # Calibrated probability via sigmoid of decision function
        decision_val = self.model.decision_function(df)[0]
        survival_probability = round(float(self._sigmoid(decision_val)), 4)

        # Confidence = distance from 0.5 boundary, scaled to [0, 1]
        confidence = round(min(abs(survival_probability - 0.5) * 2, 1.0), 4)

        # Build profile dict for risk analysis
        profile = df.iloc[0].to_dict()
        risk_factors = self._analyze_risk_factors(profile)

        return {
            "survived": survived,
            "survival_probability": survival_probability,
            "confidence": confidence,
            "risk_factors": risk_factors,
            "passenger_profile": {
                "title": self._extract_title(raw_input.get("Name", "")),
                "class": raw_input.get("Pclass", 3),
                "age": float(df["Age"].iloc[0]),
                "sex": raw_input.get("Sex", "unknown"),
                "family_size": int(df["FamilySize"].iloc[0]),
                "is_alone": bool(df["IsAlone"].iloc[0]),
                "has_cabin": bool(df["HasCabin"].iloc[0]),
                "embarked": self._resolve_embarked(df),
                "fare": float(df["Fare"].iloc[0]),
            },
            "input_features": raw_input,
        }


# Singleton instance — initialized during app lifespan
titanic_service = TitanicModelService()
