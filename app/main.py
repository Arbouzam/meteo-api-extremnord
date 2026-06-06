import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.exceptions import register_exception_handlers
from app.routers.health import router as health_router
from app.routers.info import router as info_router
from app.routers.pluies_intenses import router as pluie_router
from app.routers.vagues_chaleur import router as chaleur_router
from app.services.model_loader import load_models

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Gestion du cycle de vie de l'application."""
    logger.info("Démarrage — chargement des modèles ML…")
    load_models()
    logger.info("Modèles chargés avec succès.")
    yield
    logger.info("Arrêt de l'API.")


app = FastAPI(
    title="API Prévision des Phénomènes Extrêmes",
    description="Prévision des vagues de chaleur et pluies intenses — Extrême-Nord Cameroun.",
    version="1.0.0",
    lifespan=lifespan,
)

# Gestionnaires d'erreurs globaux
register_exception_handlers(app)

# Middleware CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # TODO: restreindre à l'URL du dashboard en production
    allow_methods=["GET", "POST"],
    allow_headers=["X-API-Key", "Content-Type"],
)

# Routers
app.include_router(health_router)
app.include_router(info_router)
app.include_router(pluie_router)
app.include_router(chaleur_router)