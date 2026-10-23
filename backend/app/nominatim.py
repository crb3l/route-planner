import asyncio
import time

import httpx
from fastapi import HTTPException

from app.schemas import Coordinate, GeocodeResponse
from app.settings import settings

class RateLimiter:
    """Lets one call through per `interval` seconds. Later callers wait their turn."""

    def __init__(self, interval: float):
        self.interval = interval
        self.lock = asyncio.Lock()
        self.last_call = 0.0

    async def wait(self):
        async with self.lock:
            delay = self.last_call + self.interval - time.monotonic()
            if delay > 0:
                await asyncio.sleep(delay)
            self.last_call = time.monotonic()

limiter = RateLimiter(interval = 1.0) # at most 1 request per second
cache: dict[tuple[float, float], GeocodeResponse | None] = {} # None = no address here

def make_label(place: dict) -> str:
    address = place.get("address", {})
    road = address.get("road")
    number = address.get("house_number")

    if road and number:
        return f"{road} {number}"
    if road:
        return road
    return place.get("name") or place["display_name"].split(",")[0]

async def fetch_place(http: httpx.AsyncClient, lat: float, lng: float) -> dict:
    await limiter.wait()
    try:
        response = await http.get(
            f"{settings.nominatim_url}/reverse",
            params={"format": "jsonv2", "lat": lat, "lon": lng},
            headers={"User-Agent": settings.nominatim_user_agent},
            timeout=10,
        )
    except httpx.TimeoutException:
        raise HTTPException(status_code=504, detail="The address service didn't answer in time")
    except httpx.HTTPError:
        raise HTTPException(status_code=502, detail="Can't reach the address service")
    if response.status_code != 200:
        raise HTTPException(status_code=502, detail=f"The address service answered {response.status_code}")
    return response.json()

async def reverse_geocode(http: httpx.AsyncClient, point: Coordinate) -> GeocodeResponse:
    key = (round(point.lat, 5), round(point.lng, 5))  # 5 decimals = about 1 metre
    if key not in cache:
        place = await fetch_place(http, *key)
        if "error" in place:
            cache[key] = None
        else:
            cache[key] = GeocodeResponse(label=make_label(place), display_name=place["display_name"])
    if cache[key] is None:
        raise HTTPException(status_code=404, detail="No address found here")
    return cache[key]