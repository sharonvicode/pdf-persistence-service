"""Registro del servicio en Consul (descubrimiento de servicios).

Solo infraestructura: la lógica de negocio no sabe nada de Consul.
"""

import os
import socket
from dataclasses import dataclass

import requests

DEFAULT_SERVICE_NAME = "persistence"
DEFAULT_SERVICE_PORT = 8000
REQUEST_TIMEOUT_SECONDS = 5


class ServiceRegistryError(Exception):
    """Consul no respondió o rechazó el pedido."""


@dataclass(frozen=True)
class ServiceRegistration:
    service_id: str
    name: str
    address: str
    port: int


def get_consul_url() -> str | None:
    """URL de Consul (CONSUL_URL). Sin ella, el servicio no se registra."""
    return os.getenv("CONSUL_URL")


def build_registration() -> ServiceRegistration:
    """Describe esta réplica: id y dirección propios, así cada réplica se registra aparte."""
    name = os.getenv("CONSUL_SERVICE_NAME", DEFAULT_SERVICE_NAME)
    hostname = socket.gethostname()
    return ServiceRegistration(
        service_id=f"{name}-{hostname}",
        name=name,
        address=socket.gethostbyname(hostname),
        port=int(os.getenv("SERVICE_PORT", DEFAULT_SERVICE_PORT)),
    )


class ConsulRegistry:
    """Cliente de la API de Consul para registrar y dar de baja el servicio."""

    def __init__(self, consul_url: str) -> None:
        self._consul_url = consul_url.rstrip("/")

    def register(self, registration: ServiceRegistration) -> None:
        """Registra el servicio con un health check HTTP sobre /health."""
        self._put(
            "/v1/agent/service/register",
            {
                "ID": registration.service_id,
                "Name": registration.name,
                "Address": registration.address,
                "Port": registration.port,
                "Check": {
                    "HTTP": f"http://{registration.address}:{registration.port}/health",
                    "Interval": "10s",
                    "Timeout": "5s",
                    "DeregisterCriticalServiceAfter": "1m",
                },
            },
        )

    def deregister(self, service_id: str) -> None:
        """Da de baja el servicio en Consul."""
        self._put(f"/v1/agent/service/deregister/{service_id}")

    def _put(self, path: str, payload: dict | None = None) -> None:
        try:
            response = requests.put(
                f"{self._consul_url}{path}", json=payload, timeout=REQUEST_TIMEOUT_SECONDS
            )
            response.raise_for_status()
        except requests.RequestException as exc:
            raise ServiceRegistryError(f"Consul no respondió a {path}: {exc}") from exc