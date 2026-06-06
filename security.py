import os
import secrets

from dotenv import load_dotenv
from fastapi import HTTPException, Security, status
from fastapi.security.api_key import APIKeyHeader

load_dotenv()

API_KEY: str | None = os.getenv("API_KEY")

api_key_header = APIKeyHeader(
    name="X-API-Key",
    auto_error=False,
)


async def verify_api_key(
    api_key: str | None = Security(api_key_header),
) -> str:
    """
    Vérifie la clé API transmise dans l'en-tête X-API-Key.

    Utilise secrets.compare_digest pour éviter les attaques
    par mesure du temps de comparaison (timing attack).
    """
    if not API_KEY:
        # Clé non configurée côté serveur → erreur de configuration
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Clé API non configurée sur le serveur.",
        )

    if api_key is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="En-tête X-API-Key manquant.",
            headers={"WWW-Authenticate": "ApiKey"},
        )

    # compare_digest résiste aux timing attacks
    if not secrets.compare_digest(api_key, API_KEY):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Clé API invalide.",
            headers={"WWW-Authenticate": "ApiKey"},
        )

    return api_key