from fastapi import FastAPI

from app.routers.health import router as health_router
from app.routers.pluies_intenses import router as pluie_router
from app.routers.vagues_chaleur import router as chaleur_router

from app.services.model_loader import load_models

app = FastAPI(
    title="API Prévision des Phénomènes Extrêmes",
    version="1.0.0"
)

@app.on_event("startup")
def startup_event():
    load_models()

app.include_router(health_router)
app.include_router(pluie_router)
app.include_router(chaleur_router)