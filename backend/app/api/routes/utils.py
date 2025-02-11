from fastapi import APIRouter

router = APIRouter()

@router.get("/health-check/", tags=["utils"])
def health_check():
    return {"status": "ok"}
