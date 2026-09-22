import pdfplumber
import pandas as pd
import re
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
PDF_PATH = BASE_DIR / "../../data/raw/pdfs/ResolucionBOCYL2010.pdf"  # ajusta la ruta a donde lo tengas
PAGINA_INICIO = 2  # primera pagina del ANEXO I (numero de pagina del PDF, 1-indexed)
PAGINA_FIN = 11    # ultima pagina del ANEXO I (inclusive) -- AJUSTA ESTE NUMERO
OUTPUT_PATH = BASE_DIR / "../../data/raw/csv/CSV_2010/anexo1_2010_completo.csv"

COL_CABECERA = "Perceptor (Solicitante)"  # primera columna de la cabecera real en este anexo

CAUSA_OBJETIVO = (
    "Inexistencia de crédito adecuado y suficiente para financiar las "
    "obligaciones derivadas de la concesión de las subvenciones en el "
    "ejercicio correspondiente."
)


def normalizar(texto):
    """Colapsa saltos de linea y espacios multiples para poder comparar de forma robusta."""
    if texto is None:
        return ""
    return re.sub(r'\s+', ' ', texto.replace('\n', ' ')).strip()


def limpiar_saltos_linea(df):
    df.columns = [str(c).replace('\n', ' ') if c is not None else '' for c in df.columns]
    for col in df.columns:
        df[col] = df[col].astype(str).str.replace('\n', ' ', regex=False)
    return df


def es_fila_titulo_seccion(row):
    """Detecta filas tipo ['A) Solicitantes...', None, None, None]"""
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
                    # 1) fila de titulo de seccion (A) / B) / C) ...) -> actualiza categoria
                    if es_fila_titulo_seccion(row):
                        categoria_actual = row[0].strip()
                        continue

                    # 2) fila de cabecera real (se repite en cada pagina) -> se captura una vez y se descarta
                    if row[0] is not None and row[0].strip() == COL_CABECERA:
                        if header is None:
                            header = list(row)
                        continue

                    # 3) fila de datos
                    todas_las_filas.append(list(row) + [categoria_actual])
                    filas_pagina += 1

            print(f"Pagina {num_pagina}: {filas_pagina} filas")

    if header is None:
        raise RuntimeError(f"No se encontro ninguna fila de cabecera ('{COL_CABECERA}') en el rango de paginas indicado")

    columnas = header + ["Categoria"]
    df = pd.DataFrame(todas_las_filas, columns=columnas)
    df = limpiar_saltos_linea(df)

    print(f"\nTotal filas combinadas (sin filtrar): {len(df)}")
    print(f"Columnas: {list(df.columns)}")

    # --- Filtro por causa de denegacion ---
    col_causa = "Causa de denegación"
    causa_objetivo_norm = normalizar(CAUSA_OBJETIVO)
    df["_causa_normalizada"] = df[col_causa].apply(normalizar)

    df_filtrado = df[df["_causa_normalizada"] == causa_objetivo_norm].drop(columns=["_causa_normalizada"]).reset_index(drop=True)

    print(f"\nFilas que coinciden con la causa objetivo: {len(df_filtrado)} de {len(df)}")
    print()
    print(df_filtrado.head(3).to_string())

    return df


if __name__ == "__main__":
    df = main()

    print("\n=== INFO DEL DATAFRAME FILTRADO ===")
    print(df.info())

    print("\n=== PRIMERAS 2 FILAS ===")
    print(df.head(2).to_string())

    print("\n=== ULTIMAS 2 FILAS ===")
    print(df.tail(2).to_string())

    print("\n=== FILAS POR CATEGORIA ===")
    print(df["Categoria"].value_counts())

    output_path = OUTPUT_PATH
    df.to_csv(output_path, index=True)
    print(f"\nGuardado en: {output_path}")