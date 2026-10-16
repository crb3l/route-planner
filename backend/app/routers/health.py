from fastapi import APIRouter


router = APIRouter(tags=["health"])

@router.post("/health")
def health():
    return {"status": "ok"}