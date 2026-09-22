"""
Gráfico de barras apiladas por Género Solicitante y Año de Inicio.
Eje X: años (2021, 2023, 2024, 2025, Todos)
Columnas por año: Masculino y Femenino
Cada barra: apilada Aceptadas (abajo, sólido) + Suplentes (arriba, transparente)
Encima de cada barra: % Aceptadas / Total de ese género-año
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
OUTPUT_PATH = str(BASE_DIR / "../../outputs/graphs/grafico_genero.png")
# ──────────────────────────────────────────────────────────────────────────────

GENEROS = ["Masculino", "Femenino"]
AÑOS    = [2010, 2014, 2015, 2016, 2017, 2019, 2021, 2024, 2025, 2026]

COLORES_GENERO = {
    "Masculino": "#0EA5E9",   
    "Femenino":  "#EC4848",   
}


def main():
    client = MongoClient(MONGO_URI)
    col    = client[DB_NAME][COLECCION]

    # data[año][genero] = {"Aceptada": n, "Suplente": n}
    data = defaultdict(lambda: defaultdict(lambda: {"Aceptada": 0, "Suplente": 0}))

    for doc in col.find(
        {"Género Solicitante": {"$in": GENEROS}},
        {"Año Inicio": 1, "Género Solicitante": 1, "Estado Solicitud": 1}
    ):
        año     = doc.get("Año Inicio")
        genero  = doc.get("Género Solicitante")
        estado  = doc.get("Estado Solicitud")

        if año and genero and estado in ("Aceptada", "Suplente"):
            data[año][genero][estado] += 1
            data["Todos"][genero][estado] += 1

    client.close()

    # ─── Layout ───────────────────────────────────────────────────────────────
    fig, ax = plt.subplots(figsize=(24, 13.5))   # 1920×1080 @ 80dpi
    fig.patch.set_facecolor("#F8FAFC")
    ax.set_facecolor("#F8FAFC")

    n_años    = len(AÑOS)
    n_generos = len(GENEROS)
    group_w   = 0.5          # ancho total del grupo por año (más estrecho, solo 2 barras)
    bar_w     = group_w / n_generos
    group_gap = 1.0

    x_centers = np.arange(n_años) * group_gap

    for g_idx, año in enumerate(AÑOS):
        x_base = x_centers[g_idx] - group_w / 2 + bar_w / 2

        for gen_idx, genero in enumerate(GENEROS):
            x_pos  = x_base + gen_idx * bar_w
            counts = data[año][genero]
            aceptadas = counts["Aceptada"]
            suplentes = counts["Suplente"]
            total     = aceptadas + suplentes

            color = COLORES_GENERO[genero]

            # Aceptadas (base, sólido)
            ax.bar(x_pos, aceptadas, width=bar_w * 0.8,
                   color=color, alpha=1.0, zorder=3)
            # Suplentes (encima, transparente)
            ax.bar(x_pos, suplentes, width=bar_w * 0.8,
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
        "Solicitudes por Género y Año\n",
        fontsize=16, fontweight="bold", color="#0F172A", pad=20
    )

    ax.yaxis.set_major_locator(plt.MaxNLocator(integer=True))
    ax.tick_params(axis="y", labelsize=11, colors="#475569")
    ax.spines[["top", "right"]].set_visible(False)
    ax.spines[["left", "bottom"]].set_color("#CBD5E1")
    ax.yaxis.grid(True, linestyle="--", alpha=0.5, color="#CBD5E1", zorder=0)
    ax.set_axisbelow(True)

    # ─── Leyenda ──────────────────────────────────────────────────────────────
    legend_genero = [
        mpatches.Patch(color=COLORES_GENERO[g], label=g) for g in GENEROS
    ]
    legend_estados = [
        mpatches.Patch(facecolor="#888", alpha=1.0,  label="Aceptada"),
        mpatches.Patch(facecolor="#888", alpha=0.35, label="Suplente"),
    ]
    leg1 = ax.legend(
        handles=legend_genero,
        title="Género", title_fontsize=11,
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