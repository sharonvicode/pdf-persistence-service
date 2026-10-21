"""Tests del repositorio MongoDB (necesitan MongoDB levantado)."""
import pytest

from app.application.services import Extraction, ExtractionTooLargeError
from app.infrastructure.repositories import MongoExtractionRepository
from tests.payloads import OVERSIZED_TEXT

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
    
def test_save_raises_too_large_error_when_text_exceeds_mongo_limit(mongo_collection):
    repository = MongoExtractionRepository(mongo_collection)
    extraction = Extraction(id="grande", file_name="grande.pdf", text=OVERSIZED_TEXT, page_count=1)

    with pytest.raises(ExtractionTooLargeError):
        repository.save(extraction)