from pathlib import Path
import sys
import json
import re
import time
import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient
from ddgs import DDGS
import ollama

# ── CONFIG ───────────────────────────────────────────────────────────────────
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from db_config import MONGO_URI, DB_NAME
COL_NAME      = "solicitudesNew"

OLLAMA_HOST   = "http://localhost:11434"
OLLAMA_MODEL  = "phi4-reasoning:14b"

UMBRAL        = 0.80
MAX_CHARS_WEB = 2000  # caracteres a extraer de la página
# ─────────────────────────────────────────────────────────────────────────────

RAMAS = [
    "Filosofía y Letras",
    "Ciencias Sociales - Educación",
    "Ciencias Sociales - Resto",
    "Ciencias - Matemáticas y Física",
    "Ciencias - Ciencias de la Salud",
    "Ciencias - Resto",
    "Ingenierías",
]

SYSTEM_PROMPT = f"""Eres un clasificador de proyectos de investigación científica en español.
Dada la descripción de un proyecto y contexto adicional sobre el investigador principal, clasifícalo en una de las siguientes ramas:
{chr(10).join(f'- {r}' for r in RAMAS)}

Criterios:
- Filosofía y Letras: humanidades, historia, literatura, lingüística, patrimonio cultural, arqueología, filología, traducción, filosofía.
- Ciencias Sociales - Educación: proyectos cuyo objeto de estudio principal es la educación, la enseñanza, el aprendizaje, la pedagogía, la formación, el rendimiento académico, la inclusión educativa, metodologías didácticas, tecnología educativa, o la evaluación de sistemas educativos. Si el proyecto aplica IA o tecnología PARA mejorar procesos educativos, también es Educación.
- Ciencias Sociales - Resto: economía, turismo, sociología, psicología, derecho, comunicación, política, demografía, geografía humana.
- Ciencias - Matemáticas y Física: matemáticas puras o aplicadas, física teórica o experimental, computación cuántica, modelización numérica, estadística.
- Ciencias - Ciencias de la Salud: medicina, farmacia, biología molecular, biomedicina, veterinaria, enfermería, nutrición, salud pública, oncología, neurociencia.
- Ciencias - Resto: química, geología, medio ambiente, ecología, agronomía, biología no médica, botánica, zoología, ciencias del suelo.
- Ingenierías: ingeniería civil, industrial, informática, telecomunicaciones, materiales, energía, robótica, automatización, arquitectura técnica.

IMPORTANTE: Usa el contexto del investigador (departamento, área, grupo de investigación) como apoyo para decidir en casos ambiguos.

Devuelve la rama exactamente como aparece en la lista y una confianza entre 0 y 1."""

FORMAT_SCHEMA = {
    "type": "object",
    "properties": {
        "rama":      {"type": "string", "enum": RAMAS},
        "confianza": {"type": "number"}
    },
    "required": ["rama", "confianza"]
}

# ── CLIENTE ───────────────────────────────────────────────────────────────────
client_ollama = ollama.Client(host=OLLAMA_HOST)

# ── BÚSQUEDA WEB ──────────────────────────────────────────────────────────────
def fetch_texto(url):
    try:
        r = requests.get(url, timeout=8, headers={"User-Agent": "Mozilla/5.0"})
        soup = BeautifulSoup(r.text, "html.parser")
        # Eliminar scripts y estilos
        for tag in soup(["script", "style", "nav", "footer", "header"]):
            tag.decompose()
        texto = soup.get_text(separator=" ", strip=True)
        return texto[:MAX_CHARS_WEB]
    except Exception:
        return ""

def buscar_contexto(nombre, centro):
    try:
        query = f"{nombre} {centro}"
        with DDGS() as ddgs:
            resultados = list(ddgs.text(query, max_results=3))

        if not resultados:
            return ""

        # Fetch de la primera URL
        url_principal = resultados[0]["href"]
        texto_web = fetch_texto(url_principal)

        # Snippets de los 3 resultados como fallback
        snippets = "\n".join([r["body"] for r in resultados])

        contexto = f"Búsqueda: {query}\n\nContenido página principal:\n{texto_web}\n\nSnippets adicionales:\n{snippets}"
        return contexto

    except Exception as e:
        print(f"  [Web] Error búsqueda: {e}")
        return ""

# ── CLASIFICADOR ──────────────────────────────────────────────────────────────
def parsear_respuesta(texto):
    try:
        datos = json.loads(texto)
    except json.JSONDecodeError:
        match = re.search(r'\{.*?\}', texto, re.DOTALL)
        if not match:
            return None, 0.0
        try:
            datos = json.loads(match.group())
        except json.JSONDecodeError:
            return None, 0.0
    rama      = datos.get("rama")
    confianza = float(datos.get("confianza", 0.0))
    if rama not in RAMAS:
        return None, 0.0
    return rama, confianza

def clasificar(descripcion, contexto_web=""):
    if contexto_web:
        user_content = f"Descripción del proyecto: {descripcion}\n\nContexto del investigador:\n{contexto_web}"
    else:
        user_content = f"Descripción del proyecto: {descripcion}"

    print(user_content)

    try:
        response = client_ollama.chat(
            model=OLLAMA_MODEL,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user",   "content": user_content}
            ],
            format=FORMAT_SCHEMA,
            options={
                "temperature": 0.1,    # Esto hace que el modelo sea determinista
                "top_p": 0.9           # Controla la diversidad de tokens
            }
        )
        return parsear_respuesta(response["message"]["content"])
    except Exception as e:
        print(f"  [Ollama] Error: {e}")
        return None, 0.0

# ── MAIN ──────────────────────────────────────────────────────────────────────
client_mongo = MongoClient(MONGO_URI)
col          = client_mongo[DB_NAME][COL_NAME]

documentos = list(col.find(
    {"Rama": {"$in": ["", None]}},
    {"_id": 1, "Descripción": 1, "Solicitante": 1, "Centro de Investigación": 1}
))
print(f"Documentos sin rama: {len(documentos)}")

actualizados = 0
omitidos     = 0

for doc in documentos:
    descripcion = doc.get("Descripción", "")
    nombre      = doc.get("Solicitante", "")
    centro      = doc.get("Centro de Investigación", "")

    print(f"\n→ {descripcion[:80]}...")
    print(f"  Buscando contexto: {nombre} {centro}")

    contexto = buscar_contexto(nombre, centro)
    time.sleep(1)  # evitar rate limit de DDG

    rama, confianza = clasificar(descripcion, contexto)

    if rama and confianza >= UMBRAL:
        col.update_one({"_id": doc["_id"]}, {"$set": {"Rama": rama}})
        actualizados += 1
        print(f"  ✓ {rama} ({confianza:.0%})")
    else:
        omitidos += 1
        print(f"  ✗ Confianza insuficiente o error ({confianza:.0%}), omitido")

print(f"\nActualizados: {actualizados} | Omitidos (revisar a mano): {omitidos}")