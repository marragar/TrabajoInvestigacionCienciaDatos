"""
MOSAIC PLOT: Centro de Investigación × Género Solicitante × Estado Solicitud

Un mosaic plot representa una tabla de contingencia como un rectángulo que se va
subdividiendo. El ÁREA de cada bloque es proporcional al número de solicitudes,
así que el gráfico entero suma el 100% de los datos y ningún bloque miente sobre
su peso.

Se lee en tres niveles, cada uno cortando en dirección alterna:

  Nivel 1 — CENTRO   -> corte VERTICAL:   el ANCHO de cada columna es la
                        proporción de solicitudes de ese centro.
  Nivel 2 — GÉNERO   -> corte HORIZONTAL: dentro de cada columna, la ALTURA de
                        cada franja es el reparto por género DE ESE CENTRO.
  Nivel 3 — ESTADO   -> corte VERTICAL:   dentro de cada franja, el corte marca
                        la TASA DE ACEPTACIÓN de ese centro y género.

Los cortes alternan de dirección a propósito: dos cortes seguidos en la misma
dirección serían imposibles de distinguir a ojo.

─── CÓDIGO DE COLOR (dos ejes a la vez) ──────────────────────────────────────
  · TONO      = género  -> azul (masculino) / rojo (femenino)
  · INTENSIDAD= estado  -> saturado (aceptada) / pálido (suplente)

De un vistazo: cuanto más "sólido" se ve un bloque, más se acepta ahí.

─── QUÉ BUSCAR ───────────────────────────────────────────────────────────────
  · Anchos de columna    -> qué centros concentran las solicitudes
  · Alturas dentro de una columna -> si un centro está más masculinizado que otro
  · Posición del corte vertical interno -> tasa de aceptación. Si TODOS los cortes
    caen a la misma altura, no hay relación con centro ni género (independencia).
    Los desalineamientos son exactamente lo que test_centros.py y test_genero.py
    detectan como significativo.

Este gráfico es la versión visual de esos tests: donde ellos dan un p-valor, el
mosaico enseña dónde está la diferencia y de qué tamaño es.
"""

import sys
from datetime import datetime
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from matplotlib.lines import Line2D
from pymongo import MongoClient

# ─── CONFIGURACIÓN ────────────────────────────────────────────────────────────
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from db_config import MONGO_URI, DB_NAME
COLECCION = "Solicitudes"

CARPETA_SALIDA = str(BASE_DIR / "../../outputs/graphs/Graficas")
NOMBRE_FICHERO = "34_mosaico_centro_genero_estado.png"

# Ordenar los centros por nº de solicitudes (convención habitual en mosaicos).
# Ponlo a False para respetar el orden fijo de la lista CENTROS.
ORDENAR_POR_TAMANO = True

# Anotar dentro de cada franja el % de aceptación
MOSTRAR_PORCENTAJES = True
# ──────────────────────────────────────────────────────────────────────────────

CENTROS = [
    "Universidad de Valladolid",
    "Universidad de Salamanca",
    "Universidad de León",
    "Universidad de Burgos",
    "CSIC",
]

# Abreviaturas para el eje (los nombres completos no caben)
ABREV = {
    "Universidad de Valladolid": "UVa",
    "Universidad de Salamanca":  "USAL",
    "Universidad de León":       "ULE",
    "Universidad de Burgos":     "UBU",
    "CSIC":                      "CSIC",
}

GENEROS = ["Masculino", "Femenino"]
ESTADOS = ["Aceptada", "Suplente"]

# TONO = género, INTENSIDAD = estado
COLORES = {
    ("Masculino", "Aceptada"): "#1F5FA8",   # azul saturado
    ("Masculino", "Suplente"): "#AECBE8",   # azul pálido
    ("Femenino",  "Aceptada"): "#B02A2A",   # rojo saturado
    ("Femenino",  "Suplente"): "#EBAFAF",   # rojo pálido
}

# Huecos entre bloques: se reducen con la profundidad, para que la jerarquía
# se lea sola (separación grande = división importante).
HUECO_CENTRO = 0.015
HUECO_GENERO = 0.010
HUECO_ESTADO = 0.004


def contar(docs):
    """Devuelve {(centro, genero, estado): n} y los totales por nivel."""
    conteo = {}
    for doc in docs:
        centro = doc.get("Centro de Investigación")
        genero = doc.get("Género Solicitante")
        estado = doc.get("Estado Solicitud")
        if centro not in CENTROS or genero not in GENEROS or estado not in ESTADOS:
            continue
        clave = (centro, genero, estado)
        conteo[clave] = conteo.get(clave, 0) + 1
    return conteo


def n_centro(conteo, centro):
    return sum(v for (c, _, _), v in conteo.items() if c == centro)


def n_centro_genero(conteo, centro, genero):
    return sum(v for (c, g, _), v in conteo.items() if c == centro and g == genero)


def dibujar_mosaico(conteo, ax):
    total = sum(conteo.values())
    if total == 0:
        raise ValueError("No hay datos que representar.")

    centros = [c for c in CENTROS if n_centro(conteo, c) > 0]
    if ORDENAR_POR_TAMANO:
        centros.sort(key=lambda c: n_centro(conteo, c), reverse=True)

    # ── Nivel 1: ancho de cada columna ∝ nº solicitudes del centro ────────────
    ancho_util = 1.0 - HUECO_CENTRO * (len(centros) - 1)
    x = 0.0
    ticks_x, etiquetas_x = [], []

    for centro in centros:
        n_c = n_centro(conteo, centro)
        w_centro = (n_c / total) * ancho_util

        ticks_x.append(x + w_centro / 2)
        etiquetas_x.append(f"{ABREV.get(centro, centro)}\n(n={n_c})")

        # ── Nivel 2: altura de cada franja ∝ reparto por género DEL CENTRO ────
        generos_presentes = [g for g in GENEROS if n_centro_genero(conteo, centro, g) > 0]
        alto_util = 1.0 - HUECO_GENERO * (len(generos_presentes) - 1)
        y = 0.0

        for genero in generos_presentes:
            n_cg = n_centro_genero(conteo, centro, genero)
            h_genero = (n_cg / n_c) * alto_util

            # ── Nivel 3: corte vertical ∝ tasa de aceptación ──────────────────
            estados_presentes = [e for e in ESTADOS if conteo.get((centro, genero, e), 0) > 0]
            ancho_franja = w_centro - HUECO_ESTADO * (len(estados_presentes) - 1)
            x_sub = x

            for estado in estados_presentes:
                n_cge = conteo.get((centro, genero, estado), 0)
                w_estado = (n_cge / n_cg) * ancho_franja

                ax.add_patch(Rectangle(
                    (x_sub, y), w_estado, h_genero,
                    facecolor=COLORES[(genero, estado)],
                    edgecolor="white", linewidth=0.6,
                ))
                x_sub += w_estado + HUECO_ESTADO

            # Anotación: % de aceptación de esta franja (centro × género)
            if MOSTRAR_PORCENTAJES:
                n_acep = conteo.get((centro, genero, "Aceptada"), 0)
                pct = 100 * n_acep / n_cg
                # Solo si el bloque da de sí; si no, el texto se sale
                if w_centro > 0.05 and h_genero > 0.07:
                    ax.text(
                        x + w_centro / 2, y + h_genero / 2,
                        f"{pct:.0f}%",
                        ha="center", va="center",
                        fontsize=9, fontweight="bold",
                        color="white" if pct > 50 else "#333333",
                    )

            y += h_genero + HUECO_GENERO

        x += w_centro + HUECO_CENTRO

    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_xticks(ticks_x)
    ax.set_xticklabels(etiquetas_x, fontsize=10)
    ax.set_yticks([])
    ax.tick_params(axis="x", length=0, pad=6)
    for lado in ("top", "right", "left", "bottom"):
        ax.spines[lado].set_visible(False)

    ax.set_xlabel("Centro de investigación  ·  el ancho es proporcional al nº de solicitudes",
                  fontsize=10, labelpad=10)
    ax.set_ylabel("Género  ·  la altura es proporcional al reparto dentro del centro",
                  fontsize=10, labelpad=10)

    return centros


def main():
    client = MongoClient(MONGO_URI)
    col = client[DB_NAME][COLECCION]
    docs = list(col.find(
        {},
        {"Centro de Investigación": 1, "Género Solicitante": 1, "Estado Solicitud": 1},
    ))
    client.close()

    conteo = contar(docs)
    total = sum(conteo.values())
    print(f"Solicitudes representadas: {total}")

    os.makedirs(CARPETA_SALIDA, exist_ok=True)

    fig, ax = plt.subplots(figsize=(12, 7))
    dibujar_mosaico(conteo, ax)

    ax.set_title(
        "Solicitudes por centro, género y estado",
        fontsize=15, fontweight="bold", pad=16,
    )

    # Leyenda: los dos ejes de color por separado, que es como se lee el gráfico
    handles = [
        Line2D([], [], marker="s", linestyle="", markersize=11,
               markerfacecolor=COLORES[(g, e)], markeredgecolor="white",
               label=f"{g} · {e}")
        for g in GENEROS for e in ESTADOS
    ]
    ax.legend(
        handles=handles, title="Género · Estado",
        loc="upper left", bbox_to_anchor=(1.01, 1.0),
        frameon=True, fontsize=9, title_fontsize=10,
    )

    fig.text(
        0.01, 0.015,
        "El % dentro de cada franja es la tasa de aceptación. Si todos los cortes verticales "
        "cayeran alineados, no habría relación entre centro/género y aceptación.",
        fontsize=8.5, color="#555555",
    )

    fig.tight_layout(rect=[0, 0.04, 1, 1])
    ruta = os.path.join(CARPETA_SALIDA, NOMBRE_FICHERO)
    fig.savefig(ruta, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"✓ Guardada: {ruta}")


if __name__ == "__main__":
    main()