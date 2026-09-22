"""
Test de independencia entre Rama y Estado de Solicitud (Aceptada / Suplente).

Como hay 7 ramas (tabla 7x2, no 2x2), el test exacto de Fisher clásico de
scipy no aplica directamente a la tabla completa (solo soporta 2x2). Por eso:
  · Chi-cuadrado de independencia sobre la tabla completa.
  · Fisher exacto por rama (esa rama vs. el resto agrupado), igual que se
    hizo con los centros.
"""

from pathlib import Path
import sys
from pymongo import MongoClient
from scipy.stats import chi2_contingency, fisher_exact
import pandas as pd
from datetime import datetime

# ─── CONFIGURACIÓN ────────────────────────────────────────────────────────────
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from db_config import MONGO_URI, DB_NAME
COLECCION      = "Solicitudes"
OUTPUT_MD = "test_ramas.md"
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

ESTADOS = ["Aceptada", "Suplente"]


def construir_tabla(docs):
    tabla = pd.DataFrame(0, index=RAMAS, columns=ESTADOS)
    for doc in docs:
        rama   = doc.get("ramaDep")
        estado = doc.get("Estado Solicitud")
        if rama in RAMAS and estado in ESTADOS:
            tabla.loc[rama, estado] += 1
    return tabla


def test_chi2(tabla, etiqueta):
    md = [f"## {etiqueta}\n"]

    md.append("| Rama | Aceptada | Suplente | Total |")
    md.append("|---|---:|---:|---:|")
    for rama in RAMAS:
        acept = tabla.loc[rama, "Aceptada"]
        supl  = tabla.loc[rama, "Suplente"]
        md.append(f"| {rama} | {acept} | {supl} | {acept + supl} |")
    total = tabla.values.sum()
    md.append(f"| **Total** | **{tabla['Aceptada'].sum()}** | "
               f"**{tabla['Suplente'].sum()}** | **{total}** |")
    md.append("")

    if (total == 0) or (tabla.sum(axis=1) == 0).any():
        md.append("> ⚠ No hay datos suficientes para el test en este subconjunto.\n")
        bloque = "\n".join(md)
        print(bloque)
        return bloque

    chi2, p, dof, esperado = chi2_contingency(tabla)
    significativo = p < 0.05

    md.append(f"**Chi-cuadrado de independencia** (tabla {tabla.shape[0]}×{tabla.shape[1]})")
    md.append("")
    md.append(f"- χ² = `{chi2:.4f}`")
    md.append(f"- gl = `{dof}`")
    md.append(f"- p-valor = `{p:.5f}`")
    md.append(f"- **Conclusión:** {'Hay' if significativo else 'No hay'} asociación "
               f"significativa entre Rama y Estado (α = 0.05)")

    if (esperado < 5).any():
        md.append("")
        md.append("> ⚠ Alguna celda esperada < 5: el chi-cuadrado puede no ser fiable, "
                   "revisa los tests de Fisher por rama abajo.")

    md.append("")
    md.append("**Test exacto de Fisher — cada rama vs. el resto**\n")
    md.append("| Rama | p-valor | Odds Ratio | Significativo |")
    md.append("|---|---:|---:|:---:|")

    for rama in RAMAS:
        fila_rama  = tabla.loc[rama]
        fila_resto = tabla.drop(index=rama).sum()

        tabla_2x2 = [
            [fila_rama["Aceptada"],  fila_rama["Suplente"]],
            [fila_resto["Aceptada"], fila_resto["Suplente"]],
        ]

        if sum(tabla_2x2[0]) == 0:
            md.append(f"| {rama} | sin datos | — | — |")
            continue

        odds_ratio, p_fisher = fisher_exact(tabla_2x2)
        marca = "✅ sí" if p_fisher < 0.05 else "no"
        md.append(f"| {rama} | {p_fisher:.5f} | {odds_ratio:.3f} | {marca} |")

    md.append("")

    bloque = "\n".join(md)
    print(bloque)
    return bloque


def main():
    client = MongoClient(MONGO_URI)
    col    = client[DB_NAME][COLECCION]

    proyeccion = {"Año Inicio": 1, "ramaDep": 1, "Estado Solicitud": 1}
    docs = list(col.find({"ramaDep": {"$in": RAMAS}}, proyeccion))
    client.close()

    bloques_md = [
        "# Test de independencia — Rama(Departamento) vs. Estado de Solicitud\n",
        f"_Generado el {datetime.now().strftime('%Y-%m-%d %H:%M')}_\n",
        (
            "> Nota metodológica: la tabla es de 7 ramas × 2 estados, por lo que "
            "el test exacto de Fisher clásico (solo válido en tablas 2×2) no puede "
            "aplicarse directamente a la tabla completa. Por eso se combina un "
            "**chi-cuadrado de independencia** sobre la tabla completa con un "
            "**Fisher exacto** de cada rama comparada contra el resto agrupado.\n"
        ),
    ]

    # General
    tabla_general = construir_tabla(docs)
    bloques_md.append(test_chi2(tabla_general, "GENERAL — Todos los años"))

    # Por año
    años = sorted({d.get("Año Inicio") for d in docs if d.get("Año Inicio")})
    for año in años:
        docs_año = [d for d in docs if d.get("Año Inicio") == año]
        tabla_año = construir_tabla(docs_año)
        bloques_md.append(test_chi2(tabla_año, f"AÑO {año}"))

    with open(OUTPUT_MD, "w", encoding="utf-8") as f:
        f.write("\n".join(bloques_md))

    print(f"\n✓ Resultados guardados en: {OUTPUT_MD}")


if __name__ == "__main__":
    main()