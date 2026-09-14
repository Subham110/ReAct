"""Router layer re-exports."""

from app.routers.iris_router import router as iris_router
from app.routers.titanic_router import router as titanic_router

__all__ = ["iris_router", "titanic_router"]
