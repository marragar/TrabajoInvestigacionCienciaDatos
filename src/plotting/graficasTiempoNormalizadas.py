"""
Gráficas de % de solicitudes aceptadas por año, desglosadas por Género,
Centro de Investigación y Rama (en bloques), en versión CRUDA y en tres
versiones NORMALIZADAS.

─── EJE X ────────────────────────────────────────────────────────────────
Año Inicio usado como valor numérico REAL (no posición categórica): si no
hay convocatoria entre 2010 y 2014, esos dos años NO quedan pegados, el
hueco se respeta proporcionalmente. Los ticks se fijan con los años de todo
el dataset, así que todas las gráficas empiezan en el mismo año (2010) aunque
un grupo concreto no tenga datos hasta más tarde.

─── EL PROBLEMA QUE RESUELVEN LAS GRÁFICAS NORMALIZADAS ──────────────────
El % de aceptadas crudo mezcla dos cosas:

  (A) Lo generosa que fue la convocatoria ese año. Si un año entran 20M en
      vez de 6M, se acepta un porcentaje mayor de TODO el mundo y todas las
      líneas suben a la vez. Eso no dice nada sobre género/centro/rama.
  (B) La posición relativa de cada grupo respecto a los demás. Esto es lo
      que de verdad queremos ver.

Las gráficas normalizadas quitan (A) comparando cada grupo contra la TASA
GLOBAL DE ACEPTACIÓN DE SU PROPIO AÑO (calculada sobre TODAS las solicitudes
de la convocatoria, incluido el CSIC y todas las ramas). No hace falta saber
cuánto dinero entró cada año: la tasa global ya absorbe ese efecto.

  1. DIFERENCIA (puntos porcentuales) = pct_grupo − pct_global
     Centrado en 0. Lectura: "este grupo estuvo 8 puntos por encima de la
     media de ese año".

  2. RATIO / tasa relativa = pct_grupo ÷ pct_global
     Centrado en 1. Lectura: "este grupo tuvo 1.2× la tasa de aceptación
     media de ese año".

  3. RESIDUO ESTANDARIZADO DE PEARSON = (O − E) / √(E·(1−p)·(1−n/N))
     donde O = aceptadas del grupo, E = n·p = aceptadas esperadas si el grupo
     se comportara como la media del año, n = solicitudes del grupo ese año,
     p = tasa global del año, N = solicitudes totales del año. El término
     (1−n/N) es la corrección por población finita (el grupo es parte del
     total, no una muestra independiente de él). Centrado en 0, en unidades
     de desviación estándar: |z| > 2 ≈ desviación notable respecto a lo
     esperado. Conecta directamente con el chi-cuadrado de test_relaciones.py.

─── AVISO IMPORTANTE (lo que la normalización NO arregla) ────────────────
Normalizar corrige (A), pero NO el ruido por muestras pequeñas: si una rama
tiene 4 solicitudes en un año, pasar de 1 a 3 aceptadas la mueve del 25% al
75% por puro azar. Esos saltos siguen ahí después de normalizar. El residuo
de Pearson es el único de los tres que lo mitiga un poco (escala con √n, así
que un año con pocas solicitudes produce residuos pequeños automáticamente).
Para el resto, mira los conteos por año que imprime el script en consola
antes de interpretar un salto como real.
"""

import sys
import math
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
from collections import defaultdict

from pymongo import MongoClient
import matplotlib.pyplot as plt

# ─── CONFIGURACIÓN ────────────────────────────────────────────────────────────
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from db_config import MONGO_URI, DB_NAME
COLECCION   = "Solicitudes"
OUTPUT_DIR  = str(BASE_DIR / "../../outputs/graphs/graficasNORM")
# ──────────────────────────────────────────────────────────────────────────────

ESTADOS_VALIDOS = ("Aceptada", "Suplente")

GENEROS = ["Masculino", "Femenino"]

# Solo los cuatro centros públicos (universidades); CSIC excluido de las
# GRÁFICAS a propósito. OJO: el CSIC sí cuenta para la tasa global del año,
# porque el baseline es toda la convocatoria.
CENTROS_PUBLICOS = [
    "Universidad de Valladolid",
    "Universidad de Salamanca",
    "Universidad de León",
    "Universidad de Burgos",
]

# Cada bloque es UNA línea, con las solicitudes de sus ramas agregadas.
BLOQUES_RAMA = [
    ("Ciencias de la Salud / Ciencias - Resto",
     ["Ciencias - Ciencias de la Salud", "Ciencias - Resto"]),
    ("Ingenierías / Matemáticas y Física",
     ["Ingenierías", "Ciencias - Matemáticas y Física"]),
    ("Ciencias Sociales / Filosofía y Letras",
     ["Ciencias Sociales - Resto", "Ciencias Sociales - Educación", "Filosofía y Letras"]),
]

# (sufijo_archivo, nombre_para_titulos, campo_mongo, [(etiqueta_leyenda, valores)])
GRUPOS = [
    ("genero", "Género", "Género Solicitante", [(g, g) for g in GENEROS]),
    ("centro", "Centro (universidades públicas)", "Centro de Investigación",
     [(c, c) for c in CENTROS_PUBLICOS]),
    ("rama", "Rama (bloques)", "ramaDep", BLOQUES_RAMA),
]

# (clave_metrica, prefijo_archivo, titulo, ylabel, ylim, linea_referencia, lineas_extra)
METRICAS = [
    ("pct", "pct_aceptadas",
     "% de solicitudes aceptadas",
     "% de solicitudes aceptadas", (0, 100), None, None),
    ("diferencia", "norm_diferencia",
     "Diferencia vs. tasa global del año",
     "Puntos porcentuales sobre/bajo la media del año", None, 0, None),
    ("ratio", "norm_ratio",
     "Tasa relativa vs. global del año",
     "Tasa del grupo ÷ tasa global del año", None, 1, None),
    ("residuo", "norm_residuos",
     "Residuos estandarizados de Pearson",
     "Residuo estandarizado (desviaciones estándar)", None, 0, (-2, 2)),
]


def conteos_por_año(docs, campo_filtro, valores_filtro,
                     campo_año="Año Inicio", campo_estado="Estado Solicitud"):
    """
    Devuelve {año: {"acept": n, "total": n}} para los documentos cuyo
    campo_filtro esté en valores_filtro.

    valores_filtro puede ser un único valor ("Universidad de León") o una
    lista (las ramas de un bloque). Si es una lista, las solicitudes de todas
    esas categorías se AGREGAN en una sola serie: los conteos se suman, de
    modo que el porcentaje resultante pondera cada rama por su volumen real
    de solicitudes (no es la media de los porcentajes individuales).
    """
    if isinstance(valores_filtro, (list, tuple, set)):
        valores = set(valores_filtro)
    else:
        valores = {valores_filtro}

    conteo = defaultdict(lambda: {"acept": 0, "total": 0})
    for doc in docs:
        if doc.get(campo_filtro) not in valores:
            continue
        año = doc.get(campo_año)
        estado = doc.get(campo_estado)
        if año is None or estado not in ESTADOS_VALIDOS:
            continue
        conteo[año]["total"] += 1
        if estado == "Aceptada":
            conteo[año]["acept"] += 1
    return dict(conteo)


def tasas_globales_por_año(docs, campo_año="Año Inicio", campo_estado="Estado Solicitud"):
    """
    Tasa global de aceptación de cada año, sobre TODAS las solicitudes de la
    convocatoria (sin filtrar por centro, género ni rama; el CSIC incluido).
    Devuelve {año: {"acept": A, "total": N, "p": proporción_0_a_1}}.

    Esta es la referencia contra la que se normaliza: absorbe el efecto del
    volumen de financiación de cada año.
    """
    conteo = defaultdict(lambda: {"acept": 0, "total": 0})
    for doc in docs:
        año = doc.get(campo_año)
        estado = doc.get(campo_estado)
        if año is None or estado not in ESTADOS_VALIDOS:
            continue
        conteo[año]["total"] += 1
        if estado == "Aceptada":
            conteo[año]["acept"] += 1

    return {
        año: {"acept": c["acept"], "total": c["total"], "p": c["acept"] / c["total"]}
        for año, c in conteo.items() if c["total"] > 0
    }


def serie_metrica(conteos, globales, metrica):
    """
    Convierte {año: {"acept","total"}} en {año: valor} según la métrica.
    Los años sin datos suficientes (o con denominador nulo) se omiten, para
    que la línea no dibuje puntos inventados.
    """
    salida = {}
    for año, c in conteos.items():
        n = c["total"]
        if n == 0:
            continue
        pct = c["acept"] / n * 100

        if metrica == "pct":
            salida[año] = pct
            continue

        g = globales.get(año)
        if g is None or g["total"] == 0:
            continue
        p_glob = g["p"]
        pct_glob = p_glob * 100

        if metrica == "diferencia":
            salida[año] = pct - pct_glob

        elif metrica == "ratio":
            if pct_glob == 0:
                continue          # ningún aceptado ese año: el ratio no está definido
            salida[año] = pct / pct_glob

        elif metrica == "residuo":
            esperado = n * p_glob
            n_total_año = g["total"]
            correccion_pob_finita = 1 - (n / n_total_año) if n_total_año > 0 else 1
            varianza = esperado * (1 - p_glob) * correccion_pob_finita
            if varianza <= 0:
                continue          # p=0, p=1, o el grupo ES toda la convocatoria
            salida[año] = (c["acept"] - esperado) / math.sqrt(varianza)

    return salida


def graficar_lineas_por_año(series_por_grupo, titulo, archivo_salida, años_referencia=None,
                             ylabel="% de solicitudes aceptadas", ylim=None,
                             linea_referencia=None, lineas_extra=None):
    """
    series_por_grupo: {nombre_grupo: {año: valor}}. Una línea por grupo.

    años_referencia: años de TODO el dataset, para los ticks y el rango del
      eje X, de modo que todas las gráficas empiecen en el año más antiguo
      global aunque un grupo concreto no tenga datos hasta más tarde.
    linea_referencia: valor donde dibujar la línea horizontal de "sin efecto"
      (0 para diferencias y residuos, 1 para ratios).
    lineas_extra: tupla de valores donde dibujar líneas punteadas auxiliares
      (p.ej. (-2, 2) para marcar el umbral de residuo notable).
    """
    fig, ax = plt.subplots(figsize=(10, 6))

    if linea_referencia is not None:
        ax.axhline(linea_referencia, color="black", linewidth=1, linestyle="-", alpha=0.6)
    if lineas_extra:
        for v in lineas_extra:
            ax.axhline(v, color="grey", linewidth=1, linestyle="--", alpha=0.5)

    for nombre_grupo, serie in series_por_grupo.items():
        if not serie:
            continue
        años = sorted(serie.keys())
        valores = [serie[a] for a in años]
        ax.plot(años, valores, marker="o", linewidth=2, label=nombre_grupo)

    ax.set_xlabel("Año")
    ax.set_ylabel(ylabel)
    ax.set_title(titulo)
    if ylim is not None:
        ax.set_ylim(*ylim)
    ax.legend()
    ax.grid(True, alpha=0.3)

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

    # Tasa global de cada año (toda la convocatoria) = referencia de normalización
    globales = tasas_globales_por_año(docs)
    años_dataset = sorted(globales.keys())

    print("\n─── Tasa global de aceptación por año (toda la convocatoria) ───")
    print("Es la referencia contra la que se normaliza. Mira también el N:")
    print("un año con pocas solicitudes da porcentajes ruidosos.\n")
    print(f"{'Año':<8}{'Aceptadas':>10}{'Total':>8}{'% global':>10}")
    for año in años_dataset:
        g = globales[año]
        print(f"{año:<8}{g['acept']:>10}{g['total']:>8}{g['p']*100:>9.1f}%")
    print()

    # ── Todas las combinaciones (grupo × métrica) ────────────────────────────
    for sufijo, nombre_grupo, campo, definicion_series in GRUPOS:

        conteos_por_serie = {
            etiqueta: conteos_por_año(docs, campo, valores)
            for etiqueta, valores in definicion_series
        }

        # Conteos por año en consola, para poder juzgar si un salto es real
        print(f"─── Conteos por año — {nombre_grupo} (aceptadas/total) ───")
        for etiqueta, conteos in conteos_por_serie.items():
            resumen = ", ".join(
                f"{año}: {conteos[año]['acept']}/{conteos[año]['total']}"
                for año in sorted(conteos)
            )
            print(f"  {etiqueta}: {resumen}")
        print()

        for metrica, prefijo, titulo_base, ylabel, ylim, linea_ref, lineas_extra in METRICAS:
            series = {
                etiqueta: serie_metrica(conteos, globales, metrica)
                for etiqueta, conteos in conteos_por_serie.items()
            }
            graficar_lineas_por_año(
                series,
                f"{titulo_base} — {nombre_grupo}",
                os.path.join(OUTPUT_DIR, f"{prefijo}_{sufijo}.png"),
                años_referencia=años_dataset,
                ylabel=ylabel,
                ylim=ylim,
                linea_referencia=linea_ref,
                lineas_extra=lineas_extra,
            )

    print(f"\n✓ Todas las gráficas guardadas en: {OUTPUT_DIR}/")


if __name__ == "__main__":
    main()