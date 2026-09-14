"""
Polymorphic response schemas supporting both Iris and Titanic domains.

The VisualizationData model uses a `domain` discriminator field to indicate
which set of fields are populated, allowing the frontend to conditionally
render the correct visualizer.
"""

from pydantic import BaseModel, Field
from typing import Optional, Any


# ── Iris-specific models ───────────────────────────────

class PredictionDetail(BaseModel):
    species: str
    confidence: float


class ProbabilityEntry(BaseModel):
    species: str
    probability: float


class FeatureComparison(BaseModel):
    feature: str
    input_value: float
    setosa_avg: float
    versicolor_avg: float
    virginica_avg: float


# ── Polymorphic Visualization Data ─────────────────────

class VisualizationData(BaseModel):
    """
    Unified response from the AI agent.

    When domain="iris":  prediction, probabilities, feature_comparison are populated.
    When domain="titanic": survived, survival_probability, confidence, risk_factors,
                           passenger_profile are populated.
    Both domains always have: analysis, visualization_hints.
    """

    domain: str = Field(..., description='Domain discriminator: "iris" or "titanic"')

    # ── Iris fields (present when domain="iris") ───────
    prediction: Optional[PredictionDetail] = None
    probabilities: Optional[list[ProbabilityEntry]] = None
    feature_comparison: Optional[list[FeatureComparison]] = None

    # ── Titanic fields (present when domain="titanic") ─
    survived: Optional[bool] = None
    survival_probability: Optional[float] = None
    confidence: Optional[float] = None
    risk_factors: Optional[dict[str, str]] = None
    passenger_profile: Optional[dict[str, Any]] = None

    # ── Shared fields ──────────────────────────────────
    analysis: str
    visualization_hints: dict[str, str] = Field(default_factory=dict)


# ── API Envelope ───────────────────────────────────────

class AnalyzeResponse(BaseModel):
    success: bool
    data: Optional[VisualizationData] = None
    raw_query: str
    processing_time_ms: float
    error: Optional[str] = None
