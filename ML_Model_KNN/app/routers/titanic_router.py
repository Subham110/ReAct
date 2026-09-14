"""
Titanic survival prediction API router.

Endpoints:
    POST /titanic/predict    — Single passenger survival prediction
    GET  /titanic/metadata   — Model metadata & feature info
"""

import logging

from fastapi import APIRouter, HTTPException, status

from app.schemas.titanic_schemas import (
    TitanicInput,
    TitanicPredictionResponse,
)
from app.services.titanic_service import titanic_service

logger = logging.getLogger("ml_api.titanic")

router = APIRouter(tags=["Titanic"])


@router.post(
    "/predict",
    response_model=TitanicPredictionResponse,
    status_code=status.HTTP_200_OK,
    summary="Predict Titanic passenger survival",
)
def predict_survival(passenger: TitanicInput):
    """
    Predict whether a Titanic passenger would survive.

    Accepts raw passenger data (name, class, sex, age, etc.) and applies
    feature engineering, imputation, and LinearSVC classification.
    Returns survival prediction with calibrated probability and risk factors.
    """
    try:
        result = titanic_service.predict_survival(passenger.model_dump())
        return result
    except Exception as e:
        logger.error("Titanic prediction error: %s", e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )


@router.get(
    "/metadata",
    status_code=status.HTTP_200_OK,
    summary="Titanic model metadata",
)
def get_metadata():
    """Return Titanic model version, accuracy, features, and training stats."""
    if not titanic_service.is_ready():
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Titanic model not loaded",
        )
    return titanic_service.metadata
