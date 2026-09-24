"""Tests del repositorio MongoDB (necesitan MongoDB levantado)."""

from app.application.services import Extraction
from app.infrastructure.repositories import MongoExtractionRepository

EXTRACTION = Extraction(
    id="abc-123", file_name="documento.pdf", text="Texto extraído del PDF.", page_count=3
)


def test_save_and_get_returns_same_extraction(mongo_collection):
    repository = MongoExtractionRepository(mongo_collection)

    repository.save(EXTRACTION)

    assert repository.get(EXTRACTION.id) == EXTRACTION


def test_get_returns_none_when_not_found(mongo_collection):
    repository = MongoExtractionRepository(mongo_collection)

    assert repository.get("id-inexistente") is None


def test_extraction_persists_across_repository_instances(mongo_collection):
    MongoExtractionRepository(mongo_collection).save(EXTRACTION)

    other_repository = MongoExtractionRepository(mongo_collection)

    assert other_repository.get(EXTRACTION.id) == EXTRACTION