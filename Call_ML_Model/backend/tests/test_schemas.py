"""Tests for Pydantic models in ml_contract and response_schemas."""

import pytest
from pydantic import ValidationError
from app.schemas.ml_contract import LoanFeatures, LoanPrediction, IrisFeatures, TitanicPassenger
from app.schemas.response_schemas import VisualizationData


def test_iris_features_valid():
    feat = IrisFeatures(sepal_length=5.1, sepal_width=3.5, petal_length=1.4, petal_width=0.2)
    assert feat.sepal_length == 5.1


def test_iris_features_invalid():
    with pytest.raises(ValidationError):
        IrisFeatures(sepal_length=-1.0, sepal_width=3.5, petal_length=1.4, petal_width=0.2)


def test_titanic_passenger_valid():
    p = TitanicPassenger(Pclass=1, Name="Smith, Mr. John", Sex="male", Age=30.0)
    assert p.Pclass == 1
    assert p.SibSp == 0


def test_titanic_passenger_invalid_class():
    with pytest.raises(ValidationError):
        TitanicPassenger(Pclass=4, Name="Bad, Mr.", Sex="male")


def test_loan_features_valid():
    loan = LoanFeatures(
        no_of_dependents=2,
        education="Graduate",
        self_employed="No",
        income_annum=5000000.0,
        loan_amount=10000000.0,
        loan_term=10,
        cibil_score=750,
        residential_assets_value=5000000.0,
        commercial_assets_value=0.0,
        luxury_assets_value=1000000.0,
        bank_asset_value=1500000.0,
    )
    assert loan.cibil_score == 750
    assert loan.loan_term == 10


def test_loan_features_invalid_cibil():
    with pytest.raises(ValidationError):
        LoanFeatures(
            no_of_dependents=2,
            education="Graduate",
            self_employed="No",
            income_annum=5000000.0,
            loan_amount=10000000.0,
            loan_term=10,
            cibil_score=200,  # below 300 minimum
        )


def test_polymorphic_visualization_data_iris():
    data = VisualizationData(
        domain="iris",
        prediction={"species": "setosa", "confidence": 0.95},
        analysis="Setosa prediction",
    )
    assert data.domain == "iris"
    assert data.prediction.species == "setosa"
    assert data.approved is None


def test_polymorphic_visualization_data_loan():
    data = VisualizationData(
        domain="loan",
        approved=True,
        approval_probability=0.92,
        cibil_rating="Good",
        analysis="Approved due to high credit",
    )
    assert data.domain == "loan"
    assert data.approved is True
    assert data.cibil_rating == "Good"
    assert data.prediction is None

