# Seguridad Docker — Subetapa 2: construcción multi-stage

## Objetivo

Separar la instalación de dependencias de la imagen de ejecución del microservicio Persistence. `uv` debe utilizarse únicamente durante la construcción y no formar parte de la imagen final.

## Situación inicial y problema identificado

El Dockerfile anterior partía de `python:3.12-slim`, copiaba `uv` a `/bin/uv`, ejecutaba `uv sync --frozen --no-dev --no-install-project` y, posteriormente, arrancaba Uvicorn desde el mismo stage. Por ello, el binario `uv`, requerido para construir el entorno virtual, permanecía disponible en la imagen de ejecución aunque el proceso de inicio no lo utiliza.

El entorno creado por `uv` ya se ubicaba en `/service/.venv` y el comando de ejecución usaba `uvicorn` a través de `PATH=/service/.venv/bin:$PATH`.

## Implementación realizada

El Dockerfile quedó organizado en tres stages:

1. `base`: define `python:3.12-slim`, `PYTHONUNBUFFERED=1`, el `PATH` de `/service/.venv/bin` y el directorio de trabajo `/service`.
2. `builder`: deriva de `base`, incorpora `uv` desde `ghcr.io/astral-sh/uv:0.11`, establece `UV_LINK_MODE=copy`, copia `pyproject.toml` y `uv.lock`, y ejecuta `uv sync --frozen --no-dev --no-install-project`.
3. `runtime`: deriva de `base`, copia solamente `/service/.venv` desde `builder` y el directorio `app/` desde el contexto de build. Conserva el puerto 8000 y el comando de Uvicorn preexistente.

## Separación entre builder y runtime

| Stage | Responsabilidad | Componentes relevantes |
| --- | --- | --- |
| `builder` | Construir el entorno de producción bloqueado | `uv`, `UV_LINK_MODE=copy`, `pyproject.toml`, `uv.lock`, `/service/.venv` |
| `runtime` | Ejecutar el microservicio | Python 3.12, `/service/.venv`, `app/`, `PYTHONUNBUFFERED`, `PATH`, Uvicorn |

El único artefacto transferido desde `builder` a `runtime` es `/service/.venv`. El código de aplicación se copia directamente como `app/` en `runtime`.

No se transfieren a la imagen final el binario `/bin/uv`, la variable de instalación `UV_LINK_MODE=copy`, `pyproject.toml` ni `uv.lock`.

## Justificación técnica de la base común

`builder` y `runtime` derivan de la misma etapa `base`, basada en `python:3.12-slim`. Así, el entorno virtual se genera y ejecuta con la misma familia de intérprete y de bibliotecas del sistema dentro de la misma construcción. Esto preserva la compatibilidad de los scripts del entorno virtual y de dependencias que puedan contener extensiones nativas.

El proyecto declara `requires-python = ">=3.12"` y el lockfile también declara `requires-python = ">=3.12"`. La implementación mantiene Python 3.12, `uv sync --frozen`, `--no-dev` y `--no-install-project`; por tanto, no modifica la resolución bloqueada en `uv.lock` ni incorpora dependencias de desarrollo.

## Alcance y archivos modificados

- `Dockerfile` — modificado para usar los stages `base`, `builder` y `runtime`.
- `doc/seguridad-docker-subetapa-2.md` — creado para documentar esta subetapa.

No se modificaron la aplicación Python, `pyproject.toml`, `uv.lock`, `docker-compose.yml`, `.dockerignore`, variables de entorno ni el comando de inicio. Esta subetapa no incorpora un usuario no root; ese cambio corresponde a la Subetapa 4.

## Validaciones realizadas

Se realizaron comprobaciones estáticas, sin construir imágenes ni iniciar contenedores:

- Se revisó el Dockerfile resultante.
- Se comprobó que la copia de `uv` y `UV_LINK_MODE=copy` están únicamente en `builder`.
- Se comprobó que `runtime` copia `/service/.venv` desde `builder` y `app/` desde el contexto.
- Se comprobó que se preservan Python 3.12, `/service`, `/service/.venv`, `PYTHONUNBUFFERED=1`, el `PATH`, `EXPOSE 8000` y el comando de Uvicorn existente.
- Se verificó la integridad de espacios en blanco con `git diff --check`.
- Se revisó el estado de Git para confirmar que sólo cambiaron los archivos autorizados.

## Validaciones pendientes

No se construyó la imagen ni se ejecutaron contenedores en esta subetapa. Permanecen pendientes, para una fase autorizada posterior:

- Construir la imagen y verificar que el stage `runtime` no contiene `/bin/uv`.
- Iniciar el servicio y comprobar `GET /health`.
- Verificar la conectividad con MongoDB y el registro en Consul mediante la configuración existente.
- Ejecutar las pruebas pertinentes.
- Medir el tamaño final de imagen, si se requiere una comparación cuantitativa.

## Limitaciones

No se realizó un escaneo de vulnerabilidades ni se midió el tamaño de ninguna imagen. Por tanto, esta subetapa no afirma reducciones de CVE ni mejoras cuantificadas de tamaño. La separación elimina `uv` de la etapa final por diseño, pero las mediciones y la validación en ejecución requieren una fase posterior autorizada.

## Relación con la Subetapa 3

Esta subetapa limita la imagen de ejecución a Python, el entorno virtual de producción y la aplicación. La Subetapa 3 podrá revisar de manera independiente los siguientes controles de seguridad definidos en el plan, sin alterar la separación lograda aquí.
