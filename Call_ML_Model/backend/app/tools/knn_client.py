"""
ML Model API HTTP Client with retry logic.

Provides async methods for both Iris and Titanic prediction endpoints,
plus health checking against the multi-model inference service.
"""

import httpx
import asyncio
import logging

from app.config import settings
from app.schemas.ml_contract import (
    IrisFeatures,
    KNNPrediction,
    KNNBatchResponse,
    KNNHealthResponse,
    TitanicPassenger,
    TitanicPrediction,
)
from app.core.exceptions import KNNServiceUnavailable

logger = logging.getLogger(__name__)


class MLClient:
    """Async HTTP client connecting to the ML Model Inference API on :8000."""

    def __init__(self, base_url: str):
        self.base_url = base_url
        self._client: httpx.AsyncClient | None = None

    async def startup(self):
        self._client = httpx.AsyncClient(base_url=self.base_url, timeout=10.0)

    async def shutdown(self):
        if self._client:
            await self._client.aclose()

    # ── Iris Endpoints ─────────────────────────────────

    async def predict_iris(self, features: IrisFeatures) -> KNNPrediction:
        """POST /iris/predict with exponential backoff retry."""
        delays = [0.5, 1.0, 2.0]
        for attempt, delay in enumerate(delays + [0]):
            try:
                response = await self._client.post(
                    "/iris/predict", json=features.model_dump()
                )
                response.raise_for_status()
                return KNNPrediction.model_validate(response.json())
            except httpx.RequestError as e:
                if attempt < len(delays):
                    logger.warning(
                        "Iris predict attempt %d failed, retrying in %.1fs...",
                        attempt + 1, delay,
                    )
                    await asyncio.sleep(delay)
                else:
                    logger.error("Iris predict failed after retries: %s", e)
                    raise KNNServiceUnavailable(str(e))

    async def predict_iris_batch(self, samples: list[IrisFeatures]) -> KNNBatchResponse:
        """POST /iris/predict/batch."""
        try:
            response = await self._client.post(
                "/iris/predict/batch",
                json={"samples": [s.model_dump() for s in samples]},
            )
            response.raise_for_status()
            return KNNBatchResponse.model_validate(response.json())
        except httpx.RequestError as e:
            logger.error("Iris batch predict failed: %s", e)
            raise KNNServiceUnavailable(str(e))

    # ── Titanic Endpoints ──────────────────────────────

    async def predict_titanic(self, passenger: TitanicPassenger) -> TitanicPrediction:
        """POST /titanic/predict with exponential backoff retry."""
        delays = [0.5, 1.0, 2.0]
        for attempt, delay in enumerate(delays + [0]):
            try:
                response = await self._client.post(
                    "/titanic/predict", json=passenger.model_dump()
                )
                response.raise_for_status()
                return TitanicPrediction.model_validate(response.json())
            except httpx.RequestError as e:
                if attempt < len(delays):
                    logger.warning(
                        "Titanic predict attempt %d failed, retrying in %.1fs...",
                        attempt + 1, delay,
                    )
                    await asyncio.sleep(delay)
                else:
                    logger.error("Titanic predict failed after retries: %s", e)
                    raise KNNServiceUnavailable(str(e))

    # ── Health ─────────────────────────────────────────

    async def health_check(self) -> KNNHealthResponse:
        """GET /health/ready — reports status of all loaded models."""
        try:
            response = await self._client.get("/health/ready")
            response.raise_for_status()
            return KNNHealthResponse.model_validate(response.json())
        except httpx.RequestError as e:
            logger.error("ML service health check failed: %s", e)
            raise KNNServiceUnavailable(str(e))


# Singleton — backward compatible name for existing imports
knn_client = MLClient(settings.KNN_SERVICE_URL)
