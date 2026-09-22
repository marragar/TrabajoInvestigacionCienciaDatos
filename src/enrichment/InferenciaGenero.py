from pathlib import Path
import sys
import json
from pymongo import MongoClient
import ollama

# ── CONFIG ───────────────────────────────────────────────────────────────────
MODELO          = "phi4-reasoning:14b"
UMBRAL          = 0.80
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from db_config import MONGO_URI, DB_NAME
COL_NAME        = "solicitudesNew"
# ─────────────────────────────────────────────────────────────────────────────

SYSTEM_PROMPT = """Eres un clasificador de género a partir de nombres propios en español.
Te llegará una cadena que contiene nombre y apellidos, en cualquier orden.
Tu tarea es identificar cuál es el nombre propio (no los apellidos) y determinar el género asociado.
Devuelve Masculino o Femenino y una confianza entre 0 y 1 que refleje tu certeza."""

client_ollama = ollama.Client(host="http://localhost:11434")

def inferir_genero(nombre):
    if not nombre or nombre.strip() == "":
        return None, 0.0

    response = client_ollama.chat(
        model=MODELO,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user",   "content": f"Nombre y apellidos: {nombre}"}
        ],
        format={
            "type": "object",
            "properties": {
                "genero":    {"type": "string", "enum": ["Masculino", "Femenino"]},
                "confianza": {"type": "number"}
            },
            "required": ["genero", "confianza"]
        }
    )

    datos     = json.loads(response["message"]["content"])
    genero    = datos.get("genero")
    confianza = float(datos.get("confianza", 0.0))
    return genero, confianza

# ── MAIN ─────────────────────────────────────────────────────────────────────
client_mongo = MongoClient(MONGO_URI)
col          = client_mongo[DB_NAME][COL_NAME]

documentos = list(col.find({"Género Solicitante": {"$in": ["", None]}}, {"_id": 1, "Solicitante": 1}))
print(f"Documentos sin género: {len(documentos)}")

actualizados = 0
omitidos     = 0

for doc in documentos:
    nombre = doc.get("Solicitante", "")
    try:
        genero, confianza = inferir_genero(nombre)
        if genero and confianza >= UMBRAL:
            col.update_one({"_id": doc["_id"]}, {"$set": {"Género Solicitante": genero}})
            actualizados += 1
            print(f"✓ {nombre} → {genero} ({confianza:.0%})")
        else:
            omitidos += 1
            print(f"✗ {nombre} → confianza insuficiente ({confianza:.0%}), omitido")
    except Exception as e:
        omitidos += 1
        print(f"✗ {nombre} → error: {e}")

print(f"\nActualizados: {actualizados} | Omitidos (revisar a mano): {omitidos}")