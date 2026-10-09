from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from schemas import OptimizeRequest, OptimizeResponse
from vroom import VroomError, solve

app = FastAPI()
@app.get("/")
def hello():
    return {"message": "Hello from route-planner"}

@app.get("/add")
def add(a: int, b: int):
    return {"result": a + b}

@app.get("/multiply")
def multiply(a: int, b: int):
    return {"result": a * b}

@app.exception_handler(VroomError)
async def handle_vroom_error(request: Request, error: VroomError):
    return JSONResponse(
        status_code=error.status_code,
        content={"detail": error.detail, "source":"vroom"},
    )

@app.post("/optimize", response_model=OptimizeResponse)
async def optimize(problem: OptimizeRequest):
    return await solve(problem)