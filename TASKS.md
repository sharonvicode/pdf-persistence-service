# PDF Persistence — TASKS

## Objetivo 1 — API y persistencia básica

### POST `/extractions`

* [X] Crear tests para registrar una extracción.
* [X] Verificar respuesta `201 Created`.
* [X] Verificar generación del `id`.
* [X] Verificar validaciones de datos.
* [X] Crear DTO de entrada.
* [X] Crear DTO de respuesta.
* [X] Implementar `ExtractionService`.
* [X] Definir la abstracción `ExtractionRepository`.
* [X] Implementar `InMemoryExtractionRepository`.
* [X] Implementar endpoint `POST /extractions`.

### GET `/extractions/{id}`

* [X] Crear test para consultar una extracción existente.
* [X] Verificar respuesta `200 OK`.
* [X] Implementar consulta por ID.
* [X] Manejar extracción inexistente con `404 Not Found`.
* [X] Crear test para verificar el `404`.

### Refactor

* [X] Revisar separación API → Application → Infrastructure.
* [X] Revisar responsabilidades de cada clase.
* [X] Evitar que las rutas dependan directamente del repositorio concreto.
* [X] Revisar inyección de dependencias.
* [X] Revisar nombres y organización del código.
* [X] Mantener el código simple y sin funcionalidades innecesarias.
* [X] Ejecutar todos los tests y verificar que pasen.

---

## Objetivo 2 — Persistencia

### Preparar persistencia real

* [X] Analizar cómo reemplazar el repositorio en memoria por una persistencia real.
* [X] Mantener `ExtractionRepository` como abstracción.
* [X] Implementar el repositorio de persistencia.
* [X] Configurar las variables de entorno necesarias.
* [X] Mantener `InMemoryExtractionRepository` para los tests.
* [X] Verificar que POST y GET sigan funcionando.

### Tests

* [X] Verificar creación de una extracción.
* [X] Verificar consulta de una extracción.
* [X] Verificar extracción inexistente.
* [X] Ejecutar todos los tests.

---

## Objetivo 3 — Integración y pruebas

### Integración

* [X] Revisar cómo Persistence recibirá los resultados del microservicio Extract.
* [X] Verificar el formato de los datos enviados.
* [X] Verificar que Persistence pueda guardar esos resultados.

### Pruebas

* [X] Revisar tests existentes.
* [X] Agregar solamente los tests necesarios.
* [X] Ejecutar todos los tests.
* [X] Corregir errores encontrados.

---

## Objetivo 4 — Preparación final

* [X] Revisar estructura del proyecto.
* [X] Revisar código innecesario o duplicado.
* [X] Revisar nombres y responsabilidades.
* [X] Verificar manejo de errores.
* [X] Verificar respuestas HTTP.
* [X] Ejecutar todos los tests.
* [X] Revisar documentación básica.
* [X] Preparar commit final.

---


## Forma de trabajo

Cada funcionalidad se desarrolla mediante:

**RED → GREEN → REFACTOR**

* [X] 🔴 **RED:** crear el test y comprobar que falla por el motivo correcto.
* [X] 🟢 **GREEN:** implementar lo mínimo necesario para que pase.
* [X] 🔵 **REFACTOR:** mejorar el código sin cambiar el comportamiento.
