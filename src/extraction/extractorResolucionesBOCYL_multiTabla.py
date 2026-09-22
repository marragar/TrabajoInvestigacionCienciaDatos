import pdfplumber
import pandas as pd
import re
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
PDF_PATH = BASE_DIR / "../../data/raw/pdfs/ResolucionBOCYL2017.pdf"  # ajusta la ruta a donde lo tengas
PAGINA_INICIO = 12  # primera pagina del ANEXO I (numero de pagina del PDF, 1-indexed)
PAGINA_FIN = 18   # ultima pagina del ANEXO I (inclusive)
OUTPUT_PATH = BASE_DIR / "../../data/raw/csv/CSV_2017/anexo2_2017_completo.csv"

COL_REFERENCIA = "Referencia"  # nombre de la primera columna en la cabecera real


def limpiar_saltos_linea(df):
    df.columns = [str(c).replace('\n', ' ') if c is not None else '' for c in df.columns]
    for col in df.columns:
        df[col] = df[col].astype(str).str.replace('\n', ' ', regex=False)
    return df


def es_fila_titulo_seccion(row):
    """Detecta filas tipo ['A) Beneficiarios...', None, None, None, None, None, None, None]"""
    primera = row[0]
    resto = row[1:]
    if primera is None:
        return False
    return bool(re.match(r'^[A-Z]\)\s', primera.strip())) and all(c is None for c in resto)


def extraer_tablas_pagina(page):
    """Filtra el texto de fondo (texto a 6.19pt y 8.51pt) y devuelve TODAS las tablas de la pagina."""
    clean_page = page.filter(
        lambda obj: obj.get('object_type') != 'char'
                    or round(obj.get('size', 0), 2) not in (6.19, 8.51, 6.36, 8.04, 8.82, 8.76)
    )
    return clean_page.extract_tables()


def main():
    todas_las_filas = []
    header = None
    categoria_actual = None

    with pdfplumber.open(PDF_PATH) as pdf:
        for num_pagina in range(PAGINA_INICIO, PAGINA_FIN + 1):
            page = pdf.pages[num_pagina - 1]  # pdfplumber es 0-indexed
            tablas = extraer_tablas_pagina(page)

            if not tablas:
                print(f"Pagina {num_pagina}: sin tabla detectada, se omite")
                continue

            filas_pagina = 0
            for tabla in tablas:
                for row in tabla:
                    # 1) fila de titulo de seccion (A) / B) / C) ...) -> actualiza categoria, no es dato
                    if es_fila_titulo_seccion(row):
                        categoria_actual = row[0].strip()
                        continue

                    # 2) fila de cabecera real (se repite en cada pagina) -> se captura una vez y se descarta
                    if row[0] is not None and row[0].strip() == COL_REFERENCIA:
                        if header is None:
                            header = list(row)
                        continue

                    # 3) fila de datos
                    todas_las_filas.append(list(row) + [categoria_actual])
                    filas_pagina += 1

            print(f"Pagina {num_pagina}: {filas_pagina} filas")

    if header is None:
        raise RuntimeError("No se encontro ninguna fila de cabecera ('Referencia') en el rango de paginas indicado")

    columnas = header + ["Categoria"]
    df = pd.DataFrame(todas_las_filas, columns=columnas)
    df = limpiar_saltos_linea(df)

    print(f"\nTotal filas combinadas: {len(df)}")
    print(f"Columnas: {list(df.columns)}")
    print()
    print(df.head(3).to_string())

    return df


if __name__ == "__main__":
    df = main()

    print("\n=== INFO DEL DATAFRAME ===")
    print(df.info())

    print("\n=== PRIMERAS 2 FILAS ===")
    print(df.head(2).to_string())

    print("\n=== FILA DEL MEDIO ===")
    medio = len(df) // 2
    print(df.iloc[[medio]].to_string())

    print("\n=== ULTIMAS 2 FILAS ===")
    print(df.tail(2).to_string())

    print("\n=== VALORES NULOS POR COLUMNA ===")
    print(df.isnull().sum())

    print("\n=== FILAS POR CATEGORIA ===")
    print(df["Categoria"].value_counts())

    output_path = OUTPUT_PATH
    df.to_csv(output_path, index=True)
    print(f"\nGuardado en: {output_path}")