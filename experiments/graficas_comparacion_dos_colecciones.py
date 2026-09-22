"""
Compara la distribución de la Rama (y algunas métricas asociadas) entre DOS
colecciones de MongoDB que siguen el mismo esquema de documento (ver scripts
anteriores). Útil, por ejemplo, para comparar los resultados de dos ejecuciones
distintas del clasificador, o dos convocatorias distintas.

Solo hay que cambiar COL_A y COL_B antes de cada ejecución.
Las gráficas se guardan en OUTPUT_DIR.
"""

from pathlib import Path
import sys
import os
import warnings

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import pandas as pd
import seaborn as sns
from pymongo import MongoClient

warnings.filterwarnings("ignore")

# ── CONFIG ───────────────────────────────────────────────────────────────────
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from db_config import MONGO_URI, DB_NAME

COL_A = "SolicitudesR1-i"      # <-- primera colección a comparar
COL_B = "solicitudesPi"      # <-- segunda colección a comparar

OUTPUT_DIR = os.path.join("graficas_comparacion", f"{COL_A}_vs_{COL_B}")
DPI        = 150
# ─────────────────────────────────────────────────────────────────────────────

sns.set_theme(style="whitegrid", palette="deep")
plt.rcParams["axes.titlesize"]   = 13
plt.rcParams["axes.titleweight"] = "bold"
plt.rcParams["figure.autolayout"] = True

RAMAS_ORDEN = [
    "Filosofía y Letras",
    "Ciencias Sociales - Educación",
    "Ciencias Sociales - Resto",
    "Ciencias - Matemáticas y Física",
    "Ciencias - Ciencias de la Salud",
    "Ciencias - Resto",
    "Ingenierías",
    "Sin clasificar",
]


# ── CARGA Y LIMPIEZA ──────────────────────────────────────────────────────────
def cargar_coleccion(nombre_col):
    client = MongoClient(MONGO_URI)
    col = client[DB_NAME][nombre_col]
    docs = list(col.find({}))
    client.close()

    if not docs:
        raise SystemExit(f"La colección '{nombre_col}' no tiene documentos.")

    df = pd.DataFrame(docs)

    for campo in ["Nota", "Cantidad Total", "Año Inicio", "Nº Petición"]:
        if campo in df.columns:
            df[campo] = pd.to_numeric(df[campo], errors="coerce")

    if "Rama" in df.columns:
        df["Rama"] = df["Rama"].replace("", pd.NA).fillna("Sin clasificar")
    else:
        df["Rama"] = "Sin clasificar"

    df["__coleccion__"] = nombre_col
    return df


def guardar(fig, nombre):
    path = os.path.join(OUTPUT_DIR, f"{nombre}.png")
    fig.savefig(path, dpi=DPI, bbox_inches="tight")
    plt.close(fig)
    print(f"  ✓ {nombre}.png")


def formato_miles(ax, eje="y"):
    formatter = mticker.FuncFormatter(lambda x, _: f"{x:,.0f}".replace(",", "."))
    if eje == "y":
        ax.yaxis.set_major_formatter(formatter)
    else:
        ax.xaxis.set_major_formatter(formatter)


def orden_ramas_presentes(*series):
    presentes = set()
    for s in series:
        presentes.update(s.unique())
    return [r for r in RAMAS_ORDEN if r in presentes] + \
           sorted(presentes - set(RAMAS_ORDEN))


# ── GRÁFICAS COMPARATIVAS ─────────────────────────────────────────────────────
def g_conteo_absoluto(df_a, df_b):
    orden = orden_ramas_presentes(df_a["Rama"], df_b["Rama"])
    conteo_a = df_a["Rama"].value_counts().reindex(orden, fill_value=0)
    conteo_b = df_b["Rama"].value_counts().reindex(orden, fill_value=0)

    tabla = pd.DataFrame({COL_A: conteo_a, COL_B: conteo_b})
    fig, ax = plt.subplots(figsize=(11, 7))
    tabla.plot(kind="barh", ax=ax, color=["#4C72B0", "#DD8452"])
    ax.invert_yaxis()
    ax.set_title(f"Nº de solicitudes por rama: {COL_A} vs {COL_B}")
    ax.set_xlabel("Solicitudes")
    ax.legend(title="Colección")
    guardar(fig, "01_conteo_absoluto_por_rama")
    return tabla


def g_porcentaje_relativo(df_a, df_b):
    orden = orden_ramas_presentes(df_a["Rama"], df_b["Rama"])
    pct_a = (df_a["Rama"].value_counts(normalize=True) * 100).reindex(orden, fill_value=0)
    pct_b = (df_b["Rama"].value_counts(normalize=True) * 100).reindex(orden, fill_value=0)

    tabla = pd.DataFrame({COL_A: pct_a, COL_B: pct_b})
    fig, ax = plt.subplots(figsize=(11, 7))
    tabla.plot(kind="barh", ax=ax, color=["#55A868", "#C44E52"])
    ax.invert_yaxis()
    ax.set_title(f"Distribución porcentual por rama: {COL_A} vs {COL_B}")
    ax.set_xlabel("% de solicitudes")
    ax.legend(title="Colección")
    guardar(fig, "02_porcentaje_relativo_por_rama")


def g_diferencia_porcentual(df_a, df_b):
    orden = orden_ramas_presentes(df_a["Rama"], df_b["Rama"])
    pct_a = (df_a["Rama"].value_counts(normalize=True) * 100).reindex(orden, fill_value=0)
    pct_b = (df_b["Rama"].value_counts(normalize=True) * 100).reindex(orden, fill_value=0)
    diferencia = (pct_b - pct_a).sort_values()

    colores = ["#C44E52" if v < 0 else "#55A868" for v in diferencia.values]
    fig, ax = plt.subplots(figsize=(10, 7))
    ax.barh(diferencia.index, diferencia.values, color=colores)
    ax.axvline(0, color="black", linewidth=0.8)
    ax.set_title(f"Diferencia en % de peso por rama ({COL_B} − {COL_A})")
    ax.set_xlabel("Diferencia en puntos porcentuales")
    guardar(fig, "03_diferencia_porcentual_por_rama")


def g_cantidad_total_por_rama(df_a, df_b):
    if "Cantidad Total" not in df_a.columns or "Cantidad Total" not in df_b.columns:
        return
    combinado = pd.concat([df_a, df_b], ignore_index=True)
    orden = orden_ramas_presentes(df_a["Rama"], df_b["Rama"])
    fig, ax = plt.subplots(figsize=(11, 7))
    sns.boxplot(data=combinado, x="Cantidad Total", y="Rama", hue="__coleccion__",
                order=orden, ax=ax, palette=["#4C72B0", "#DD8452"])
    ax.set_title(f"Cantidad total concedida por rama: {COL_A} vs {COL_B}")
    formato_miles(ax, "x")
    ax.legend(title="Colección")
    guardar(fig, "04_cantidad_total_por_rama")


def g_nota_por_rama(df_a, df_b):
    if "Nota" not in df_a.columns or "Nota" not in df_b.columns:
        return
    combinado = pd.concat([df_a, df_b], ignore_index=True)
    orden = orden_ramas_presentes(df_a["Rama"], df_b["Rama"])
    fig, ax = plt.subplots(figsize=(11, 7))
    sns.boxplot(data=combinado, x="Nota", y="Rama", hue="__coleccion__",
                order=orden, ax=ax, palette=["#55A868", "#C44E52"])
    ax.set_title(f"Nota por rama: {COL_A} vs {COL_B}")
    ax.legend(title="Colección")
    guardar(fig, "05_nota_por_rama")


def g_heatmap_conteo(df_a, df_b):
    orden = orden_ramas_presentes(df_a["Rama"], df_b["Rama"])
    conteo_a = df_a["Rama"].value_counts().reindex(orden, fill_value=0)
    conteo_b = df_b["Rama"].value_counts().reindex(orden, fill_value=0)
    tabla = pd.DataFrame({COL_A: conteo_a, COL_B: conteo_b})

    fig, ax = plt.subplots(figsize=(6, 7))
    sns.heatmap(tabla, annot=True, fmt=".0f", cmap="YlGnBu", ax=ax,
                cbar_kws={"label": "Solicitudes"})
    ax.set_title("Nº de solicitudes por rama y colección")
    guardar(fig, "06_heatmap_conteo_por_rama")


# ── MAIN ──────────────────────────────────────────────────────────────────────
def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    print(f"Comparando '{COL_A}' vs '{COL_B}'")

    df_a = cargar_coleccion(COL_A)
    df_b = cargar_coleccion(COL_B)
    print(f"  {COL_A}: {len(df_a)} documentos")
    print(f"  {COL_B}: {len(df_b)} documentos")
    print(f"Guardando gráficas en: {OUTPUT_DIR}\n")

    tabla_conteo = None
    for funcion in [g_conteo_absoluto, g_porcentaje_relativo, g_diferencia_porcentual,
                     g_cantidad_total_por_rama, g_nota_por_rama, g_heatmap_conteo]:
        try:
            resultado = funcion(df_a, df_b)
            if funcion is g_conteo_absoluto:
                tabla_conteo = resultado
        except Exception as e:
            print(f"  ✗ Error en {funcion.__name__}: {e}")

    if tabla_conteo is not None:
        csv_path = os.path.join(OUTPUT_DIR, "tabla_conteo_por_rama.csv")
        tabla_conteo.to_csv(csv_path, encoding="utf-8-sig")
        print(f"  ✓ tabla_conteo_por_rama.csv")

    print(f"\nListo. Resultados en '{OUTPUT_DIR}'.")


if __name__ == "__main__":
    main()