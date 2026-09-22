import csv
import re

# ── CONFIG ──────────────────────────────────────────────────────────────────
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent

ESTADO_SOLICITUD = "Aceptada"
INPUT_FILE  = BASE_DIR / "../../data/raw/csv/CSV_2014/anexo1_2014_completo.csv"
OUTPUT_FILE = BASE_DIR / "../../data/clean/CSV_2014_CLEAN/anexo1_2014.csv"
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
    Ej: 'SÁNCHEZ GARCÍA, ISIDRO JAVIER, 07844538C (C.S.I.C., Q2818002D)'
    DNI completo, sin censurar. Tolera centros con paréntesis anidados.
    """
    patron = r"^(.+?),\s*(\d{6,8}[A-Za-z]?)\s*\((.+),\s*([A-Z0-9]+)\)$"
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

        anios_valores = {}
        for i, col_anio in enumerate(columnas_anio[:5], start=1):
            anios_valores[f"Año{i}"] = num_es(row.get(col_anio, ""))
        for i in range(len(columnas_anio) + 1, 6):
            anios_valores[f"Año{i}"] = ""

        nota_100 = num_es(row["Puntuación"])
        nota_10 = round(nota_100 / 10, 3) if nota_100 != "" else ""

        row_out = {
            "Referencia":              row["Referencia"].strip(),
            "Solicitante":             campos["Solicitante"],
            "Género Solicitante":      "",
            "DNI":                     campos["DNI"],
            "Nº Petición":             "",
            "Centro de Investigación": campos["Centro de Investigación"],
            "CIF":                     campos["CIF"],
            "Nota":                    nota_10,
            "Descripción":             row["Descripción: Organismos públicos"].strip(),
            "Rama":                    "",
            "Cantidad Total":          num_es(row["Cantidad"]),
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