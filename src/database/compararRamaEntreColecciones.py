"""
Compara dos colecciones de MongoDB buscando solicitudes por Descripción.
- Si la Rama coincide → se inserta en la colección resultado tal cual.
- Si la Rama difiere → se inserta con el campo extra `fallo: "si"`.
"""

from pathlib import Path
import sys
from pymongo import MongoClient
from pymongo.errors import BulkWriteError

# ─── CONFIGURACIÓN ────────────────────────────────────────────────────────────
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from db_config import MONGO_URI, DB_NAME

COLECCION_B     = "SolicitudesR1-i"   # colección fuente principal
COLECCION_A     = "solicitudesPi"   # colección con la que se compara
COLECCION_OUT   = "solicitudesFinalVersion2"  # colección resultado

DESC_PREFIX_LEN = None

def normalizar(texto: str) -> str:
    """Elimina espacios extra y pasa a minúsculas para comparaciones robustas."""
    return texto


def main():
    client = MongoClient(MONGO_URI)
    db     = client[DB_NAME]

    col_a  = db[COLECCION_A]
    col_b  = db[COLECCION_B]
    col_out = db[COLECCION_OUT]

    # Limpia la colección de salida para evitar duplicados en ejecuciones repetidas
    col_out.drop()
    print(f"Colección '{COLECCION_OUT}' reiniciada.")

    # Construye un índice de la colección B: descripción normalizada → documento
    print(f"Indexando '{COLECCION_B}'…")
    indice_b: dict[str, dict] = {}
    for doc in col_b.find():
        desc = doc.get("Descripción") or doc.get("Descripcion") or ""
        if DESC_PREFIX_LEN:
            desc = desc[:DESC_PREFIX_LEN]
        clave = normalizar(desc)
        if clave:
            indice_b[clave] = doc

    print(f"  {len(indice_b)} documentos indexados.")

    # Recorre la colección A y compara
    total = col_a.count_documents({})
    print(f"Procesando '{COLECCION_A}' ({total} documentos)…\n")

    iguales   = 0
    distintas = 0
    sin_match = 0
    a_insertar = []

    for doc_a in col_a.find():
        desc_a = doc_a.get("Descripción") or doc_a.get("Descripcion") or ""
        if DESC_PREFIX_LEN:
            desc_a = desc_a[:DESC_PREFIX_LEN]
        clave = normalizar(desc_a)

        doc_b = indice_b.get(clave)

        if doc_b is None:
            sin_match += 1
            # Sin contraparte → se inserta igualmente, marcado
            nuevo = {k: v for k, v in doc_a.items() if k != "_id"}
            nuevo["fallo"] = "si"
            nuevo["motivo_fallo"] = "sin_match_en_coleccion_b"
            a_insertar.append(nuevo)
            continue

        rama_a = normalizar(doc_a.get("Rama") or "")
        rama_b = normalizar(doc_b.get("Rama") or "")

        nuevo = {k: v for k, v in doc_a.items() if k != "_id"}

        if rama_a == rama_b:
            iguales += 1
        else:
            distintas += 1
            nuevo["fallo"] = "si"

        a_insertar.append(nuevo)

    # Inserción masiva
    if a_insertar:
        col_out.insert_many(a_insertar, ordered=False)

    # Resumen
    print("─" * 50)
    print(f"  Rama igual   : {iguales}")
    print(f"  Rama distinta: {distintas}  ← marcados con fallo='si'")
    print(f"  Sin match    : {sin_match}  ← marcados con fallo='si' + motivo")
    print(f"  TOTAL        : {iguales + distintas + sin_match}")
    print(f"\nResultados guardados en '{DB_NAME}.{COLECCION_OUT}'")

    client.close()


if __name__ == "__main__":
    main()