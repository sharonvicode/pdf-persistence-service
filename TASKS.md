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
* [ ] Crear test para verificar el `404`.

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

* [ ] Analizar cómo reemplazar el repositorio en memoria por una persistencia real.
* [ ] Mantener `ExtractionRepository` como abstracción.
* [ ] Implementar el repositorio de persistencia.
* [ ] Configurar las variables de entorno necesarias.
* [ ] Mantener `InMemoryExtractionRepository` para los tests.
* [ ] Verificar que POST y GET sigan funcionando.

### Tests

* [ ] Verificar creación de una extracción.
* [ ] Verificar consulta de una extracción.
* [ ] Verificar extracción inexistente.
* [ ] Ejecutar todos los tests.

---

## Objetivo 3 — Integración y pruebas

### Integración

* [ ] Revisar cómo Persistence recibirá los resultados del microservicio Extract.
* [ ] Verificar el formato de los datos enviados.
* [ ] Verificar que Persistence pueda guardar esos resultados.

### Pruebas

* [ ] Revisar tests existentes.
* [ ] Agregar solamente los tests necesarios.
* [ ] Ejecutar todos los tests.
* [ ] Corregir errores encontrados.

---

## Objetivo 4 — Preparación final

* [ ] Revisar estructura del proyecto.
* [ ] Revisar código innecesario o duplicado.
* [ ] Revisar nombres y responsabilidades.
* [ ] Verificar manejo de errores.
* [ ] Verificar respuestas HTTP.
* [ ] Ejecutar todos los tests.
* [ ] Revisar documentación básica.
* [ ] Preparar commit final.

---


## Forma de trabajo

Cada funcionalidad se desarrolla mediante:

**RED → GREEN → REFACTOR**

* [ ] 🔴 **RED:** crear el test y comprobar que falla por el motivo correcto.
* [ ] 🟢 **GREEN:** implementar lo mínimo necesario para que pase.
* [ ] 🔵 **REFACTOR:** mejorar el código sin cambiar el comportamiento.
