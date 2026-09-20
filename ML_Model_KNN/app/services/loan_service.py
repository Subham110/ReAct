"""
Loan RandomForest Model Service — Singleton inference engine.

Loads the trained RandomForestClassifier pipeline and applies the same
feature encoding used during training to produce approval predictions
with calibrated probabilities.
"""

import json
import os
import logging

import joblib
import numpy as np
import pandas as pd

from app.config import settings
from app.schemas.loan_schemas import LoanInput, LoanPredictionResponse

logger = logging.getLogger("ml_api.loan")


class LoanModelService:
    """Manages the Loan RandomForestClassifier pipeline lifecycle and inference."""

    def __init__(self) -> None:
        self.model = None
        self.metadata: dict = {}

    def load_model(self) -> None:
        """Load the Loan pipeline and metadata from disk."""
        if not os.path.exists(settings.LOAN_MODEL_PATH):
            raise FileNotFoundError(
                f"Loan model not found at {settings.LOAN_MODEL_PATH}. "
                "Please run: uv run python train_loan.py"
            )

        self.model = joblib.load(settings.LOAN_MODEL_PATH)

        if os.path.exists(settings.LOAN_METADATA_PATH):
            with open(settings.LOAN_METADATA_PATH, "r") as f:
                self.metadata = json.load(f)
        else:
            self.metadata = {"model_version": "unknown", "model_type": "RandomForestClassifier"}

        logger.info(
            "Loan model loaded — version=%s, accuracy=%.2f%%",
            self.metadata.get("model_version", "?"),
            self.metadata.get("accuracy", 0) * 100,
        )

    def is_ready(self) -> bool:
        """Check if the model is loaded and ready for inference."""
        return self.model is not None

    def _get_cibil_rating(self, score: int) -> str:
        if score >= 750:
            return "Excellent"
        elif score >= 650:
            return "Good"
        elif score >= 550:
            return "Fair"
        else:
            return "Poor"

    def predict(self, req: LoanInput) -> LoanPredictionResponse:
        """Run inference and return a full loan approval response."""
        # Encode inputs to match training
        edu_val = 1 if req.education.strip().lower() == "graduate" else 0
        emp_val = 1 if req.self_employed.strip().lower() == "yes" else 0

        features = [
            req.no_of_dependents,
            edu_val,
            emp_val,
            req.income_annum,
            req.loan_amount,
            req.loan_term,
            req.cibil_score,
            req.residential_assets_value,
            req.commercial_assets_value,
            req.luxury_assets_value,
            req.bank_asset_value,
        ]

        feature_cols = self.metadata.get("features", [])
        df_input = pd.DataFrame([features], columns=feature_cols)

        probs = self.model.predict_proba(df_input)[0]  # [prob_rejected, prob_approved]
        approval_prob = float(probs[1])
        approved = bool(approval_prob >= 0.5)
        confidence = round(approval_prob if approved else 1.0 - approval_prob, 4)

        # Financial metrics
        total_assets = (
            req.residential_assets_value
            + req.commercial_assets_value
            + req.luxury_assets_value
            + req.bank_asset_value
        )
        asset_coverage = round(total_assets / req.loan_amount, 2) if req.loan_amount > 0 else 0.0
        loan_to_income = round(req.loan_amount / req.income_annum, 2) if req.income_annum > 0 else 0.0

        cibil_rating = self._get_cibil_rating(req.cibil_score)

        # Risk factor analysis
        risk_factors: dict[str, str] = {}

        if req.cibil_score >= 750:
            risk_factors["cibil_score"] = f"positive — excellent credit history, CIBIL {req.cibil_score} ({cibil_rating})"
        elif req.cibil_score >= 650:
            risk_factors["cibil_score"] = f"positive — good credit history, CIBIL {req.cibil_score} ({cibil_rating})"
        elif req.cibil_score >= 550:
            risk_factors["cibil_score"] = f"negative — fair credit, higher default risk, CIBIL {req.cibil_score} ({cibil_rating})"
        else:
            risk_factors["cibil_score"] = f"negative — poor credit history, CIBIL {req.cibil_score} ({cibil_rating})"

        if asset_coverage >= 2.0:
            risk_factors["collateral"] = f"positive — strong asset backing ({asset_coverage}x coverage ratio)"
        elif asset_coverage >= 1.0:
            risk_factors["collateral"] = f"positive — adequate asset collateral ({asset_coverage}x coverage ratio)"
        else:
            risk_factors["collateral"] = f"negative — insufficient collateral, assets only cover {asset_coverage}x of loan"

        if loan_to_income <= 3.0:
            risk_factors["income_ratio"] = f"positive — manageable loan-to-income ratio ({loan_to_income}x)"
        elif loan_to_income <= 6.0:
            risk_factors["income_ratio"] = f"neutral — moderate loan-to-income ratio ({loan_to_income}x)"
        else:
            risk_factors["income_ratio"] = f"negative — high loan-to-income ratio ({loan_to_income}x), repayment risk"

        if edu_val == 1:
            risk_factors["education"] = "positive — Graduate status associated with higher income stability"
        else:
            risk_factors["education"] = "neutral — Not Graduate, income stability assessed via other factors"

        return LoanPredictionResponse(
            approved=approved,
            approval_probability=round(approval_prob, 4),
            confidence=confidence,
            cibil_rating=cibil_rating,
            risk_factors=risk_factors,
            financial_summary={
                "total_assets": total_assets,
                "asset_coverage_ratio": asset_coverage,
                "loan_to_income_ratio": loan_to_income,
                "annual_income": req.income_annum,
                "loan_amount": req.loan_amount,
                "loan_term_years": req.loan_term,
            },
            feature_importance=self.metadata.get("feature_importance", {}),
            input_features=req.model_dump(),
        )


loan_service = LoanModelService()

