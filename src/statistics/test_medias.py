"""
Comparación de MEDIAS de variables numéricas (Nota, Nº Contratos) según las
variables categóricas del proyecto (Estado Solicitud, Género, Centro, Rama).

A diferencia de test_centros.py / test_ramas.py / test_genero.py (que cruzan
dos variables CATEGÓRICAS con chi-cuadrado y Fisher) y de test_relaciones.py
(categórica × categórica con Cramér y Theil), aquí la variable de interés es
NUMÉRICA y lo que se compara es su media entre grupos.

El test depende del número de grupos de la variable categórica:
  · 2 grupos (Estado Aceptada/Suplente, Género M/F) -> t de Student
  · 3+ grupos (5 Centros, 7 Ramas)                  -> ANOVA

ANOVA es la generalización del t de Student a 3 o más grupos: con exactamente
2 grupos ambos dan el mismo resultado.

─── VARIANTE DE WELCH ────────────────────────────────────────────────────
Tanto el t-test como el ANOVA se calculan en su variante de WELCH, que NO
asume que las varianzas sean iguales entre grupos. Es lo prudente aquí porque
los grupos tienen tamaños muy dispares (p.ej. Universidad de Valladolid vs
Universidad de Burgos). Se reporta también la versión clásica y el test de
Levene de homocedasticidad, para que se vea si ambas coinciden.

─── SOBRE LA NORMALIDAD ──────────────────────────────────────────────────
El t-test y el ANOVA no exigen que los DATOS sean normales, sino que lo sea
la distribución de la MEDIA. Con ~2.300 solicitudes, el Teorema Central del
Límite lo garantiza de sobra, así que la asimetría de la Nota no invalida
nada. No se aplica Shapiro-Wilk: con esta n rechazaría la normalidad siempre,
sin que eso signifique que el test no sirva.

─── POST-HOC (3+ grupos) ─────────────────────────────────────────────────
El ANOVA es un test GLOBAL: dice "hay alguna diferencia entre los grupos",
pero no dice cuál. Igual que el chi-cuadrado de test_centros.py. Por eso, si
el ANOVA sale significativo, se hacen comparaciones DOS A DOS entre todos los
pares de grupos, corrigiendo los p-valores por comparaciones múltiples con el
mismo criterio que en test_centros.py (Bonferroni o FDR/Benjamini-Hochberg,
configurable en METODO_CORRECCION).

─── TAMAÑO DEL EFECTO ────────────────────────────────────────────────────
Igual que Cramér's V acompaña al chi-cuadrado, aquí:
  · d de Cohen (2 grupos): diferencia de medias en desviaciones típicas.
    Referencia orientativa: 0.2 pequeño, 0.5 medio, 0.8 grande.
  · Eta cuadrado η² (3+ grupos): qué proporción de la variabilidad de la
    variable numérica se explica por el grupo. Va de 0 a 1.
    Referencia orientativa: 0.01 pequeño, 0.06 medio, 0.14 grande.

─── AVISOS DE CIRCULARIDAD ───────────────────────────────────────────────
  · Nº Contratos solo se analiza sobre las ACEPTADAS: las no aceptadas tienen
    los contratos a 0 por definición, así que cruzarlo con Estado Solicitud
    sería tautológico (por eso esa combinación se omite automáticamente).
  · Nota × Estado Solicitud SÍ se calcula, pero si el procedimiento consiste
    en ordenar por nota y aceptar de arriba abajo, saldrá significativo POR
    CONSTRUCCIÓN. Confirma el procedimiento, no es un hallazgo. El script lo
    marca con un aviso.
"""

from pathlib import Path
import sys
import math
from datetime import datetime

from pymongo import MongoClient
from scipy.stats import ttest_ind, f_oneway, levene, f as f_dist
from statsmodels.stats.multitest import multipletests
from itertools import combinations
import numpy as np

# ─── CONFIGURACIÓN ────────────────────────────────────────────────────────────
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from db_config import MONGO_URI, DB_NAME
COLECCION  = "solicitudesFinalVersion2"
OUTPUT_MD  = "test_medias.md"
ALPHA = 0.05
# Corrección para las comparaciones dos a dos post-hoc (igual que test_centros.py):
#   "bonferroni" -> controla el FWER (más conservador)
#   "fdr_bh"     -> controla el FDR (Benjamini-Hochberg, más potencia)
METODO_CORRECCION = "bonferroni"
# ──────────────────────────────────────────────────────────────────────────────

ESTADOS = ["Aceptada", "Suplente"]
GENEROS = ["Masculino", "Femenino"]

CENTROS = [
    "Universidad de Valladolid",
    "Universidad de Salamanca",
    "Universidad de León",
    "Universidad de Burgos",
    "CSIC",
]

RAMAS = [
    "Ciencias - Ciencias de la Salud",
    "Ciencias - Resto",
    "Ingenierías",
    "Ciencias Sociales - Resto",
    "Filosofía y Letras",
    "Ciencias - Matemáticas y Física",
    "Ciencias Sociales - Educación",
]

# (campo_mongo, etiqueta, filtro_estado)
#   filtro_estado="Aceptada" -> la variable solo tiene sentido en las aceptadas,
#   así que se filtra y se omite el cruce con Estado Solicitud (sería circular).
VARIABLES_NUMERICAS = [
    ("Nota", "Nota", None),
    ("Nº Contratos", "Nº Contratos", "Aceptada"),
]

# (campo_mongo, etiqueta, categorías)
VARIABLES_GRUPO = [
    ("Estado Solicitud", "Estado Solicitud", ESTADOS),
    ("Género Solicitante", "Género", GENEROS),
    ("Centro de Investigación", "Centro", CENTROS),
    ("ramaDep", "Rama", RAMAS),
]


def a_numero(valor):
    """Convierte a float lo que se pueda; None si no es un número utilizable."""
    if valor is None or isinstance(valor, bool):
        return None
    if isinstance(valor, (int, float)):
        return None if (isinstance(valor, float) and math.isnan(valor)) else float(valor)
    if isinstance(valor, str):
        texto = valor.strip().replace(",", ".")
        if not texto:
            return None
        try:
            return float(texto)
        except ValueError:
            return None
    return None


def extraer_grupos(docs, campo_num, campo_grupo, categorias):
    """
    Devuelve {categoría: [valores numéricos]}, descartando categorías vacías.
    """
    grupos = {cat: [] for cat in categorias}
    for doc in docs:
        cat = doc.get(campo_grupo)
        if cat not in grupos:
            continue
        val = a_numero(doc.get(campo_num))
        if val is None:
            continue
        grupos[cat].append(val)
    return {cat: vals for cat, vals in grupos.items() if len(vals) >= 2}


def cohens_d(a, b):
    """d de Cohen con desviación típica agrupada (pooled)."""
    n1, n2 = len(a), len(b)
    s1, s2 = np.var(a, ddof=1), np.var(b, ddof=1)
    sd_pooled = math.sqrt(((n1 - 1) * s1 + (n2 - 1) * s2) / (n1 + n2 - 2))
    if sd_pooled == 0:
        return float("nan")
    return (np.mean(a) - np.mean(b)) / sd_pooled


def interpretar_d(d):
    ad = abs(d)
    if ad < 0.2:
        return "despreciable"
    elif ad < 0.5:
        return "pequeño"
    elif ad < 0.8:
        return "medio"
    else:
        return "grande"


def eta_cuadrado(grupos):
    """η² = SS_entre / SS_total. Proporción de varianza explicada por el grupo."""
    todos = np.concatenate([np.asarray(v) for v in grupos.values()])
    media_global = todos.mean()
    ss_total = ((todos - media_global) ** 2).sum()
    if ss_total == 0:
        return float("nan")
    ss_entre = sum(len(v) * (np.mean(v) - media_global) ** 2 for v in grupos.values())
    return ss_entre / ss_total


def interpretar_eta2(e):
    if e < 0.01:
        return "despreciable"
    elif e < 0.06:
        return "pequeño"
    elif e < 0.14:
        return "medio"
    else:
        return "grande"


def welch_anova(grupos):
    """
    ANOVA de Welch: no asume varianzas iguales entre grupos.
    Devuelve (F, gl1, gl2, p) o None si no se puede calcular.

    Fórmula clásica de Welch (1951):
        w_j = n_j / s_j²                (peso de cada grupo)
        W   = Σ w_j
        x̄_w = (1/W) Σ w_j x̄_j          (media global ponderada)
        A   = Σ w_j (x̄_j − x̄_w)² / (k−1)
        Λ   = 3 Σ [(1 − w_j/W)² / (n_j−1)] / (k²−1)
        F   = A / (1 + 2Λ(k−2)/3)
        gl1 = k−1,  gl2 = 1/Λ
    """
    k = len(grupos)
    if k < 2:
        return None

    n = np.array([len(v) for v in grupos.values()], dtype=float)
    medias = np.array([np.mean(v) for v in grupos.values()], dtype=float)
    varianzas = np.array([np.var(v, ddof=1) for v in grupos.values()], dtype=float)

    if np.any(varianzas <= 0) or np.any(n < 2):
        return None      # algún grupo sin variabilidad: Welch no está definido

    w = n / varianzas
    W = w.sum()
    media_ponderada = (w * medias).sum() / W

    A = (w * (medias - media_ponderada) ** 2).sum() / (k - 1)
    lam = 3 * (((1 - w / W) ** 2 / (n - 1)).sum()) / (k ** 2 - 1)

    F = A / (1 + 2 * lam * (k - 2) / 3)
    gl1 = k - 1
    gl2 = 1 / lam
    p = f_dist.sf(F, gl1, gl2)
    return F, gl1, gl2, p


def tabla_descriptiva(grupos, etiqueta_grupo):
    md = ["| " + etiqueta_grupo + " | n | Media | Mediana | Desv. típica | Mín | Máx |",
          "|---|---:|---:|---:|---:|---:|---:|"]
    for cat, vals in grupos.items():
        v = np.asarray(vals)
        md.append(f"| {cat} | {len(v)} | {v.mean():.3f} | {np.median(v):.3f} | "
                   f"{v.std(ddof=1):.3f} | {v.min():.3f} | {v.max():.3f} |")
    return md


def post_hoc_dos_a_dos(grupos, etiqueta_grupo):
    """Comparaciones dos a dos (t de Welch) con corrección por múltiples tests."""
    md = []
    nombre_metodo = ("Bonferroni (FWER)" if METODO_CORRECCION == "bonferroni"
                     else "FDR / Benjamini-Hochberg")
    md.append(f"**Post-hoc — comparaciones dos a dos** (t de Welch, corrección: {nombre_metodo})\n")

    pares = list(combinations(grupos.keys(), 2))
    resultados = []
    for c1, c2 in pares:
        a, b = grupos[c1], grupos[c2]
        t, p = ttest_ind(a, b, equal_var=False)
        d = cohens_d(a, b)
        resultados.append((c1, c2, t, p, d))

    p_crudos = [r[3] for r in resultados]
    if p_crudos:
        rechazo, p_ajust, _, _ = multipletests(p_crudos, alpha=ALPHA, method=METODO_CORRECCION)
    else:
        rechazo, p_ajust = [], []

    md.append("| Par | Dif. de medias | p crudo | p ajustado | d de Cohen | Significativo |")
    md.append("|---|---:|---:|---:|---:|:---:|")
    for (c1, c2, t, p, d), sig, pa in zip(resultados, rechazo, p_ajust):
        dif = np.mean(grupos[c1]) - np.mean(grupos[c2])
        marca = "✅ sí" if sig else "no"
        md.append(f"| {c1} vs. {c2} | {dif:+.3f} | {p:.5f} | {pa:.5f} | {d:+.3f} | {marca} |")

    md.append("")
    md.append(f"> {len(pares)} comparaciones dos a dos; el p-valor ajustado es el que se "
               f"compara contra α = {ALPHA}.")
    md.append("")
    return md


def analizar(grupos, etiqueta_num, etiqueta_grupo, aviso=None):
    md = [f"### {etiqueta_num} × {etiqueta_grupo}\n"]

    if aviso:
        md.append(f"> ⚠ {aviso}\n")

    if len(grupos) < 2:
        md.append("> ⚠ No hay al menos 2 grupos con datos suficientes.\n")
        bloque = "\n".join(md)
        print(bloque)
        return bloque

    md += tabla_descriptiva(grupos, etiqueta_grupo)
    md.append("")

    valores = list(grupos.values())
    k = len(grupos)

    # Homocedasticidad (informativo: justifica usar Welch)
    try:
        stat_lev, p_lev = levene(*valores)
        md.append(f"**Homocedasticidad (Levene):** W = `{stat_lev:.4f}`, p = `{p_lev:.5f}` — "
                   f"las varianzas {'NO son' if p_lev < ALPHA else 'son'} homogéneas entre grupos"
                   f"{'; por eso se usa la variante de Welch como referencia' if p_lev < ALPHA else ''}.")
        md.append("")
    except Exception:
        pass

    if k == 2:
        # ─── t de Student (2 grupos) ─────────────────────────────────────────
        (c1, a), (c2, b) = list(grupos.items())

        t_w, p_w = ttest_ind(a, b, equal_var=False)   # Welch
        t_c, p_c = ttest_ind(a, b, equal_var=True)    # clásico
        d = cohens_d(a, b)

        md.append("**t de Student**\n")
        md.append(f"- Welch (no asume varianzas iguales): t = `{t_w:.4f}`, p = `{p_w:.5f}`")
        md.append(f"- Clásico (asume varianzas iguales): t = `{t_c:.4f}`, p = `{p_c:.5f}`")
        md.append(f"- Diferencia de medias ({c1} − {c2}) = `{np.mean(a) - np.mean(b):+.3f}`")
        md.append(f"- **Conclusión (Welch):** {'Hay' if p_w < ALPHA else 'No hay'} diferencia "
                   f"significativa de {etiqueta_num} entre {c1} y {c2} (α = {ALPHA})")
        md.append("")
        md.append("**Tamaño del efecto**\n")
        md.append(f"- d de Cohen = `{d:+.3f}` ({interpretar_d(d)})")
        md.append("")

    else:
        # ─── ANOVA (3+ grupos) ───────────────────────────────────────────────
        f_c, p_c = f_oneway(*valores)
        md.append(f"**ANOVA** (tabla de {k} grupos)\n")
        md.append(f"- Clásico: F = `{f_c:.4f}`, p = `{p_c:.5f}`")

        res_w = welch_anova(grupos)
        if res_w is not None:
            f_w, gl1, gl2, p_w = res_w
            md.append(f"- Welch: F = `{f_w:.4f}`, gl = `{gl1:.0f}, {gl2:.2f}`, p = `{p_w:.5f}`")
            p_ref, etiqueta_ref = p_w, "Welch"
        else:
            md.append("- Welch: no calculable (algún grupo sin variabilidad)")
            p_ref, etiqueta_ref = p_c, "clásico"

        md.append(f"- **Conclusión ({etiqueta_ref}):** {'Hay' if p_ref < ALPHA else 'No hay'} "
                   f"diferencia significativa de {etiqueta_num} entre los {k} grupos de "
                   f"{etiqueta_grupo} (α = {ALPHA})")
        md.append("")

        e2 = eta_cuadrado(grupos)
        md.append("**Tamaño del efecto**\n")
        md.append(f"- η² = `{e2:.4f}` ({interpretar_eta2(e2)}) — el grupo explica el "
                   f"{e2*100:.1f}% de la variabilidad de {etiqueta_num}")
        md.append("")

        if p_ref < ALPHA:
            md += post_hoc_dos_a_dos(grupos, etiqueta_grupo)
        else:
            md.append("> El ANOVA no es significativo: no se hacen comparaciones post-hoc.")
            md.append("")

    bloque = "\n".join(md)
    print(bloque)
    return bloque


def main():
    client = MongoClient(MONGO_URI)
    col = client[DB_NAME][COLECCION]

    proyeccion = {
        "Nota": 1,
        "Nº Contratos": 1,
        "Personal Contratado": 1,
        "Estado Solicitud": 1,
        "Género Solicitante": 1,
        "Centro de Investigación": 1,
        "ramaDep": 1,
    }
    docs = list(col.find({}, proyeccion))
    client.close()

    bloques = [
        "# Comparación de medias — variables numéricas vs. categóricas\n",
        f"_Generado el {datetime.now().strftime('%Y-%m-%d %H:%M')}_\n",
        (
            "> Nota metodológica: se comparan las medias de las variables NUMÉRICAS "
            "(Nota, Nº Contratos) entre los grupos de cada variable CATEGÓRICA. "
            "Con 2 grupos se usa el **t de Student**; con 3 o más, **ANOVA** (que es "
            "su generalización). Ambos en variante de **Welch**, que no asume varianzas "
            "iguales — prudente aquí porque los grupos tienen tamaños muy dispares. "
            "El ANOVA es un test global (dice que hay diferencia, no dónde), así que "
            "cuando sale significativo se añaden comparaciones **dos a dos** con "
            f"corrección por múltiples tests (método: {METODO_CORRECCION}). Se reporta "
            "el tamaño del efecto (**d de Cohen** con 2 grupos, **η²** con 3+) porque el "
            "p-valor dice si la diferencia es real, no si es relevante.\n"
        ),
    ]

    for campo_num, etiq_num, filtro_estado in VARIABLES_NUMERICAS:
        bloques.append(f"## {etiq_num}\n")

        if filtro_estado:
            docs_num = [d for d in docs if d.get("Estado Solicitud") == filtro_estado]
            bloques.append(
                f"> Filtrado a solicitudes con Estado = **{filtro_estado}** "
                f"(n = {len(docs_num)}): fuera de ahí esta variable está a 0 por "
                f"definición, así que incluir el resto sería circular.\n"
            )
        else:
            docs_num = docs

        for campo_grp, etiq_grp, categorias in VARIABLES_GRUPO:
            # Si la numérica ya está filtrada por Estado, cruzarla con Estado no aporta
            if filtro_estado and campo_grp == "Estado Solicitud":
                continue

            aviso = None
            if campo_num == "Nota" and campo_grp == "Estado Solicitud":
                aviso = ("Si el procedimiento consiste en ordenar por nota y aceptar de "
                         "arriba abajo, este test saldrá significativo POR CONSTRUCCIÓN: "
                         "confirma el procedimiento, no es un hallazgo.")

            grupos = extraer_grupos(docs_num, campo_num, campo_grp, categorias)
            bloques.append(analizar(grupos, etiq_num, etiq_grp, aviso=aviso))

    with open(OUTPUT_MD, "w", encoding="utf-8") as f:
        f.write("\n".join(bloques))

    print(f"\n✓ Resultados guardados en: {OUTPUT_MD}")


if __name__ == "__main__":
    main()