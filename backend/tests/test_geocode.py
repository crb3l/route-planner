import asyncio
import time

import pytest

from app import nominatim
from app.nominatim import RateLimiter, make_label
from app.settings import settings

PALACE = {  # a real Nominatim answer, shortened
    "name": "Palais princier de Monaco",
    "address": {"road": "Place du Palais", "town": "Monaco", "country": "Monaco"},
    "display_name": "Palais princier de Monaco, Place du Palais, Monaco-Ville, Monaco, 98000, Monaco",
}


@pytest.fixture(autouse=True)
def empty_cache():
    nominatim.cache.clear()


def test_make_label():
    with_number = {"address": {"road": "Strada Lipscani", "house_number": "12"}, "display_name": "..."}
    no_street = {"name": "France métropolitaine", "address": {}, "display_name": "France métropolitaine, France"}

    assert make_label(with_number) == "Strada Lipscani 12"
    assert make_label(PALACE) == "Place du Palais"
    assert make_label(no_street) == "France métropolitaine"


def test_geocode_returns_label_and_display_name(client, monkeypatch):
    async def fake_fetch_place(http, lat, lng):
        return PALACE

    monkeypatch.setattr(nominatim, "fetch_place", fake_fetch_place)

    response = client.get("/api/v1/geocode", params={"lat": 43.7311, "lng": 7.4197})

    assert response.status_code == 200
    assert response.json() == {"label": "Place du Palais", "displayName": PALACE["display_name"]}


def test_nothing_here_gives_404(client, monkeypatch):
    async def fake_fetch_place(http, lat, lng):
        return {"error": "Unable to geocode"}

    monkeypatch.setattr(nominatim, "fetch_place", fake_fetch_place)

    response = client.get("/api/v1/geocode", params={"lat": 0, "lng": 0})

    assert response.status_code == 404


def test_asks_nominatim_only_once_per_place(client, monkeypatch):
    calls = []

    async def fake_fetch_place(http, lat, lng):
        calls.append((lat, lng))
        return PALACE

    monkeypatch.setattr(nominatim, "fetch_place", fake_fetch_place)

    client.get("/api/v1/geocode", params={"lat": 43.7311, "lng": 7.4197})
    client.get("/api/v1/geocode", params={"lat": 43.7311, "lng": 7.4197})

    assert len(calls) == 1


def test_bad_latitude_gives_422(client):
    response = client.get("/api/v1/geocode", params={"lat": 200, "lng": 7.4197})

    assert response.status_code == 422


def test_address_service_down_gives_502(client, monkeypatch):
    monkeypatch.setattr(settings, "nominatim_url", "http://localhost:1")

    response = client.get("/api/v1/geocode", params={"lat": 43.7311, "lng": 7.4197})

    assert response.status_code == 502


def test_rate_limiter_spaces_calls_out():
    limiter = RateLimiter(interval=0.2)

    async def three_calls():
        start = time.monotonic()
        for _ in range(3):
            await limiter.wait()
        return time.monotonic() - start

    assert asyncio.run(three_calls()) >= 0.4