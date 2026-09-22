# Subvenciones BOCYL — Análisis de las ayudas a personal investigador en Castilla y León

Pipeline de datos completo sobre las resoluciones de subvenciones a personal investigador publicadas en el **Boletín Oficial de Castilla y León (BOCYL)**: desde los PDF oficiales hasta el análisis estadístico de si variables como el **género**, la **rama de conocimiento** o el **centro de investigación** están asociadas con que una solicitud sea aceptada.

El proyecto cubre **10 convocatorias** (2010, 2013, 2014, 2016, 2017, 2018, 2021, 2023, 2024 y 2025) y forma parte de un trabajo de investigación en la Universidad de León.

## Qué hace

```
PDF oficiales ──► CSV crudo ──► CSV limpio ──► MongoDB ──► Enriquecimiento ──► Tests estadísticos
 (BOCYL)       pdfplumber    parsers por     Docker      LLM local +          chi², Fisher,
                             año y anexo                 heurísticas          ANOVA, t-test
                                                                    └──────► Gráficas
```

- **Extracción** de tablas desde PDF con `pdfplumber`, lidiando con formatos distintos cada año, tablas partidas entre páginas y capas de texto fantasma.
- **Limpieza y normalización** de cada convocatoria a un esquema común (números en formato español, identificadores, notas en distintas escalas, nombres de centros...).
- **Almacenamiento** en MongoDB, levantado con Docker.
- **Enriquecimiento** de campos que no vienen en el BOCYL (género, rama) mediante LLMs locales, búsqueda web y un clasificador propio (embeddings + SVM), con muestra de validación manual.
- **Análisis estadístico**: tests de independencia (chi-cuadrado, Fisher exacto), comparación de medias (t de Welch, ANOVA) con tamaños del efecto y corrección por comparaciones múltiples.
- **Visualización** de estadística descriptiva y evolución temporal.

## Stack

Python · pdfplumber · MongoDB · Docker · Ollama (LLMs locales) · sentence-transformers · scikit-learn · SciPy · R (vía rpy2) · Power BI

## Puesta en marcha

**Requisitos:** Python 3, Docker y, para algunos tests estadísticos, R instalado en el sistema (lo usa `rpy2`).

```bash
# 1. Levantar MongoDB
cp .env.example .env        # ajusta las credenciales si quieres
docker compose up -d

# 2. Instalar dependencias (mejor en un entorno virtual)
pip install -r requirements.txt
```

La conexión a MongoDB se centraliza en `db_config.py`, que lee `MONGO_USER`, `MONGO_PASSWORD`, `MONGO_HOST`, `MONGO_PORT` y `MONGO_DB_NAME` desde `.env` (o usa los valores de `.env.example` si no existe). El `.env` no se sube al repositorio.

## Pipeline

Los scripts se ejecutan en este orden:

| Paso | Carpeta | Entrada → Salida | Descripción |
|------|---------|------------------|-------------|
| 1 | `src/extraction/` | `data/raw/pdfs/` → `data/raw/csv/` | Extrae las tablas de cada anexo del PDF a CSV. Las rutas se configuran por año dentro del script. |
| 2 | `src/parsing/` | `data/raw/csv/` → `data/clean/` | Un parser por año y anexo (`parserRowBOCYL_<año><anexo>.py`) que normaliza columnas y separa campos. |
| 3 | `src/database/` | `data/clean/` → MongoDB | `insertarDatosMongo.py` carga los 10 años de una pasada. Incluye también utilidades para comparar colecciones. |
| 4 | `src/enrichment/` | MongoDB → MongoDB | Rellena `Género` y `Rama` cuando faltan y calcula el personal contratado. |
| 5 | `src/statistics/` | MongoDB → `outputs/reports/` | Tests de independencia y de comparación de medias; resultados en Markdown. |
| 6 | `src/plotting/` | MongoDB → `outputs/graphs/` | Gráficas descriptivas y de series temporales. |

## Estructura del repositorio

```
├── data/
│   ├── raw/
│   │   ├── pdfs/        # Resoluciones originales del BOCYL (una por año)
│   │   └── csv/         # CSV extraído del PDF, sin limpiar
│   ├── clean/           # CSV limpio, listo para cargar en MongoDB
│   ├── validation/      # Muestra de validación manual del enriquecimiento
│   ├── exports/         # Snapshots de las colecciones de MongoDB (solo referencia)
│   └── archive/         # Copias antiguas conservadas, fuera del pipeline
├── src/
│   ├── extraction/      # PDF → CSV
│   ├── parsing/         # CSV crudo → CSV limpio
│   ├── database/        # Carga y comparación de colecciones
│   ├── enrichment/      # Relleno de Género / Rama
│   ├── statistics/      # Tests de hipótesis
│   └── plotting/        # Gráficas
├── outputs/
│   ├── graphs/          # Gráficas (PNG) y cuadro de mando de Power BI
│   └── reports/         # Resultados de los tests en Markdown
├── experiments/         # Scripts exploratorios fuera del pipeline principal
├── notes/               # Ideas y variables pendientes de analizar
├── db_config.py
├── docker-compose.yml
├── .env.example
└── requirements.txt
```

### Sobre `experiments/`

Scripts exploratorios que no forman parte del pipeline principal, conservados como referencia: el clasificador de rama por machine learning (sentence-transformers + SVM), herramientas de corrección manual, comparativas entre colecciones y versiones antiguas de gráficas y tests.

## Fuente de los datos

Resoluciones de concesión de subvenciones a personal investigador publicadas en el [BOCYL](https://bocyl.jcyl.es/), la fuente oficial de la Junta de Castilla y León.
