"""Contrato del docker-compose.yml: Persistence se registra en su propio Consul."""

from pathlib import Path

import pytest
import yaml

COMPOSE_FILE = Path(__file__).resolve().parent.parent / "docker-compose.yml"


@pytest.fixture(scope="module")
def services() -> dict:
    return yaml.safe_load(COMPOSE_FILE.read_text(encoding="utf-8"))["services"]


def test_compose_includes_consul_and_mongo(services):
    assert "consul" in services
    assert "mongo" in services


def test_persistence_registers_in_consul(services):
    environment = services["persistence"]["environment"]

    assert environment["CONSUL_URL"] == "http://consul:8500"
    assert environment["CONSUL_SERVICE_NAME"] == "persistence"


def test_persistence_uses_the_compose_mongo(services):
    assert services["persistence"]["environment"]["MONGODB_URI"] == "mongodb://mongo:27017"


def test_persistence_waits_for_consul(services):
    assert services["persistence"]["depends_on"]["consul"]["condition"] == "service_healthy"