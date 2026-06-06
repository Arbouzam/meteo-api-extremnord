from fastapi import APIRouter

router = APIRouter(prefix="/health", tags=["health"])


@router.get("/", summary="Vérification de l'état de l'API")
async def health_check() -> dict:
    """Retourne le statut de l'API. Utilisé par les load balancers et le monitoring."""
    return {
        "status": "ok",
        "version": "1.0.0",
        "service": "phenomenes_extremes_api",
    }