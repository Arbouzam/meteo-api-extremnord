from fastapi import APIRouter, Depends

from app.security import verify_api_key

router = APIRouter()

@router.get("/health")
def health(
    api_key: str = Depends(verify_api_key)
):
    return {
        "status": "ok",
        "message": "API Phénomènes Extrêmes opérationnelle"
    }