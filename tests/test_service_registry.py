"""Registro de Persistence en Consul (descubrimiento de servicios).

Un Consul falso responde por HTTP real, así los tests verifican los pedidos
que el servicio le envía a la API de Consul.
"""

import json
import socket
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import logging
from fastapi.testclient import TestClient
from app.main import app
import pytest

from app.infrastructure.service_registry import (
    ConsulRegistry,
    ServiceRegistration,
    ServiceRegistryError,
    build_registration,
)

REGISTRATION = ServiceRegistration(
    service_id="persistence-abc123",
    name="persistence",
    address="172.18.0.5",
    port=8000,
)


class _FakeConsulHandler(BaseHTTPRequestHandler):
    def do_PUT(self):
        length = int(self.headers.get("Content-Length", 0))
        body = json.loads(self.rfile.read(length)) if length else None
        self.server.received.append((self.path, body))
        self.send_response(self.server.status)
        self.end_headers()

    def log_message(self, *args):
        pass


class FakeConsul:
    def __init__(self) -> None:
        self._server = ThreadingHTTPServer(("127.0.0.1", 0), _FakeConsulHandler)
        self._server.received = []
        self._server.status = 200
        threading.Thread(target=self._server.serve_forever, daemon=True).start()

    @property
    def url(self) -> str:
        return f"http://127.0.0.1:{self._server.server_port}"

    @property
    def received(self) -> list:
        return self._server.received

    def answer_with(self, status: int) -> None:
        self._server.status = status

    def stop(self) -> None:
        self._server.shutdown()
        self._server.server_close()


@pytest.fixture
def consul():
    fake = FakeConsul()
    yield fake
    fake.stop()


def test_registers_the_service_with_a_health_check(consul):
    ConsulRegistry(consul.url).register(REGISTRATION)

    assert consul.received == [
        (
            "/v1/agent/service/register",
            {
                "ID": "persistence-abc123",
                "Name": "persistence",
                "Address": "172.18.0.5",
                "Port": 8000,
                "Check": {
                    "HTTP": "http://172.18.0.5:8000/health",
                    "Interval": "10s",
                    "Timeout": "5s",
                    "DeregisterCriticalServiceAfter": "1m",
                },
            },
        )
    ]


def test_deregisters_the_service(consul):
    ConsulRegistry(consul.url).deregister("persistence-abc123")

    assert consul.received == [("/v1/agent/service/deregister/persistence-abc123", None)]


def test_rejected_registration_raises(consul):
    consul.answer_with(500)

    with pytest.raises(ServiceRegistryError):
        ConsulRegistry(consul.url).register(REGISTRATION)


def test_unreachable_consul_raises():
    with pytest.raises(ServiceRegistryError):
        ConsulRegistry("http://127.0.0.1:1").register(REGISTRATION)


def test_build_registration_uses_hostname_and_env(monkeypatch):
    monkeypatch.setattr(socket, "gethostname", lambda: "abc123")
    monkeypatch.setattr(socket, "gethostbyname", lambda host: "172.18.0.5")
    monkeypatch.setenv("CONSUL_SERVICE_NAME", "persistence")
    monkeypatch.setenv("SERVICE_PORT", "8000")

    assert build_registration() == REGISTRATION


def test_build_registration_defaults(monkeypatch):
    monkeypatch.setattr(socket, "gethostname", lambda: "abc123")
    monkeypatch.setattr(socket, "gethostbyname", lambda host: "172.18.0.5")
    monkeypatch.delenv("CONSUL_SERVICE_NAME", raising=False)
    monkeypatch.delenv("SERVICE_PORT", raising=False)

    assert build_registration() == REGISTRATION
    

def test_registers_on_startup_and_deregisters_on_shutdown(consul, monkeypatch):
    monkeypatch.setenv("CONSUL_URL", consul.url)

    with TestClient(app):
        assert [path for path, _ in consul.received] == ["/v1/agent/service/register"]

    assert consul.received[-1][0].startswith("/v1/agent/service/deregister/persistence-")


def test_without_consul_url_does_not_register(consul, monkeypatch):
    monkeypatch.delenv("CONSUL_URL", raising=False)

    with TestClient(app) as client:
        assert client.get("/health").status_code == 200

    assert consul.received == []


def test_does_not_start_when_consul_is_unreachable(monkeypatch):
    monkeypatch.setenv("CONSUL_URL", "http://127.0.0.1:1")

    with pytest.raises(ServiceRegistryError):
        with TestClient(app):
            pass


def test_failed_deregistration_does_not_break_shutdown(consul, monkeypatch, caplog):
    monkeypatch.setenv("CONSUL_URL", consul.url)

    with caplog.at_level(logging.WARNING):
        with TestClient(app):
            consul.answer_with(500)

    assert "Consul" in caplog.text