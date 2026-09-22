"""
Recorre las solicitudes con "Género Solicitante" vacío y permite asignar
el género manualmente pulsando una tecla:
    v -> Masculino
    f -> Femenino
    s -> Saltar (no modificar, seguir a la siguiente)
    q -> Salir y guardar progreso
"""

from pathlib import Path
import sys
from pymongo import MongoClient

# ---------------- CONFIG ----------------
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from db_config import MONGO_URI, DB_NAME
COL_NAME = "solicitudesNew"  # <-- cambia aquí la colección si hace falta
# -----------------------------------------

TECLA_A_GENERO = {
    "v": "Masculino",
    "f": "Femenino",
}


def main():
    client = MongoClient(MONGO_URI)
    col = client[DB_NAME][COL_NAME]

    query = {
        "$or": [
            {"Género Solicitante": ""},
            {"Género Solicitante": {"$exists": False}},
            {"Género Solicitante": None},
        ]
    }

    total = col.count_documents(query)
    if total == 0:
        print("No hay solicitudes con género vacío. Nada que hacer.")
        return

    print(f"Se encontraron {total} solicitudes sin género.\n")
    print("Controles: v = Masculino | f = Femenino | s = Saltar | q = Salir\n")

    procesadas = 0
    for doc in col.find(query):
        procesadas += 1
        print("-" * 60)
        print(f"[{procesadas}/{total}] Ref: {doc.get('Referencia', '')}")
        print(f"Solicitante: {doc.get('Solicitante', '')}")
        print(f"Centro: {doc.get('Centro de Investigación', '')}")
        print(f"Descripción: {doc.get('Descripción', '')[:100]}")

        while True:
            tecla = input(">> (v/f/s/q): ").strip().lower()

            if tecla == "q":
                print(f"\nSaliendo. Procesadas {procesadas - 1} de {total}.")
                client.close()
                return

            if tecla == "s":
                break

            if tecla in TECLA_A_GENERO:
                genero = TECLA_A_GENERO[tecla]
                col.update_one(
                    {"_id": doc["_id"]},
                    {"$set": {"Género Solicitante": genero}},
                )
                print(f"   -> Asignado: {genero}")
                break

            print("   Tecla no válida. Usa v, f, s o q.")

    print(f"\nCompletado. {procesadas} solicitudes revisadas.")
    client.close()


if __name__ == "__main__":
    main()