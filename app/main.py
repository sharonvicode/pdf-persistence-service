"""Punto de entrada del microservicio PDF ExtractText Persistence.

Aquí se crea y configura la aplicación FastAPI (routers, manejo de errores, etc.)
y se ensamblan las dependencias concretas de cada capa.
"""

from fastapi import FastAPI

from app.api.routes import router
from app.application.services import ExtractionService
from app.infrastructure.repositories import InMemoryExtractionRepository

app = FastAPI(title="PDF ExtractText Persistence")
app.state.extraction_service = ExtractionService(InMemoryExtractionRepository())
app.include_router(router)
