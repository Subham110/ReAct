from pydantic import BaseModel, Field
from typing import Optional
from app.schemas.ml_contract import IrisFeatures

class AnalyzeRequest(BaseModel):
    query: str = Field(..., min_length=1, max_length=1000, description="Natural language query or iris measurements")
    measurements: Optional[IrisFeatures] = Field(None, description="Direct measurements if provided")
