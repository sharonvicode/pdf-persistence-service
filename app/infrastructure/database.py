"""Conexión a MongoDB.

Único lugar del servicio que conoce los detalles de la base de datos.
"""
import os

from pymongo import MongoClient
from pymongo.database import Database

DEFAULT_URI = "mongodb://localhost:27017"
DEFAULT_DATABASE = "pdf_extractext"


def get_database() -> Database:
    """Devuelve la base configurada con MONGODB_URI y MONGODB_DATABASE."""
    client = MongoClient(os.getenv("MONGODB_URI", DEFAULT_URI))
    return client[os.getenv("MONGODB_DATABASE", DEFAULT_DATABASE)]