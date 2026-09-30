from fastapi import FastAPI

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