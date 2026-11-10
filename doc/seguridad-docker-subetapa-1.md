# Seguridad Docker — Subetapa 1: `.dockerignore`

## Objetivo

Incorporar un archivo `.dockerignore` para reducir el contexto enviado al proceso de construcción Docker del microservicio Persistence. La medida evita que archivos locales, cachés y configuraciones que podrían contener secretos se incluyan innecesariamente en ese contexto.

## Situación inicial

Antes de esta subetapa no existían ni `.dockerignore` ni el directorio `doc/` en la raíz del repositorio. El servicio `persistence` de `docker-compose.yml` usa `build: .`, por lo que el contexto de construcción es la raíz del repositorio.

El Dockerfile actual sólo copia al contexto de la imagen los archivos `pyproject.toml`, `uv.lock` y el directorio `app/`. No copia los tests, documentación, archivos de entorno ni artefactos de desarrollo. Sin `.dockerignore`, sin embargo, Docker debía enviar esos archivos al daemon como parte del contexto antes de procesar las instrucciones `COPY`.

## Implementación

Se creó `.dockerignore` en la raíz del contexto de construcción. Sus reglas son deliberadamente acotadas y se basan en los archivos que el Dockerfile actual consume.

| Regla | Motivo |
| --- | --- |
| `.git/` | El historial y metadatos de Git no se usan para construir ni ejecutar el servicio. |
| `.venv/`, `venv/`, `env/` | Son entornos locales; la imagen crea su propia virtualenv mediante `uv sync`. |
| `**/__pycache__/`, `**/*.py[cod]` | Son bytecode y cachés generados localmente, no código fuente. El prefijo `**/` se agregó en la auditoría final: sin él, las reglas sólo aplicaban a la raíz del contexto y no a `app/`. |
| `.pytest_cache/`, `.mypy_cache/`, `.ruff_cache/`, `.coverage`, `htmlcov/` | Son resultados y cachés de herramientas de calidad y pruebas. |
| `.env`, `.env.*` | Evitan enviar configuraciones locales que pueden contener secretos. |
| `!.env.example` | Conserva la plantilla versionada, que no contiene secretos y documenta variables esperadas. |
| `tests/` | El Dockerfile de producción actual no copia ni ejecuta las pruebas. |
| `doc/`, `README.md`, `TASKS.md`, `docker-compose.yml` | Son documentación y configuración de desarrollo/orquestación que el Dockerfile actual no consume. |
| Temporales, IDE y SO | `*.log`, `*.tmp`, `*.swp`, `.vscode/`, `.idea/`, `.DS_Store` y `Thumbs.db` no intervienen en el build. |

No se excluyen `pyproject.toml`, `uv.lock` ni `app/`, porque el Dockerfile los necesita explícitamente. Tampoco se excluye `Dockerfile`.

## Justificación técnica

El contexto de Docker puede contener información que no termina en la imagen final, pero que igualmente se transfiere al daemon durante el build. Excluir entornos virtuales, cachés y metadatos de Git reduce esa superficie de exposición y evita transferencias innecesarias.

La exclusión de `.env` y sus variantes protege frente a una copia accidental de credenciales, tokens o URIs locales si estos archivos aparecen en el directorio de trabajo. La excepción para `.env.example` conserva una plantilla no secreta; además, el Dockerfile actual no la copia a la imagen.

## Relación con Docker

Al ejecutar un build con contexto `.` —como lo hace el servicio `persistence` mediante `build: .`— Docker prepara los archivos de la raíz antes de evaluar las instrucciones del Dockerfile. `.dockerignore` filtra ese conjunto inicial. Por tanto, sus reglas afectan qué archivos pueden estar disponibles para las instrucciones `COPY` o `ADD` y qué datos se transfieren al daemon.

En el estado actual, las instrucciones necesarias siguen disponibles:

- `COPY pyproject.toml uv.lock ./`
- `COPY app ./app`

La subetapa no modifica dichas instrucciones ni el modo de ejecutar Uvicorn.

## Validaciones

Se realizaron las siguientes comprobaciones, sin construir imágenes ni iniciar o detener contenedores:

- Se verificó que la rama es `main`, que `HEAD` es `5219af3dd4b18a451fc658d475aded250af8ce75` y que no había cambios locales al inicio.
- Se confirmó que no existía `.dockerignore` antes de la implementación.
- Se confirmó que no existía el directorio `doc/` antes de la implementación.
- Se inspeccionaron Dockerfile, `docker-compose.yml`, `pyproject.toml`, `.env.example` y la estructura del proyecto.
- Se verificó que Compose utiliza la raíz mediante `build: .`.
- Se verificó que el Dockerfile sólo copia `pyproject.toml`, `uv.lock` y `app/`; ninguno está excluido.
- Se revisaron las reglas creadas para comprobar que no incorporan secretos.
- No se midió el tamaño del contexto ni se realizaron builds; por ello no se afirma una reducción cuantificada de tamaño ni de vulnerabilidades.

## Archivos modificados

- `.dockerignore` — creado.
- `doc/seguridad-docker-subetapa-1.md` — creado.

## Limitaciones

`.dockerignore` no corrige vulnerabilidades CVE de la imagen base ni de dependencias Python. Tampoco elimina secretos que ya estén presentes en capas de una imagen previamente construida, ni sustituye la gestión correcta de secretos en tiempo de ejecución.

La medida tampoco impide que un futuro cambio al Dockerfile copie explícitamente un archivo que no esté cubierto por una regla adecuada. Las reglas deben revisarse cada vez que cambie el contexto o las instrucciones `COPY`/`ADD`.

## Resultado

El repositorio ahora define un contexto de build más acotado, preservando los insumos necesarios para el Dockerfile actual y excluyendo datos locales y artefactos no requeridos. Esta subetapa no modifica el Dockerfile, las dependencias, la aplicación ni la configuración de Compose. No se realizó un análisis de vulnerabilidades ni se afirma una reducción de CVEs.

## Próxima subetapa

La siguiente etapa del plan será revisar el Dockerfile y evaluar una construcción multi-stage para reducir los componentes presentes en la imagen final.
