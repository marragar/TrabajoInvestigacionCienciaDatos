"""Config de conexión a MongoDB compartida por todos los scripts del repo.

Lee las credenciales de variables de entorno (ver .env.example) en vez de
tenerlas hardcodeadas en cada script. Con los valores por defecto de abajo
sigue funcionando igual que antes si no existe un .env.
"""
import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parent / ".env")

MONGO_USER = os.getenv("MONGO_USER", "admin")
MONGO_PASSWORD = os.getenv("MONGO_PASSWORD", "admin123")
MONGO_HOST = os.getenv("MONGO_HOST", "localhost")
MONGO_PORT = os.getenv("MONGO_PORT", "27017")
DB_NAME = os.getenv("MONGO_DB_NAME", "SubvencionesBOCYL")

MONGO_URI = f"mongodb://{MONGO_USER}:{MONGO_PASSWORD}@{MONGO_HOST}:{MONGO_PORT}/?directConnection=true"
