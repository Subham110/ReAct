"""Health check response schemas for multi-model API."""

from pydantic import BaseModel


class ModelStatusDetail(BaseModel):
    """Status of an individual model."""

    loaded: bool
    version: str
    model_type: str


class HealthResponse(BaseModel):
    """Aggregated health status for all loaded models."""

    status: str
    models: dict[str, ModelStatusDetail]
