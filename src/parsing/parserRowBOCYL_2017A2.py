import csv
import re

# ── CONFIG ──────────────────────────────────────────────────────────────────
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent

ESTADO_SOLICITUD = "Suplente"
INPUT_FILE  = BASE_DIR / "../../data/raw/csv/CSV_2017/anexo2_2017.csv"
OUTPUT_FILE = BASE_DIR / "../../data/clean/CSV_2017_CLEAN/anexo2_2017.csv"
# ────────────────────────────────────────────────────────────────────────────

CAMPOS_SALIDA = [
    "Referencia", "Solicitante", "Género Solicitante", "DNI", "Nº Petición",
    "Centro de Investigación", "CIF", "Nota", "Descripción", "Rama",
    "Cantidad Total", "Año Inicio", "Año1", "Año2", "Año3", "Año4", "Año5",
    "Estado Solicitud"
]


def parsear_perceptor(perceptor):
    """
    Formato: 'APELLIDOS, NOMBRE, DNI (CENTRO, CIF)'
    Ej: 'BARRIENTOS BENITO, MARÍA CARMEN, 12361445A (UNIVERSIDAD DE VALLADOLID, Q4718001C)'
    DNI completo, sin censurar.
    """
    patron = r"^(.+?),\s*(\d{6,8}[A-Za-z]?)\s*\((.+?),\s*([A-Z0-9]+)\)$"
    m = re.match(patron, perceptor.strip())
    if m:
        return {
            "Solicitante": m.group(1).strip(),
            "DNI": m.group(2).strip().upper(),
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
    """
    Extrae el primer número de un campo potencialmente contaminado
    con texto OCR pegado (ej. 'SUB', 'DIDAS', etc.)
    Prioriza formato español con decimales (12,34); si no hay coma,
    coge el primer número que encuentre.
    """
    valor = (valor or "").strip()
    if not valor:
        return ""
    m = re.search(r"\d{1,3}(?:\.\d{3})*,\d+", valor)
    if m:
        return float(m.group(0).replace(".", "").replace(",", "."))
    m = re.search(r"\d+(?:[.,]\d+)?", valor)
    if m:
        return float(m.group(0).replace(",", "."))
    return ""


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
            "Descripción":             row["Descripción: Finalidades denegadas"],
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