"""
ML Model Inference API — Root FastAPI Application.

Mounts domain-specific routers for Iris and Titanic prediction
models under /iris/* and /titanic/* prefixes respectively.
"""

import time
import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, Request, status
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.routers.iris_router import router as iris_router
from app.routers.titanic_router import router as titanic_router
from app.services.iris_service import iris_service
from app.services.titanic_service import titanic_service
from app.schemas.health_schemas import HealthResponse, ModelStatusDetail


# ── Logging ─────────────────────────────────────────────
logging.basicConfig(
    level=settings.LOG_LEVEL,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)
logger = logging.getLogger("ml_api")


# ── Lifespan — loads all models once at startup ────────
@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Initializing ML Model Inference Service v%s ...", settings.VERSION)

    # Load Iris model
    try:
        iris_service.load_model()
        logger.info("✓ Iris KNN model loaded successfully.")
    except Exception as e:
        logger.error("✗ Failed to load Iris model: %s", e)

    # Load Titanic model
    try:
        titanic_service.load_model()
        logger.info("✓ Titanic LinearSVC model loaded successfully.")
    except Exception as e:
        logger.error("✗ Failed to load Titanic model: %s", e)

    yield
    logger.info("Shutting down ML Model Inference Service.")


# ── FastAPI app instance ────────────────────────────────
app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="Multi-model ML inference API serving Iris classification and Titanic survival prediction.",
    lifespan=lifespan,
)


# ── CORS ────────────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ── Request latency tracking middleware ─────────────────
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.perf_counter()
    response = await call_next(request)
    process_time = (time.perf_counter() - start_time) * 1000
    response.headers["X-Process-Time-Ms"] = f"{process_time:.2f}"
    logger.info(
        "%s %s — %d — %.2fms",
        request.method,
        request.url.path,
        response.status_code,
        process_time,
    )
    return response


# ── Global health endpoints ────────────────────────────

@app.get("/health/live", status_code=status.HTTP_200_OK)
def liveness():
    """Liveness probe — confirms the process is alive."""
    return {"status": "alive"}


@app.get(
    "/health/ready",
    response_model=HealthResponse,
    status_code=status.HTTP_200_OK,
)
def readiness():
    """Readiness probe — reports load status of every model."""
    iris_ready = iris_service.is_ready()
    titanic_ready = titanic_service.is_ready()

    models = {
        "iris": ModelStatusDetail(
            loaded=iris_ready,
            version=iris_service.metadata.get("model_version", "unknown"),
            model_type=iris_service.metadata.get("model_type", "KNN"),
        ),
        "titanic": ModelStatusDetail(
            loaded=titanic_ready,
            version=titanic_service.metadata.get("model_version", "unknown"),
            model_type=titanic_service.metadata.get("model_type", "LinearSVC"),
        ),
    }

    all_ready = iris_ready and titanic_ready

    if not all_ready:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Not all models are ready",
        )

    return HealthResponse(status="ready", models=models)


# ── Mount domain routers ───────────────────────────────
app.include_router(iris_router, prefix="/iris")
app.include_router(titanic_router, prefix="/titanic")
