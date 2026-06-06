from app.services.metadata_loader import PLUIE_METADATA

print("Nombre de variables :")
print(len(PLUIE_METADATA["features_clf"]))

print("\nListe des variables :")
for feature in PLUIE_METADATA["features_clf"]:
    print(feature)