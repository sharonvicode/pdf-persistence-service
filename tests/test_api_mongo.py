"""Tests de POST y GET usando MongoDB real."""

import pytest
from fastapi.testclient import TestClient

from app.application.services import ExtractionService
from app.infrastructure.repositories import MongoExtractionRepository
from app.main import app

from tests.payloads import VALID_PAYLOAD


@pytest.fixture
def mongo_api(mongo_collection):
    app.state.extraction_service = ExtractionService(MongoExtractionRepository(mongo_collection))
    return TestClient(app)


def test_create_extraction_persists_in_mongo(mongo_api, mongo_collection):
    response = mongo_api.post("/extractions", json=VALID_PAYLOAD)

    assert response.status_code == 201
    assert mongo_collection.find_one({"_id": response.json()["id"]}) is not None


def test_get_existing_extraction_from_mongo(mongo_api):
    extraction_id = mongo_api.post("/extractions", json=VALID_PAYLOAD).json()["id"]

    response = mongo_api.get(f"/extractions/{extraction_id}")

    assert response.status_code == 200
    assert response.json() == {"id": extraction_id, **VALID_PAYLOAD}


def test_get_nonexistent_extraction_returns_404_with_mongo(mongo_api):
    response = mongo_api.get("/extractions/id-inexistente")

    assert response.status_code == 404