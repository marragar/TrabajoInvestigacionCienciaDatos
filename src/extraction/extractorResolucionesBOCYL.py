import pdfplumber
import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
PDF_PATH = BASE_DIR / "../../data/raw/pdfs/ResolucionBOCYL2010.pdf"  # ajusta la ruta a donde lo tengas
PAGINA_INICIO = 2  # primera pagina del ANEXO I (numero de pagina del PDF, 1-indexed)
PAGINA_FIN = 11    # ultima pagina del ANEXO I (inclusive) -- AJUSTA ESTE NUMERO
OUTPUT_PATH = BASE_DIR / "../../data/raw/csv/CSV_2010/anexo2_2010_completo.csv"

def limpiar_saltos_linea(df):
    df.columns = [
        (c.replace('\n', ' ') if c is not None else f'col_{i}')
        for i, c in enumerate(df.columns)
    ]
    for col in df.columns:
        df[col] = df[col].apply(lambda x: '' if x is None else str(x).replace('\n', ' '))
    return df


def extraer_pagina(page):
    """Filtra el texto de fondo (texto a 6.19pt y 8.51pt) y extrae la tabla."""
    clean_page = page.filter(
        lambda obj: obj.get('object_type') != 'char' 
                    or round(obj.get('size', 0), 2) not in (6.19, 8.51)
    )
    tables = clean_page.extract_tables()
    if not tables:
        return None
    return tables[0]

def limpiar_fila(fila):
    return [celda if celda is not None else '' for celda in fila]

def main():
    todas_las_filas = []
    header = None

    with pdfplumber.open(PDF_PATH) as pdf:
        for num_pagina in range(PAGINA_INICIO, PAGINA_FIN + 1):
            page = pdf.pages[num_pagina - 1]
            tabla = extraer_pagina(page)

            if tabla is None:
                print(f"Pagina {num_pagina}: sin tabla detectada, se omite")
                continue

            tabla = [limpiar_fila(fila) for fila in tabla]

            if header is None:
                header = tabla[0]
                filas = tabla[1:]
            else:
                filas = tabla[1:] if tabla[0] == header else tabla

            print(f"Pagina {num_pagina}: {len(filas)} filas")
            todas_las_filas.extend(filas)

    df = pd.DataFrame(todas_las_filas, columns=header)
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

    # print("\n=== REFERENCIAS DUPLICADAS (deberian ser 0) ===")
    # print(df['Referencia'].duplicated().sum())

    output_path = OUTPUT_PATH
    df.to_csv(output_path, index=True)
    print(f"\nGuardado en: {output_path}")