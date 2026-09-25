"""Implementaciones de los repositorios definidos en la capa de aplicación."""

from pymongo.collection import Collection

from app.application.services import Extraction

class InMemoryExtractionRepository:
    """Repositorio en memoria, usado en los tests unitarios."""

    def __init__(self) -> None:
        self._extractions: dict[str, Extraction] = {}

    def save(self, extraction: Extraction) -> None:
        self._extractions[extraction.id] = extraction

    def get(self, extraction_id: str) -> Extraction | None:
        return self._extractions.get(extraction_id)


class MongoExtractionRepository:
    """Repositorio que persiste las extracciones en MongoDB."""

    def __init__(self, collection: Collection) -> None:
        self._collection = collection

    def save(self, extraction: Extraction) -> None:
        self._collection.insert_one(
            {
                "_id": extraction.id,
                "file_name": extraction.file_name,
                "text": extraction.text,
                "page_count": extraction.page_count,
            }
        )

    def get(self, extraction_id: str) -> Extraction | None:
        document = self._collection.find_one({"_id": extraction_id})
        if document is None:
            return None
        return Extraction(
            id=document["_id"],
            file_name=document["file_name"],
            text=document["text"],
            page_count=document["page_count"],
        )