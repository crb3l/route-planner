from typing import Annotated

from fastapi import APIRouter, Query

from app.deps import HttpClient
from app.nominatim import reverse_geocode
from app.schemas import Coordinate, GeocodeResponse

router = APIRouter(tags=["geocode"])


@router.get("/geocode", response_model=GeocodeResponse)
async def geocode(point: Annotated[Coordinate, Query()], http: HttpClient):
    return await reverse_geocode(http, point)