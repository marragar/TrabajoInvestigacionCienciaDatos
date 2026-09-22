import csv
import re

# ── CONFIG ──────────────────────────────────────────────────────────────────
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent

ESTADO_SOLICITUD = "Aceptada"
INPUT_FILE  = BASE_DIR / "../../data/raw/csv/CSV_2017/anexo1_2017_completo.csv"
OUTPUT_FILE = BASE_DIR / "../../data/clean/CSV_2017_CLEAN/anexo1_2017.csv"
# ────────────────────────────────────────────────────────────────────────────

CAMPOS_SALIDA = [
    "Referencia", "Solicitante", "Género Solicitante", "DNI", "Nº Petición",
    "Centro de Investigación", "CIF", "Nota", "Descripción", "Rama",
    "Cantidad Total", "Año Inicio", "Año1", "Año2", "Año3", "Año4", "Año5",
    "Estado Solicitud"
]

# Posiciones fijas por columna (la cabecera viene corrupta por el OCR)
COL_REFERENCIA   = 1
COL_PERCEPTOR    = 2
COL_PUNTUACION   = 3
COL_DESCRIPCION  = 4
COL_CANTIDAD     = 5
COL_ANIOS        = [6, 7, 8]  # 2017, 2018, 2019 en este anexo


def parsear_perceptor(perceptor):
    """
    Formato: 'APELLIDOS, NOMBRE, DNI (CENTRO, CIF)'
    Ej: 'RODRÍGUEZ OLIVERA, ELÍAS, 13121758M (UNIVERSIDAD DE LEÓN, Q2432001B)'
    Aquí el DNI viene completo, sin censurar.
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


def num_es_sucio(valor):
    """
    Extrae el primer número con formato español (miles con '.', decimales con ',')
    de un campo potencialmente contaminado con texto OCR pegado.
    Ej: '120.000,00 DIDAS' -> 120000.00 | '8,2 SU' -> 8.2
    """
    if not valor:
        return ""
    valor = valor.strip()
    m = re.search(r"\d{1,3}(?:\.\d{3})*,\d+|\d+,\d+", valor)
    if not m:
        return ""
    return float(m.group(0).replace(".", "").replace(",", "."))


def limpiar_descripcion(texto):
    """Elimina restos de OCR pegados (ej. 'BVENCIONES CONCE' insertado a media palabra)."""
    return texto.strip()


with open(INPUT_FILE, newline="", encoding="utf-8") as f_in:
    reader = csv.reader(f_in)
    header = next(reader)  # descartamos cabecera, es posicional

    # Años reales según la cabecera original (para Año Inicio)
    anios_header = [h.strip() for h in header if re.fullmatch(r"\d{4}", h.strip())]
    anio_inicio = int(anios_header[0]) if anios_header else ""

    rows_out = []

    for row in reader:
        if len(row) <= max(COL_ANIOS + [COL_CANTIDAD, COL_DESCRIPCION]):
            continue  # fila incompleta/corrupta, se salta

        campos = parsear_perceptor(row[COL_PERCEPTOR])

        anios_valores = {}
        for i, col in enumerate(COL_ANIOS, start=1):
            anios_valores[f"Año{i}"] = num_es_sucio(row[col])
        for i in range(len(COL_ANIOS) + 1, 6):
            anios_valores[f"Año{i}"] = ""

        row_out = {
            "Referencia":              row[COL_REFERENCIA].strip(),
            "Solicitante":             campos["Solicitante"],
            "Género Solicitante":      "",
            "DNI":                     campos["DNI"],
            "Nº Petición":             "",
            "Centro de Investigación": campos["Centro de Investigación"],
            "CIF":                     campos["CIF"],
            "Nota":                    num_es_sucio(row[COL_PUNTUACION]),
            "Descripción":             limpiar_descripcion(row[COL_DESCRIPCION]),
            "Rama":                    "",
            "Cantidad Total":          num_es_sucio(row[COL_CANTIDAD]),
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