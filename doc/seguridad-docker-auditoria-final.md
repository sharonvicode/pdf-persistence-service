# Seguridad Docker — Auditoría final y cierre

## Objetivo

Registrar el estado real de la imagen y de la configuración Docker del microservicio Persistence después de las subetapas 1 a 4: pruebas reales que habían quedado pendientes, escaneo de vulnerabilidades, correcciones aplicadas y riesgos que permanecen.

Este documento no afirma que la imagen esté libre de vulnerabilidades. Los resultados corresponden a las herramientas y a la fecha indicadas.

## Herramientas y fecha

| Herramienta | Versión | Fuente de datos | Fecha |
| --- | --- | --- | --- |
| Trivy (imagen `aquasec/trivy`) | 0.76.2 | Base de vulnerabilidades de Trivy, actualizada el 2026-11-10 19:01 UTC | 2026-11-10 |
| `uv audit` (experimental) | uv 0.11.2 | OSV | 2026-11-10 |

Trivy se ejecutó sobre un archivo generado con `docker save`, montado en modo lectura y sin acceso al socket de Docker. Docker Scout no se utilizó porque exige iniciar sesión.

## Pruebas reales pendientes de las subetapas 1 a 4

Las subetapas anteriores dejaron pendiente la validación con un build y un arranque reales. Se ejecutaron y pasaron:

| Prueba | Resultado |
| --- | --- |
| Construcción de la imagen multi-stage sobre `python:3.12-slim-trixie` | Correcta |
| Disponibilidad de `groupadd` y `useradd` en la base | Correcta |
| Proceso principal como `appuser` | `uid=999(appuser) gid=999(appgroup)`; PID 1 es Uvicorn |
| `appuser` sin escritura sobre `/service/app` | Correcto (`Permission denied`) |
| `GET /health` | HTTP 200 `{"status":"ok"}` |
| Conexión con MongoDB (`POST` y `GET /extractions`) | HTTP 201 y 200; datos recuperados iguales a los enviados |
| Registro en Consul y check HTTP de `/health` | Instancia registrada con el hostname del contenedor; check `passing` |

## Vulnerabilidades encontradas

### Dependencias Python de la aplicación

`uv audit` detectó dos avisos, corregidos actualizando únicamente `uv.lock` (commit `11f59f5`):

| CVE | Paquete | Antes | Después | Aplicabilidad |
| --- | --- | --- | --- | --- |
| CVE-2026-106435 | `pymongo` (directa) | 4.18.2 | 4.19.0 | Condicionada: requiere que el servidor MongoDB o la red interna entreguen BSON malformado |
| CVE-2026-114605 | `dnspython` (transitiva) | 2.8.0 | 2.9.2 | No aplicable con la URI actual `mongodb://`; sólo se usa con `mongodb+srv://` |

Después de la actualización, `uv audit` no informa avisos en los 25 paquetes de runtime ni en los 35 con el grupo de desarrollo. Trivy tampoco informa vulnerabilidades en los paquetes del entorno virtual `/service/.venv`.

### Sistema base (Debian 13.7, 87 paquetes)

Resultado de Trivy sobre la imagen final:

| Severidad | Hallazgos | CVE únicas |
| --- | --- | --- |
| Crítica | 0 | 0 |
| Alta | 49 | 13 |
| Media | 75 | 39 |
| Baja | 65 | 35 |
| Sin clasificar | 15 | 5 |
| Total | 204 | 92 |

Un mismo CVE se cuenta una vez por cada paquete binario afectado; por eso los hallazgos superan a las CVE únicas. De los 204 hallazgos, 199 no tienen corrección publicada en Debian 13, 2 tienen la corrección diferida y 3 tienen corrección disponible (todos de `zlib1g`).

CVE de severidad alta:

| CVE | Paquete | Versión instalada | Corrección en Debian 13 | Aplicabilidad al servicio |
| --- | --- | --- | --- | --- |
| CVE-2026-85091, CVE-2026-76844 | `zlib1g` | 1:1.3.dfsg+really1.3.1-1+b1 | 1:1.3.dfsg+really1.3.1-1+deb13u1 | No verificada. La aplicación no usa directamente las funciones `gz*` de zlib |
| CVE-2026-119373, CVE-2026-119374, CVE-2026-119379 | `libsqlite3-0` | 3.46.1-7+deb13u2 | Sin corrección | No aplicable: la aplicación no usa SQLite |
| CVE-2026-76642, CVE-2026-78408, CVE-2026-78409, CVE-2026-78410 | `util-linux` (`mount`, `login`, `bsdutils` y bibliotecas) | 2.41.5-0+deb13u1 | Sin corrección | Local: exige ejecutar `mount` o `nsenter` dentro del contenedor. Mitigada por usuario no root, `cap_drop: ALL` y `no-new-privileges` |
| CVE-2025-69720 | `ncurses` | 6.5+20250216-2 | Sin corrección | No aplicable: el servicio no usa terminal |
| CVE-2026-16742 | `libsystemd0`, `libudev1` | 257.13-1~deb13u1 | Sin corrección | No aplicable: afecta a `systemd-homed`, que no está instalado |
| CVE-2026-54369 | `libacl1` | 2.3.2-2+b1 | Sin corrección | Local; el servicio no manipula ACL |
| CVE-2026-9538 | `perl-base` | 5.40.1-6+deb13u1 | Diferida | No aplicable: el servicio no ejecuta Perl |

Otros hallazgos relevantes de severidad media o sin clasificar:

- `libc6`: 14 de severidad media y 8 baja, sin corrección. Las relacionadas con el resolvedor DNS (por ejemplo CVE-2026-6238 y CVE-2026-5435) sólo serían alcanzables con respuestas DNS manipuladas dentro de la red interna de Docker.
- `openssl` y `libssl3t64` 3.5.7-1~deb13u3: 5 CVE sin severidad asignada. El servicio no usa TLS en sus conexiones actuales.
- `pip` 25.0.1 de la imagen base (`/usr/local/lib/python3.12`): 5 de severidad media y 1 baja, corregidas en versiones 25.3 a 26.2.0. `pip` no se ejecuta en runtime ni pertenece al entorno virtual de la aplicación.

La aplicabilidad indicada surge del título de cada aviso y del uso que hace el servicio; no se realizaron pruebas de explotación.

## Correcciones realizadas

| Cambio | Archivo | Motivo |
| --- | --- | --- |
| `pymongo` 4.19.0 y `dnspython` 2.9.2 | `uv.lock` | Corregir los dos avisos de `uv audit` |
| `**/__pycache__/` y `**/*.py[cod]` | `.dockerignore` | Los patrones anteriores sólo aplicaban a la raíz del contexto y la imagen incluía los `.pyc` locales de `app/` |
| Puertos publicados sólo en `127.0.0.1` | `docker-compose.yml` | Consul (8500) y Persistence (8003) quedaban accesibles desde toda la red local sin autenticación |
| `cap_drop: ALL`, `no-new-privileges:true`, `read_only: true` en `persistence` | `docker-compose.yml` | Reducir lo que puede hacer el proceso si resulta comprometido; anula los binarios SUID de la base |

No se modificaron el Dockerfile, `pyproject.toml` ni el código de la aplicación.

## Configuración Docker final

- Imagen: multi-stage (`base`, `builder`, `runtime`) sobre `python:3.12-slim-trixie`; dependencias instaladas con `uv sync --frozen --no-dev --no-install-project`.
- Contenido de `/service`: sólo `.venv` y los siete archivos fuente de `app/`.
- Usuario de ejecución: `appuser` (UID y GID 999), sin capacidades (`CapBnd` en cero), `NoNewPrivs: 1` y filesystem raíz de sólo lectura.
- Persistence: `127.0.0.1:8003` en el host, puerto 8000 en el contenedor.
- Consul: `127.0.0.1:8500`, modo desarrollo.
- MongoDB: sin puerto publicado al host; accesible sólo desde la red del proyecto; datos en el volumen `pdf-persistence-service_mongo_data`.

## Validación posterior a los cambios

| Prueba | Resultado |
| --- | --- |
| Reconstrucción de la imagen | Correcta; sin `__pycache__` ni `.pyc` en `/service/app` |
| Trivy | Sin cambios respecto del escaneo previo (204 hallazgos, 0 críticos): los cambios no modifican la base |
| `uv audit` | Sin avisos |
| Usuario | `appuser` (999), 0 reinicios |
| Opciones efectivas | `ReadonlyRootfs=true`, `CapDrop=[ALL]`, `no-new-privileges:true` |
| `GET /health` | HTTP 200 |
| `POST` y `GET /extractions` | HTTP 201 y 200; campos coincidentes |
| Persistencia en MongoDB | Los documentos creados en arranques anteriores siguen disponibles tras recrear los contenedores |
| Consul | Instancia registrada; check `passing` |
| MongoDB no publicado | Puerto 27017 cerrado en el host |
| Puertos sólo en localhost | 8003 y 8500 escuchan en `127.0.0.1`; cerrados en las demás interfaces del equipo |
| `tests/test_docker_compose.py` | 4 pruebas correctas |

## Cómo reconstruir y ejecutar

Desde la raíz del repositorio:

```bash
docker compose build persistence
docker compose up -d
docker compose ps
```

Comprobaciones:

```bash
curl http://localhost:8003/health
curl http://localhost:8500/v1/health/service/persistence
```

Uvicorn puede tardar varios segundos en responder después de iniciar el contenedor.

Para detener los servicios conservando los datos:

```bash
docker compose down
```

No usar `docker compose down -v`: elimina el volumen de MongoDB.

## Limitaciones conocidas

- Las vulnerabilidades del sistema base permanecen: 201 de los 204 hallazgos no tienen corrección disponible en Debian 13 y las 3 de `zlib1g` requieren que la imagen base las incorpore o actualizar el paquete en el Dockerfile.
- `pip`, `apt` y los intérpretes de comandos forman parte de la imagen base y siguen presentes.
- La API no tiene autenticación; MongoDB y Consul tampoco. La protección actual es de red: puertos en `127.0.0.1` y MongoDB sin publicar.
- Consul se ejecuta en modo desarrollo, sin ACL ni persistencia. No es una configuración de producción.
- Con los puertos en `127.0.0.1`, otros equipos de la red no pueden acceder a Persistence ni a Consul.
- `mongo:latest` y las etiquetas de las imágenes base no están fijadas por versión exacta ni por digest.
- `read_only: true` impide cualquier escritura en disco; una futura funcionalidad que escriba archivos necesitará un `tmpfs` o un volumen.
- Cada `docker compose up` crea volúmenes anónimos de MongoDB (`/data/configdb`) y Consul (`/consul/data`) que `docker compose down` no elimina.
- `/health` no consulta MongoDB: responde 200 aunque la base no esté disponible.
- Los resultados de los escaneos son válidos a la fecha indicada y deben repetirse periódicamente.
