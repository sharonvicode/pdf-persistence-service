# PDF ExtractText Persistence

Microservicio responsable de **persistir y consultar los resultados de extracción de texto de PDFs**.

Es el único servicio con acceso directo a la base de datos (MongoDB) y expone una API para que el Orchestrator guarde y consulte resultados.

No recibe, valida ni procesa archivos PDF: esas responsabilidades pertenecen a Validator, Extractor y Orchestrator.

## Ejecución con Docker

```bash
docker compose build persistence
docker compose up -d
```

La API queda en `http://localhost:8003` y la UI de Consul en `http://localhost:8500`, ambas accesibles sólo desde el propio equipo.

El estado de seguridad de la imagen, las pruebas ejecutadas y las limitaciones conocidas están en [`doc/seguridad-docker-auditoria-final.md`](doc/seguridad-docker-auditoria-final.md).
