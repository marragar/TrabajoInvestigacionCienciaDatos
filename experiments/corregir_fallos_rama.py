"""
Recorre los documentos con fallo='si' en la colección de comparación.
Por cada uno muestra Rama y Descripción y pide V (verdadero) o F (falso).
- V → elimina el campo 'fallo' del documento
- F → lo deja tal cual
"""

from pathlib import Path
import sys
from pymongo import MongoClient

# ─── CONFIGURACIÓN ────────────────────────────────────────────────────────────
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from db_config import MONGO_URI, DB_NAME
COLECCION      = "solicitudesFinalVersion2"
# ──────────────────────────────────────────────────────────────────────────────


def main():
    client  = MongoClient(MONGO_URI)
    col     = client[DB_NAME][COLECCION]

    fallos  = list(col.find({"fallo": "si"}))
    total   = len(fallos)

    if total == 0:
        print("No hay documentos con fallo='si'.")
        client.close()
        return

    print(f"\n{total} documentos con fallo='si'. Revisando...\n")
    print("─" * 60)

    corregidos = 0

    for i, doc in enumerate(fallos, 1):
        desc  = doc.get("Descripción") or doc.get("Descripcion") or "(sin descripción)"
        rama  = doc.get("Rama") or "(sin rama)"
        ref   = doc.get("Referencia") or str(doc["_id"])

        print(f"\n[{i}/{total}]  Ref: {ref}")
        print(f"  Rama       : {rama}")
        print(f"  Descripción: {desc}")

        while True:
            resp = input("  ¿Es correcta la rama? [V/F]: ").strip().upper()
            if resp in ("V", "F"):
                break
            print("  Escribe V o F.")

        if resp == "V":
            col.update_one({"_id": doc["_id"]}, {"$unset": {"fallo": ""}})
            corregidos += 1
            print("  ✓ Campo 'fallo' eliminado.")
        else:
            print("  · Dejado como fallo.")

        print("─" * 60)

    print(f"\nFin. {corregidos}/{total} documentos corregidos.")
    client.close()


if __name__ == "__main__":
    main()