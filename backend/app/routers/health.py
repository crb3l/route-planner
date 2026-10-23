import httpx
from fastapi import APIRouter, Response

from app.deps import HttpClient
from app.schemas import HealthResponse
from app.settings import settings

router = APIRouter(tags=["health"])


async def is_up(http: httpx.AsyncClient, url: str) -> bool:
    try:
        response = await http.get(url, timeout=2)
    except httpx.HTTPError:
        return False
    return response.status_code == 200


@router.get("/health", response_model=HealthResponse)
async def health(response: Response, http: HttpClient):
    vroom_up = await is_up(http, f"{settings.vroom_url}/health")
    # OSRM has no health URL, so ask it a tiny real question: the road nearest to 0,0
    osrm_up = await is_up(http, f"{settings.osrm_url}/nearest/v1/driving/0,0")

    all_up = vroom_up and osrm_up
    if not all_up:
        response.status_code = 503

    return HealthResponse(status="ok" if all_up else "degraded", vroom=vroom_up, osrm=osrm_up)