import time
from fastapi import APIRouter, HTTPException
from app.schemas.request_schemas import AnalyzeRequest
from app.schemas.response_schemas import AnalyzeResponse
from app.agents.botanical_agent import botanical_agent
from app.core.exceptions import KNNServiceUnavailable, AgentExecutionError

router = APIRouter(prefix="/api/v1", tags=["agent"])

@router.post("/analyze", response_model=AnalyzeResponse)
async def analyze(request: AnalyzeRequest):
    start = time.perf_counter()
    try:
        data = await botanical_agent.analyze(
            query=request.query
        )
        
        elapsed = (time.perf_counter() - start) * 1000
        return AnalyzeResponse(
            success=True,
            data=data,
            raw_query=request.query,
            processing_time_ms=round(elapsed, 2)
        )
    except KNNServiceUnavailable as e:
        raise HTTPException(503, detail=f"KNN Service Error: {str(e)}")
    except AgentExecutionError as e:
        raise HTTPException(500, detail=f"Agent Error: {str(e)}")
    except Exception as e:
        raise HTTPException(500, detail=f"Internal Server Error: {str(e)}")
