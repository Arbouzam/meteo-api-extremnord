import json
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

BASE_DIR = Path(__file__).resolve().parents[2]


def _load_json(path: Path, label: str) -> dict:
    """Charge un fichier JSON avec un message d'erreur explicite si absent."""
    if not path.exists():
        raise RuntimeError(
            f"Fichier de métadonnées introuvable : {path}\n"
            f"Vérifiez que le fichier '{label}' est bien présent dans models/."
        )
    with open(path, encoding="utf-8") as f:
        return json.load(f)


PLUIE_METADATA = _load_json(
    BASE_DIR / "models" / "pluie" / "metadata_v2.json",
    "metadata_v2.json",
)
CHALEUR_METADATA = _load_json(
    BASE_DIR / "models" / "chaleur" / "metadata.json",
    "metadata.json",
)