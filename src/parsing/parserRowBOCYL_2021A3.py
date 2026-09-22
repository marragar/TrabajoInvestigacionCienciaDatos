import csv
import re

# ── CONFIG ──────────────────────────────────────────────────────────────────
AÑO_INICIO = 2021
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent

ESTADO_SOLICITUD = "Suplente" 
INPUT_FILE  = BASE_DIR / "../../data/raw/csv/CSV_2021/anexo3_2021_completo.csv"
OUTPUT_FILE = BASE_DIR / "../../data/clean/CSV_2021_CLEAN/anexo3_2021_completo.csv"
ERRORES_FILE = BASE_DIR / "proyectos_investigacion_no_parseados.csv"
# ────────────────────────────────────────────────────────────────────────────

def limpiar_numero(valor):
    if valor is None:
        return ""
    v = str(valor).strip().replace('"', '')
    if not v:
        return ""
    return v.replace(".", "").replace(",", ".")

def parsear_peticion(peticion):
    vacio = {
        "Solicitante": "",
        "DNI": "",
        "Nº Petición": "",
        "Centro de Investigación": "",
        "CIF": "",
    }
    if not peticion:
        return vacio

    s = peticion.strip().strip('"').rstrip(".").strip()

    # Acepta con o sin coma antes del DNI
    m = re.match(
        r"^(?P<nombre>.+?)(?:,\s*|\s+)(?P<dni>\*+\d+\*+)\s*\((?P<resto>Petición.+)\)$",
        s,
        flags=re.IGNORECASE
    )
    if not m:
        return vacio

    nombre_raw = m.group("nombre").strip().strip(",")
    dni = m.group("dni").strip()
    resto = m.group("resto").strip()

    # Nº petición
    m_num = re.search(r"Petición\s+n[.\s]*[ºo]\s*(\d+)", resto, flags=re.IGNORECASE)
    num = m_num.group(1) if m_num else ""

    # CIF final
    m_cif = re.search(r"([A-Z]\d{7}[A-Z0-9])\s*$", resto, flags=re.IGNORECASE)
    cif = m_cif.group(1).upper() if m_cif else ""

    # Centro
    centro = resto
    if num:
        m_pos = re.search(rf"Petición\s+n[.\s]*[ºo]\s*{re.escape(num)}", resto, flags=re.IGNORECASE)
        if m_pos:
            centro = resto[m_pos.end():]

    if cif:
        centro = re.sub(rf"{re.escape(cif)}\s*$", "", centro, flags=re.IGNORECASE)

    centro = centro.strip(" .,:;")
    centro = re.sub(r"^(del|de)\s+", "", centro, flags=re.IGNORECASE).strip()
    centro = re.sub(r"\s+", " ", centro).strip().title()

    # "APELLIDOS, NOMBRE" -> "Nombre Apellidos"
    if "," in nombre_raw:
        apellidos, nombre = [p.strip() for p in nombre_raw.split(",", 1)]
        solicitante = f"{nombre} {apellidos}".strip().title()
    else:
        solicitante = nombre_raw.title()

    return {
        "Solicitante": solicitante,
        "DNI": dni,
        "Nº Petición": num,
        "Centro de Investigación": centro,
        "CIF": cif,
    }

campos_salida = [
    "Referencia", "Solicitante", "Género Solicitante", "DNI", "Nº Petición",
    "Centro de Investigación", "CIF", "Nota", "Descripción", "Rama",
    "Cantidad Total", "Año Inicio", "Año1", "Año2", "Año3", "Año4", "Año5",
    "Estado Solicitud"
]

rows_out = []
no_parseadas = []

with open(INPUT_FILE, newline="", encoding="utf-8-sig") as f_in:
    reader = csv.DictReader(f_in)
    for row in reader:
        campos = parsear_peticion(row.get("Petición", ""))

        if not campos["Solicitante"] and (row.get("Petición", "") or "").strip():
            no_parseadas.append({"Petición": row.get("Petición", "")})

        rows_out.append({
            "Referencia":              "",  # no viene en este input
            "Solicitante":             campos["Solicitante"],
            "Género Solicitante":      "",
            "DNI":                     campos["DNI"],
            "Nº Petición":             campos["Nº Petición"],
            "Centro de Investigación": campos["Centro de Investigación"],
            "CIF":                     campos["CIF"],
            "Nota":                    limpiar_numero(row.get("Puntuación", "")),
            "Descripción":             (row.get("Descripción", "") or "").strip(),
            "Rama":                    "",
            "Cantidad Total":          "",
            "Año Inicio":              AÑO_INICIO,
            "Año1":                    "",
            "Año2":                    "",
            "Año3":                    "",
            "Año4":                    "",
            "Año5":                    "",
            "Estado Solicitud":        ESTADO_SOLICITUD,
        })

with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as f_out:
    writer = csv.DictWriter(f_out, fieldnames=campos_salida)
    writer.writeheader()
    writer.writerows(rows_out)

with open(ERRORES_FILE, "w", newline="", encoding="utf-8") as f_err:
    writer = csv.DictWriter(f_err, fieldnames=["Petición"])
    writer.writeheader()
    writer.writerows(no_parseadas)

print(f"Listo → {OUTPUT_FILE}")
print(f"No parseadas: {len(no_parseadas)} → {ERRORES_FILE}")