"""
Gráfico de barras apiladas por Rama y Año de Inicio.
Eje X: años (2021, 2023, 2024, 2025, Todos)
Columnas por año: una por cada Rama (7 ramas)
Cada barra: apilada Aceptadas (abajo, sólido) + Suplentes (arriba, transparente)
Encima de cada barra: % Aceptadas / Total de esa rama-año
"""

import sys
import matplotlib
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
from pymongo import MongoClient
from collections import defaultdict

# ─── CONFIGURACIÓN ────────────────────────────────────────────────────────────
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from db_config import MONGO_URI, DB_NAME
COLECCION      = "Solicitudes"
OUTPUT_PATH = str(BASE_DIR / "../../outputs/graphs/grafico_ramasDEP.png")
# ──────────────────────────────────────────────────────────────────────────────

RAMAS = [
    "Ciencias - Ciencias de la Salud",
    "Ciencias - Resto",
    "Ingenierías",
    "Ciencias Sociales - Resto",
    "Filosofía y Letras",
    "Ciencias - Matemáticas y Física",
    "Ciencias Sociales - Educación"
]

AÑOS = [2010, 2014, 2015, 2016, 2017, 2019, 2021, 2024, 2025, 2026]


COLORES_RAMA = {
    "Filosofía y Letras":               "#8B5CF6",  # violeta
    "Ciencias Sociales - Educación":    "#F59E0B",  # ámbar
    "Ciencias Sociales - Resto":        "#F97316",  # naranja
    "Ciencias - Matemáticas y Física":  "#10B981",  # verde
    "Ciencias - Ciencias de la Salud":  "#EF4444",  # rojo
    "Ciencias - Resto":                 "#84CC16",  # lima
    "Ingenierías":                      "#0EA5E9",  # azul
}


def main():
    client = MongoClient(MONGO_URI)
    col    = client[DB_NAME][COLECCION]

    # data[año][rama] = {"Aceptada": n, "Suplente": n}
    data = defaultdict(lambda: defaultdict(lambda: {"Aceptada": 0, "Suplente": 0}))

    for doc in col.find(
        {"ramaDep": {"$in": RAMAS}},
        {"Año Inicio": 1, "ramaDep": 1, "Estado Solicitud": 1}
    ):
        año    = doc.get("Año Inicio")
        rama   = doc.get("ramaDep")
        estado = doc.get("Estado Solicitud")

        if año and rama and estado in ("Aceptada", "Suplente"):
            data[año][rama][estado] += 1
            data["Todos"][rama][estado] += 1

    client.close()

    # ─── Layout ───────────────────────────────────────────────────────────────
    fig, ax = plt.subplots(figsize=(24, 13.5))   # 1920×1080 @ 80dpi
    fig.patch.set_facecolor("#F8FAFC")
    ax.set_facecolor("#F8FAFC")

    n_años  = len(AÑOS)
    n_ramas = len(RAMAS)
    group_w   = 0.85
    bar_w     = group_w / n_ramas
    group_gap = 1.0

    x_centers = np.arange(n_años) * group_gap

    for g_idx, año in enumerate(AÑOS):
        x_base = x_centers[g_idx] - group_w / 2 + bar_w / 2

        for r_idx, rama in enumerate(RAMAS):
            x_pos  = x_base + r_idx * bar_w
            counts = data[año][rama]
            aceptadas = counts["Aceptada"]
            suplentes = counts["Suplente"]
            total     = aceptadas + suplentes

            color = COLORES_RAMA[rama]

            # Aceptadas (base, sólido)
            ax.bar(x_pos, aceptadas, width=bar_w * 0.85,
                   color=color, alpha=1.0, zorder=3)
            # Suplentes (encima, transparente)
            ax.bar(x_pos, suplentes, width=bar_w * 0.85,
                   bottom=aceptadas, color=color, alpha=0.35, zorder=3)

            # Porcentaje encima
            if total > 0:
                pct = aceptadas / total * 100
                ax.text(
                    x_pos, total + 0.4,
                    f"{pct:.0f}",
                    ha="center", va="bottom",
                    fontsize=10, fontweight="bold",
                    color=color,
                )

    # ─── Ejes y etiquetas ─────────────────────────────────────────────────────
    ax.set_xticks(x_centers)
    ax.set_xticklabels([str(a) for a in AÑOS], fontsize=14, fontweight="bold", color="#1E293B")
    ax.set_ylabel("Nº de Solicitudes", fontsize=13, color="#475569", labelpad=12)
    ax.set_xlabel("Año de Inicio", fontsize=13, color="#475569", labelpad=12)
    ax.set_title(
        "Solicitudes por Rama(Departamento) y Año\n",
        fontsize=16, fontweight="bold", color="#0F172A", pad=20
    )

    ax.yaxis.set_major_locator(plt.MaxNLocator(integer=True))
    ax.tick_params(axis="y", labelsize=11, colors="#475569")
    ax.spines[["top", "right"]].set_visible(False)
    ax.spines[["left", "bottom"]].set_color("#CBD5E1")
    ax.yaxis.grid(True, linestyle="--", alpha=0.5, color="#CBD5E1", zorder=0)
    ax.set_axisbelow(True)

    # Un poco de margen extra arriba para que quepan los % en vertical
    ymax = ax.get_ylim()[1]
    ax.set_ylim(0, ymax * 1.12)

    # ─── Leyenda ──────────────────────────────────────────────────────────────
    legend_ramas = [
        mpatches.Patch(color=COLORES_RAMA[r], label=r) for r in RAMAS
    ]
    legend_estados = [
        mpatches.Patch(facecolor="#888", alpha=1.0,  label="Aceptada"),
        mpatches.Patch(facecolor="#888", alpha=0.35, label="Suplente"),
    ]
    leg1 = ax.legend(
        handles=legend_ramas,
        title="Rama", title_fontsize=11,
        fontsize=9, loc="upper right",
        framealpha=0.9, edgecolor="#E2E8F0"
    )
    ax.add_artist(leg1)
    ax.legend(
        handles=legend_estados,
        title="Estado", title_fontsize=11,
        fontsize=10, loc="upper left",
        framealpha=0.9, edgecolor="#E2E8F0"
    )

    plt.tight_layout(pad=2)
    plt.savefig(OUTPUT_PATH, dpi=80, bbox_inches="tight", facecolor=fig.get_facecolor())
    print(f"Gráfico guardado en: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()