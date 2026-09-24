"""Casos de uso del microservicio: guardar y consultar resultados de extracción.

No deben conocer FastAPI ni detalles de MongoDB.
"""

from dataclasses import dataclass
from typing import Protocol
from uuid import uuid4


@dataclass(frozen=True)
class Extraction:
    id: str
    file_name: str
    text: str
    page_count: int


class ExtractionNotFoundError(Exception):
    """No existe una extracción con el identificador solicitado."""


class ExtractionRepository(Protocol):
    def save(self, extraction: Extraction) -> None:
        """Persiste la extracción."""
        ...

    def get(self, extraction_id: str) -> Extraction | None:
        """Devuelve la extracción con ese identificador, o None si no existe."""
        ...


class ExtractionService:
    def __init__(self, repository: ExtractionRepository) -> None:
        self._repository = repository

    def create(self, file_name: str, text: str, page_count: int) -> Extraction:
        extraction = Extraction(
            id=str(uuid4()), file_name=file_name, text=text, page_count=page_count
        )
        self._repository.save(extraction)
        return extraction

    def get(self, extraction_id: str) -> Extraction:
        extraction = self._repository.get(extraction_id)
        if extraction is None:
            raise ExtractionNotFoundError(extraction_id)
        return extraction
