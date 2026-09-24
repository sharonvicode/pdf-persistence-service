"""Casos de uso del microservicio: guardar y consultar resultados de extracción.

No deben conocer FastAPI ni detalles de MongoDB.
"""

from typing import Protocol


class ExtractionRepository(Protocol):
    def save(self, extraction: dict) -> str:
        """Persiste la extracción y devuelve su identificador."""
        ...


class ExtractionService:
    def __init__(self, repository: ExtractionRepository) -> None:
        self._repository = repository

    def create(self, file_name: str, text: str, page_count: int) -> str:
        return self._repository.save(
            {"file_name": file_name, "text": text, "page_count": page_count}
        )
