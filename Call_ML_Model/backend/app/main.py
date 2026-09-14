from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.api.v1.chat import router as chat_router
from app.api.v1.health import router as health_router
from app.tools.knn_client import knn_client
from app.core.logging_config import setup_logging

setup_logging()

@asynccontextmanager
async def lifespan(app: FastAPI):
    await knn_client.startup()
    yield
    await knn_client.shutdown()

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chat_router)
app.include_router(health_router)

