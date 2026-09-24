"""Casos de uso del microservicio: guardar y consultar resultados de extracción.

No deben conocer FastAPI ni detalles de MongoDB.
"""

from typing import Protocol


class ExtractionRepository(Protocol):
    def save(self, extraction: dict) -> str:
        """Persiste la extracción y devuelve su identificador."""
        ...

    def get(self, extraction_id: str) -> dict | None:
        """Devuelve la extracción con ese identificador, o None si no existe."""
        ...


class ExtractionNotFoundError(Exception):
    """No existe una extracción con el identificador solicitado."""


class ExtractionService:
    def __init__(self, repository: ExtractionRepository) -> None:
        self._repository = repository

    def create(self, file_name: str, text: str, page_count: int) -> str:
        return self._repository.save(
            {"file_name": file_name, "text": text, "page_count": page_count}
        )

    def get(self, extraction_id: str) -> dict:
        extraction = self._repository.get(extraction_id)
        if extraction is None:
            raise ExtractionNotFoundError(extraction_id)
        return extraction
