from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    PROJECT_NAME: str = "Call ML Model"
    VERSION: str = "2.0.4"
    GROQ_API_KEY: str
    KNN_SERVICE_URL: str
    LOG_LEVEL: str
    AGENT_MODEL: str
    AGENT_TEMPERATURE: float

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8"
        )

settings = Settings()


