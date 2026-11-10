# Seguridad Docker — Subetapa 4: ejecución sin privilegios administrativos

## Objetivo

Ejecutar el proceso de la aplicación con una identidad sin privilegios administrativos en la etapa final de la imagen, sin alterar las etapas de construcción ni el comando de inicio.

## Usuario y grupo creados

La etapa `runtime` crea exclusivamente las siguientes identidades de sistema:

- Grupo: `appgroup`.
- Usuario: `appuser`, perteneciente a `appgroup` y sin directorio home.

El Dockerfile utiliza `groupadd --system` y `useradd --system`, herramientas esperadas en la base Debian seleccionada. No se instaló ningún paquete adicional; su disponibilidad efectiva se deja como comprobación pendiente de un build autorizado.

## Cambios en el Dockerfile

Después de declarar `FROM base AS runtime`, el Dockerfile crea el grupo y usuario:

```dockerfile
RUN groupadd --system appgroup \
    && useradd --system --gid appgroup --no-create-home appuser
```

Después de copiar `/service/.venv` y `app/`, establece:

```dockerfile
USER appuser
```

Por lo tanto, Uvicorn y la aplicación se inician como `appuser`. Las etapas `base` y `builder` no fueron modificadas. Se preservan `/service`, `/service/.venv`, `PATH`, el puerto 8000 y el comando existente de Uvicorn.

## Permisos y justificación

No se añadieron `chmod`, `chown` ni permisos amplios. En particular, no se utiliza `chmod 777`.

Los directorios y archivos de aplicación, junto con el entorno virtual, se copian antes de declarar `USER appuser`. Permanecen con la propiedad y permisos por defecto de las instrucciones `COPY`; el usuario de ejecución no recibe permisos generales de escritura sobre `/service`, el código ni las dependencias. El proceso sólo necesita atravesar directorios, leer módulos y ejecutar los scripts del entorno virtual; sus logs se envían a salida estándar por la configuración actual de Uvicorn.

Evitar cambios de propietario preserva el principio de mínimo privilegio y evita conceder a la aplicación capacidad de modificar su código o dependencias en runtime. La disponibilidad efectiva de permisos de lectura y ejecución debe confirmarse mediante una construcción y arranque posteriores.

## Validaciones estáticas realizadas

- Se verificó que `USER appuser` aparece sólo en la etapa `runtime`, después de preparar sus archivos.
- Se verificó que `appuser` se crea como usuario de sistema perteneciente a `appgroup` y que no es el usuario root.
- Se verificó que no se agregaron paquetes, `chmod`, `chown` ni permisos de escritura generales.
- Se verificó que las etapas `base` y `builder` permanecen sin cambios.
- Se verificó que permanecen la copia de `uv` sólo en `builder`, la instalación bloqueada con `uv sync --frozen --no-dev --no-install-project`, `/service/.venv`, `app/`, las variables, el puerto y el comando de Uvicorn.
- Se ejecutó `git diff --check` y se revisó el estado de Git y el alcance de cambios.

## Pruebas reales pendientes

No se construyó una imagen ni se ejecutó un contenedor en esta subetapa. Permanecen pendientes:

- Confirmar durante el build que las herramientas de gestión de usuarios están disponibles en la variante Debian seleccionada.
- Confirmar que `appuser` puede leer el código y ejecutar Python, Uvicorn y las dependencias desde `/service/.venv`.
- Iniciar el servicio como `appuser` y comprobar `GET /health`.
- Verificar conectividad con MongoDB, registro en Consul y cierre ordenado.
- Ejecutar las pruebas aplicables y cualquier análisis de imagen autorizado.

No se afirma que la ejecución sin privilegios haya sido comprobada: la compatibilidad indicada es estática y debe validarse con esas pruebas reales.
