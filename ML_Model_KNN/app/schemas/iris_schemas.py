"""Pydantic validation schemas for the Iris KNN prediction API."""

from pydantic import BaseModel, Field


class IrisInput(BaseModel):
    """Single Iris sample with strict biological boundary constraints."""

    sepal_length: float = Field(
        ..., gt=0.0, lt=15.0, examples=[5.1], description="Sepal length in cm"
    )
    sepal_width: float = Field(
        ..., gt=0.0, lt=15.0, examples=[3.5], description="Sepal width in cm"
    )
    petal_length: float = Field(
        ..., gt=0.0, lt=15.0, examples=[1.4], description="Petal length in cm"
    )
    petal_width: float = Field(
        ..., gt=0.0, lt=15.0, examples=[0.2], description="Petal width in cm"
    )


class IrisBatchInput(BaseModel):
    """Batch of Iris samples for bulk prediction."""

    samples: list[IrisInput]


class IrisPredictionResponse(BaseModel):
    """Prediction output for a single Iris sample."""

    predicted_species: str
    confidence: float
    probabilities: dict[str, float]
    input_features: dict[str, float]


class IrisBatchPredictionResponse(BaseModel):
    """Batch prediction output with sample count."""

    predictions: list[IrisPredictionResponse]
    total_samples: int
