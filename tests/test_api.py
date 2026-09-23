"""Tests de la API."""

import pytest
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)

VALID_PAYLOAD = {
    "file_name": "documento.pdf",
    "text": "Texto extraído del PDF.",
    "page_count": 3,
}


def test_app_is_created():
    assert app.title == "PDF ExtractText Persistence"


def test_create_extraction_returns_201_with_id():
    response = client.post("/extractions", json=VALID_PAYLOAD)

    assert response.status_code == 201
    body = response.json()
    assert isinstance(body["id"], str)
    assert body["id"]


@pytest.mark.parametrize(
    "payload",
    [
        pytest.param({}, id="body_vacio"),
        pytest.param({k: v for k, v in VALID_PAYLOAD.items() if k != "file_name"}, id="sin_file_name"),
        pytest.param({k: v for k, v in VALID_PAYLOAD.items() if k != "text"}, id="sin_text"),
        pytest.param({k: v for k, v in VALID_PAYLOAD.items() if k != "page_count"}, id="sin_page_count"),
        pytest.param({**VALID_PAYLOAD, "file_name": ""}, id="file_name_vacio"),
        pytest.param({**VALID_PAYLOAD, "page_count": -1}, id="page_count_negativo"),
        pytest.param({**VALID_PAYLOAD, "page_count": "tres"}, id="page_count_no_entero"),
    ],
)
def test_create_extraction_rejects_invalid_data_with_422(payload):
    response = client.post("/extractions", json=payload)

    assert response.status_code == 422
