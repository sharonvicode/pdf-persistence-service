"""Punto de entrada del microservicio PDF ExtractText Persistence.

Aquí se crea y configura la aplicación FastAPI (routers, manejo de errores, etc.)
y se ensamblan las dependencias concretas de cada capa.
"""
import logging
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.routes import router
from app.application.services import ExtractionService
from app.infrastructure.database import EXTRACTIONS_COLLECTION, get_database
from app.infrastructure.repositories import MongoExtractionRepository
from app.infrastructure.service_registry import (
    ConsulRegistry,
    ServiceRegistryError,
    build_registration,
    get_consul_url,
)


logger = logging.getLogger(__name__)


@asynccontextmanager
async def consul_lifespan(_: FastAPI) -> AsyncIterator[None]:
    """Registra la réplica en Consul al arrancar y la da de baja al apagar."""
    consul_url = get_consul_url()
    if consul_url is None:
        yield
        return

    registry = ConsulRegistry(consul_url)
    registration = build_registration()
    # Si Consul no responde, el servicio no arranca: nadie lo encontraría.
    registry.register(registration)
    try:
        yield
    finally:
        try:
            registry.deregister(registration.service_id)
        except ServiceRegistryError:
            # Consul lo borra igual cuando su health check queda en rojo.
            logger.warning("No se pudo dar de baja la réplica en Consul", exc_info=True)

app = FastAPI(title="PDF ExtractText Persistence", lifespan=consul_lifespan)
repository = MongoExtractionRepository(get_database()[EXTRACTIONS_COLLECTION])
app.state.extraction_service = ExtractionService(repository)
app.include_router(router)