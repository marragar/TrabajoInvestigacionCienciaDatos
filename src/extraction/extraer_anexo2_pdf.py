import pdfplumber
import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
PDF_PATH = BASE_DIR / "../../data/raw/pdfs/ResolucionBOCYL2010.pdf"  # ajusta la ruta a donde lo tengas
PAGINA_INICIO = 12
PAGINA_FIN = 27
OUTPUT_PATH = BASE_DIR / "../../data/raw/csv/CSV_2010/anexo2_2010_completo.csv"


def limpiar_fila(fila):
    return [celda if celda is not None else '' for celda in fila]


def deduplicar_columnas(columnas):
    """Evita nombres de columna repetidos (p.ej. varias '' o 'Punt.')."""
    vistas = {}
    resultado = []
    for i, c in enumerate(columnas):
        nombre = c.replace('\n', ' ').strip() if c else f'col_{i}'
        if nombre == '':
            nombre = f'col_{i}'
        if nombre in vistas:
            vistas[nombre] += 1
            nombre = f'{nombre}_{vistas[nombre]}'
        else:
            vistas[nombre] = 0
        resultado.append(nombre)
    return resultado


def limpiar_saltos_linea(df):
    # Iteramos por POSICIÓN, nunca por nombre, para evitar ambigüedad
    for i in range(df.shape[1]):
        df.iloc[:, i] = df.iloc[:, i].apply(
            lambda x: '' if x is None else str(x).replace('\n', ' ')
        )
    return df


def extraer_pagina(page):
    clean_page = page.filter(
        lambda obj: obj.get('object_type') != 'char'
                    or round(obj.get('size', 0), 2) not in (6.19, 8.51)
    )
    tables = clean_page.extract_tables()
    if not tables:
        return None
    return tables[0]


def main():
    todas_las_filas = []
    header = None
    n_columnas_esperadas = None

    with pdfplumber.open(PDF_PATH) as pdf:
        for num_pagina in range(PAGINA_INICIO, PAGINA_FIN + 1):
            page = pdf.pages[num_pagina - 1]
            tabla = extraer_pagina(page)

            if tabla is None:
                print(f"Pagina {num_pagina}: sin tabla detectada, se omite")
                continue

            tabla = [limpiar_fila(fila) for fila in tabla]

            if header is None:
                header = deduplicar_columnas(tabla[0])
                n_columnas_esperadas = len(header)
                filas = tabla[1:]
            else:
                filas = tabla

            # Descarta filas de longitud distinta y cabeceras repetidas
            filas_validas = [
                f for f in filas
                if len(f) == n_columnas_esperadas and f[0] != tabla[0][0]
            ]
            descartadas = len(filas) - len(filas_validas)
            if descartadas:
                print(f"  -> {descartadas} filas descartadas (cabecera repetida o nº columnas distinto) en pagina {num_pagina}")

            print(f"Pagina {num_pagina}: {len(filas_validas)} filas")
            todas_las_filas.extend(filas_validas)

    df = pd.DataFrame(todas_las_filas, columns=header)
    df = limpiar_saltos_linea(df)

    print(f"\nTotal filas combinadas: {len(df)}")
    print(f"Columnas: {list(df.columns)}")

    return df


if __name__ == "__main__":
    df = main()
    print(df.head(3).to_string())
    df.to_csv(OUTPUT_PATH, index=True)
    print(f"\nGuardado en: {OUTPUT_PATH}")