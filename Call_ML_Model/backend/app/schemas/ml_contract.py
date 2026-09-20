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


# ── Loan Contracts ─────────────────────────────────────

class LoanFeatures(BaseModel):
    no_of_dependents: int = Field(..., ge=0, le=10)
    education: str = Field(..., description="'Graduate' or 'Not Graduate'")
    self_employed: str = Field(..., description="'Yes' or 'No'")
    income_annum: float = Field(..., gt=0)
    loan_amount: float = Field(..., gt=0)
    loan_term: int = Field(..., gt=0, le=30)
    cibil_score: int = Field(..., ge=300, le=900)
    residential_assets_value: float = Field(default=0.0, ge=0)
    commercial_assets_value: float = Field(default=0.0, ge=0)
    luxury_assets_value: float = Field(default=0.0, ge=0)
    bank_asset_value: float = Field(default=0.0, ge=0)


class LoanPrediction(BaseModel):
    approved: bool
    approval_probability: float
    confidence: float
    cibil_rating: str
    risk_factors: dict[str, str]
    financial_summary: dict[str, Any]
    feature_importance: dict[str, float]
    input_features: dict[str, Any]


# ── Health Contracts ───────────────────────────────────

class ModelStatusDetail(BaseModel):
    loaded: bool
    version: str
    model_type: str


class KNNHealthResponse(BaseModel):
    status: str
    models: dict[str, ModelStatusDetail]
