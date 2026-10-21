"""Persistence guarda los resultados del Extractor sin modificarlos (MongoDB real)."""
from tests.payloads import OVERSIZED_TEXT

import pytest

from tests.extractor_samples import EXTRACTOR_RESPONSE, to_persistence_payload

LARGE_MARKDOWN = "".join(
    f"# Página {n}\n\n" + "Texto extraído del PDF con acentos: áéíóú ñ. " * 50 + "\n\n"
    for n in range(1, 91)
)


def save_and_get(mongo_api, payload):
    created = mongo_api.post("/extractions", json=payload)
    assert created.status_code == 201
    return mongo_api.get(f"/extractions/{created.json()['id']}")


def test_saves_extractor_result_and_returns_it_unchanged(mongo_api):
    payload = to_persistence_payload(EXTRACTOR_RESPONSE)

    response = save_and_get(mongo_api, payload)

    assert response.status_code == 200
    assert response.json() == {"id": response.json()["id"], **payload}


@pytest.mark.parametrize(
    "text",
    [
        pytest.param("# Título\n\nPárrafo uno.\n\n## Subtítulo\n\nPárrafo dos.", id="markdown"),
        pytest.param("Acentos áéíóú, eñe ñÑ, comillas «» y símbolos €°", id="caracteres_especiales"),
        pytest.param(LARGE_MARKDOWN, id="texto_largo_90_paginas"),
    ],
)
def test_preserves_text_exactly(mongo_api, text):
    payload = {**to_persistence_payload(EXTRACTOR_RESPONSE), "text": text}

    response = save_and_get(mongo_api, payload)

    assert response.json()["text"] == text


def test_accepts_file_name_with_spaces_and_accents(mongo_api):
    payload = {**to_persistence_payload(EXTRACTOR_RESPONSE), "file_name": "Filosofía Lean.pdf"}

    response = save_and_get(mongo_api, payload)

    assert response.json()["file_name"] == "Filosofía Lean.pdf"


def test_ignores_extra_extractor_metadata(mongo_api):
    payload = {**to_persistence_payload(EXTRACTOR_RESPONSE), "tamanio_bytes": 314572}

    response = save_and_get(mongo_api, payload)

    assert "tamanio_bytes" not in response.json()
    
def test_rejects_text_larger_than_mongo_limit_with_413(mongo_api):
    payload = {**to_persistence_payload(EXTRACTOR_RESPONSE), "text": OVERSIZED_TEXT}

    response = mongo_api.post("/extractions", json=payload)

    assert response.status_code == 413