import csv
import re

# ── CONFIG ──────────────────────────────────────────────────────────────────
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent

ESTADO_SOLICITUD = "Suplente"
INPUT_FILE  = BASE_DIR / "../../data/raw/csv/CSV_2018/anexo2_2018.csv"
OUTPUT_FILE = BASE_DIR / "../../data/clean/CSV_2018_CLEAN/anexo_suplentes_2018.csv"
# ────────────────────────────────────────────────────────────────────────────

CAMPOS_SALIDA = [
    "Referencia", "Solicitante", "Género Solicitante", "DNI", "Nº Petición",
    "Centro de Investigación", "CIF", "Nota", "Descripción", "Rama",
    "Cantidad Total", "Año Inicio", "Año1", "Año2", "Año3", "Año4", "Año5",
    "Estado Solicitud"
]


def parsear_perceptor(perceptor):
    """
    Formato: 'APELLIDOS, NOMBRE, NNNN (CENTRO, CIF)'
    Ej: 'GUERRERO ARROYO, CARMEN, 9827 (UNIVERSIDAD DE SALAMANCA, Q3718001E)'
    El número de 4 dígitos son los dígitos centrales del DNI censurado.
    """
    patron = r"^(.+?),\s*(\d+)\s*\((.+?),\s*([A-Z0-9]+)\)$"
    m = re.match(patron, perceptor.strip())
    if m:
        digitos_dni = m.group(2).strip()
        return {
            "Solicitante": m.group(1).strip(),
            "DNI": f"***{digitos_dni}**",
            "Centro de Investigación": m.group(3).strip(),
            "CIF": m.group(4).strip(),
        }
    return {
        "Solicitante": "",
        "DNI": "",
        "Centro de Investigación": "",
        "CIF": "",
    }


def num_es(valor):
    """Convierte '7,65' -> 7.65 (float). Vacío -> ''"""
    valor = (valor or "").strip()
    if not valor:
        return ""
    return float(valor.replace(".", "").replace(",", "."))


with open(INPUT_FILE, newline="", encoding="utf-8") as f_in:
    reader = csv.DictReader(f_in)
    rows_out = []

    for row in reader:
        campos = parsear_perceptor(row["Perceptor (Solicitante)"])

        row_out = {
            "Referencia":              "",
            "Solicitante":             campos["Solicitante"],
            "Género Solicitante":      "",
            "DNI":                     campos["DNI"],
            "Nº Petición":             "",
            "Centro de Investigación": campos["Centro de Investigación"],
            "CIF":                     campos["CIF"],
            "Nota":                    num_es(row["Puntuación"]),
            "Descripción":             row["Finalidad"],
            "Rama":                    "",
            "Cantidad Total":          "",
            "Año Inicio":              "",
            "Año1":                    "",
            "Año2":                    "",
            "Año3":                    "",
            "Año4":                    "",
            "Año5":                    "",
            "Estado Solicitud":        ESTADO_SOLICITUD,
        }

        rows_out.append(row_out)

with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as f_out:
    writer = csv.DictWriter(f_out, fieldnames=CAMPOS_SALIDA)
    writer.writeheader()
    writer.writerows(rows_out)

print(f"Listo → {OUTPUT_FILE}")