"""Implementaciones de los repositorios definidos en la capa de aplicación."""

from app.application.services import Extraction


class InMemoryExtractionRepository:
    """Repositorio en memoria, provisorio hasta integrar MongoDB."""

    def __init__(self) -> None:
        self._extractions: dict[str, Extraction] = {}

    def save(self, extraction: Extraction) -> None:
        self._extractions[extraction.id] = extraction

    def get(self, extraction_id: str) -> Extraction | None:
        return self._extractions.get(extraction_id)
