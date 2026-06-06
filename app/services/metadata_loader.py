import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]

with open(
    BASE_DIR / "models" / "pluie" / "metadata_v2.json",
    encoding="utf-8"
) as f:

    PLUIE_METADATA = json.load(f)

with open(
    BASE_DIR / "models" / "chaleur" / "metadata.json",
    encoding="utf-8"
) as f:

    CHALEUR_METADATA = json.load(f)
    