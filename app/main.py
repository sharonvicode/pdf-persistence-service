"""Punto de entrada del microservicio PDF ExtractText Persistence.

Aquí se crea y configura la aplicación FastAPI (routers, manejo de errores, etc.)
y se ensamblan las dependencias concretas de cada capa.
"""

from fastapi import FastAPI

from app.api.routes import router
from app.application.services import ExtractionService
from app.infrastructure.database import EXTRACTIONS_COLLECTION, get_database
from app.infrastructure.repositories import MongoExtractionRepository

app = FastAPI(title="PDF ExtractText Persistence")
repository = MongoExtractionRepository(get_database()[EXTRACTIONS_COLLECTION])
app.state.extraction_service = ExtractionService(repository)
app.include_router(router)