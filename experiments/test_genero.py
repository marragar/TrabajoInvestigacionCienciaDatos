"""
Test de independencia entre Género Solicitante y Estado de Solicitud
(Aceptada / Suplente).

Como la tabla es 2x2 (Masculino/Femenino x Aceptada/Suplente), el test
EXACTO de Fisher de scipy se aplica directamente a la tabla completa.
Se calculan: chi-cuadrado de independencia y Fisher exacto (scipy).
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
COLECCION  = "Solicitudes"
OUTPUT_MD  = "test_genero.md"
# ──────────────────────────────────────────────────────────────────────────────

GENEROS = ["Masculino", "Femenino"]
ESTADOS = ["Aceptada", "Suplente"]
N_REPLICAS_MC = 100_000


def construir_tabla(docs):
    tabla = pd.DataFrame(0, index=GENEROS, columns=ESTADOS)
    for doc in docs:
        genero = doc.get("Género Solicitante")
        estado = doc.get("Estado Solicitud")
        if genero in GENEROS and estado in ESTADOS:
            tabla.loc[genero, estado] += 1
    return tabla


def fisher_exacto_tabla_completa(tabla, n_replicas=N_REPLICAS_MC):
    """
    Aplica el test exacto de Fisher a la tabla RxC completa usando R (rpy2).
    Versión robusta para Windows que evita problemas de carga de librerías.
    
    Devuelve (p_valor, metodo) o (None, mensaje_error).
    """
    try:
        import os
        # Añadir bin\x64 de R al PATH ANTES de importar rpy2. Es habitual en
        # Windows que R_HOME esté bien configurado pero la carpeta bin\x64
        # (donde vive R.dll y otras DLLs de las que dependen los paquetes,
        # como stats.dll) no esté en el PATH, causando "LoadLibrary failure".
        r_home = os.environ.get("R_HOME", r"C:\Program Files\R\R-4.6.1")
        r_bin = os.path.join(r_home, "bin", "x64")
        if os.path.isdir(r_bin) and r_bin not in os.environ.get("PATH", ""):
            os.environ["PATH"] = r_bin + os.pathsep + os.environ.get("PATH", "")

        import rpy2.robjects as robjects
        from rpy2.rinterface_lib.callbacks import logger as rpy2_logger
        import logging
    except ImportError:
        return None, "rpy2 no está instalado (pip install rpy2, y R en el sistema)"

    try:
        # Suprimir warnings de R que causan UnicodeDecodeError en Windows
        rpy2_logger.setLevel(logging.ERROR)
        
        # Silenciar mensajes de inicio de R
        robjects.r('options(warn=-1)')
        
        # Forzar carga explícita de 'stats' (a veces no se carga por defecto
        # en Windows si hay conflictos de PATH/DLL, p.ej. con conda)
        try:
            robjects.r('suppressWarnings(suppressMessages(library(stats)))')
        except Exception as e_lib:
            return None, (f"no se pudo cargar el paquete 'stats' de R: {str(e_lib)[:200]} "
                           f"— revisa si conda está interfiriendo con el PATH de R "
                           f"(ejecuta 'where R' y 'where Rscript' para comprobarlo)")
        
        # Ejecutar fisher.test directamente via código R como string
        valores = tabla.values.flatten(order="F").tolist()
        nrow = tabla.shape[0]
        ncol = tabla.shape[1]
        
        # Construir código R que intenta exacto, y si falla, usa simulación
        r_code = f"""
        suppressWarnings({{
            m <- matrix(c({', '.join(map(str, valores))}), nrow={nrow}, ncol={ncol})
            tryCatch({{
                result <- stats::fisher.test(m, simulate.p.value=FALSE)
                list(p_val=result$p.value, metodo="exacto")
            }}, error = function(e) {{
                result <- stats::fisher.test(m, simulate.p.value=TRUE, B={n_replicas})
                list(p_val=result$p.value, metodo="simulado")
            }})
        }})
        """
        
        resultado = robjects.r(r_code)
        p_valor = float(resultado.rx2("p_val")[0])
        metodo = str(resultado.rx2("metodo")[0])
        
        if metodo == "simulado":
            metodo = f"simulado (Monte Carlo, B={n_replicas})"
        
        return p_valor, metodo

    except Exception as e:
        return None, f"error al ejecutar R: {str(e)[:150]}"


def test_tabla(tabla, etiqueta):
    md = [f"## {etiqueta}\n"]

    md.append("| Género | Aceptada | Suplente | Total |")
    md.append("|---|---:|---:|---:|")
    for genero in GENEROS:
        acept = tabla.loc[genero, "Aceptada"]
        supl  = tabla.loc[genero, "Suplente"]
        md.append(f"| {genero} | {acept} | {supl} | {acept + supl} |")
    total = tabla.values.sum()
    md.append(f"| **Total** | **{tabla['Aceptada'].sum()}** | "
               f"**{tabla['Suplente'].sum()}** | **{total}** |")
    md.append("")

    if (total == 0) or (tabla.sum(axis=1) == 0).any():
        md.append("> ⚠ No hay datos suficientes para el test en este subconjunto.\n")
        bloque = "\n".join(md)
        print(bloque)
        return bloque

    # Chi-cuadrado
    chi2, p_chi2, dof, esperado = chi2_contingency(tabla)
    sig_chi2 = p_chi2 < 0.05

    md.append("**Chi-cuadrado de independencia**")
    md.append("")
    md.append(f"- χ² = `{chi2:.4f}`")
    md.append(f"- gl = `{dof}`")
    md.append(f"- p-valor = `{p_chi2:.5f}`")
    md.append(f"- **Conclusión:** {'Hay' if sig_chi2 else 'No hay'} asociación "
               f"significativa entre Género y Estado (α = 0.05)")

    if (esperado < 5).any():
        md.append("")
        md.append("> ⚠ Alguna celda esperada < 5: el chi-cuadrado puede no ser fiable, "
                   "usa el p-valor de Fisher como referencia principal.")

    # Fisher exacto (tabla 2x2 directa, scipy)
    tabla_2x2 = [
        [tabla.loc["Masculino", "Aceptada"], tabla.loc["Masculino", "Suplente"]],
        [tabla.loc["Femenino",  "Aceptada"], tabla.loc["Femenino",  "Suplente"]],
    ]
    odds_ratio, p_fisher = fisher_exact(tabla_2x2)
    sig_fisher = p_fisher < 0.05

    md.append("")
    md.append("**Test exacto de Fisher (scipy)**")
    md.append("")
    md.append(f"- p-valor = `{p_fisher:.5f}`")
    md.append(f"- Odds Ratio = `{odds_ratio:.3f}`")
    md.append(f"- **Conclusión:** {'Hay' if sig_fisher else 'No hay'} asociación "
               f"significativa entre Género y Estado (α = 0.05)")

    # Fisher exacto sobre la tabla completa (vía R) — verificación cruzada
    p_fisher_r, metodo_r = fisher_exacto_tabla_completa(tabla)
    md.append("")
    md.append("**Test exacto de Fisher — tabla completa (vía R / rpy2)**")
    md.append("")
    if p_fisher_r is None:
        md.append(f"> ⚠ No se pudo calcular: {metodo_r}")
    else:
        sig_r = p_fisher_r < 0.05
        md.append(f"- p-valor = `{p_fisher_r:.5f}` (método: {metodo_r})")
        md.append(f"- **Conclusión:** {'Hay' if sig_r else 'No hay'} asociación "
                   f"significativa entre Género y Estado (α = 0.05)")

    # Proporciones de aceptación por género, para contexto
    md.append("")
    md.append("**% de aceptación por género**")
    md.append("")
    for genero in GENEROS:
        acept = tabla.loc[genero, "Aceptada"]
        tot_g = tabla.loc[genero].sum()
        pct   = (acept / tot_g * 100) if tot_g > 0 else 0
        md.append(f"- {genero}: {pct:.1f}% ({acept}/{tot_g})")

    md.append("")

    bloque = "\n".join(md)
    print(bloque)
    return bloque


def main():
    client = MongoClient(MONGO_URI)
    col    = client[DB_NAME][COLECCION]

    proyeccion = {"Año Inicio": 1, "Género Solicitante": 1, "Estado Solicitud": 1}
    docs = list(col.find({"Género Solicitante": {"$in": GENEROS}}, proyeccion))
    client.close()

    bloques_md = [
        "# Test de independencia — Género Solicitante vs. Estado de Solicitud\n",
        f"_Generado el {datetime.now().strftime('%Y-%m-%d %H:%M')}_\n",
        (
            "> Nota metodológica: al ser una tabla 2×2 (Masculino/Femenino × "
            "Aceptada/Suplente), el test exacto de Fisher se aplica directamente "
            "sobre la tabla completa (scipy), junto con el chi-cuadrado de independencia "
            "y una verificación cruzada del Fisher exacto vía R (rpy2).\n"
        ),
    ]

    # General
    tabla_general = construir_tabla(docs)
    bloques_md.append(test_tabla(tabla_general, "GENERAL — Todos los años"))

    # Por año
    años = sorted({d.get("Año Inicio") for d in docs if d.get("Año Inicio")})
    for año in años:
        docs_año = [d for d in docs if d.get("Año Inicio") == año]
        tabla_año = construir_tabla(docs_año)
        bloques_md.append(test_tabla(tabla_año, f"AÑO {año}"))

    with open(OUTPUT_MD, "w", encoding="utf-8") as f:
        f.write("\n".join(bloques_md))

    print(f"\n✓ Resultados guardados en: {OUTPUT_MD}")


if __name__ == "__main__":
    main()
