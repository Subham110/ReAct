import os
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "ML Model Inference API"
    VERSION: str = "2.0.8"

    # Iris KNN Model
    IRIS_MODEL_PATH: str = os.getenv("IRIS_MODEL_PATH", "models/knn_pipeline.joblib")
    IRIS_METADATA_PATH: str = os.getenv("IRIS_METADATA_PATH", "models/model_metadata.json")

    # Titanic LinearSVC Model
    TITANIC_MODEL_PATH: str = os.getenv("TITANIC_MODEL_PATH", "models/titanic_pipeline.joblib")
    TITANIC_METADATA_PATH: str = os.getenv("TITANIC_METADATA_PATH", "models/titanic_metadata.json")

    # Loan RandomForest Model
    LOAN_MODEL_PATH: str = os.getenv("LOAN_MODEL_PATH", "models/loan_pipeline.joblib")
    LOAN_METADATA_PATH: str = os.getenv("LOAN_METADATA_PATH", "models/loan_metadata.json")

    #General
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")

    model_config = {"env_file": ".env", "extra": "ignore"}


settings = Settings()
