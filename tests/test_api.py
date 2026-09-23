"""Tests de la API."""

from app.main import app


def test_app_is_created():
    assert app.title == "PDF ExtractText Persistence"
