import sys
import os
import glob
import numpy as np
import pandas as pd
from pathlib import Path
from pymongo import MongoClient

# =====================================================================
# CONFIGURACIÓN OPTIMIZADA
# =====================================================================
BASE_DIR = Path(__file__).resolve().parent
# Forzamos directConnection=True para evitar el cierre del socket en local
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from db_config import MONGO_URI, DB_NAME
COLLECTION_NAME = "solicitudesNew"
CARPETA_RAIZ = str(BASE_DIR / "../../data/clean")   # Apunta a la carpeta madre de tus CSVs (fusiona lo que antes eran CSV_Parseados y CSV_Parseados/new)
TAMANO_LOTE = 1000                  # Insertar de 1000 en 1000 evita saturar la conexión

def importar_csvs_seguro():
    # 1. Conexión y verificación real (Ping)
    try:
        client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
        db = client[DB_NAME]
        coleccion = db[COLLECTION_NAME]
        
        # Forzamos un ping real para asegurarnos de que Python habla con MongoDB
        client.admin.command('ping')
        print(f"¡Conexión verificada con MongoDB exitosamente!")
        print(f"BD: {DB_NAME} | Colección: {COLLECTION_NAME}\n")
    except Exception as e:
        print(f"[ERROR CRÍTICO] No se pudo establecer comunicación con MongoDB: {e}")
        return

    # 2. Búsqueda de archivos
    patron_busqueda = os.path.join(CARPETA_RAIZ, "**", "*.csv")
    archivos_csv = glob.glob(patron_busqueda, recursive=True)

    if not archivos_csv:
        print(f"[AVISO] No se encontraron archivos CSV en: {CARPETA_RAIZ}")
        return

    print(f"Se detectaron {len(archivos_csv)} archivos CSV para procesar.")
    print("-" * 60)

    # 3. Procesamiento
    for ruta_archivo in archivos_csv:
        nombre_archivo = os.path.basename(ruta_archivo)
        print(f"Leyendo: {nombre_archivo}")

        try:
            # Leer CSV
            df = pd.read_csv(ruta_archivo, encoding='utf-8')

            # Limpieza estricta: Reemplazar Infinitos y NaNs que rompen BSON
            df = df.replace([np.inf, -np.inf], np.nan)
            df = df.fillna("")

            datos_a_insertar = df.to_dict(orient='records')

            if datos_a_insertar:
                total_insertados = 0
                # Insertar en porciones (chunks) para proteger el socket
                for i in range(0, len(datos_a_insertar), TAMANO_LOTE):
                    lote = datos_a_insertar[i:i + TAMANO_LOTE]
                    resultado = coleccion.insert_many(lote)
                    total_insertados += len(resultado.inserted_ids)
                
                print(f"  --> ¡Éxito! Se insertaron {total_insertados} registros en total.")
            else:
                print(f"  --> [AVISO] El archivo estaba vacío.")

        except Exception as e:
            print(f"  --> [ERROR] Falló el procesamiento: {e}")
        
        print("-" * 60)

    print("\n¡Proceso finalizado!")

if __name__ == "__main__":
    importar_csvs_seguro()