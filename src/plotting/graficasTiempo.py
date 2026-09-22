"""
Gráficas de % de solicitudes aceptadas por año, desglosadas por Género,
Centro de Investigación y Rama (en bloques).

- Eje X = Año Inicio, usando el año REAL como valor numérico (no una
  posición categórica). Esto hace que, si por ejemplo no hay datos entre
  2010 y 2014, esos dos años no queden pegados: el hueco se respeta
  proporcionalmente, igual que en cualquier eje temporal continuo.
- Eje Y = % de aceptadas sobre el total de esa categoría en ese año
  (Aceptadas / (Aceptadas + Suplentes) * 100).
- Un punto por año, unidos con una línea; una línea por categoría dentro
  de cada gráfica.

Gráficas generadas (3 en total):
  1. Género: una línea por género (Masculino, Femenino).
  2. Centro: una línea por cada uno de los CUATRO centros públicos
     (universidades de Valladolid, Salamanca, León y Burgos). Se excluye
     CSIC porque no es una universidad; si en realidad quieres incluirlo,
     añádelo a CENTROS_PUBLICOS.
  3. Rama: una sola gráfica con TRES líneas, una por bloque. Cada bloque
     agrupa varias ramas y sus solicitudes se agregan en una única serie:
       - Ciencias de la Salud / Ciencias - Resto
       - Ingenierías / Matemáticas y Física
       - Ciencias Sociales (Resto + Educación) / Filosofía y Letras
"""

import sys
import os
from pathlib import Path
from collections import defaultdict

BASE_DIR = Path(__file__).resolve().parent
from datetime import datetime

from pymongo import MongoClient
import matplotlib.pyplot as plt

# ─── CONFIGURACIÓN ────────────────────────────────────────────────────────────
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from db_config import MONGO_URI, DB_NAME
COLECCION   = "Solicitudes"
OUTPUT_DIR  = str(BASE_DIR / "../../outputs/graphs/graficas")
# ──────────────────────────────────────────────────────────────────────────────

GENEROS = ["Masculino", "Femenino"]

# Solo los cuatro centros públicos (universidades); CSIC excluido a propósito.
CENTROS_PUBLICOS = [
    "Universidad de Valladolid",
    "Universidad de Salamanca",
    "Universidad de León",
    "Universidad de Burgos",
]

# Bloques de ramas: cada bloque es UNA línea en la gráfica de ramas, con las
# solicitudes de sus ramas agregadas (no una gráfica por bloque).
# Formato: (etiqueta para la leyenda, lista de ramas que componen el bloque)
BLOQUES_RAMA = [
    ("Ciencias de la Salud / Ciencias - Resto",
     ["Ciencias - Ciencias de la Salud", "Ciencias - Resto"]),
    ("Ingenierías / Matemáticas y Física",
     ["Ingenierías", "Ciencias - Matemáticas y Física"]),
    ("Ciencias Sociales / Filosofía y Letras",
     ["Ciencias Sociales - Resto", "Ciencias Sociales - Educación", "Filosofía y Letras"]),
]

ESTADOS_VALIDOS = ("Aceptada", "Suplente")


def porcentaje_aceptadas_por_año(docs, campo_filtro, valores_filtro,
                                  campo_año="Año Inicio", campo_estado="Estado Solicitud"):
    """
    Devuelve un dict {año: porcentaje_de_aceptadas} para los documentos cuyo
    campo_filtro esté en valores_filtro.

    valores_filtro puede ser un único valor (p.ej. "Universidad de León") o
    una lista/tupla de valores (p.ej. las ramas de un bloque). Si es una
    lista, las solicitudes de todas esas categorías se AGREGAN en una sola
    serie: el porcentaje se calcula sobre el total conjunto del bloque
    (suma de aceptadas / suma de aceptadas+suplentes), no como media de los
    porcentajes individuales — así cada rama pesa según su volumen real.
    """
    if isinstance(valores_filtro, (list, tuple, set)):
        valores = set(valores_filtro)
    else:
        valores = {valores_filtro}

    conteo = defaultdict(lambda: {"Aceptada": 0, "Suplente": 0})
    for doc in docs:
        if doc.get(campo_filtro) not in valores:
            continue
        año = doc.get(campo_año)
        estado = doc.get(campo_estado)
        if año is None or estado not in ESTADOS_VALIDOS:
            continue
        conteo[año][estado] += 1

    resultado = {}
    for año, c in conteo.items():
        total = c["Aceptada"] + c["Suplente"]
        if total > 0:
            resultado[año] = c["Aceptada"] / total * 100
    return resultado


def graficar_lineas_por_año(series_por_grupo, titulo, archivo_salida, años_referencia=None,
                             ylabel="% de solicitudes aceptadas"):
    """
    series_por_grupo: dict {nombre_grupo: {año: porcentaje}}.
    Una línea por grupo. El eje X usa el año como valor numérico real, así
    que los huecos entre años sin datos quedan reflejados en el espaciado.

    años_referencia: lista de años a usar para los ticks del eje X (y para
    fijar el rango del eje). Debe ser la lista de TODOS los años presentes
    en el dataset completo (no solo en esta gráfica en concreto), para que
    todas las gráficas empiecen en el mismo año (p.ej. 2010) aunque algún
    grupo concreto no tenga datos hasta más tarde (p.ej. 2021). Si no se
    pasa, se calcula solo a partir de los grupos de esta gráfica.
    """
    fig, ax = plt.subplots(figsize=(10, 6))

    for nombre_grupo, serie in series_por_grupo.items():
        if not serie:
            continue
        años = sorted(serie.keys())
        valores = [serie[a] for a in años]
        ax.plot(años, valores, marker="o", linewidth=2, label=nombre_grupo)

    ax.set_xlabel("Año")
    ax.set_ylabel(ylabel)
    ax.set_title(titulo)
    ax.set_ylim(0, 100)
    ax.legend()
    ax.grid(True, alpha=0.3)

    # Ticks y rango del eje X. Si se pasa años_referencia (años de TODO el
    # dataset), se usa eso para que el eje empiece siempre en el año más
    # antiguo global (p.ej. 2010) y no en el primer año en el que esta
    # gráfica en concreto tiene datos.
    if años_referencia:
        todos_los_años = sorted(set(años_referencia))
    else:
        todos_los_años = sorted({a for serie in series_por_grupo.values() for a in serie.keys()})

    if todos_los_años:
        ax.set_xticks(todos_los_años)
        ax.set_xticklabels([str(a) for a in todos_los_años], rotation=45)
        margen = max((todos_los_años[-1] - todos_los_años[0]) * 0.02, 0.5)
        ax.set_xlim(todos_los_años[0] - margen, todos_los_años[-1] + margen)

    fig.tight_layout()
    os.makedirs(os.path.dirname(archivo_salida) or ".", exist_ok=True)
    fig.savefig(archivo_salida, dpi=150)
    plt.close(fig)
    print(f"✓ Guardado: {archivo_salida}")


def main():
    client = MongoClient(MONGO_URI)
    col = client[DB_NAME][COLECCION]

    proyeccion = {
        "Año Inicio": 1,
        "Género Solicitante": 1,
        "Centro de Investigación": 1,
        "ramaDep": 1,
        "Estado Solicitud": 1,
    }
    docs = list(col.find({}, proyeccion))
    client.close()

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # Años presentes en TODO el dataset (con Estado Aceptada/Suplente), para
    # que todas las gráficas compartan el mismo eje X y empiecen siempre en
    # el año más antiguo global, aunque un grupo concreto no tenga datos
    # hasta más tarde.
    años_dataset = sorted({
        d.get("Año Inicio") for d in docs
        if d.get("Año Inicio") is not None and d.get("Estado Solicitud") in ESTADOS_VALIDOS
    })

    # ── 1. Género ────────────────────────────────────────────────────────────
    series_genero = {
        g: porcentaje_aceptadas_por_año(docs, "Género Solicitante", g)
        for g in GENEROS
    }
    graficar_lineas_por_año(
        series_genero,
        "% de solicitudes aceptadas por Género y año",
        os.path.join(OUTPUT_DIR, "pct_aceptadas_genero.png"),
        años_referencia=años_dataset,
    )

    # ── 2. Centro (solo universidades públicas) ─────────────────────────────
    series_centro = {
        c: porcentaje_aceptadas_por_año(docs, "Centro de Investigación", c)
        for c in CENTROS_PUBLICOS
    }
    graficar_lineas_por_año(
        series_centro,
        "% de solicitudes aceptadas por Centro (universidades públicas) y año",
        os.path.join(OUTPUT_DIR, "pct_aceptadas_centro.png"),
        años_referencia=años_dataset,
    )

    # ── 3. Rama: UNA sola gráfica, una línea por bloque (ramas agregadas) ───
    series_rama = {
        etiqueta: porcentaje_aceptadas_por_año(docs, "ramaDep", ramas)
        for etiqueta, ramas in BLOQUES_RAMA
    }
    graficar_lineas_por_año(
        series_rama,
        "% de solicitudes aceptadas por Rama (bloques) y año",
        os.path.join(OUTPUT_DIR, "pct_aceptadas_rama.png"),
        años_referencia=años_dataset,
    )

    print(f"\n✓ Todas las gráficas guardadas en: {OUTPUT_DIR}/")


if __name__ == "__main__":
    main()