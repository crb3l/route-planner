from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.routers import health, optimize
from app.vroom import VroomError, solve

app = FastAPI()


@app.exception_handler(VroomError)
async def handle_vroom_error(request: Request, error: VroomError):
    return JSONResponse(
        status_code=error.status_code,
        content={"detail": error.detail, "source":"vroom"},
    )

app.include_router(optimize.router, prefix="/api/v1")
app.include_router(health.router, prefix="/api/v1")