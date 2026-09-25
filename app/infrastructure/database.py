"""Conexión a MongoDB.

Único lugar del servicio que conoce los detalles de la base de datos.
"""

import os

from pymongo import MongoClient
from pymongo.database import Database

DEFAULT_URI = "mongodb://localhost:27017"
DEFAULT_DATABASE = "pdf_extractext"
EXTRACTIONS_COLLECTION = "extractions"


def get_mongo_uri() -> str:
    """Devuelve la URI de MongoDB configurada en MONGODB_URI."""
    return os.getenv("MONGODB_URI", DEFAULT_URI)


def get_database() -> Database:
    """Devuelve la base configurada con MONGODB_URI y MONGODB_DATABASE."""
    client = MongoClient(get_mongo_uri())
    return client[os.getenv("MONGODB_DATABASE", DEFAULT_DATABASE)]