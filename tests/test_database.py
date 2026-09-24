"""Tests de la configuración de MongoDB por variables de entorno."""

from app.infrastructure.database import get_database


def test_get_database_uses_env_variable(monkeypatch):
    monkeypatch.setenv("MONGODB_DATABASE", "base_de_prueba")

    assert get_database().name == "base_de_prueba"


def test_get_database_uses_default_name_when_env_missing(monkeypatch):
    monkeypatch.delenv("MONGODB_DATABASE", raising=False)

    assert get_database().name == "pdf_extractext"