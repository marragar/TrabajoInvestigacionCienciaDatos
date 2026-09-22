import sys
import pandas as pd
from pathlib import Path
from pymongo import MongoClient

BASE_DIR = Path(__file__).resolve().parent

# ── CONFIG ───────────────────────────────────────────────────────────────────
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from db_config import MONGO_URI, DB_NAME
OUTPUT_FILE = str(BASE_DIR / "../../data/validation/muestra_validacion.csv")
SEED        = 42
# ─────────────────────────────────────────────────────────────────────────────

client = MongoClient(MONGO_URI)
db     = client[DB_NAME]

colecciones = {
    "solicitudesG":  db["solicitudesG"],
    "solicitudesM":  db["solicitudesM"],
}

RAMAS = [
    "Filosofía y Letras",
    "Ciencias Sociales - Educación",
    "Ciencias Sociales - Resto",
    "Ciencias - Matemáticas y Física",
    "Ciencias - Ciencias de la Salud",
    "Ciencias - Resto",
    "Ingenierías",
]

# ── CARGAR COLECCIONES ────────────────────────────────────────────────────────
campos = {"_id": 0, "Referencia": 1, "Solicitante": 1, "Género Solicitante": 1, "Descripción": 1, "Rama": 1}
dfs = {}
for nombre, col in colecciones.items():
    dfs[nombre] = pd.DataFrame(list(col.find(
        {"Rama": {"$nin": ["", None]}, "Género Solicitante": {"$nin": ["", None]}},
        campos
    )))
    print(f"{nombre}: {len(dfs[nombre])} docs con rama y género")

# ── CRUZAR POR REFERENCIA Y RAMA COINCIDENTE EN LOS 4 MODELOS ────────────────
referencias = set(dfs["solicitudesG"]["Referencia"])
coincidentes = []

for ref in referencias:
    ramas = {}
    for nombre, df in dfs.items():
        fila = df[df["Referencia"] == ref]
        if fila.empty:
            break
        ramas[nombre] = fila.iloc[0]["Rama"]
    else:
        valores = list(ramas.values())
        if len(set(valores)) == 1:
            fila_base = dfs["solicitudesG"][dfs["solicitudesG"]["Referencia"] == ref].iloc[0]
            coincidentes.append({
                "Referencia":  ref,
                "Solicitante": fila_base["Solicitante"],
                "Género":      fila_base["Género Solicitante"],
                "Descripción": fila_base["Descripción"],
                "Rama":        valores[0],
            })

df_coin = pd.DataFrame(coincidentes)
print(f"\nDocumentos con rama coincidente en los 4 modelos: {len(df_coin)}")

# ── MUESTREO ESTRATIFICADO: 25H + 25M, mínimo 2 por rama ─────────────────────
def muestrear_genero(df_genero, n_total, min_por_rama, seed):
    ramas_presentes = [r for r in RAMAS if r in df_genero["Rama"].values]
    seleccionados   = []

    # Primero garantizar mínimo 2 por rama
    for rama in ramas_presentes:
        pool = df_genero[df_genero["Rama"] == rama]
        n    = min(min_por_rama, len(pool))
        seleccionados.append(pool.sample(n, random_state=seed))

    ya_seleccionados = pd.concat(seleccionados)
    restantes_pool   = df_genero[~df_genero["Referencia"].isin(ya_seleccionados["Referencia"])]
    n_restantes      = n_total - len(ya_seleccionados)

    if n_restantes > 0 and len(restantes_pool) >= n_restantes:
        extra = restantes_pool.sample(n_restantes, random_state=seed)
        ya_seleccionados = pd.concat([ya_seleccionados, extra])
    elif n_restantes > 0:
        print(f"  ⚠ Solo se pudieron seleccionar {len(ya_seleccionados)} de {n_total}")

    return ya_seleccionados

hombres = df_coin[df_coin["Género"] == "Masculino"]
mujeres = df_coin[df_coin["Género"] == "Femenino"]

print(f"Hombres disponibles: {len(hombres)}")
print(f"Mujeres disponibles: {len(mujeres)}")

muestra_h = muestrear_genero(hombres, 25, 2, SEED)
muestra_m = muestrear_genero(mujeres, 25, 2, SEED)

muestra = pd.concat([muestra_h, muestra_m]).sample(frac=1, random_state=SEED).reset_index(drop=True)

print(f"\nDistribución final por rama:")
print(muestra.groupby(["Rama", "Género"]).size().to_string())

muestra[["Solicitante", "Género", "Descripción", "Rama"]].to_csv(OUTPUT_FILE, index=False, encoding="utf-8")
print(f"\nCSV guardado → {OUTPUT_FILE} ({len(muestra)} filas)")