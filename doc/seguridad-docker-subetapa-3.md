# Seguridad Docker — Subetapa 3: base Debian Trixie explícita

## Objetivo

Especificar explícitamente Debian 13 Trixie como base de la imagen del microservicio Persistence, manteniendo Python 3.12 y la construcción multi-stage introducida en la Subetapa 2.

## Imagen anterior y seleccionada

La imagen base anterior era `python:3.12-slim`. La imagen seleccionada es `python:3.12-slim-trixie`.

Trixie es Debian 13. La etiqueta explícita documenta la distribución elegida y evita depender de que la etiqueta genérica `python:3.12-slim` siga apuntando a la misma variante Debian en el futuro.

La etiqueta `python:3.12-slim-trixie` sigue siendo móvil respecto de actualizaciones de la imagen y no se fijó un digest SHA256 en esta subetapa. Por ello, la selección explicita la distribución, pero no inmoviliza el contenido exacto de la imagen.

## Alternativas evaluadas

Durante la auditoría se evaluaron la etiqueta genérica `python:3.12-slim`, la variante explícita `python:3.12-slim-bookworm` y la variante explícita `python:3.12-slim-trixie`.

- La etiqueta genérica no expresa la distribución Debian y puede cambiar de destino.
- Bookworm mantiene soporte, pero corresponde a la anterior distribución estable de Debian.
- Trixie es Debian 13 y fue seleccionada como variante explícita de la distribución estable actual, sin cambiar de familia de sistema operativo ni de versión de Python.

No se adoptó Alpine, porque esta subetapa se limita a especificar la variante Debian y no busca cambiar las bibliotecas de sistema ni el modelo de compatibilidad de dependencias nativas.

## Conservación de Python y de multi-stage

Se conserva Python 3.12, compatible con el requisito `requires-python = ">=3.12"` del proyecto y del lockfile. No se modificaron `pyproject.toml`, `uv.lock` ni las dependencias.

La estructura multi-stage se preserva sin cambios:

| Stage | Base o función |
| --- | --- |
| `base` | `python:3.12-slim-trixie`, directorio `/service`, `PYTHONUNBUFFERED` y `PATH` del entorno virtual |
| `builder` | Hereda de `base`; contiene `uv` y ejecuta `uv sync --frozen --no-dev --no-install-project` |
| `runtime` | Hereda de `base`; recibe `/service/.venv` desde `builder` y `app/` desde el contexto |

Mantener `builder` y `runtime` sobre la misma base conserva la misma familia de intérprete y bibliotecas del sistema para crear y ejecutar `/service/.venv`.

## Compatibilidad

La compatibilidad esperada se basa en que se mantiene Python 3.12, el lockfile, el comando de Uvicorn y la base Debian slim en ambas etapas. Esto favorece la ejecución de dependencias con extensiones nativas presentes en el lockfile, como `pydantic-core`, `httptools` y `uvloop`.

La compatibilidad no fue comprobada en ejecución: no se construyó la imagen ni se iniciaron contenedores. Por ello no se afirma que el cambio haya sido validado contra todas las arquitecturas, bibliotecas compartidas o escenarios de ejecución.

## Riesgos identificados

- El cambio de variante Debian puede modificar versiones de bibliotecas del sistema requeridas por extensiones nativas.
- La etiqueta seleccionada sigue siendo móvil; una reconstrucción futura puede recibir actualizaciones distintas.
- No fijar un digest prioriza recibir actualizaciones de la etiqueta, pero no ofrece reproducibilidad inmutable por sí solo.
- No se realizaron escaneos de vulnerabilidades ni mediciones de imagen; no se afirma reducción de CVE ni de tamaño.

## Archivos modificados

- `Dockerfile` — se reemplazó exclusivamente la imagen de la etapa `base` por `python:3.12-slim-trixie`.
- `doc/seguridad-docker-subetapa-3.md` — creado para documentar esta subetapa.

No se modificaron la aplicación, Docker Compose, `.dockerignore`, dependencias, lockfile, variables de entorno, rutas, puerto ni comando de inicio. No se incorporó un usuario no root.

## Validaciones realizadas

Se realizaron únicamente comprobaciones estáticas:

- Se verificó que `base` declara `python:3.12-slim-trixie`.
- Se verificó que `builder` y `runtime` continúan heredando de `base`.
- Se verificó que se conservan la copia de `uv` sólo en `builder`, `uv sync --frozen --no-dev --no-install-project`, la transferencia de `/service/.venv`, la copia de `app/`, variables, rutas, puerto y comando de Uvicorn.
- Se revisó este documento.
- Se ejecutó `git diff --check`.
- Se revisó el estado de Git y el alcance de archivos modificados.

## Validaciones pendientes

En una fase posterior autorizada deben realizarse, como mínimo:

- Build de la imagen para la arquitectura objetivo.
- Confirmación de que `uv sync --frozen` resuelve sin modificar el lockfile.
- Prueba de importación y ejecución de dependencias con extensiones nativas.
- Verificación de `GET /health`, conectividad con MongoDB y registro en Consul.
- Ejecución de pruebas aplicables.
- Evaluación de tamaño, vulnerabilidades y, si corresponde, una política de digest y su actualización.

## Relación con las subetapas siguientes

Esta subetapa deja una base Debian explícita y conserva la separación entre construcción y ejecución de la Subetapa 2. Las subetapas posteriores pueden aplicar controles adicionales de manera independiente; en particular, no se introdujo todavía la ejecución con usuario no root, prevista para la Subetapa 4.
