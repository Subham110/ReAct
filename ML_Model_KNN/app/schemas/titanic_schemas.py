"""Pydantic validation schemas for the Titanic survival prediction API."""

from typing import Any
from pydantic import BaseModel, Field


class TitanicInput(BaseModel):
    """Raw passenger data matching the Titanic dataset columns."""

    Pclass: int = Field(
        ..., ge=1, le=3,
        description="Passenger class (1 = 1st, 2 = 2nd, 3 = 3rd)",
    )
    Name: str = Field(
        ..., min_length=1,
        description="Full passenger name (used for title extraction)",
    )
    Sex: str = Field(
        ..., pattern=r"^(male|female)$",
        description="Biological sex",
    )
    Age: float | None = Field(
        None, ge=0, le=120,
        description="Age in years (null = imputed by model)",
    )
    SibSp: int = Field(
        0, ge=0, le=10,
        description="Number of siblings/spouses aboard",
    )
    Parch: int = Field(
        0, ge=0, le=10,
        description="Number of parents/children aboard",
    )
    Fare: float | None = Field(
        None, ge=0,
        description="Ticket fare in pounds (null = imputed by model)",
    )
    Cabin: str | None = Field(
        None,
        description="Cabin number (null = unknown, used for HasCabin flag)",
    )
    Embarked: str | None = Field(
        None, pattern=r"^[CSQ]$",
        description="Port of embarkation (C = Cherbourg, Q = Queenstown, S = Southampton)",
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "Pclass": 3,
                    "Name": "Braund, Mr. Owen Harris",
                    "Sex": "male",
                    "Age": 22,
                    "SibSp": 1,
                    "Parch": 0,
                    "Fare": 7.25,
                    "Cabin": None,
                    "Embarked": "S",
                }
            ]
        }
    }


class TitanicPredictionResponse(BaseModel):
    """Structured prediction result for a Titanic passenger."""

    survived: bool
    survival_probability: float = Field(
        ..., ge=0.0, le=1.0,
        description="Calibrated survival probability (sigmoid of decision function)",
    )
    confidence: float = Field(
        ..., ge=0.0, le=1.0,
        description="Prediction confidence (distance from decision boundary)",
    )
    risk_factors: dict[str, str] = Field(
        ...,
        description="Positive and negative factors affecting survival",
    )
    passenger_profile: dict[str, Any] = Field(
        ...,
        description="Engineered features used by the model",
    )
    input_features: dict[str, Any] = Field(
        ...,
        description="Original raw input values",
    )
