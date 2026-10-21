"""Ejemplos de lo que devuelve el Extractor (POST /api/v1/extraer)."""

EXTRACTOR_RESPONSE = {
    "texto": (
        "# Guía de Scrum\n\n"
        "Scrum es un marco de trabajo liviano que ayuda a generar valor.\n\n"
        "## Teoría de Scrum\n\n"
        "Transparencia, inspección y adaptación."
    ),
    "metadatos": {
        "nombre_archivo": "2020-Scrum-Guide-Spanish-Latin-South-American.pdf",
        "tamanio_bytes": 314572,
        "cantidad_paginas": 16,
        "tiempo_procesamiento_ms": 41.0,
    },
}


def to_persistence_payload(extractor_response: dict) -> dict:
    """Traduce la respuesta del Extractor al DTO de Persistence, como lo hará el Orchestrator."""
    metadatos = extractor_response["metadatos"]
    return {
        "file_name": metadatos["nombre_archivo"],
        "text": extractor_response["texto"],
        "page_count": metadatos["cantidad_paginas"],
    }