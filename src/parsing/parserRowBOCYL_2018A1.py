import csv
import re

# ── CONFIG ──────────────────────────────────────────────────────────────────
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent

ESTADO_SOLICITUD = "Aceptada"   # no viene en este CSV, se fija por config
INPUT_FILE  = BASE_DIR / "../../data/raw/csv/CSV_2018/anexo1_2018_completo.csv"
OUTPUT_FILE = BASE_DIR / "../../data/clean/CSV_2018_CLEAN/anexo1_2018.csv"
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
    Ej: 'TORROBA PÉREZ, TOMÁS, 3812 (UNIVERSIDAD DE BURGOS, Q0968272E)'
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
    """Convierte '120.000,00' -> 120000.00 (float). Vacío -> ''"""
    valor = (valor or "").strip()
    if not valor:
        return ""
    return float(valor.replace(".", "").replace(",", "."))


def detectar_columnas_anio(fieldnames):
    """Devuelve las columnas de año (4 dígitos) ordenadas ascendentemente."""
    anios = [f for f in fieldnames if re.fullmatch(r"\d{4}", f.strip())]
    return sorted(anios, key=int)


with open(INPUT_FILE, newline="", encoding="utf-8") as f_in:
    reader = csv.DictReader(f_in)
    columnas_anio = detectar_columnas_anio(reader.fieldnames)
    anio_inicio = int(columnas_anio[0]) if columnas_anio else ""

    rows_out = []

    for row in reader:
        campos = parsear_perceptor(row["Perceptor (Beneficiario)"])

        # Mapea cada columna de año detectada a Año1..Año5 en orden
        anios_valores = {}
        for i, col_anio in enumerate(columnas_anio[:5], start=1):
            anios_valores[f"Año{i}"] = num_es(row.get(col_anio, ""))
        for i in range(len(columnas_anio) + 1, 6):
            anios_valores[f"Año{i}"] = ""

        row_out = {
            "Referencia":              row["Referencia"],
            "Solicitante":             campos["Solicitante"],
            "Género Solicitante":      "",
            "DNI":                     campos["DNI"],
            "Nº Petición":             "",
            "Centro de Investigación": campos["Centro de Investigación"],
            "CIF":                     campos["CIF"],
            "Nota":                    num_es(row["Puntuación"]),
            "Descripción":             row["Finalidad"],
            "Rama":                    "",
            "Cantidad Total":          num_es(row["Cantidad total"]),
            "Año Inicio":              anio_inicio,
            **anios_valores,
            "Estado Solicitud":        ESTADO_SOLICITUD,
        }

        rows_out.append(row_out)

with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as f_out:
    writer = csv.DictWriter(f_out, fieldnames=CAMPOS_SALIDA)
    writer.writeheader()
    writer.writerows(rows_out)

print(f"Listo → {OUTPUT_FILE}")