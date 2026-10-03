import httpx
from fastapi import FastAPI

from schemas import OptimizeRequest, OptimizeResponse
from vroom import from_vroom, to_vroom

VROOM_URL = "http://localhost:3000"

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

@app.post("/optimize", response_model=OptimizeResponse)
async def optimize(problem: OptimizeRequest):
    async with httpx.AsyncClient() as client:
        response = await client.post(VROOM_URL, json=to_vroom(problem))
    return from_vroom(response.json())