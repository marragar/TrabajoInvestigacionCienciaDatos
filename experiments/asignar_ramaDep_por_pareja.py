"""
Añade el campo 'ramaDep' a cada documento de la colección A,
tomando el valor de 'Rama' de su pareja en la colección B (match por Descripción).
Si no hay match, deja el documento sin ese campo y lo reporta al final.
"""

from pathlib import Path
import sys
from pymongo import MongoClient

# ─── CONFIGURACIÓN ────────────────────────────────────────────────────────────
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from db_config import MONGO_URI, DB_NAME

COLECCION_A = "solicitudesFinalVersion2"   # colección a actualizar
COLECCION_B = "solicitudesInv"    # colección fuente del campo Rama
# ──────────────────────────────────────────────────────────────────────────────


def normalizar(texto: str) -> str:
    return " ".join(texto.strip().lower().split()) if texto else ""


def main():
    client = MongoClient(MONGO_URI)
    db     = client[DB_NAME]
    col_a  = db[COLECCION_A]
    col_b  = db[COLECCION_B]

    # Indexar B por descripción normalizada
    print("Indexando colección B…")
    indice_b: dict[str, str] = {}  # clave → valor de Rama
    for doc in col_b.find():
        desc  = doc.get("Descripción") or doc.get("Descripcion") or ""
        clave = normalizar(desc)
        rama  = doc.get("Rama") or ""
        if clave and rama:
            indice_b[clave] = rama
    print(f"  {len(indice_b)} documentos indexados.\n")

    docs_a    = list(col_a.find())
    total     = len(docs_a)
    añadidos  = 0
    sin_match = []

    print(f"Procesando {total} documentos de '{COLECCION_A}'…")

    for doc in docs_a:
        desc  = doc.get("Descripción") or doc.get("Descripcion") or ""
        clave = normalizar(desc)
        ref   = doc.get("Referencia") or str(doc["_id"])

        rama_dep = indice_b.get(clave)

        if rama_dep:
            col_a.update_one(
                {"_id": doc["_id"]},
                {"$set": {"ramaDep": rama_dep}}
            )
            añadidos += 1
        else:
            sin_match.append(ref)

    print(f"\n  ✓ ramaDep añadido : {añadidos}")
    print(f"  ✗ Sin match en B  : {len(sin_match)}")

    if sin_match:
        print("\n  Documentos sin match:")
        for ref in sin_match:
            print(f"    - {ref}")

    print("\nHecho.")
    client.close()


if __name__ == "__main__":
    main()