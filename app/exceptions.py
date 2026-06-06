import logging

from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

logger = logging.getLogger(__name__)


def register_exception_handlers(app: FastAPI) -> None:
    """Enregistre tous les gestionnaires d'erreurs sur l'application."""

    @app.exception_handler(StarletteHTTPException)
    async def http_exception_handler(
        request: Request, exc: StarletteHTTPException
    ) -> JSONResponse:
        """Formate toutes les erreurs HTTP en JSON cohérent."""
        logger.warning(
            "HTTP %s — %s %s",
            exc.status_code,
            request.method,
            request.url.path,
        )
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "erreur": exc.detail,
                "code": exc.status_code,
                "chemin": request.url.path,
            },
        )

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(
        request: Request, exc: RequestValidationError
    ) -> JSONResponse:
        """Formate les erreurs de validation Pydantic en messages lisibles."""
        erreurs = []
        for error in exc.errors():
            champ = " → ".join(str(loc) for loc in error["loc"] if loc != "body")
            erreurs.append({
                "champ": champ,
                "message": error["msg"],
                "valeur": error.get("input"),
            })

        logger.warning(
            "Validation échouée — %s %s — %d erreur(s)",
            request.method,
            request.url.path,
            len(erreurs),
        )
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={
                "erreur": "Données invalides",
                "code": 422,
                "details": erreurs,
            },
        )

    @app.exception_handler(Exception)
    async def unhandled_exception_handler(
        request: Request, exc: Exception
    ) -> JSONResponse:
        """Capture toute exception non gérée — évite les stack traces en production."""
        logger.exception(
            "Erreur non gérée — %s %s",
            request.method,
            request.url.path,
        )
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "erreur": "Erreur interne du serveur.",
                "code": 500,
                "chemin": request.url.path,
            },
        )