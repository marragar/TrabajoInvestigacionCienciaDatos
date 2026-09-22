"""
Genera un conjunto amplio y variado de gráficas a partir de una colección de MongoDB
con documentos del estilo:

{
  "Referencia": "CSI259P20",
  "Solicitante": "Sergio Moreno Pérez",
  "Género Solicitante": "Masculino",
  "DNI": "***9893**",
  "Nº Petición": 2,
  "Centro de Investigación": "Ibfg. Csic",
  "CIF": "Q2818002D",
  "Nota": 9.67,
  "Descripción": "...",
  "Rama": "Ciencias - Ciencias de la Salud",
  "Cantidad Total": 264000,
  "Año Inicio": 2021,
  "Año1": 116000, "Año2": 116000, "Año3": 32000, "Año4": "", "Año5": "",
  "Estado Solicitud": "Aceptada"
}

Solo hay que cambiar COL_NAME antes de cada ejecución. Las gráficas se guardan
en OUTPUT_DIR (una subcarpeta por colección) como archivos .png.
"""

from pathlib import Path
import sys
import os
import warnings

import matplotlib
matplotlib.use("Agg")  # backend sin pantalla, para poder correr en servidor/headless
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import pandas as pd
import seaborn as sns
from pymongo import MongoClient

warnings.filterwarnings("ignore")

# ── CONFIG ───────────────────────────────────────────────────────────────────
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from db_config import MONGO_URI, DB_NAME
COL_NAME  = "solicitudesPi"      # <-- cambia esto en cada ejecución
COL_NAME2  = "Solicitudes(Phi4(Con Internet))" 

OUTPUT_DIR = os.path.join("graficas", COL_NAME2)
DPI        = 150
TOP_N      = 15                    # nº de categorías a mostrar en rankings "top"
# ─────────────────────────────────────────────────────────────────────────────

sns.set_theme(style="whitegrid", palette="deep")
plt.rcParams["axes.titlesize"]  = 13
plt.rcParams["axes.titleweight"] = "bold"
plt.rcParams["figure.autolayout"] = True


# ── CARGA Y LIMPIEZA ──────────────────────────────────────────────────────────
def cargar_datos():
    client = MongoClient(MONGO_URI)
    col = client[DB_NAME][COL_NAME]
    docs = list(col.find({}))
    client.close()

    if not docs:
        raise SystemExit(f"La colección '{COL_NAME}' no tiene documentos.")

    df = pd.DataFrame(docs)

    # Numéricos
    for campo in ["Nota", "Cantidad Total", "Año Inicio", "Nº Petición",
                  "Año1", "Año2", "Año3", "Año4", "Año5"]:
        if campo in df.columns:
            df[campo] = pd.to_numeric(df[campo], errors="coerce")

    # Categóricos: valores vacíos -> "Sin clasificar" / "Sin especificar"
    for campo, relleno in [("Rama", "Sin clasificar"),
                            ("Género Solicitante", "Sin especificar"),
                            ("Estado Solicitud", "Sin especificar"),
                            ("Centro de Investigación", "Sin especificar")]:
        if campo in df.columns:
            df[campo] = df[campo].replace("", pd.NA).fillna(relleno)

    return df


# ── UTILIDADES ────────────────────────────────────────────────────────────────
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


# ── GRÁFICAS ──────────────────────────────────────────────────────────────────
def g_distribucion_genero(df):
    if "Género Solicitante" not in df.columns:
        return
    conteo = df["Género Solicitante"].value_counts()
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.pie(conteo.values, labels=conteo.index, autopct="%1.1f%%", startangle=90,
           colors=sns.color_palette("Set2"))
    ax.set_title("Distribución por género del solicitante")
    guardar(fig, "01_distribucion_genero")


def g_distribucion_rama(df):
    if "Rama" not in df.columns:
        return
    conteo = df["Rama"].value_counts()
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(x=conteo.values, y=conteo.index, ax=ax, palette="crest")
    ax.set_title("Número de solicitudes por rama")
    ax.set_xlabel("Solicitudes")
    ax.set_ylabel("")
    guardar(fig, "02_distribucion_rama")


def g_estado_solicitud(df):
    if "Estado Solicitud" not in df.columns:
        return
    conteo = df["Estado Solicitud"].value_counts()
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.pie(conteo.values, labels=conteo.index, autopct="%1.1f%%", startangle=90,
           colors=sns.color_palette("pastel"))
    ax.set_title("Distribución por estado de la solicitud")
    guardar(fig, "03_estado_solicitud")


def g_histograma_nota(df):
    if "Nota" not in df.columns or df["Nota"].dropna().empty:
        return
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.histplot(df["Nota"].dropna(), bins=20, kde=True, ax=ax, color="steelblue")
    ax.set_title("Distribución de la nota")
    ax.set_xlabel("Nota")
    guardar(fig, "04_histograma_nota")


def g_nota_por_rama(df):
    if "Rama" not in df.columns or "Nota" not in df.columns:
        return
    fig, ax = plt.subplots(figsize=(10, 6))
    orden = df.groupby("Rama")["Nota"].median().sort_values(ascending=False).index
    sns.boxplot(data=df, x="Nota", y="Rama", order=orden, ax=ax, palette="crest")
    ax.set_title("Distribución de la nota por rama")
    guardar(fig, "05_nota_por_rama")


def g_histograma_cantidad(df):
    if "Cantidad Total" not in df.columns or df["Cantidad Total"].dropna().empty:
        return
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.histplot(df["Cantidad Total"].dropna(), bins=25, kde=True, ax=ax, color="darkorange")
    ax.set_title("Distribución de la cantidad total concedida")
    ax.set_xlabel("Cantidad total (€)")
    formato_miles(ax, "x")
    guardar(fig, "06_histograma_cantidad_total")


def g_cantidad_por_rama(df):
    if "Rama" not in df.columns or "Cantidad Total" not in df.columns:
        return
    fig, ax = plt.subplots(figsize=(10, 6))
    orden = df.groupby("Rama")["Cantidad Total"].median().sort_values(ascending=False).index
    sns.boxplot(data=df, x="Cantidad Total", y="Rama", order=orden, ax=ax, palette="flare")
    ax.set_title("Cantidad total concedida por rama")
    formato_miles(ax, "x")
    guardar(fig, "07_cantidad_por_rama")


def g_top_centros(df):
    if "Centro de Investigación" not in df.columns:
        return
    conteo = df["Centro de Investigación"].value_counts().head(TOP_N)
    fig, ax = plt.subplots(figsize=(10, 7))
    sns.barplot(x=conteo.values, y=conteo.index, ax=ax, palette="mako")
    ax.set_title(f"Top {TOP_N} centros de investigación por nº de solicitudes")
    ax.set_xlabel("Solicitudes")
    ax.set_ylabel("")
    guardar(fig, "08_top_centros_investigacion")


def g_evolucion_anual_solicitudes(df):
    if "Año Inicio" not in df.columns:
        return
    conteo = df["Año Inicio"].dropna().astype(int).value_counts().sort_index()
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.lineplot(x=conteo.index, y=conteo.values, marker="o", ax=ax, color="teal")
    ax.set_title("Evolución del número de solicitudes por año de inicio")
    ax.set_xlabel("Año de inicio")
    ax.set_ylabel("Nº de solicitudes")
    ax.xaxis.set_major_locator(mticker.MaxNLocator(integer=True))
    guardar(fig, "09_evolucion_solicitudes_por_anio")


def g_evolucion_anual_cantidad(df):
    if "Año Inicio" not in df.columns or "Cantidad Total" not in df.columns:
        return
    agregado = df.dropna(subset=["Año Inicio"]).groupby(
        df["Año Inicio"].astype(int))["Cantidad Total"].sum()
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.barplot(x=agregado.index, y=agregado.values, ax=ax, color="indianred")
    ax.set_title("Cantidad total concedida por año de inicio")
    ax.set_xlabel("Año de inicio")
    ax.set_ylabel("Cantidad total (€)")
    formato_miles(ax, "y")
    guardar(fig, "10_cantidad_total_por_anio")


def g_numero_peticion(df):
    if "Nº Petición" not in df.columns or df["Nº Petición"].dropna().empty:
        return
    conteo = df["Nº Petición"].dropna().astype(int).value_counts().sort_index()
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.barplot(x=conteo.index, y=conteo.values, ax=ax, color="mediumpurple")
    ax.set_title("Distribución del número de petición")
    ax.set_xlabel("Nº de petición")
    ax.set_ylabel("Solicitudes")
    guardar(fig, "11_distribucion_numero_peticion")


def g_cantidad_por_genero(df):
    if "Género Solicitante" not in df.columns or "Cantidad Total" not in df.columns:
        return
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.boxplot(data=df, x="Género Solicitante", y="Cantidad Total", ax=ax, palette="Set2")
    ax.set_title("Cantidad total concedida por género")
    formato_miles(ax, "y")
    guardar(fig, "12_cantidad_por_genero")


def g_nota_vs_cantidad(df):
    if "Nota" not in df.columns or "Cantidad Total" not in df.columns:
        return
    fig, ax = plt.subplots(figsize=(8, 6))
    hue = "Rama" if "Rama" in df.columns else None
    sns.scatterplot(data=df, x="Nota", y="Cantidad Total", hue=hue, ax=ax,
                     palette="tab10", alpha=0.75, edgecolor="white")
    ax.set_title("Relación entre nota y cantidad total concedida")
    formato_miles(ax, "y")
    if hue:
        ax.legend(bbox_to_anchor=(1.02, 1), loc="upper left", fontsize=8)
    guardar(fig, "13_nota_vs_cantidad")


def g_heatmap_estado_rama(df):
    if "Estado Solicitud" not in df.columns or "Rama" not in df.columns:
        return
    tabla = pd.crosstab(df["Rama"], df["Estado Solicitud"])
    fig, ax = plt.subplots(figsize=(10, 7))
    sns.heatmap(tabla, annot=True, fmt="d", cmap="YlGnBu", ax=ax, cbar_kws={"label": "Solicitudes"})
    ax.set_title("Estado de la solicitud por rama")
    guardar(fig, "14_heatmap_estado_por_rama")


def g_genero_por_rama_apilado(df):
    if "Rama" not in df.columns or "Género Solicitante" not in df.columns:
        return
    tabla = pd.crosstab(df["Rama"], df["Género Solicitante"])
    fig, ax = plt.subplots(figsize=(10, 6))
    tabla.plot(kind="barh", stacked=True, ax=ax, colormap="Set2")
    ax.set_title("Composición por género dentro de cada rama")
    ax.set_xlabel("Solicitudes")
    ax.set_ylabel("")
    ax.legend(title="Género", bbox_to_anchor=(1.02, 1), loc="upper left")
    guardar(fig, "15_genero_por_rama")


def g_top_solicitantes(df):
    if "Solicitante" not in df.columns or "Cantidad Total" not in df.columns:
        return
    top = (df.groupby("Solicitante")["Cantidad Total"]
             .sum().sort_values(ascending=False).head(TOP_N))
    fig, ax = plt.subplots(figsize=(10, 7))
    sns.barplot(x=top.values, y=top.index, ax=ax, palette="rocket")
    ax.set_title(f"Top {TOP_N} solicitantes por cantidad total acumulada")
    ax.set_xlabel("Cantidad total (€)")
    formato_miles(ax, "x")
    guardar(fig, "16_top_solicitantes")


def g_desglose_anual_medio(df):
    cols_anio = [c for c in ["Año1", "Año2", "Año3", "Año4", "Año5"] if c in df.columns]
    if not cols_anio:
        return
    medias = df[cols_anio].mean()
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.barplot(x=medias.index, y=medias.values, ax=ax, color="cadetblue")
    ax.set_title("Importe medio concedido por anualidad")
    ax.set_ylabel("Importe medio (€)")
    formato_miles(ax, "y")
    guardar(fig, "17_importe_medio_por_anualidad")


def g_correlacion_numerica(df):
    numericas = [c for c in ["Nota", "Cantidad Total", "Año Inicio", "Nº Petición"]
                 if c in df.columns]
    numericas = [c for c in numericas if df[c].notna().sum() > 1]
    if len(numericas) < 2:
        return
    corr = df[numericas].corr()
    fig, ax = plt.subplots(figsize=(6, 5))
    sns.heatmap(corr, annot=True, fmt=".2f", cmap="coolwarm", vmin=-1, vmax=1, ax=ax)
    ax.set_title("Correlación entre variables numéricas")
    guardar(fig, "18_correlacion_variables_numericas")


def g_nota_por_estado(df):
    if "Estado Solicitud" not in df.columns or "Nota" not in df.columns:
        return
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.violinplot(data=df, x="Estado Solicitud", y="Nota", ax=ax, palette="Set3", cut=0)
    ax.set_title("Distribución de la nota según el estado de la solicitud")
    guardar(fig, "19_nota_por_estado")


def g_solicitudes_por_rama_y_anio(df):
    if "Rama" not in df.columns or "Año Inicio" not in df.columns:
        return
    tabla = pd.crosstab(df["Año Inicio"].dropna().astype(int), df["Rama"])
    fig, ax = plt.subplots(figsize=(11, 6))
    tabla.plot(kind="bar", stacked=True, ax=ax, colormap="tab20")
    ax.set_title("Solicitudes por año y rama")
    ax.set_xlabel("Año de inicio")
    ax.set_ylabel("Solicitudes")
    ax.legend(title="Rama", bbox_to_anchor=(1.02, 1), loc="upper left", fontsize=8)
    guardar(fig, "20_solicitudes_por_anio_y_rama")


GRAFICAS = [
    g_distribucion_genero,
    g_distribucion_rama,
    g_estado_solicitud,
    g_histograma_nota,
    g_nota_por_rama,
    g_histograma_cantidad,
    g_cantidad_por_rama,
    g_top_centros,
    g_evolucion_anual_solicitudes,
    g_evolucion_anual_cantidad,
    g_numero_peticion,
    g_cantidad_por_genero,
    g_nota_vs_cantidad,
    g_heatmap_estado_rama,
    g_genero_por_rama_apilado,
    g_top_solicitantes,
    g_desglose_anual_medio,
    g_correlacion_numerica,
    g_nota_por_estado,
    g_solicitudes_por_rama_y_anio,
]


# ── MAIN ──────────────────────────────────────────────────────────────────────
def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    print(f"Colección: {COL_NAME}")
    df = cargar_datos()
    print(f"Documentos cargados: {len(df)}")
    print(f"Guardando gráficas en: {OUTPUT_DIR}\n")

    for funcion in GRAFICAS:
        try:
            funcion(df)
        except Exception as e:
            print(f"  ✗ Error en {funcion.__name__}: {e}")

    print(f"\nListo. {len(os.listdir(OUTPUT_DIR))} gráficas generadas en '{OUTPUT_DIR}'.")


if __name__ == "__main__":
    main()