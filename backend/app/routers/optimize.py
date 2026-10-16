from fastapi import APIRouter

from app.schemas import OptimizeRequest, OptimizeResponse
from app.vroom import solve

router = APIRouter(tags=["optimize"])

@router.post("/optimize", response_model=OptimizeResponse)
async def optimize(problem: OptimizeRequest):
    return await solve(problem)