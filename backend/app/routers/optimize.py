from fastapi import APIRouter

from app.schemas import OptimizeRequest, OptimizeResponse
from app.vroom import solve
from app.deps import HttpClient

router = APIRouter(tags=["optimize"])

@router.post("/optimize", response_model=OptimizeResponse)
async def optimize(problem: OptimizeRequest, http: HttpClient):
    return await solve(problem, http)