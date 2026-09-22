"""
Genera un conjunto amplio y variado de gráficas descriptivas a partir de una
colección de MongoDB con documentos del estilo:

{
  "Referencia": "CSI259P20",
  "Solicitante": "Sergio Moreno Pérez",
  "Género Solicitante": "Masculino",
  "DNI": "***9893**",
  "Nº Petición": 2,
  "Centro de Investigación": "CSIC",
  "CIF": "Q2818002D",
  "Nota": 9.67,
  "Descripción": "...",
  "Rama": "Ciencias - Ciencias de la Salud",
  "Cantidad Total": 264000,
  "Año Inicio": 2021,
  "Año1": 116000, "Año2": 116000, "Año3": 32000, "Año4": "", "Año5": "",
  "Estado Solicitud": "Aceptada",
  "ramaDep": "Ciencias - Ciencias de la Salud",
  "N° Contratos": 2,
  "Personal Contratado": true
}

Solo hay que cambiar COL_NAME antes de cada ejecución. Las gráficas se guardan
en OUTPUT_DIR (una subcarpeta por colección) como archivos .png.
"""

import sys
import os
import warnings
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np
import pandas as pd
import seaborn as sns
from pymongo import MongoClient

warnings.filterwarnings("ignore")

# ── CONFIG ───────────────────────────────────────────────────────────────────
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from db_config import MONGO_URI, DB_NAME
COL_NAME   = "Solicitudes"          # <-- cambia esto en cada ejecución
COL_NAME2  = "DescripcionDatos"

OUTPUT_DIR = os.path.join(str(BASE_DIR / "../../outputs/graphs/Graficas"), COL_NAME2)
DPI        = 150
TOP_N      = 15                        # nº de categorías en rankings "top" genéricos
TOP_N_SOLICITANTES = 30                # top solicitantes (punto 16)
N_BINS_CANTIDAD = 12                   # nº de rangos para la gráfica 07

COLOR_MASCULINO = "#2563EB"   # azul
COLOR_FEMENINO  = "#DC2626"   # rojo
COLOR_OTRO      = "#94A3B8"   # gris, por si hay género no especificado
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

    # El campo de nº de contratos puede venir con distintos símbolos según
    # cómo se guardó ("N°", "Nº", "N"), lo normalizamos a "N° Contratos".
    candidatos_contratos = ["N° Contratos", "Nº Contratos", "N Contratos", "Numero Contratos"]
    for cand in candidatos_contratos:
        if cand in df.columns and cand != "N° Contratos":
            df = df.rename(columns={cand: "N° Contratos"})
            break

    # Numéricos
    for campo in ["Nota", "Cantidad Total", "Año Inicio", "Nº Petición",
                  "Año1", "Año2", "Año3", "Año4", "Año5", "N° Contratos"]:
        if campo in df.columns:
            df[campo] = pd.to_numeric(df[campo], errors="coerce")

    # Booleano
    if "Personal Contratado" in df.columns:
        df["Personal Contratado"] = df["Personal Contratado"].map(
            {True: "Sí", False: "No", "true": "Sí", "false": "No"}
        ).fillna("Sin especificar")

    # Categóricos: valores vacíos -> relleno legible
    for campo, relleno in [("Rama", "Sin clasificar"),
                            ("ramaDep", "Sin clasificar"),
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


def color_genero(genero):
    if genero == "Masculino":
        return COLOR_MASCULINO
    if genero == "Femenino":
        return COLOR_FEMENINO
    return COLOR_OTRO


def bar_mediana_iqr(df, categoria, valor, ax, orden=None, color="steelblue"):
    """Barra horizontal con la mediana y barras de error mostrando el rango
    intercuartílico (P25-P75). Sustituye a los boxplots poco legibles."""
    agg = df.groupby(categoria)[valor].agg(
        mediana="median", p25=lambda s: s.quantile(0.25), p75=lambda s: s.quantile(0.75)
    )
    if orden is None:
        orden = agg["mediana"].sort_values(ascending=False).index
    agg = agg.loc[orden]

    err_bajo = agg["mediana"] - agg["p25"]
    err_alto = agg["p75"] - agg["mediana"]

    ax.barh(agg.index, agg["mediana"], color=color, alpha=0.85, zorder=3)
    ax.errorbar(agg["mediana"], agg.index, xerr=[err_bajo, err_alto],
                fmt="none", ecolor="#334155", elinewidth=1.5, capsize=4, zorder=4)
    return agg


# ── GRÁFICAS EXISTENTES (revisadas) ───────────────────────────────────────────

def g_distribucion_genero(df):
    # 1. Pasado de tarta a barras
    if "Género Solicitante" not in df.columns:
        return
    conteo = df["Género Solicitante"].value_counts()
    fig, ax = plt.subplots(figsize=(7, 5))
    colores = [color_genero(g) for g in conteo.index]
    sns.barplot(x=conteo.values, y=conteo.index, ax=ax, palette=colores)
    ax.set_title("Distribución por género del solicitante")
    ax.set_xlabel("Solicitudes")
    ax.set_ylabel("")
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
    # 3. Pasado de tarta a barras
    if "Estado Solicitud" not in df.columns:
        return
    conteo = df["Estado Solicitud"].value_counts()
    fig, ax = plt.subplots(figsize=(7, 5))
    sns.barplot(x=conteo.values, y=conteo.index, ax=ax, palette="pastel")
    ax.set_title("Distribución por estado de la solicitud")
    ax.set_xlabel("Solicitudes")
    ax.set_ylabel("")
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


def g_nota_por_rangos(df):
    # 6. Sustituye al ECDF (poco claro): distribución de la nota agrupada
    # en rangos, mostrando el nº de solicitudes en cada uno.
    if "Nota" not in df.columns or df["Nota"].dropna().empty:
        return
    bins = [0, 2, 4, 6, 7, 8, 9, 10]
    etiquetas = ["0-2", "2-4", "4-6", "6-7", "7-8", "8-9", "9-10"]
    datos = df["Nota"].dropna()
    rangos = pd.cut(datos, bins=bins, labels=etiquetas, include_lowest=True)
    conteo = rangos.value_counts().reindex(etiquetas)

    fig, ax = plt.subplots(figsize=(9, 5))
    sns.barplot(x=conteo.index, y=conteo.values, ax=ax, color="steelblue")
    for i, v in enumerate(conteo.values):
        ax.text(i, v + max(conteo.values) * 0.01, f"{v}", ha="center", fontsize=9)
    ax.set_title("Nº de solicitudes por rango de nota")
    ax.set_xlabel("Rango de nota")
    ax.set_ylabel("Solicitudes")
    guardar(fig, "06_nota_por_rangos")


def g_histograma_cantidad(df):
    # 7. CORREGIDO: antes se contaba cada valor único de "Cantidad Total",
    # pero hay demasiados importes distintos y el gráfico quedaba ilegible.
    # Ahora se agrupa en N_BINS_CANTIDAD rangos de anchura uniforme.
    if "Cantidad Total" not in df.columns or df["Cantidad Total"].dropna().empty:
        return
    datos = df["Cantidad Total"].dropna()

    minimo, maximo = datos.min(), datos.max()
    if minimo == maximo:
        # Todos los proyectos tienen el mismo importe: no tiene sentido binear.
        conteo = datos.value_counts()
        etiquetas = [f"{int(v):,}".replace(",", ".") for v in conteo.index]
        valores = conteo.values
    else:
        bins = np.linspace(minimo, maximo, N_BINS_CANTIDAD + 1)
        rangos = pd.cut(datos, bins=bins, include_lowest=True)
        conteo = rangos.value_counts().sort_index()
        etiquetas = [
            f"{int(iv.left):,}-{int(iv.right):,}".replace(",", ".")
            for iv in conteo.index
        ]
        valores = conteo.values

    fig, ax = plt.subplots(figsize=(11, 6))
    sns.barplot(x=etiquetas, y=valores, ax=ax, color="darkorange")
    for i, v in enumerate(valores):
        if v > 0:
            ax.text(i, v + max(valores) * 0.01, f"{v}", ha="center", fontsize=9)
    ax.set_title("Nº de solicitudes por rango de importe total concedido")
    ax.set_xlabel("Rango de cantidad total (€)")
    ax.set_ylabel("Solicitudes")
    plt.setp(ax.get_xticklabels(), rotation=45, ha="right")
    guardar(fig, "07_cantidad_total_valores")


def g_cantidad_por_rama(df):
    # 8. Rehecho: fuera mediana/IQR (no convencía), ahora importe medio
    # absoluto por rama, con el nº de solicitudes (n) anotado en cada barra.
    if "Rama" not in df.columns or "Cantidad Total" not in df.columns:
        return
    agg = df.groupby("Rama")["Cantidad Total"].agg(media="mean", n="count")
    agg = agg.sort_values("media", ascending=False)

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.barh(agg.index, agg["media"], color="#F97316", alpha=0.9, zorder=3)
    for i, (media, n) in enumerate(zip(agg["media"], agg["n"])):
        ax.text(media + agg["media"].max() * 0.01, i, f"n={n}",
                va="center", fontsize=9, color="#334155")
    ax.set_title("Importe medio concedido por rama (con nº de solicitudes)")
    ax.set_xlabel("Importe medio (€)")
    formato_miles(ax, "x")
    guardar(fig, "08_cantidad_por_rama")


def g_top_centros(df):
    if "Centro de Investigación" not in df.columns:
        return
    conteo = df["Centro de Investigación"].value_counts().head(TOP_N)
    fig, ax = plt.subplots(figsize=(10, 7))
    sns.barplot(x=conteo.values, y=conteo.index, ax=ax, palette="mako")
    ax.set_title(f"Top {TOP_N} centros de investigación por nº de solicitudes")
    ax.set_xlabel("Solicitudes")
    ax.set_ylabel("")
    guardar(fig, "09_top_centros_investigacion")


def g_evolucion_anual_solicitudes(df):
    # 9. Fix: eje Y empieza en 0
    if "Año Inicio" not in df.columns:
        return
    conteo = df["Año Inicio"].dropna().astype(int).value_counts().sort_index()
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.lineplot(x=conteo.index, y=conteo.values, marker="o", ax=ax, color="teal")
    ax.set_title("Evolución del número de solicitudes por año de inicio")
    ax.set_xlabel("Año de inicio")
    ax.set_ylabel("Nº de solicitudes")
    ax.xaxis.set_major_locator(mticker.MaxNLocator(integer=True))
    ax.set_ylim(bottom=0)
    guardar(fig, "10_evolucion_solicitudes_por_anio")


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
    guardar(fig, "11_cantidad_total_por_anio")


def g_evolucion_anual_cantidad_b(df):
    # 11b. Versión b de la gráfica 11: en vez de sumar "Cantidad Total"
    # agrupando por Año Inicio del proyecto (que le asigna todo el importe
    # al primer año), aquí se reparte el dinero en sus años reales usando
    # Año1..Año5 (Año1 == Año Inicio, Año2 == Año Inicio + 1, etc.), así que
    # muestra lo que realmente se desembolsó cada año natural.
    largo = construir_dinero_anual(df)
    if largo.empty:
        return
    serie = largo.groupby("Año")["Importe"].sum().sort_index()
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.barplot(x=serie.index, y=serie.values, ax=ax, color="indianred")
    ax.set_title("Cantidad concedida por año (natural, según anualidades)")
    ax.set_xlabel("Año")
    ax.set_ylabel("Cantidad total (€)")
    formato_miles(ax, "y")
    guardar(fig, "11b_cantidad_total_por_anio_natural")


def g_cantidad_por_genero(df):
    # 12. Cambiado a valores absolutos: importe medio por género, con el
    # nº de solicitudes (n) anotado en cada barra.
    if "Género Solicitante" not in df.columns or "Cantidad Total" not in df.columns:
        return
    agg = df.groupby("Género Solicitante")["Cantidad Total"].agg(media="mean", n="count")
    agg = agg.sort_values("media", ascending=False)

    fig, ax = plt.subplots(figsize=(8, 5))
    colores = [color_genero(g) for g in agg.index]
    ax.bar(agg.index, agg["media"], color=colores, alpha=0.9, zorder=3)
    for i, (media, n) in enumerate(zip(agg["media"], agg["n"])):
        ax.text(i, media + agg["media"].max() * 0.02, f"n={n}",
                ha="center", fontsize=9, color="#334155")
    ax.set_title("Importe medio concedido por género (con nº de solicitudes)")
    ax.set_ylabel("Importe medio (€)")
    formato_miles(ax, "y")
    guardar(fig, "12_cantidad_por_genero")


def g_cantidad_por_genero_b(df):
    # 12b. Versión b de la 12: importe TOTAL concedido por género en vez
    # de la media, con el nº de solicitudes (n) anotado en cada barra.
    if "Género Solicitante" not in df.columns or "Cantidad Total" not in df.columns:
        return
    agg = df.groupby("Género Solicitante")["Cantidad Total"].agg(total="sum", n="count")
    agg = agg.sort_values("total", ascending=False)

    fig, ax = plt.subplots(figsize=(8, 5))
    colores = [color_genero(g) for g in agg.index]
    ax.bar(agg.index, agg["total"], color=colores, alpha=0.9, zorder=3)
    for i, (total, n) in enumerate(zip(agg["total"], agg["n"])):
        ax.text(i, total + agg["total"].max() * 0.02, f"n={n}",
                ha="center", fontsize=9, color="#334155")
    ax.set_title("Importe total concedido por género (con nº de solicitudes)")
    ax.set_ylabel("Importe total (€)")
    formato_miles(ax, "y")
    guardar(fig, "12b_cantidad_por_genero_total")


def g_nota_vs_cantidad(df):
    # 13. El violin seguía sin verse claro. Cambiado a un heatmap de
    # densidad conjunta: cruza rangos de Nota con rangos de Cantidad Total
    # y muestra cuántas solicitudes caen en cada combinación.
    if "Nota" not in df.columns or "Cantidad Total" not in df.columns:
        return
    datos = df.dropna(subset=["Nota", "Cantidad Total"]).copy()
    if datos.empty:
        return

    bins_nota = [0, 5, 6, 7, 8, 9, 10]
    etiquetas_nota = ["<5", "5-6", "6-7", "7-8", "8-9", "9-10"]
    datos["Rango Nota"] = pd.cut(datos["Nota"], bins=bins_nota, labels=etiquetas_nota, include_lowest=True)

    # Rangos de cantidad basados en cuantiles para que las celdas queden equilibradas
    try:
        datos["Rango Cantidad"] = pd.qcut(datos["Cantidad Total"], q=6, duplicates="drop")
    except ValueError:
        datos["Rango Cantidad"] = pd.cut(datos["Cantidad Total"], bins=6)

    etiquetas_cantidad = [
        f"{int(iv.left):,}-{int(iv.right):,}".replace(",", ".")
        for iv in sorted(datos["Rango Cantidad"].cat.categories)
    ]
    datos["Rango Cantidad"] = datos["Rango Cantidad"].cat.rename_categories(etiquetas_cantidad)

    tabla = pd.crosstab(datos["Rango Nota"], datos["Rango Cantidad"])
    tabla = tabla.reindex(index=etiquetas_nota)

    fig, ax = plt.subplots(figsize=(11, 6))
    sns.heatmap(tabla, annot=True, fmt="d", cmap="YlOrRd", ax=ax,
                cbar_kws={"label": "Solicitudes"})
    ax.set_title("Relación entre Nota y Cantidad Total concedida")
    ax.set_xlabel("Rango de cantidad total (€)")
    ax.set_ylabel("Rango de nota")
    plt.setp(ax.get_xticklabels(), rotation=30, ha="right")
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
    # 16. Top 30, en columnas (barras verticales), sin nombres en el eje,
    # coloreado según género (azul = hombre, rojo = mujer).
    if "Solicitante" not in df.columns or "Cantidad Total" not in df.columns:
        return

    genero_por_solicitante = (
        df.groupby("Solicitante")["Género Solicitante"]
        .agg(lambda s: s.mode().iat[0] if not s.mode().empty else "Sin especificar")
    )

    top = (df.groupby("Solicitante")["Cantidad Total"]
             .sum().sort_values(ascending=False).head(TOP_N_SOLICITANTES))

    colores = [color_genero(genero_por_solicitante.get(s, "Sin especificar")) for s in top.index]

    fig, ax = plt.subplots(figsize=(14, 6))
    ax.bar(range(len(top)), top.values, color=colores)
    ax.set_title(f"Top {TOP_N_SOLICITANTES} solicitantes por cantidad total acumulada")
    ax.set_xlabel(f"Solicitantes (ranking 1–{TOP_N_SOLICITANTES})")
    ax.set_ylabel("Cantidad total (€)")
    ax.set_xticks([])
    formato_miles(ax, "y")

    handles = [
        plt.Rectangle((0, 0), 1, 1, color=COLOR_MASCULINO, label="Masculino"),
        plt.Rectangle((0, 0), 1, 1, color=COLOR_FEMENINO, label="Femenino"),
        plt.Rectangle((0, 0), 1, 1, color=COLOR_OTRO, label="Sin especificar"),
    ]
    ax.legend(handles=handles, title="Género", loc="upper right")
    guardar(fig, "16_top_solicitantes")


def g_nota_por_estado(df):
    if "Estado Solicitud" not in df.columns or "Nota" not in df.columns:
        return
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.violinplot(data=df, x="Estado Solicitud", y="Nota", ax=ax, palette="Set3", cut=0)
    ax.set_title("Distribución de la nota según el estado de la solicitud")
    guardar(fig, "17_nota_por_estado")


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
    guardar(fig, "18_solicitudes_por_anio_y_rama")


# ── GRÁFICAS NUEVAS (10 propuestas) ───────────────────────────────────────────

def g_tasa_aceptacion_por_anio(df):
    # 19. Evolución de la tasa de aceptación (%) año a año
    if "Año Inicio" not in df.columns or "Estado Solicitud" not in df.columns:
        return
    datos = df.dropna(subset=["Año Inicio"]).copy()
    datos["Año Inicio"] = datos["Año Inicio"].astype(int)
    tasa = (datos.groupby("Año Inicio")["Estado Solicitud"]
            .apply(lambda s: (s == "Aceptada").mean() * 100))
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.lineplot(x=tasa.index, y=tasa.values, marker="o", ax=ax, color="#059669")
    ax.set_title("Evolución de la tasa de aceptación por año")
    ax.set_xlabel("Año de inicio")
    ax.set_ylabel("% de solicitudes aceptadas")
    ax.set_ylim(0, 100)
    ax.xaxis.set_major_locator(mticker.MaxNLocator(integer=True))
    guardar(fig, "19_tasa_aceptacion_por_anio")


def g_tasa_aceptacion_por_centro(df):
    # 20. Tasa de aceptación por centro (barras ordenadas)
    if "Centro de Investigación" not in df.columns or "Estado Solicitud" not in df.columns:
        return
    tasa = (df.groupby("Centro de Investigación")["Estado Solicitud"]
            .apply(lambda s: (s == "Aceptada").mean() * 100)
            .sort_values(ascending=False))
    fig, ax = plt.subplots(figsize=(10, 7))
    sns.barplot(x=tasa.values, y=tasa.index, ax=ax, palette="viridis")
    ax.set_title("Tasa de aceptación por centro de investigación")
    ax.set_xlabel("% de solicitudes aceptadas")
    ax.set_ylabel("")
    ax.set_xlim(0, 100)
    guardar(fig, "20_tasa_aceptacion_por_centro")


def g_heatmap_centro_rama(df):
    # 21. Concentración de solicitudes: Centro x Rama
    if "Centro de Investigación" not in df.columns or "Rama" not in df.columns:
        return
    top_centros = df["Centro de Investigación"].value_counts().head(TOP_N).index
    subset = df[df["Centro de Investigación"].isin(top_centros)]
    tabla = pd.crosstab(subset["Centro de Investigación"], subset["Rama"])
    fig, ax = plt.subplots(figsize=(12, 8))
    sns.heatmap(tabla, annot=True, fmt="d", cmap="rocket_r", ax=ax,
                cbar_kws={"label": "Solicitudes"})
    ax.set_title(f"Concentración de solicitudes: Centro (top {TOP_N}) x Rama")
    guardar(fig, "21_heatmap_centro_rama")


def g_heatmap_centro_ramadep(df):
    # 21b. Igual que el anterior pero usando ramaDep en vez de Rama.
    if "Centro de Investigación" not in df.columns or "ramaDep" not in df.columns:
        return
    top_centros = df["Centro de Investigación"].value_counts().head(TOP_N).index
    subset = df[df["Centro de Investigación"].isin(top_centros)]
    tabla = pd.crosstab(subset["Centro de Investigación"], subset["ramaDep"])
    fig, ax = plt.subplots(figsize=(12, 8))
    sns.heatmap(tabla, annot=True, fmt="d", cmap="rocket_r", ax=ax,
                cbar_kws={"label": "Solicitudes"})
    ax.set_title(f"Concentración de solicitudes: Centro (top {TOP_N}) x ramaDep")
    guardar(fig, "21b_heatmap_centro_ramadep")


def g_personal_contratado(df):
    # 22. Distribución de Personal Contratado (sí/no), sin la categoría
    # "Sin especificar" que no aportaba información. Solo se cuentan las
    # solicitudes con Estado Solicitud == "Aceptada", porque el personal
    # contratado únicamente tiene sentido en proyectos que sí se concedieron.
    if "Personal Contratado" not in df.columns:
        return
    datos = df
    if "Estado Solicitud" in df.columns:
        datos = df[df["Estado Solicitud"] == "Aceptada"]
    if datos.empty:
        return
    conteo = datos["Personal Contratado"].value_counts()
    conteo = conteo.drop("Sin especificar", errors="ignore")
    if conteo.empty:
        return
    fig, ax = plt.subplots(figsize=(6, 5))
    sns.barplot(x=conteo.index, y=conteo.values, ax=ax, palette="Set2")
    ax.set_title("Solicitudes aceptadas con personal contratado")
    ax.set_xlabel("")
    ax.set_ylabel("Solicitudes")
    guardar(fig, "22_personal_contratado")


def g_contratos_por_rama(df):
    # 23. Nº medio de contratos generados por rama
    if "N° Contratos" not in df.columns or "Rama" not in df.columns:
        return
    medias = (df.groupby("Rama")["N° Contratos"].mean()
              .sort_values(ascending=False))
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(x=medias.values, y=medias.index, ax=ax, palette="flare")
    ax.set_title("Nº medio de contratos generados por rama")
    ax.set_xlabel("Nº medio de contratos")
    ax.set_ylabel("")
    guardar(fig, "23_contratos_por_rama")


def g_rama_vs_ramadep(df):
    # 24. Validación de clasificación: Rama (LLM) vs ramaDep (referencia externa)
    if "Rama" not in df.columns or "ramaDep" not in df.columns:
        return
    tabla = pd.crosstab(df["Rama"], df["ramaDep"])
    fig, ax = plt.subplots(figsize=(11, 9))
    sns.heatmap(tabla, annot=True, fmt="d", cmap="Blues", ax=ax,
                cbar_kws={"label": "Solicitudes"})
    ax.set_title("Coincidencia entre Rama y ramaDep")
    ax.set_xlabel("ramaDep")
    ax.set_ylabel("Rama")
    guardar(fig, "24_rama_vs_ramadep")


def g_duracion_proyectos(df):
    # 25. Reemplaza al gráfico de importe por anualidad (aportaba poco).
    # Ahora: cuántos años dura cada proyecto (nº de anualidades con importe > 0).
    cols_anio = [c for c in ["Año1", "Año2", "Año3", "Año4", "Año5"] if c in df.columns]
    if not cols_anio:
        return
    datos = df[cols_anio].apply(pd.to_numeric, errors="coerce").fillna(0)
    duracion = (datos > 0).sum(axis=1)
    conteo = duracion.value_counts().sort_index()
    conteo = conteo[conteo.index > 0]  # descartar proyectos sin ninguna anualidad

    fig, ax = plt.subplots(figsize=(8, 5))
    sns.barplot(x=conteo.index, y=conteo.values, ax=ax, color="#0EA5E9")
    for i, v in enumerate(conteo.values):
        ax.text(i, v + max(conteo.values) * 0.01, f"{v}", ha="center", fontsize=9)
    ax.set_title("Duración de los proyectos (nº de anualidades financiadas)")
    ax.set_xlabel("Años de duración")
    ax.set_ylabel("Nº de proyectos")
    guardar(fig, "25_duracion_proyectos")


def g_cantidad_por_centro(df):
    # 26. Cambiado a valores absolutos: suma total concedida por centro
    # (top N), en vez de mediana + IQR.
    if "Centro de Investigación" not in df.columns or "Cantidad Total" not in df.columns:
        return
    top_centros = df["Centro de Investigación"].value_counts().head(TOP_N).index
    subset = df[df["Centro de Investigación"].isin(top_centros)]
    total = subset.groupby("Centro de Investigación")["Cantidad Total"].sum().sort_values(ascending=False)

    fig, ax = plt.subplots(figsize=(10, 7))
    sns.barplot(x=total.values, y=total.index, ax=ax, color="#0EA5E9")
    ax.set_title(f"Cantidad total concedida por centro (top {TOP_N}, suma absoluta)")
    ax.set_xlabel("Cantidad total concedida (€)")
    formato_miles(ax, "x")
    guardar(fig, "26_cantidad_por_centro")


def g_cantidad_por_personal_contratado(df):
    # 27. Reemplaza a "tasa de aceptación por nº de petición" (no aportaba).
    # Ahora: ¿los proyectos con personal contratado reciben más financiación?
    if "Personal Contratado" not in df.columns or "Cantidad Total" not in df.columns:
        return
    datos = df[df["Personal Contratado"].isin(["Sí", "No"])]
    if datos.empty:
        return
    medias = datos.groupby("Personal Contratado")["Cantidad Total"].mean()
    ns = datos.groupby("Personal Contratado")["Cantidad Total"].count()

    fig, ax = plt.subplots(figsize=(7, 5))
    sns.barplot(x=medias.index, y=medias.values, ax=ax, palette=["#94A3B8", "#0EA5E9"])
    for i, (cat, media) in enumerate(medias.items()):
        ax.text(i, media + medias.max() * 0.02, f"n={ns[cat]}", ha="center", fontsize=9)
    ax.set_title("Importe medio concedido según si hubo personal contratado")
    ax.set_xlabel("Personal contratado")
    ax.set_ylabel("Importe medio (€)")
    formato_miles(ax, "y")
    guardar(fig, "27_cantidad_por_personal_contratado")


def g_top_ramas_importe_medio(df):
    # 28. Separado en dos archivos independientes: importe medio e
    # importe total por rama, cada uno en su propia imagen.
    if "Rama" not in df.columns or "Cantidad Total" not in df.columns:
        return
    agg = df.groupby("Rama")["Cantidad Total"].agg(media="mean", total="sum")

    orden_media = agg["media"].sort_values(ascending=False).index
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(x=agg.loc[orden_media, "media"], y=orden_media, ax=ax, color="#10B981")
    ax.set_title("Importe medio concedido por rama")
    ax.set_xlabel("Importe medio (€)")
    ax.set_ylabel("")
    formato_miles(ax, "x")
    guardar(fig, "28a_importe_medio_por_rama")

    orden_total = agg["total"].sort_values(ascending=False).index
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(x=agg.loc[orden_total, "total"], y=orden_total, ax=ax, color="#059669")
    ax.set_title("Importe total concedido por rama")
    ax.set_xlabel("Importe total (€)")
    ax.set_ylabel("")
    formato_miles(ax, "x")
    guardar(fig, "28b_importe_total_por_rama")


# ── DINERO POR AÑO NATURAL (usando Año Inicio + Año1..Año5) ──────────────────

def construir_dinero_anual(df):
    """Convierte cada proyecto en una fila por cada anualidad con importe > 0,
    calculando a qué año natural corresponde cada una. Año1 coincide siempre
    con Año Inicio, Año2 con Año Inicio + 1, y así sucesivamente. Con esto se
    puede agregar el dinero realmente desembolsado cada año (en vez del año
    de inicio del proyecto) por Rama, ramaDep, Género o Centro."""
    cols_anio = [c for c in ["Año1", "Año2", "Año3", "Año4", "Año5"] if c in df.columns]
    if not cols_anio or "Año Inicio" not in df.columns:
        return pd.DataFrame()

    id_vars = [c for c in ["Año Inicio", "Rama", "ramaDep", "Género Solicitante",
                            "Centro de Investigación"] if c in df.columns]

    datos = df[id_vars + cols_anio].copy()
    datos["Año Inicio"] = pd.to_numeric(datos["Año Inicio"], errors="coerce")

    largo = datos.melt(id_vars=id_vars, value_vars=cols_anio,
                        var_name="AnualidadN", value_name="Importe")
    largo["Importe"] = pd.to_numeric(largo["Importe"], errors="coerce")
    largo = largo.dropna(subset=["Año Inicio", "Importe"])
    largo = largo[largo["Importe"] > 0]

    offset = largo["AnualidadN"].str.replace("Año", "", regex=False).astype(int) - 1
    largo["Año"] = largo["Año Inicio"].astype(int) + offset
    largo = largo.drop(columns=["AnualidadN", "Año Inicio"])
    return largo


def g_dinero_anual_total(df):
    # 29. Gasto real por año natural (distinto de g_evolucion_anual_cantidad,
    # que suma Cantidad Total agrupando por Año Inicio del proyecto).
    largo = construir_dinero_anual(df)
    if largo.empty:
        return
    serie = largo.groupby("Año")["Importe"].sum().sort_index()
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.lineplot(x=serie.index, y=serie.values, marker="o", ax=ax, color="#7C3AED")
    ax.set_title("Dinero desembolsado por año natural (todas las anualidades)")
    ax.set_xlabel("Año")
    ax.set_ylabel("Importe (€)")
    ax.xaxis.set_major_locator(mticker.MaxNLocator(integer=True))
    formato_miles(ax, "y")
    ax.set_ylim(bottom=0)
    guardar(fig, "29_dinero_anual_total")


def g_dinero_anual_por_rama(df):
    # 30. Dinero por año natural, apilado por Rama.
    largo = construir_dinero_anual(df)
    if largo.empty or "Rama" not in largo.columns:
        return
    tabla = largo.pivot_table(index="Año", columns="Rama", values="Importe",
                               aggfunc="sum", fill_value=0).sort_index()
    fig, ax = plt.subplots(figsize=(12, 6))
    tabla.plot(kind="bar", stacked=True, ax=ax, colormap="tab20")
    ax.set_title("Dinero concedido por año natural y rama")
    ax.set_xlabel("Año")
    ax.set_ylabel("Importe (€)")
    formato_miles(ax, "y")
    ax.legend(title="Rama", bbox_to_anchor=(1.02, 1), loc="upper left", fontsize=8)
    guardar(fig, "30_dinero_anual_por_rama")


def g_dinero_anual_por_ramadep(df):
    # 31. Igual que la anterior pero con ramaDep.
    largo = construir_dinero_anual(df)
    if largo.empty or "ramaDep" not in largo.columns:
        return
    tabla = largo.pivot_table(index="Año", columns="ramaDep", values="Importe",
                               aggfunc="sum", fill_value=0).sort_index()
    fig, ax = plt.subplots(figsize=(12, 6))
    tabla.plot(kind="bar", stacked=True, ax=ax, colormap="tab20")
    ax.set_title("Dinero concedido por año natural y ramaDep")
    ax.set_xlabel("Año")
    ax.set_ylabel("Importe (€)")
    formato_miles(ax, "y")
    ax.legend(title="ramaDep", bbox_to_anchor=(1.02, 1), loc="upper left", fontsize=8)
    guardar(fig, "31_dinero_anual_por_ramadep")


def g_dinero_anual_por_genero(df):
    # 32. Dinero por año natural, apilado por género (mismos colores que
    # el resto del script: azul hombre, rojo mujer).
    largo = construir_dinero_anual(df)
    if largo.empty or "Género Solicitante" not in largo.columns:
        return
    tabla = largo.pivot_table(index="Año", columns="Género Solicitante",
                               values="Importe", aggfunc="sum", fill_value=0).sort_index()
    colores = [color_genero(g) for g in tabla.columns]
    fig, ax = plt.subplots(figsize=(11, 6))
    tabla.plot(kind="bar", stacked=True, ax=ax, color=colores)
    ax.set_title("Dinero concedido por año natural y género")
    ax.set_xlabel("Año")
    ax.set_ylabel("Importe (€)")
    formato_miles(ax, "y")
    ax.legend(title="Género", bbox_to_anchor=(1.02, 1), loc="upper left")
    guardar(fig, "32_dinero_anual_por_genero")


def g_dinero_anual_por_centro(df):
    # 33. Dinero por año natural, apilado por centro/universidad
    # (limitado a los TOP_N centros por dinero total acumulado, para no
    # saturar la leyenda).
    largo = construir_dinero_anual(df)
    if largo.empty or "Centro de Investigación" not in largo.columns:
        return
    top_centros = largo.groupby("Centro de Investigación")["Importe"].sum() \
                        .sort_values(ascending=False).head(TOP_N).index
    subset = largo[largo["Centro de Investigación"].isin(top_centros)]
    tabla = subset.pivot_table(index="Año", columns="Centro de Investigación",
                                values="Importe", aggfunc="sum", fill_value=0).sort_index()
    fig, ax = plt.subplots(figsize=(12, 6))
    tabla.plot(kind="bar", stacked=True, ax=ax, colormap="tab10")
    ax.set_title(f"Dinero concedido por año natural y centro (top {TOP_N})")
    ax.set_xlabel("Año")
    ax.set_ylabel("Importe (€)")
    formato_miles(ax, "y")
    ax.legend(title="Centro", bbox_to_anchor=(1.02, 1), loc="upper left", fontsize=8)
    guardar(fig, "33_dinero_anual_por_centro")


GRAFICAS = [
    g_distribucion_genero,
    g_distribucion_rama,
    g_estado_solicitud,
    g_histograma_nota,
    g_nota_por_rama,
    g_nota_por_rangos,
    g_histograma_cantidad,
    g_cantidad_por_rama,
    g_top_centros,
    g_evolucion_anual_solicitudes,
    g_evolucion_anual_cantidad,
    g_evolucion_anual_cantidad_b,
    g_cantidad_por_genero,
    g_cantidad_por_genero_b,
    g_nota_vs_cantidad,
    g_heatmap_estado_rama,
    g_genero_por_rama_apilado,
    g_top_solicitantes,
    g_nota_por_estado,
    g_solicitudes_por_rama_y_anio,
    g_tasa_aceptacion_por_anio,
    g_tasa_aceptacion_por_centro,
    g_heatmap_centro_rama,
    g_heatmap_centro_ramadep,
    g_personal_contratado,
    g_contratos_por_rama,
    g_rama_vs_ramadep,
    g_duracion_proyectos,
    g_cantidad_por_centro,
    g_cantidad_por_personal_contratado,
    g_top_ramas_importe_medio,
    g_dinero_anual_total,
    g_dinero_anual_por_rama,
    g_dinero_anual_por_ramadep,
    g_dinero_anual_por_genero,
    g_dinero_anual_por_centro,
]


# ── MAIN ──────────────────────────────────────────────────────────────────────
def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    print(f"Colección: {COL_NAME}")
    df = cargar_datos()
    print(f"Documentos cargados: {len(df)}")
    print(f"Columnas detectadas: {list(df.columns)}\n")
    print(f"Guardando gráficas en: {OUTPUT_DIR}\n")

    for funcion in GRAFICAS:
        try:
            funcion(df)
        except Exception as e:
            print(f"  ✗ Error en {funcion.__name__}: {e}")

    print(f"\nListo. {len(os.listdir(OUTPUT_DIR))} gráficas generadas en '{OUTPUT_DIR}'.")


if __name__ == "__main__":
    main()