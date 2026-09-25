"""Fixtures compartidos por los tests."""

import os

import pytest
from fastapi.testclient import TestClient
from pymongo import MongoClient
from pymongo.errors import PyMongoError

from app.application.services import ExtractionService
from app.infrastructure.database import EXTRACTIONS_COLLECTION, get_mongo_uri
from app.infrastructure.repositories import InMemoryExtractionRepository
from app.main import app

TEST_DATABASE = "pdf_extractext_test"


@pytest.fixture
def client():
    """Cliente HTTP con el repositorio en memoria (tests unitarios, sin MongoDB)."""
    app.state.extraction_service = ExtractionService(InMemoryExtractionRepository())
    return TestClient(app)


@pytest.fixture
def mongo_collection():
    """Colección de una base MongoDB de prueba; se borra al terminar cada test."""
    

    uri = get_mongo_uri()
    mongo_client = MongoClient(uri, serverSelectionTimeoutMS=2000)
    try:
        mongo_client.admin.command("ping")
    except PyMongoError:
        pytest.skip(f"MongoDB no disponible en {uri}")

    yield mongo_client[TEST_DATABASE][EXTRACTIONS_COLLECTION]

    mongo_client.drop_database(TEST_DATABASE)
    mongo_client.close()