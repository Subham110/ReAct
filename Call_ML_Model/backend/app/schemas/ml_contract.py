"""
Data contracts matching the ML_Model_KNN microservice API schemas.

These models mirror the Pydantic schemas defined in ML_Model_KNN
to ensure type-safe communication between the agent backend and
the ML inference service.
"""

from pydantic import BaseModel, Field
from typing import Any, Optional


# ── Iris Contracts ─────────────────────────────────────

class IrisFeatures(BaseModel):
    sepal_length: float = Field(..., gt=0.0, lt=15.0)
    sepal_width: float = Field(..., gt=0.0, lt=15.0)
    petal_length: float = Field(..., gt=0.0, lt=15.0)
    petal_width: float = Field(..., gt=0.0, lt=15.0)


class KNNPrediction(BaseModel):
    predicted_species: str
    confidence: float
    probabilities: dict[str, float]
    input_features: dict[str, float]


class KNNBatchResponse(BaseModel):
    predictions: list[KNNPrediction]
    total_samples: int


# ── Titanic Contracts ──────────────────────────────────

class TitanicPassenger(BaseModel):
    Pclass: int = Field(..., ge=1, le=3)
    Name: str
    Sex: str
    Age: Optional[float] = None
    SibSp: int = 0
    Parch: int = 0
    Fare: Optional[float] = None
    Cabin: Optional[str] = None
    Embarked: Optional[str] = None


class TitanicPrediction(BaseModel):
    survived: bool
    survival_probability: float
    confidence: float
    risk_factors: dict[str, str]
    passenger_profile: dict[str, Any]
    input_features: dict[str, Any]


# ── Health Contracts ───────────────────────────────────

class ModelStatusDetail(BaseModel):
    loaded: bool
    version: str
    model_type: str


class KNNHealthResponse(BaseModel):
    status: str
    models: dict[str, ModelStatusDetail]
