import sys
from pathlib import Path
from pymongo import MongoClient

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from db_config import MONGO_URI, DB_NAME

# ── CONFIG ──────────────────────────────────────────────────────────────────
CSV_PATH   = "../data/clean/CSV_2017_CLEAN/anexo2_2017.csv"
ANIO_INICIO = 2017
COL_NAME   = "solicitudesNew"
# ────────────────────────────────────────────────────────────────────────────

import csv

client = MongoClient(MONGO_URI)
db = client[DB_NAME]
col = db[COL_NAME]

actualizados = 0
no_encontrados = []
duplicados = []

with open(CSV_PATH, newline="", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        descripcion = row.get("Descripción", "").strip()
        if not descripcion:
            continue

        coincidencias = col.count_documents({"Descripción": descripcion})

        if coincidencias == 0:
            no_encontrados.append(descripcion)
            continue
        if coincidencias > 1:
            duplicados.append(descripcion)
            # aun así actualizamos todas las coincidencias
        result = col.update_many(
            {"Descripción": descripcion},
            {"$set": {"Año Inicio": ANIO_INICIO}}
        )
        actualizados += result.modified_count

print(f"Documentos actualizados: {actualizados}")
print(f"Descripciones sin match en BD: {len(no_encontrados)}")
print(f"Descripciones con más de un match: {len(duplicados)}")

if no_encontrados:
    print("\n--- Sin match ---")
    for d in no_encontrados:
        print(f"  - {d[:100]}")

if duplicados:
    print("\n--- Duplicados (revisar) ---")
    for d in duplicados:
        print(f"  - {d[:100]}")