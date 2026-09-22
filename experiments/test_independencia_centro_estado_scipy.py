"""
Test de independencia entre Centro de Investigación y Estado de Solicitud
(Aceptada / Suplente).

- Tabla general (todos los años juntos) y una tabla por cada año.
- Como la tabla es 5 centros x 2 estados (no 2x2), el test exacto de Fisher
  clásico de scipy no aplica directamente (solo soporta 2x2). Por eso:
    · Se usa Chi-cuadrado de independencia (chi2_contingency) para la tabla completa.
    · Además se calcula el test EXACTO de Fisher 2x2 para cada centro
      comparado contra "el resto" (centro vs. resto de centros), que es
      la forma estándar de aplicar Fisher cuando hay más de 2 categorías.
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
OUTPUT_MD   = "test_independencia.md"
# ──────────────────────────────────────────────────────────────────────────────

CENTROS = [
    "Universidad de Valladolid",
    "Universidad de Salamanca",
    "Universidad de León",
    "Universidad de Burgos",
    "CSIC",
]

ESTADOS = ["Aceptada", "Suplente"]


def construir_tabla(docs):
    """Devuelve un DataFrame Centro x Estado con los conteos."""
    tabla = pd.DataFrame(0, index=CENTROS, columns=ESTADOS)
    for doc in docs:
        centro = doc.get("Centro de Investigación")
        estado = doc.get("Estado Solicitud")
        if centro in CENTROS and estado in ESTADOS:
            tabla.loc[centro, estado] += 1
    return tabla


def test_chi2(tabla, etiqueta):
    md = [f"## {etiqueta}\n"]

    md.append("| Centro | Aceptada | Suplente | Total |")
    md.append("|---|---:|---:|---:|")
    for centro in CENTROS:
        acept = tabla.loc[centro, "Aceptada"]
        supl  = tabla.loc[centro, "Suplente"]
        md.append(f"| {centro} | {acept} | {supl} | {acept + supl} |")
    total = tabla.values.sum()
    md.append(f"| **Total** | **{tabla['Aceptada'].sum()}** | "
               f"**{tabla['Suplente'].sum()}** | **{total}** |")
    md.append("")

    if (total == 0) or (tabla.sum(axis=1) == 0).any():
        md.append("> ⚠ No hay datos suficientes para el test en este subconjunto.\n")
        print("\n".join(md))
        return "\n".join(md)

    chi2, p, dof, esperado = chi2_contingency(tabla)
    significativo = p < 0.05

    md.append(f"**Chi-cuadrado de independencia** (tabla {tabla.shape[0]}×{tabla.shape[1]})")
    md.append("")
    md.append(f"- χ² = `{chi2:.4f}`")
    md.append(f"- gl = `{dof}`")
    md.append(f"- p-valor = `{p:.5f}`")
    md.append(f"- **Conclusión:** {'Hay' if significativo else 'No hay'} asociación "
               f"significativa entre Centro y Estado (α = 0.05)")

    if (esperado < 5).any():
        md.append("")
        md.append("> ⚠ Alguna celda esperada < 5: el chi-cuadrado puede no ser fiable, "
                   "revisa los tests de Fisher por centro abajo.")

    md.append("")
    md.append("**Test exacto de Fisher — cada centro vs. el resto**\n")
    md.append("| Centro | p-valor | Odds Ratio | Significativo |")
    md.append("|---|---:|---:|:---:|")

    for centro in CENTROS:
        fila_centro = tabla.loc[centro]
        fila_resto  = tabla.drop(index=centro).sum()

        tabla_2x2 = [
            [fila_centro["Aceptada"], fila_centro["Suplente"]],
            [fila_resto["Aceptada"],  fila_resto["Suplente"]],
        ]

        if sum(tabla_2x2[0]) == 0:
            md.append(f"| {centro} | sin datos | — | — |")
            continue

        odds_ratio, p_fisher = fisher_exact(tabla_2x2)
        marca = "✅ sí" if p_fisher < 0.05 else "no"
        md.append(f"| {centro} | {p_fisher:.5f} | {odds_ratio:.3f} | {marca} |")

    md.append("")

    bloque = "\n".join(md)
    print(bloque)
    return bloque


def main():
    client = MongoClient(MONGO_URI)
    col    = client[DB_NAME][COLECCION]

    proyeccion = {"Año Inicio": 1, "Centro de Investigación": 1, "Estado Solicitud": 1}
    docs = list(col.find({"Centro de Investigación": {"$in": CENTROS}}, proyeccion))
    client.close()

    bloques_md = [
        "# Test de independencia — Centro de Investigación vs. Estado de Solicitud\n",
        f"_Generado el {datetime.now().strftime('%Y-%m-%d %H:%M')}_\n",
        (
            "> Nota metodológica: la tabla es de 5 centros × 2 estados, por lo que "
            "el test exacto de Fisher clásico (solo válido en tablas 2×2) no puede "
            "aplicarse directamente a la tabla completa. Por eso se combina un "
            "**chi-cuadrado de independencia** sobre la tabla completa con un "
            "**Fisher exacto** de cada centro comparado contra el resto agrupado.\n"
        ),
    ]

    # ─── General (todos los años) ──────────────────────────────────────────
    tabla_general = construir_tabla(docs)
    bloques_md.append(test_chi2(tabla_general, "GENERAL — Todos los años"))

    # ─── Por año ────────────────────────────────────────────────────────────
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