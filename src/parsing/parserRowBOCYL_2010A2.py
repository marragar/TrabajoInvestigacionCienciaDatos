import csv
import re

# ── CONFIG ──────────────────────────────────────────────────────────────────
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent

ESTADO_SOLICITUD = "Suplente"
INPUT_FILE  = BASE_DIR / "../../data/raw/csv/CSV_2010/anexo2_2010_completo.csv"
OUTPUT_FILE = BASE_DIR / "../../data/clean/CSV_2010_CLEAN/anexo2_2010.csv"
# ────────────────────────────────────────────────────────────────────────────

CAMPOS_SALIDA = [
    "Referencia", "Solicitante", "Género Solicitante", "DNI", "Nº Petición",
    "Centro de Investigación", "CIF", "Nota", "Descripción", "Rama",
    "Cantidad Total", "Año Inicio", "Año1", "Año2", "Año3", "Año4", "Año5",
    "Estado Solicitud"
]


def parsear_perceptor(perceptor):
    """
    Formato: 'APELLIDOS, NOMBRE, DNI/NIE (CENTRO, CIF)'
    DNI: 8 dígitos + letra. NIE (extranjeros): letra (X/Y/Z) + 7 dígitos + letra.
    Ej DNI: 'HERRERO GARCÍA, MARÍA JOSÉ, 07762087R (UNIVERSIDAD DE SALAMANCA, Q3718001E)'
    Ej NIE: 'ROJAS SPANO, MARÍA JIMENA, X6192558S (UNIVERSIDAD DE VALLADOLID, Q4718001C)'
    """
    patron = r"^(.+?),\s*([XYZxyz]?\d{6,8}[A-Za-z]?)\s*\((.+),\s*([A-Z0-9]+)\)$"
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
    Extrae el primer número de un campo, tolerando basura OCR pegada.
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
        campos = parsear_perceptor(row["Solicitante (Perceptor)"])

        nota_100 = num_es(row["Punt."])
        nota_10 = round(nota_100 / 10, 3) if nota_100 != "" else ""

        row_out = {
            "Referencia":              "",
            "Solicitante":             campos["Solicitante"],
            "Género Solicitante":      "",
            "DNI":                     campos["DNI"],
            "Nº Petición":             "",
            "Centro de Investigación": campos["Centro de Investigación"],
            "CIF":                     campos["CIF"],
            "Nota":                    nota_10,
            "Descripción":             row["Descripción: Org. Públicos Línea 1"].strip(),
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