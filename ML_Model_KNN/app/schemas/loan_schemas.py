"""Loan Approval Pydantic schemas for ML_Model_KNN API."""

from pydantic import BaseModel, Field
from typing import Any


class LoanInput(BaseModel):
    """Input features for loan approval prediction."""

    no_of_dependents: int = Field(..., ge=0, le=10, description="Number of dependents")
    
    education: str = Field(..., description="'Graduate' or 'Not Graduate'")
    
    self_employed: str = Field(..., description="'Yes' or 'No'")
    
    income_annum: float = Field(..., gt=0, description="Annual income in INR")
    
    loan_amount: float = Field(..., gt=0, description="Requested loan amount in INR")
    
    loan_term: int = Field(..., gt=0, le=30, description="Loan term in years")
    
    cibil_score: int = Field(..., ge=300, le=900, description="CIBIL credit score (300-900)")
    
    residential_assets_value: float = Field(default=0.0, ge=0, description="Residential assets value in INR")
    
    commercial_assets_value: float = Field(default=0.0, ge=0, description="Commercial assets value in INR")
    
    luxury_assets_value: float = Field(default=0.0, ge=0, description="Luxury assets value in INR")
    
    bank_asset_value: float = Field(default=0.0, ge=0, description="Bank/liquid assets value in INR")


class LoanPredictionResponse(BaseModel):
    """Full loan approval prediction response with risk analysis."""

    approved: bool
    approval_probability: float
    confidence: float
    cibil_rating: str
    risk_factors: dict[str, str]
    financial_summary: dict[str, Any]
    feature_importance: dict[str, float]
    input_features: dict[str, Any]

