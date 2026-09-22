import csv
import re

# ── CONFIG ──────────────────────────────────────────────────────────────────
AÑO_INICIO = 2024
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent

ESTADO_SOLICITUD = "Suplente"
INPUT_FILE  = BASE_DIR / "../../data/raw/csv/CSV_2023/anexo3_2023_completo.csv"
OUTPUT_FILE = BASE_DIR / "../../data/clean/CSV_2023_CLEAN/anexo3_2023_completo.csv"
# ────────────────────────────────────────────────────────────────────────────

def parsear_peticion(peticion):
    patron = r"^(.*?)\s(\*+\d+\*+)\s\(Petición nº\s*(\d+)\s*,\s*(.*?)\s*,\s*([A-Z0-9]+)\)$"
    m = re.match(patron, peticion.strip())
    if not m:
        return {
            "Solicitante": "",
            "DNI": "",
            "Nº Petición": "",
            "Centro de Investigación": "",
            "CIF": "",
        }

    nombre_raw = m.group(1).strip()   # ej: "TORROBA PÉREZ, TOMÁS" o "PARES , JOSEP"
    dni = m.group(2).strip()
    num_peticion = m.group(3).strip()
    centro = m.group(4).strip().title()
    cif = m.group(5).strip()

    # Reordenar "APELLIDOS, NOMBRE" -> "Nombre Apellidos"
    if "," in nombre_raw:
        partes = [p.strip() for p in nombre_raw.split(",", 1)]
        solicitante = f"{partes[1]} {partes[0]}".strip().title()
    else:
        solicitante = nombre_raw.title()

    return {
        "Solicitante": solicitante,
        "DNI": dni,
        "Nº Petición": num_peticion,
        "Centro de Investigación": centro,
        "CIF": cif,
    }

with open(INPUT_FILE, newline="", encoding="utf-8") as f_in:
    reader = csv.DictReader(f_in)
    rows_out = []

    for row in reader:
        campos = parsear_peticion(row["Petición"])

        row_out = {
            "Referencia":              row["Referencia"],
            "Solicitante":             campos["Solicitante"],
            "Género Solicitante":      "",
            "DNI":                     campos["DNI"],
            "Nº Petición":             campos["Nº Petición"],
            "Centro de Investigación": campos["Centro de Investigación"],
            "CIF":                     campos["CIF"],
            "Nota":                    float(row["Puntuación"].replace(",", ".")),
            "Descripción":             row["Descripción"],
            "Rama":                    "",
            "Cantidad Total":          "",
            "Año Inicio":              AÑO_INICIO,
            "Año1":                    "",
            "Año2":                    "",
            "Año3":                    "",
            "Año4":                    "",
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