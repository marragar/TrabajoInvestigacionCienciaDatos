"""
Gráfico de barras apiladas por Centro de Investigación y Año de Inicio.
Eje X: años (2021, 2023, 2024, 2025, Todos)
Columnas por año: una por cada centro (5 centros)
Cada barra: apilada Aceptadas + Suplentes
Encima de cada barra: % Aceptadas / Total del centro-año
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
OUTPUT_PATH = str(BASE_DIR / "../../outputs/graphs/grafico_centros.png")
# ──────────────────────────────────────────────────────────────────────────────

CENTROS = [
    
    "Universidad de Valladolid",
    "Universidad de Salamanca",
    "Universidad de León",
    "Universidad de Burgos",
    "Otros",
    "CSIC",
]

AÑOS = [2010, 2014, 2015, 2016, 2017, 2019, 2021, 2024, 2025, 2026]


COLOR_ACEPTADA = "#2563EB"   # azul
COLOR_SUPLENTE = "#93C5FD"   # azul claro

def main():
    client = MongoClient(MONGO_URI)
    col    = client[DB_NAME][COLECCION]

    # Acumular conteos: data[año][centro] = {"Aceptada": n, "Suplente": n}
    data = defaultdict(lambda: defaultdict(lambda: {"Aceptada": 0, "Suplente": 0}))

    for doc in col.find(
        {"Centro de Investigación": {"$in": CENTROS}},
        {"Año Inicio": 1, "Centro de Investigación": 1, "Estado Solicitud": 1}
    ):
        año    = doc.get("Año Inicio")
        centro = doc.get("Centro de Investigación")
        estado = doc.get("Estado Solicitud")

        if año and centro and estado in ("Aceptada", "Suplente"):
            data[año][centro][estado] += 1
            data["Todos"][centro][estado] += 1

    client.close()

    # ─── Layout ───────────────────────────────────────────────────────────────
    fig, ax = plt.subplots(figsize=(24, 13.5))   # 1920×1080 @ 80dpi
    fig.patch.set_facecolor("#F8FAFC")
    ax.set_facecolor("#F8FAFC")

    n_años    = len(AÑOS)
    n_centros = len(CENTROS)
    group_w   = 0.8          # ancho total del grupo de barras por año
    bar_w     = group_w / n_centros
    group_gap = 1.0          # separación entre grupos de años

    colores_centros = {
        "Universidad de León":       "#1E3A5F",
        "Universidad de Valladolid": "#0EA5E9",
        "Universidad de Salamanca":  "#10B981",
        "Universidad de Burgos":     "#F59E0B",
        "CSIC":                      "#EF4444",
        "Otros":                     "#9A24FB",

    }

    x_centers = np.arange(n_años) * group_gap   # posición central de cada grupo

    for g_idx, año in enumerate(AÑOS):
        x_base = x_centers[g_idx] - group_w / 2 + bar_w / 2

        for c_idx, centro in enumerate(CENTROS):
            x_pos  = x_base + c_idx * bar_w
            counts = data[año][centro]
            aceptadas = counts["Aceptada"]
            suplentes = counts["Suplente"]
            total     = aceptadas + suplentes

            color = colores_centros[centro]

            # Barra aceptadas (parte inferior, sólida)
            ax.bar(x_pos, aceptadas, width=bar_w * 0.85,
                   color=color, alpha=1.0, zorder=3)
            # Barra suplentes (encima, más clara)
            ax.bar(x_pos, suplentes, width=bar_w * 0.85,
                   bottom=aceptadas, color=color, alpha=0.35, zorder=3)

            # Porcentaje encima
            if total > 0:
                pct = aceptadas / total * 100
                ax.text(
                    x_pos, total + 0.4,
                    f"{pct:.0f}",
                    ha="center", va="bottom",
                    fontsize=12, fontweight="bold",
                    color=color,
                )

    # ─── Ejes y etiquetas ─────────────────────────────────────────────────────
    ax.set_xticks(x_centers)
    ax.set_xticklabels([str(a) for a in AÑOS], fontsize=14, fontweight="bold", color="#1E293B")
    ax.set_ylabel("Nº de Solicitudes", fontsize=13, color="#475569", labelpad=12)
    ax.set_xlabel("Año de Inicio", fontsize=13, color="#475569", labelpad=12)
    ax.set_title(
        "Solicitudes por Centro de Investigación y Año\n",
        fontsize=16, fontweight="bold", color="#0F172A", pad=20
    )

    ax.yaxis.set_major_locator(plt.MaxNLocator(integer=True))
    ax.tick_params(axis="y", labelsize=11, colors="#475569")
    ax.spines[["top", "right"]].set_visible(False)
    ax.spines[["left", "bottom"]].set_color("#CBD5E1")
    ax.yaxis.grid(True, linestyle="--", alpha=0.5, color="#CBD5E1", zorder=0)
    ax.set_axisbelow(True)

    # ─── Leyenda ──────────────────────────────────────────────────────────────
    legend_centros = [
        mpatches.Patch(color=colores_centros[c], label=c) for c in CENTROS
    ]
    legend_estados = [
        mpatches.Patch(facecolor="#888", alpha=1.0,  label="Aceptada"),
        mpatches.Patch(facecolor="#888", alpha=0.35, label="Suplente"),
    ]
    leg1 = ax.legend(
        handles=legend_centros,
        title="Centro", title_fontsize=11,
        fontsize=10, loc="upper right",
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