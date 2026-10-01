import httpx
from fastapi import FastAPI

from schemas import OptimizeRequest
from vroom import to_vroom

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

@app.post("/optimize")
async def optimize(problem: OptimizeRequest):
    async with httpx.AsyncClient() as client:
        response = await client.post(VROOM_URL, json=to_vroom(problem))
    return response.json()