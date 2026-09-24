"""Punto de entrada del microservicio PDF ExtractText Persistence.

Aquí se crea y configura la aplicación FastAPI (routers, manejo de errores, etc.).
"""

from fastapi import FastAPI

from app.api.routes import router

app = FastAPI(title="PDF ExtractText Persistence")
app.include_router(router)
