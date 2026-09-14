"""
Iris prediction API router.

Endpoints:
    POST /iris/predict       — Single sample prediction
    POST /iris/predict/batch — Batch prediction
    GET  /iris/metadata      — Model metadata & training info
"""

import logging

from fastapi import APIRouter, HTTPException, status

from app.schemas.iris_schemas import (
    IrisInput,
    IrisBatchInput,
    IrisPredictionResponse,
    IrisBatchPredictionResponse,
)
from app.services.iris_service import iris_service

logger = logging.getLogger("ml_api.iris")

router = APIRouter(tags=["Iris"])


@router.post(
    "/predict",
    response_model=IrisPredictionResponse,
    status_code=status.HTTP_200_OK,
    summary="Predict Iris species",
)
def predict_single(item: IrisInput):
    """Classify a single Iris flower sample into setosa/versicolor/virginica."""
    try:
        results = iris_service.predict([item.model_dump()])
        return results[0]
    except Exception as e:
        logger.error("Iris prediction error: %s", e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )


@router.post(
    "/predict/batch",
    response_model=IrisBatchPredictionResponse,
    status_code=status.HTTP_200_OK,
    summary="Batch predict Iris species",
)
def predict_batch(batch: IrisBatchInput):
    """Classify multiple Iris flower samples in a single request."""
    try:
        feature_list = [sample.model_dump() for sample in batch.samples]
        results = iris_service.predict(feature_list)
        return {"predictions": results, "total_samples": len(results)}
    except Exception as e:
        logger.error("Iris batch prediction error: %s", e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )


@router.get(
    "/metadata",
    status_code=status.HTTP_200_OK,
    summary="Iris model metadata",
)
def get_metadata():
    """Return Iris model version, accuracy, features, and classes."""
    if not iris_service.is_ready():
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Iris model not loaded",
        )
    return iris_service.metadata
