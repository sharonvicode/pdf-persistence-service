"""Implementaciones de los repositorios definidos en la capa de aplicación."""

from uuid import uuid4


class InMemoryExtractionRepository:
    """Repositorio en memoria, provisorio hasta integrar MongoDB."""

    def __init__(self) -> None:
        self._extractions: dict[str, dict] = {}

    def save(self, extraction: dict) -> str:
        extraction_id = str(uuid4())
        self._extractions[extraction_id] = extraction
        return extraction_id
