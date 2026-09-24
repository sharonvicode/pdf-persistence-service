"""Fixtures compartidos por los tests."""

import os

import pytest
from fastapi.testclient import TestClient

from app.application.services import ExtractionService
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
    from pymongo import MongoClient
    from pymongo.errors import PyMongoError

    uri = os.getenv("MONGODB_URI", "mongodb://localhost:27017")
    mongo_client = MongoClient(uri, serverSelectionTimeoutMS=2000)
    try:
        mongo_client.admin.command("ping")
    except PyMongoError:
        pytest.skip(f"MongoDB no disponible en {uri}")

    yield mongo_client[TEST_DATABASE]["extractions"]

    mongo_client.drop_database(TEST_DATABASE)
    mongo_client.close()