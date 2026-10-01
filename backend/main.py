import httpx
from fastapi import FastAPI

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
async def optimize(problem: dict):
    async with httpx.AsyncClient() as client:
        response = await client.post(VROOM_URL, json=problem)
    return response.json()