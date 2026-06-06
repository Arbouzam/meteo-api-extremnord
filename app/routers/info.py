from fastapi import APIRouter, Depends

from app.security import verify_api_key
from app.services.metadata_loader import CHALEUR_METADATA, PLUIE_METADATA
from app.services.model_loader import MODELS

router = APIRouter(prefix="/info", tags=["info"])


def _modeles_charges(module: dict) -> list[str]:
    """Retourne la liste des horizons dont le modèle est chargé."""
    return [h for h, m in module.items() if m is not None]


@router.get("/", summary="Métadonnées des modèles et état des chargements")
async def get_info(api_key: str = Depends(verify_api_key)) -> dict:
    """
    Retourne les informations clés sur les deux modules de prédiction :
    version, source de données, seuils, horizons disponibles et performances test.
    """
    return {
        "api_version": "1.0.0",
        "modules": {
            "pluies_intenses": {
                "version"          : PLUIE_METADATA.get("version"),
                "source_donnees"   : PLUIE_METADATA.get("source_donnees"),
                "periode_test"     : PLUIE_METADATA.get("periode_test"),
                "seuil_pluie_mm"   : PLUIE_METADATA.get("seuil_pluie_mm"),
                "horizons_charges" : _modeles_charges(MODELS["pluie"]),
                "seuils_optimaux"  : {
                    h: PLUIE_METADATA.get(f"seuil_optimal_{h}",
                       PLUIE_METADATA.get("seuil_optimal_j0"))
                    for h in ["j0", "j3", "j7", "j14", "j30"]
                },
                "perf_test"        : PLUIE_METADATA.get("perf_test", {}),
                "date_entrainement": PLUIE_METADATA.get("date_entrainement"),
            },
            "vagues_chaleur": {
                "quantile_omm"     : CHALEUR_METADATA.get("quantile_omm"),
                "duree_min_jours"  : CHALEUR_METADATA.get("duree_min_jours"),
                "periode_test"     : f"{CHALEUR_METADATA.get('date_fin_val')} / aujourd'hui",
                "horizons_charges" : _modeles_charges(MODELS["chaleur"]),
                "seuils_optimaux"  : {
                    h: CHALEUR_METADATA.get(f"seuil_optimal_{h}",
                       CHALEUR_METADATA.get("seuil_optimal_j0"))
                    for h in ["j0", "j3", "j7", "j14", "j30"]
                },
                "perf_test"        : CHALEUR_METADATA.get("perf_test", {}),
                "date_entrainement": CHALEUR_METADATA.get("date_entrainement"),
            },
        },
    }