import csv
import re

# ── CONFIG ──────────────────────────────────────────────────────────────────
AÑO_INICIO = 2021
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent

ESTADO_SOLICITUD = "Aceptada"  # cámbialo si quieres otro estado
INPUT_FILE  = BASE_DIR / "../../data/raw/csv/CSV_2021/anexo1_2021_completo.csv"
OUTPUT_FILE = BASE_DIR / "../../data/clean/CSV_2021_CLEAN/anexo1_2021_completo.csv"
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
    # limpiezas típicas del dataset
    t = re.sub(r"\s+", " ", t)
    t = t.replace(" del CSIC", ". CSIC")
    t = t.replace(" del Ibfg", " del IBFG")
    t = t.replace(" del Ibgm", " del IBGM")
    t = t.replace(" del Irnasa", " del IRNASA")
    return t.title()

def parsear_peticion(peticion):
    """
    Devuelve dict con claves:
    Solicitante, DNI, Nº Petición, Centro de Investigación, CIF
    """
    vacio = {
        "Solicitante": "",
        "DNI": "",
        "Nº Petición": "",
        "Centro de Investigación": "",
        "CIF": "",
    }

    if not peticion:
        return vacio

    s = peticion.strip().strip('"')
    s = s.rstrip(".").strip()

    # DNI enmascarado flexible: ***1234**, ****7553*, etc.
    dni_pat = r"(\*+\d+\*+)"

    # Patrones tolerantes:
    # 1) APELLIDOS, NOMBRE, DNI (Petición n.º X. CENTRO, CIF)
    # 2) ... (Petición n.º X del CENTRO, CIF)
    # 3) ... (Petición n.º X de CENTRO, CIF)
    # 4) admite "n.º", "nº", "no"
    patrones = [
        rf"^(?P<nombre>.+?)\s*,\s*{dni_pat}\s*\(Petición\s+n[.\s]*[ºo]\s*(?P<num>\d+)\s*[.,]\s*(?P<centro>.+?)\s*,\s*(?P<cif>[A-Z]\d{{7}}[A-Z0-9])\)$",
        rf"^(?P<nombre>.+?)\s*,\s*{dni_pat}\s*\(Petición\s+n[.\s]*[ºo]\s*(?P<num>\d+)\s+del\s+(?P<centro>.+?)\s*,\s*(?P<cif>[A-Z]\d{{7}}[A-Z0-9])\)$",
        rf"^(?P<nombre>.+?)\s*,\s*{dni_pat}\s*\(Petición\s+n[.\s]*[ºo]\s*(?P<num>\d+)\s+de\s+(?P<centro>.+?)\s*,\s*(?P<cif>[A-Z]\d{{7}}[A-Z0-9])\)$",
    ]

    for pat in patrones:
        m = re.match(pat, s, flags=re.IGNORECASE)
        if m:
            nombre_raw = m.group("nombre").strip().strip(",")
            dni = m.group(2).strip()  # por dni_pat sin nombre de grupo
            num = m.group("num").strip()
            centro = normalizar_centro(m.group("centro"))
            cif = m.group("cif").upper().strip()

            # Reordenar "APELLIDOS, NOMBRE" -> "Nombre Apellidos"
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

    return vacio

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

        # marca para revisión
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
            "Descripción":             (row.get("Finalidad", "") or "").strip(),
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

# Log de no parseados
with open(ERRORES_FILE, "w", newline="", encoding="utf-8") as f_err:
    writer = csv.DictWriter(f_err, fieldnames=["Referencia", "Petición"])
    writer.writeheader()
    writer.writerows(no_parseados)

print(f"Listo → {OUTPUT_FILE}")
print(f"No parseados: {len(no_parseados)} → {ERRORES_FILE}")