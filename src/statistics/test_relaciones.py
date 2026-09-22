"""
Exploración de relaciones ENTRE variables categóricas (no contra el Estado
de Solicitud, sino entre sí): Centro de Investigación × Género, Rama × Género
y Centro × Rama.

Para cada relación se calcula, en tres subconjuntos (GENERAL, ACEPTADA,
SUPLENTE):
  · Chi-cuadrado de independencia (chi2_contingency) — ¿hay indicios de
    asociación entre las dos variables?
  · V de Cramér — tamaño del efecto (0 = nada, 1 = asociación perfecta),
    simétrico, derivado del propio estadístico χ².
  · U de Theil / coeficiente de incertidumbre — basado en entropía, mide
    cuánto reduce conocer una variable la incertidumbre sobre la otra.
    Es ASIMÉTRICO: U(A|B) no tiene por qué ser igual a U(B|A).

No se usa el test exacto de Fisher aquí (a diferencia de test_centros.py /
test_ramas.py / test_genero.py), solo estas tres medidas.
"""

from pathlib import Path
import sys
from pymongo import MongoClient
from scipy.stats import chi2_contingency, entropy
import numpy as np
import pandas as pd
from datetime import datetime

# ─── CONFIGURACIÓN ────────────────────────────────────────────────────────────
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from db_config import MONGO_URI, DB_NAME
COLECCION  = "Solicitudes"
OUTPUT_MD  = "test_relaciones.md"
ALPHA = 0.05
# ──────────────────────────────────────────────────────────────────────────────

CENTROS = [
    "Universidad de Valladolid",
    "Universidad de Salamanca",
    "Universidad de León",
    "Universidad de Burgos",
    "CSIC",
]

GENEROS = ["Masculino", "Femenino"]

RAMAS = [
    "Ciencias - Ciencias de la Salud",
    "Ciencias - Resto",
    "Ingenierías",
    "Ciencias Sociales - Resto",
    "Filosofía y Letras",
    "Ciencias - Matemáticas y Física",
    "Ciencias Sociales - Educación",
]

ESTADOS = ["Aceptada", "Suplente"]

# Las tres relaciones a explorar: (nombre bonito, campo A, valores A, campo B, valores B)
RELACIONES = [
    ("Centro de Investigación × Género", "Centro de Investigación", CENTROS, "Género Solicitante", GENEROS),
    ("Rama × Género", "ramaDep", RAMAS, "Género Solicitante", GENEROS),
    ("Centro de Investigación × Rama", "Centro de Investigación", CENTROS, "ramaDep", RAMAS),
]


def construir_tabla(docs, campo_a, valores_a, campo_b, valores_b):
    """Tabla de contingencia valores_a (filas) x valores_b (columnas)."""
    tabla = pd.DataFrame(0, index=valores_a, columns=valores_b)
    for doc in docs:
        va = doc.get(campo_a)
        vb = doc.get(campo_b)
        if va in valores_a and vb in valores_b:
            tabla.loc[va, vb] += 1
    return tabla


def cramers_v_valor(tabla):
    """
    V de Cramér, calculado con el χ² SIN la corrección de continuidad de
    Yates (esa corrección es apropiada para el test de hipótesis en tablas
    2×2, pero sesga a la baja el tamaño del efecto si se reutiliza aquí).
    """
    chi2_sin_correccion, _, _, _ = chi2_contingency(tabla, correction=False)
    n = tabla.values.sum()
    r, k = tabla.shape
    return float(np.sqrt(chi2_sin_correccion / (n * (min(r, k) - 1))))


def interpretar_cramer(v):
    """Interpretación orientativa (umbrales aproximados, no una convención única)."""
    if v < 0.1:
        return "muy débil / prácticamente despreciable"
    elif v < 0.2:
        return "débil"
    elif v < 0.4:
        return "moderada"
    elif v < 0.6:
        return "relativamente fuerte"
    else:
        return "fuerte"


def theils_u(tabla, x_dado_y=True):
    """
    Coeficiente de incertidumbre de Theil.

    x_dado_y=True  -> U(filas | columnas): cuánto reduce conocer la columna
                       la incertidumbre sobre la fila.
    x_dado_y=False -> U(columnas | filas): al revés (se calcula transponiendo).
    """
    if not x_dado_y:
        return theils_u(tabla.T, x_dado_y=True)

    n = tabla.values.sum()
    marginal_filas = tabla.sum(axis=1) / n     # p(X)
    marginal_cols  = tabla.sum(axis=0) / n     # p(Y)

    h_x = entropy(marginal_filas)
    if h_x == 0:
        # La variable objetivo no tiene incertidumbre de partida (una sola
        # categoría con todo el peso): U no está bien definido, se toma 1.0
        return 1.0

    h_x_dado_y = 0.0
    for col in tabla.columns:
        p_col = marginal_cols[col]
        if p_col == 0:
            continue
        columna = tabla[col]
        total_col = columna.sum()
        if total_col == 0:
            continue
        dist_condicional = columna / total_col
        h_x_dado_y += p_col * entropy(dist_condicional)

    return float((h_x - h_x_dado_y) / h_x)


def analizar_relacion(tabla, nombre_a, nombre_b, etiqueta):
    md = [f"### {etiqueta}\n"]

    md.append(f"**Tabla de contingencia: {nombre_a} (filas) × {nombre_b} (columnas)**\n")
    cols = list(tabla.columns)
    md.append(f"| {nombre_a} \\\\ {nombre_b} | " + " | ".join(cols) + " | Total |")
    md.append("|" + "---|" * (len(cols) + 2))
    for idx in tabla.index:
        fila = tabla.loc[idx]
        md.append(f"| {idx} | " + " | ".join(str(int(v)) for v in fila) + f" | {int(fila.sum())} |")
    totales_col = tabla.sum(axis=0)
    md.append("| **Total** | " + " | ".join(str(int(v)) for v in totales_col) +
               f" | **{int(tabla.values.sum())}** |")
    md.append("")

    total_general = tabla.values.sum()
    if total_general == 0:
        md.append("> ⚠ No hay datos suficientes para el análisis en este subconjunto.\n")
        bloque = "\n".join(md)
        print(bloque)
        return bloque

    # Se eliminan filas/columnas completamente vacías para no romper los cálculos
    tabla_valida = tabla.loc[tabla.sum(axis=1) > 0, tabla.sum(axis=0) > 0]

    if tabla_valida.shape[0] < 2 or tabla_valida.shape[1] < 2:
        md.append("> ⚠ Tras descartar categorías sin datos, no queda tabla suficiente "
                   "para el análisis (hacen falta al menos 2 filas y 2 columnas con datos).\n")
        bloque = "\n".join(md)
        print(bloque)
        return bloque

    # ── Chi-cuadrado ────────────────────────────────────────────────────────
    chi2, p, dof, esperado = chi2_contingency(tabla_valida)
    significativo = p < ALPHA

    md.append(f"**Chi-cuadrado de independencia** (tabla {tabla_valida.shape[0]}×{tabla_valida.shape[1]})\n")
    md.append(f"- χ² = `{chi2:.4f}`")
    md.append(f"- gl = `{dof}`")
    md.append(f"- p-valor = `{p:.5f}`")
    md.append(f"- **Conclusión:** {'Hay' if significativo else 'No hay'} asociación "
               f"significativa entre {nombre_a} y {nombre_b} (α = {ALPHA})")
    if (esperado < 5).any():
        md.append("")
        md.append("> ⚠ Alguna celda esperada < 5: el chi-cuadrado puede no ser fiable en esta tabla.")
    md.append("")

    # ── V de Cramér ─────────────────────────────────────────────────────────
    v = cramers_v_valor(tabla_valida)
    md.append("**V de Cramér (tamaño del efecto, simétrico)**\n")
    md.append(f"- V = `{v:.3f}`")
    md.append(f"- Interpretación orientativa: {interpretar_cramer(v)}")
    md.append("")

    # ── U de Theil (ambas direcciones) ─────────────────────────────────────
    u_a_dado_b = theils_u(tabla_valida, x_dado_y=True)
    u_b_dado_a = theils_u(tabla_valida, x_dado_y=False)
    md.append("**U de Theil / coeficiente de incertidumbre (asimétrico)**\n")
    md.append(f"- U({nombre_a} | {nombre_b}) = `{u_a_dado_b:.3f}` — cuánto reduce conocer "
               f"{nombre_b} la incertidumbre sobre {nombre_a}")
    md.append(f"- U({nombre_b} | {nombre_a}) = `{u_b_dado_a:.3f}` — cuánto reduce conocer "
               f"{nombre_a} la incertidumbre sobre {nombre_b}")
    md.append("")

    bloque = "\n".join(md)
    print(bloque)
    return bloque


def main():
    client = MongoClient(MONGO_URI)
    col = client[DB_NAME][COLECCION]

    proyeccion = {
        "Centro de Investigación": 1,
        "Género Solicitante": 1,
        "ramaDep": 1,
        "Estado Solicitud": 1,
    }
    docs = list(col.find({}, proyeccion))
    client.close()

    bloques_md = [
        "# Relaciones entre Centro, Género y Rama\n",
        f"_Generado el {datetime.now().strftime('%Y-%m-%d %H:%M')}_\n",
        (
            "> Nota metodológica: aquí se exploran relaciones ENTRE variables "
            "categóricas (no contra el Estado de Solicitud). Para cada par se "
            "calculan tres medidas: **chi-cuadrado** de independencia (¿hay "
            "asociación?), **V de Cramér** (tamaño del efecto, simétrico) y "
            "**U de Theil** (coeficiente de incertidumbre basado en entropía, "
            "asimétrico — se calcula en ambas direcciones). Cada relación se "
            "analiza tres veces: con todas las solicitudes (GENERAL), solo "
            "con las Aceptadas y solo con las Suplentes, para ver si el "
            "patrón cambia según el resultado de la solicitud.\n"
        ),
    ]

    for nombre_relacion, campo_a, valores_a, campo_b, valores_b in RELACIONES:
        bloques_md.append(f"## {nombre_relacion}\n")

        tabla_general = construir_tabla(docs, campo_a, valores_a, campo_b, valores_b)
        bloques_md.append(analizar_relacion(tabla_general, campo_a, campo_b, "GENERAL — Todas las solicitudes"))

        for estado in ESTADOS:
            docs_estado = [d for d in docs if d.get("Estado Solicitud") == estado]
            tabla_estado = construir_tabla(docs_estado, campo_a, valores_a, campo_b, valores_b)
            bloques_md.append(analizar_relacion(tabla_estado, campo_a, campo_b, estado.upper()))

    with open(OUTPUT_MD, "w", encoding="utf-8") as f:
        f.write("\n".join(bloques_md))

    print(f"\n✓ Resultados guardados en: {OUTPUT_MD}")


if __name__ == "__main__":
    main()