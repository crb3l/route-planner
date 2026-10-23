from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from app.routers import health, optimize, geocode
from app.vroom import VroomError
from app.settings import settings

from contextlib import asynccontextmanager

import httpx

@asynccontextmanager
async def lifespan(app: FastAPI):
    #runs once, when the server starts
    app.state.http = httpx.AsyncClient(timeout=settings.vroom_timeout)
    yield
    #runs once, when the server stops
    await app.state.http.aclose()

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_methods=['*'],
    allow_headers=['*']
)


@app.exception_handler(VroomError)
async def handle_vroom_error(request: Request, error: VroomError):
    return JSONResponse(
        status_code=error.status_code,
        content={"detail": error.detail, "source":"vroom"},
    )

app.include_router(optimize.router, prefix="/api/v1")
app.include_router(health.router, prefix="/api/v1")
app.include_router(geocode.router, prefix="/api/v1")