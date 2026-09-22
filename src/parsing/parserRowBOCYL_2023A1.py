import csv
import re

# ── CONFIG ──────────────────────────────────────────────────────────────────
AÑO_INICIO = 2024
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent

ESTADO_SOLICITUD = "Aceptada"
INPUT_FILE  = BASE_DIR / "../../data/raw/csv/CSV_2023/anexo1_2023_completo.csv"
OUTPUT_FILE = BASE_DIR / "../../data/clean/CSV_2023_CLEAN/anexo1_2023_completo.csv"
# ────────────────────────────────────────────────────────────────────────────

def parsear_peticion(peticion):
    patron = r"^(.+?)\s(\*+\d+\*+)\s\(Petición nº (\d+) de[l]? (.+?),\s([A-Z0-9]+)\)$"
    m = re.match(patron, peticion.strip())
    if m:
        return {
            "Solicitante": m.group(1).strip().title(),
            "DNI": m.group(2).strip(),
            "Nº Petición": m.group(3).strip(),
            "Centro de Investigación": m.group(4).strip(),
            "CIF": m.group(5).strip(),
        }
    return {
        "Solicitante": "",
        "DNI": "",
        "Nº Petición": "",
        "Centro de Investigación": "",
        "CIF": "",
    }

def limpiar_numero(valor):
    return valor.replace(".", "").replace(",", ".")

with open(INPUT_FILE, newline="", encoding="utf-8") as f_in:
    reader = csv.DictReader(f_in)
    rows_out = []

    for row in reader:
        campos = parsear_peticion(row["Petición"])
        años_origen = ["2024", "2025", "2026", "2027"]

        row_out = {
            "Referencia":              row["Referencia"],
            "Solicitante":             campos["Solicitante"],
            "Género Solicitante":      "",
            "DNI":                     campos["DNI"],
            "Nº Petición":             campos["Nº Petición"],
            "Centro de Investigación": campos["Centro de Investigación"],
            "CIF":                     campos["CIF"],
            "Nota":                    float(row["Puntuación"].replace(",", ".")),
            "Descripción":             row["Finalidad"],
            "Rama":                    "",
            "Cantidad Total":          limpiar_numero(row["Cantidad total"]),
            "Año Inicio":              AÑO_INICIO,
            "Año1":                    limpiar_numero(row[años_origen[0]]),
            "Año2":                    limpiar_numero(row[años_origen[1]]),
            "Año3":                    limpiar_numero(row[años_origen[2]]),
            "Año4":                    limpiar_numero(row[años_origen[3]]),
            "Año5":                    "",
            "Estado Solicitud":        ESTADO_SOLICITUD,
        }

        rows_out.append(row_out)

campos_salida = [
    "Referencia", "Solicitante", "Género Solicitante", "DNI", "Nº Petición",
    "Centro de Investigación", "CIF", "Nota", "Descripción", "Rama",
    "Cantidad Total", "Año Inicio", "Año1", "Año2", "Año3", "Año4", "Año5",
    "Estado Solicitud"
]

with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as f_out:
    writer = csv.DictWriter(f_out, fieldnames=campos_salida)
    writer.writeheader()
    writer.writerows(rows_out)

print(f"Listo → {OUTPUT_FILE}")