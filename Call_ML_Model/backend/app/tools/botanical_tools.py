import json
import httpx
from langchain_core.tools import tool
from app.config import settings


@tool
def predict_iris_species(
    sepal_length: float,
    sepal_width: float,
    petal_length: float,
    petal_width: float,
) -> str:
    """Predict the species of an iris flower given its measurements.
    Args:
        sepal_length: Sepal length in cm (0-15)
        sepal_width: Sepal width in cm (0-15)
        petal_length: Petal length in cm (0-15)
        petal_width: Petal width in cm (0-15)
    Returns:
        JSON string with predicted species, confidence, and probability distribution
    """
    payload = {
        "sepal_length": sepal_length,
        "sepal_width": sepal_width,
        "petal_length": petal_length,
        "petal_width": petal_width,
    }

    try:
        with httpx.Client(base_url=settings.KNN_SERVICE_URL, timeout=10.0) as client:
            response = client.post("/iris/predict", json=payload)
            response.raise_for_status()
            return json.dumps(response.json())
    except Exception as e:
        return json.dumps({"error": f"Failed to predict iris: {str(e)}"})


@tool
def predict_titanic_survival(
    Pclass: int,
    Name: str,
    Sex: str,
    Age: float | None = None,
    SibSp: int = 0,
    Parch: int = 0,
    Fare: float | None = None,
    Cabin: str | None = None,
    Embarked: str | None = None,
) -> str:
    """Predict whether a Titanic passenger would survive the 1912 disaster.
    Args:
        Pclass: Passenger class (1 = 1st, 2 = 2nd, 3 = 3rd)
        Name: Full passenger name (used for title extraction, e.g. "Smith, Mr. John")
        Sex: Biological sex ("male" or "female")
        Age: Age in years (null = model will impute)
        SibSp: Number of siblings/spouses aboard (default 0)
        Parch: Number of parents/children aboard (default 0)
        Fare: Ticket fare in pounds (null = model will impute)
        Cabin: Cabin number (null = unknown)
        Embarked: Port of embarkation (S=Southampton, C=Cherbourg, Q=Queenstown, null=default S)
    Returns:
        JSON string with survival prediction, probability, risk factors, and passenger profile
    """
    payload = {
        "Pclass": Pclass,
        "Name": Name,
        "Sex": Sex,
        "Age": Age,
        "SibSp": SibSp,
        "Parch": Parch,
        "Fare": Fare,
        "Cabin": Cabin,
        "Embarked": Embarked,
    }

    try:
        with httpx.Client(base_url=settings.KNN_SERVICE_URL, timeout=10.0) as client:
            response = client.post("/titanic/predict", json=payload)
            response.raise_for_status()
            return json.dumps(response.json())
    except Exception as e:
        return json.dumps({"error": f"Failed to predict survival: {str(e)}"})

@tool
def predict_loan_approval(
    no_of_dependents: int,
    education: str,
    self_employed: str,
    income_annum: float,
    loan_amount: float,
    loan_term: int,
    cibil_score: int,
    residential_assets_value: float = 0.0,
    commercial_assets_value: float = 0.0,
    luxury_assets_value: float = 0.0,
    bank_asset_value: float = 0.0,
) -> str:
    """Predict whether a loan application will be approved using RandomForestClassifier.
    Args:
        no_of_dependents: Number of financial dependents (0-10)
        education: Education level ("Graduate" or "Not Graduate")
        self_employed: Self-employment status ("Yes" or "No")
        income_annum: Annual income in INR (e.g. 5000000 for 50 lakhs)
        loan_amount: Requested loan amount in INR (e.g. 10000000 for 1 crore)
        loan_term: Loan repayment term in years (1-30)
        cibil_score: CIBIL credit score (300-900), higher is better
        residential_assets_value: Value of residential property owned (default 0)
        commercial_assets_value: Value of commercial property owned (default 0)
        luxury_assets_value: Value of luxury assets like vehicles/jewelry (default 0)
        bank_asset_value: Liquid assets in bank accounts (default 0)
    Returns:
        JSON string with approval decision, probability, CIBIL rating, risk factors, and financial summary
    """
    payload = {
        "no_of_dependents": no_of_dependents,
        "education": education,
        "self_employed": self_employed,
        "income_annum": income_annum,
        "loan_amount": loan_amount,
        "loan_term": loan_term,
        "cibil_score": cibil_score,
        "residential_assets_value": residential_assets_value,
        "commercial_assets_value": commercial_assets_value,
        "luxury_assets_value": luxury_assets_value,
        "bank_asset_value": bank_asset_value,
    }

    try:
        with httpx.Client(base_url=settings.KNN_SERVICE_URL, timeout=10.0) as client:
            response = client.post("/loan/predict", json=payload)
            response.raise_for_status()
            return json.dumps(response.json())
    except Exception as e:
        return json.dumps({"error": f"Failed to predict loan approval: {str(e)}"})

@tool
def get_model_info() -> str:
    """Get information about all loaded ML models including version and health status."""
    try:
        with httpx.Client(base_url=settings.KNN_SERVICE_URL, timeout=5.0) as client:
            response = client.get("/health/ready")
            response.raise_for_status()
            return json.dumps(response.json())
    except Exception as e:
        return json.dumps({"error": f"Failed to get model info: {str(e)}"})
