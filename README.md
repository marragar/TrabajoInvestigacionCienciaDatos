# ResidenciaInvestigacion — Subvenciones BOCYL

Análisis de las resoluciones de subvenciones a personal investigador de la Junta de Castilla y León (BOCYL): extracción desde PDF, limpieza, carga en MongoDB, enriquecimiento de campos, tests estadísticos e inferencia.

## Estructura

```
data/
  raw/pdfs/        PDFs originales de las resoluciones BOCYL (uno por año)
  raw/csv/         CSV extraído directamente del PDF, sin limpiar (CSV_<año>/anexoN_...)
  clean/           CSV limpio/parseado, listo para importar a Mongo (CSV_<año>_CLEAN/)
                   fusiona lo que antes eran las carpetas separadas "CSV_Parseados" y "CSV_Parseados/new"
  validation/      Muestra de validación manual (muestra_validacion.csv)
  exports/         Volcados/backups de las colecciones de Mongo en distintos momentos (*.json).
                   Ningún script del repo los lee — son solo snapshots de referencia.
  archive/         Copias/duplicados que existían en el repo original, conservados tal cual (no se usan en el pipeline)

src/
  extraction/      PDF -> CSV crudo (pdfplumber). Los PDF_PATH/OUTPUT_PATH se reconfiguran a mano por año.
  parsing/         CSV crudo -> CSV limpio, un script por año+anexo (parserRowBOCYL_<año><anexo>.py)
  database/        Carga de los CSV limpios en MongoDB, y comparación de colecciones
  enrichment/       Relleno de campos que faltan (Género, Rama) vía LLM local / heurísticas, y su muestra de validación
  statistics/        Tests de hipótesis (chi-cuadrado, Fisher exacto, ANOVA/t-test) sobre las variables categóricas
  plotting/           Generación de gráficas descriptivas y de series temporales

outputs/
  graphs/          Gráficas generadas (PNG) y el .pbix del mosaico
  reports/         Resultados de los tests estadísticos en Markdown

experiments/       Carpeta de scripts exploratorios/puntuales (antes "SCRIPTS_PRUEBAS"), no forma parte del
                   pipeline principal: clasificador de Rama por ML (sentence-transformers + SVM), herramientas
                   de corrección manual, comparativas de colecciones, y gráficas/tests antiguos conservados
                   como referencia.

notes/             Ideas y variables pendientes para futuro análisis
```

## Puesta en marcha

1. Levanta MongoDB con Docker:
   ```
   cp .env.example .env    # ajusta credenciales si quieres, si no deja las por defecto
   docker compose up -d
   ```
2. Instala las dependencias de Python (idealmente en un venv/conda propio):
   ```
   pip install -r requirements.txt
   ```
   (`rpy2`, usado por algunos tests estadísticos, necesita además R instalado en el sistema)
3. Ejecuta los scripts del pipeline en el orden de la sección siguiente.

Todos los scripts leen la conexión a Mongo desde `db_config.py`, que a su vez
lee las variables `MONGO_USER`/`MONGO_PASSWORD`/`MONGO_HOST`/`MONGO_PORT`/`MONGO_DB_NAME`
de `.env` (con los valores de `.env.example` como default si no hay `.env`).
`.env` no se sube al repo.

## Pipeline (orden de ejecución)

1. **`src/extraction/`** — PDF de la resolución → CSV crudo por anexo (`data/raw/pdfs/` → `data/raw/csv/`)
2. **`src/parsing/`** — CSV crudo → CSV limpio, normalizando columnas y separando campos (`data/raw/csv/` → `data/clean/`)
3. **`src/database/insertarDatosMongo.py`** — Carga todos los CSV de `data/clean/` en MongoDB
4. **`src/enrichment/`** — Rellena `Género`/`Rama` cuando faltan (LLM local + búsqueda web), calcula personal contratado
5. **`src/statistics/`** — Tests de independencia/asociación (chi², Fisher, ANOVA) sobre los datos ya en Mongo
6. **`src/plotting/`** — Gráficas descriptivas y de evolución temporal, salida en `outputs/graphs/`

Todos los scripts que hablan con MongoDB usan la conexión definida en `.env` (ver "Puesta en marcha" más arriba).

## Notas sobre nombres corregidos

Al reorganizar se detectaron y corrigieron dos nombres de fichero que no correspondían a su contenido real:

- **`extractorResolucionesBOCYL_multiTabla.py`** (antes `extractorResolucionesBOCYL2018.py`): su `PDF_PATH`/`OUTPUT_PATH` apuntan a `ResolucionBOCYL2017.pdf`, no a 2018.
- **`src/statistics/test_medias.py`** (antes `testTemporal.py`): no hace ningún análisis temporal/de series — compara medias (t-test/ANOVA) entre grupos categóricos. Su propia salida ya se llamaba `test_medias.md`.

El resto de scripts con nombres poco descriptivos (`a.py`, `aa.py`, `aaa.py`, `bbb.py` en `src/`; `a.py`...`dd.py`, `corregir.py`, `colapsarCol.py`, `graficas.py`, `graficas2.py`, `testFisherChi*.py`, `testItextFail.py` en `experiments/`) se renombraron a nombres que describen lo que hacen, verificado leyendo su código, no solo su nombre anterior.

## Estado de `data/clean/`

`src/database/insertarDatosMongo.py` ahora escanea toda `data/clean/` (los 10 años). Antes de la reorganización solo escaneaba el subconjunto que vivía en `CSV_Parseados/new` (2010, 2013, 2014, 2016, 2017, 2018); al fusionar esa carpeta con `CSV_Parseados` (2021, 2023, 2024, 2025) en una sola `data/clean/`, el script recoge ahora los 10 años en una sola pasada.
