import csv
import re

# ── CONFIG ──────────────────────────────────────────────────────────────────
AÑO_INICIO = 2021
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent

ESTADO_SOLICITUD = "Suplente" 
INPUT_FILE  = BASE_DIR / "../../data/raw/csv/CSV_2021/anexo2_2021_completo.csv"
OUTPUT_FILE = BASE_DIR / "../../data/clean/CSV_2021_CLEAN/anexo2_2021_completo.csv"
ERRORES_FILE = BASE_DIR / "proyectos_investigacion_no_parseados.csv"
# ────────────────────────────────────────────────────────────────────────────


def limpiar_numero(valor):
    if valor is None:
        return ""
    v = str(valor).strip().replace('"', '')
    if not v:
        return ""
    return v.replace(".", "").replace(",", ".")

def normalizar_centro(txt):
    if not txt:
        return ""
    t = txt.strip(" .")
    t = re.sub(r"\s+", " ", t)
    t = t.replace(" del CSIC", ". CSIC")
    t = t.replace(" del Ibfg", " del IBFG")
    t = t.replace(" del Ibgm", " del IBGM")
    t = t.replace(" del Irnasa", " del IRNASA")
    return t.title()

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

    m_num = re.search(r"Petición\s+n[.\s]*[ºo]\s*(\d+)", resto, flags=re.IGNORECASE)
    num = m_num.group(1) if m_num else ""

    m_cif = re.search(r"([A-Z]\d{7}[A-Z0-9])\s*$", resto, flags=re.IGNORECASE)
    cif = m_cif.group(1).upper() if m_cif else ""

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

    if "," in nombre_raw:
        ap, no = [p.strip() for p in nombre_raw.split(",", 1)]
        solicitante = f"{no} {ap}".strip().title()
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

no_parseados = []
rows_out = []

with open(INPUT_FILE, newline="", encoding="utf-8-sig") as f_in:
    reader = csv.DictReader(f_in)
    for row in reader:
        campos = parsear_peticion(row.get("Petición", ""))

        if not campos["Solicitante"] and row.get("Petición", "").strip():
            no_parseados.append({
                "Referencia": row.get("Referencia", ""),
                "Petición": row.get("Petición", "")
            })

        row_out = {
            "Referencia":              (row.get("Referencia", "") or "").strip(),
            "Solicitante":             campos["Solicitante"],
            "Género Solicitante":      "",
            "DNI":                     campos["DNI"],
            "Nº Petición":             campos["Nº Petición"],
            "Centro de Investigación": campos["Centro de Investigación"],
            "CIF":                     campos["CIF"],
            "Nota":                    limpiar_numero(row.get("Puntuación", "")),
            "Descripción":             (row.get("Descripción", "") or "").strip(),
            "Rama":                    "",
            "Cantidad Total":          limpiar_numero(row.get("Cantidad total", "")),
            "Año Inicio":              AÑO_INICIO,
            "Año1":                    limpiar_numero(row.get("2021.", "")),
            "Año2":                    limpiar_numero(row.get("2022.", "")),
            "Año3":                    limpiar_numero(row.get("2023.", "")),
            "Año4":                    "",
            "Año5":                    "",
            "Estado Solicitud":        ESTADO_SOLICITUD,
        }
        rows_out.append(row_out)

with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as f_out:
    writer = csv.DictWriter(f_out, fieldnames=campos_salida)
    writer.writeheader()
    writer.writerows(rows_out)

with open(ERRORES_FILE, "w", newline="", encoding="utf-8") as f_err:
    writer = csv.DictWriter(f_err, fieldnames=["Referencia", "Petición"])
    writer.writeheader()
    writer.writerows(no_parseados)

print(f"Listo → {OUTPUT_FILE}")
print(f"No parseados: {len(no_parseados)} → {ERRORES_FILE}")