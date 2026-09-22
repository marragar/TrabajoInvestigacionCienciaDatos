from pathlib import Path
import sys
from pymongo import MongoClient

# ── CONFIG ───────────────────────────────────────────────────────────────────
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from db_config import MONGO_URI, DB_NAME
COLECCIONES = ["solicitudesNew"]
ANIO_INICIO = 2019
# ─────────────────────────────────────────────────────────────────────────────

def n_contratos_por_rango(cantidad):
    """
    0 contratos: hasta 40.000 (inclusive)
    1 contrato:  más de 40.000 hasta 120.000 (inclusive)
    None: fuera de rango conocido -> se omite y se avisa
    """
    if cantidad <= 40000.0:
        return 0
    if cantidad <= 120000.0:
        return 1
    return None


client = MongoClient(MONGO_URI)
db     = client[DB_NAME]

for nombre_col in COLECCIONES:
    col = db[nombre_col]
    documentos = list(col.find(
        {"Año Inicio": ANIO_INICIO},
        {"_id": 1, "Cantidad Total": 1}
    ))
    print(f"\n── {nombre_col} | Año Inicio = {ANIO_INICIO} ({len(documentos)} docs) ──")

    actualizados = 0
    omitidos     = 0

    for doc in documentos:
        try:
            cantidad    = float(doc.get("Cantidad Total", 0))
            n_contratos = n_contratos_por_rango(cantidad)

            if n_contratos is None:
                print(f"  ✗ Cantidad fuera de rango: {cantidad} (id: {doc['_id']})")
                omitidos += 1
                continue

            col.update_one(
                {"_id": doc["_id"]},
                {"$set": {
                    "Personal Contratado": n_contratos > 0,
                    "Nº Contratos":        n_contratos,
                }}
            )
            actualizados += 1

        except Exception as e:
            print(f"  ✗ Error en {doc['_id']}: {e}")
            omitidos += 1

    print(f"  Actualizados: {actualizados} | Omitidos: {omitidos}")