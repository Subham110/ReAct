from fastapi import APIRouter, HTTPException
from app.tools.knn_client import knn_client

router = APIRouter(tags=["health"])

@router.get("/health/live")
async def liveness():
    return {"status": "alive"}

@router.get("/health/ready")
async def readiness():
    try:
        knn_health = await knn_client.health_check()
        return {"status": "ready", "agent": True, "knn_service": knn_health.model_dump()}
    except Exception:
        raise HTTPException(503, detail="KNN service unavailable")
