from pathlib import Path
import sys
import pandas as pd
from pymongo import MongoClient

# ── CONFIG ───────────────────────────────────────────────────────────────────
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from db_config import MONGO_URI, DB_NAME
COL_SALIDA = "solicitudesSVM"
# ─────────────────────────────────────────────────────────────────────────────

client = MongoClient(MONGO_URI)
db     = client[DB_NAME]

# ── CARGAR COLECCIONES ────────────────────────────────────────────────────────
campos_rama = {"_id": 0, "Referencia": 1, "Descripción": 1, "Rama": 1}
campos_base = {"_id": 0, "Referencia": 1, "Solicitante": 1, "Género Solicitante": 1,
               "Descripción": 1, "Estado Solicitud": 1, "Centro de Investigación": 1,
               "CIF": 1, "DNI": 1, "Nº Petición": 1, "Nota": 1, "Cantidad Total": 1,
               "Personal Contratado": 1, "Nº Contratos": 1,
               "Año Inicio": 1, "Año1": 1, "Año2": 1, "Año3": 1, "Año4": 1, "Año5": 1}

df_g    = pd.DataFrame(list(db["solicitudesG"].find({}, campos_rama)))
df_m    = pd.DataFrame(list(db["solicitudesM"].find({}, campos_rama)))
df_base = pd.DataFrame(list(db["solicitudesCopia"].find({}, campos_base)))

print(f"solicitudesG: {len(df_g)} | solicitudesM: {len(df_m)} | solicitudesCopia: {len(df_base)}")

# ── IDENTIFICAR DESCRIPCIONES DUPLICADAS EN COPIA ─────────────────────────────
desc_counts  = df_base["Descripción"].value_counts()
desc_dup     = set(desc_counts[desc_counts > 1].index)
desc_unica   = set(desc_counts[desc_counts == 1].index)

df_dup   = df_base[df_base["Descripción"].isin(desc_dup)].copy()
df_unica = df_base[df_base["Descripción"].isin(desc_unica)].copy()

print(f"Descripciones duplicadas: {len(df_dup)} docs | Únicas: {len(df_unica)} docs")

# ── FUNCIÓN DE CRUCE ──────────────────────────────────────────────────────────
def cruzar_y_asignar(df_docs, df_g, df_m, key):
    df_docs = df_docs.copy()
    lookup_g = df_g.drop_duplicates(subset=key).set_index(key)["Rama"]
    lookup_m = df_m.drop_duplicates(subset=key).set_index(key)["Rama"]

    def asignar_rama(row):
        k = row[key]
        rama_g = lookup_g.get(k)
        rama_m = lookup_m.get(k)
        if pd.notna(rama_g) and pd.notna(rama_m) and rama_g == rama_m:
            return rama_g
        return ""

    df_docs["Rama"] = df_docs.apply(asignar_rama, axis=1)
    return df_docs

# ── CRUZAR DUPLICADOS POR REFERENCIA ─────────────────────────────────────────
df_dup_resultado = cruzar_y_asignar(df_dup, df_g, df_m, "Referencia")

# ── CRUZAR ÚNICOS POR DESCRIPCIÓN ────────────────────────────────────────────
df_unica_resultado = cruzar_y_asignar(df_unica, df_g, df_m, "Descripción")

# ── UNIR Y GUARDAR ────────────────────────────────────────────────────────────
df_final = pd.concat([df_dup_resultado, df_unica_resultado], ignore_index=True)

coinciden    = (df_final["Rama"] != "").sum()
no_coinciden = (df_final["Rama"] == "").sum()
print(f"\nCoindicen: {coinciden} | No coinciden (rama vacía): {no_coinciden}")

col_salida = db[COL_SALIDA]
col_salida.drop()
col_salida.insert_many(df_final.to_dict("records"))
print(f"Guardado en {COL_SALIDA}: {len(df_final)} documentos")