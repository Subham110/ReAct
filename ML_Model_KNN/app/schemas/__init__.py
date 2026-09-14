"""Centralized schema re-exports for backward compatibility."""

from app.schemas.iris_schemas import (
    IrisInput,
    IrisBatchInput,
    IrisPredictionResponse,
    IrisBatchPredictionResponse,
)
from app.schemas.titanic_schemas import (
    TitanicInput,
    TitanicPredictionResponse,
)
from app.schemas.health_schemas import (
    HealthResponse,
    ModelStatusDetail,
)

__all__ = [
    "IrisInput",
    "IrisBatchInput",
    "IrisPredictionResponse",
    "IrisBatchPredictionResponse",
    "TitanicInput",
    "TitanicPredictionResponse",
    "HealthResponse",
    "ModelStatusDetail",
]
