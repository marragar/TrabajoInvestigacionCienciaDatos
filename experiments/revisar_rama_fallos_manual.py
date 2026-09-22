"""
Para cada documento con fallo='si' en la colección A, busca su pareja en B
por Descripción, muestra ambas ramas y pregunta si actualizar.
- V → actualiza la Rama en A con la de B y elimina el campo 'fallo'
- F → deja A como está
"""

from pathlib import Path
import sys
from pymongo import MongoClient

# ─── CONFIGURACIÓN ────────────────────────────────────────────────────────────
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from db_config import MONGO_URI, DB_NAME

COLECCION_A = "solicitudesFinalVersion2"   # la colección con los ~30 fallos
COLECCION_B = "SolicitudesR1-i"    # colección de referencia
# ──────────────────────────────────────────────────────────────────────────────


def normalizar(texto: str) -> str:
    return " ".join(texto.strip().lower().split()) if texto else ""


def main():
    client = MongoClient(MONGO_URI)
    db     = client[DB_NAME]
    col_a  = db[COLECCION_A]
    col_b  = db[COLECCION_B]

    # Indexar B por descripción
    print("Indexando colección B…")
    indice_b: dict[str, dict] = {}
    for doc in col_b.find():
        desc  = doc.get("Descripción") or doc.get("Descripcion") or ""
        clave = normalizar(desc)
        if clave:
            indice_b[clave] = doc
    print(f"  {len(indice_b)} documentos indexados.\n")

    fallos = list(col_a.find({"fallo": "si"}))
    total  = len(fallos)

    if total == 0:
        print("No hay documentos con fallo='si'.")
        client.close()
        return

    print(f"{total} documentos con fallo='si'.\n")
    print("─" * 60)

    actualizados = 0
    sin_match    = 0

    for i, doc_a in enumerate(fallos, 1):
        desc_a = doc_a.get("Descripción") or doc_a.get("Descripcion") or ""
        clave  = normalizar(desc_a)
        ref    = doc_a.get("Referencia") or str(doc_a["_id"])
        rama_a = doc_a.get("Rama") or "(sin rama)"

        doc_b = indice_b.get(clave)

        if doc_b is None:
            sin_match += 1
            print(f"\n[{i}/{total}]  Ref: {ref}  → sin coincidencia en B, omitido.")
            print("─" * 60)
            continue

        rama_b = doc_b.get("Rama") or "(sin rama)"

        print(f"\n[{i}/{total}]  Ref: {ref}")
        print(f"  Descripción  : {desc_a[:120]}")
        print(f"  Rama en A    : {rama_a}")
        print(f"  Rama en B    : {rama_b}")

        while True:
            resp = input("  ¿Actualizar rama con la de B y quitar fallo? [V/F]: ").strip().upper()
            if resp in ("V", "F"):
                break
            print("  Escribe V o F.")

        if resp == "V":
            col_a.update_one(
                {"_id": doc_a["_id"]},
                {
                    "$set":   {"Rama": rama_b},
                    "$unset": {"fallo": ""}
                }
            )
            actualizados += 1
            print(f"  ✓ Rama actualizada → '{rama_b}' y fallo eliminado.")
        else:
            print("  · Sin cambios.")

        print("─" * 60)

    print(f"\nFin. {actualizados}/{total} actualizados. {sin_match} sin coincidencia en B.")
    client.close()


if __name__ == "__main__":
    main()