"""Loan Approval REST API router."""

from fastapi import APIRouter
from app.schemas.loan_schemas import LoanInput, LoanPredictionResponse
from app.services.loan_service import loan_service

router = APIRouter(tags=["loan"])


@router.post("/predict", response_model=LoanPredictionResponse)
def predict_loan(input_data: LoanInput):
    """
    Predict loan approval using RandomForestClassifier.

    Returns approval decision, probability, CIBIL rating, risk factors,
    and financial summary metrics.
    """
    return loan_service.predict(input_data)


@router.get("/metadata")
def get_loan_metadata():
    """Returns model version, accuracy, feature list, and feature importance scores."""
    return loan_service.metadata

