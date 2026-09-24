# PDF Persistence — TASKS

## 🎯 Día Objetivo 1 — API y persistencia básica

### POST `/extractions`

* [ ] Crear tests para registrar una extracción.
* [ ] Verificar respuesta `201 Created`.
* [ ] Verificar generación del `id`.
* [ ] Verificar validaciones de datos.
* [ ] Crear DTO de entrada.
* [ ] Crear DTO de respuesta.
* [ ] Implementar `ExtractionService`.
* [ ] Definir la abstracción `ExtractionRepository`.
* [ ] Implementar `InMemoryExtractionRepository`.
* [ ] Implementar endpoint `POST /extractions`.

### GET `/extractions/{id}`

* [ ] Crear test para consultar una extracción existente.
* [ ] Verificar respuesta `200 OK`.
* [ ] Implementar consulta por ID.
* [ ] Manejar extracción inexistente con `404 Not Found`.
* [ ] Crear test para verificar el `404`.

### Refactor

* [ ] Revisar separación API → Application → Infrastructure.
* [ ] Revisar responsabilidades de cada clase.
* [ ] Evitar que las rutas dependan directamente del repositorio concreto.
* [ ] Revisar inyección de dependencias.
* [ ] Revisar nombres y organización del código.
* [ ] Mantener el código simple y sin funcionalidades innecesarias.
* [ ] Ejecutar todos los tests y verificar que pasen.

---

## 🎯 Día Objetivo 2 — Persistencia

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

## 🎯 Día Objetivo 3 — Integración y pruebas

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

## 🎯 Día Objetivo 4 — Preparación final

* [ ] Revisar estructura del proyecto.
* [ ] Revisar código innecesario o duplicado.
* [ ] Revisar nombres y responsabilidades.
* [ ] Verificar manejo de errores.
* [ ] Verificar respuestas HTTP.
* [ ] Ejecutar todos los tests.
* [ ] Revisar documentación básica.
* [ ] Preparar commit final.

---

## 📌 Estado del microservicio

| Funcionalidad           | Estado |
| ----------------------- | ------ |
| POST `/extractions`     | ⬜      |
| GET `/extractions/{id}` | ⬜      |
| Manejo `404`            | ⬜      |
| DTOs                    | ⬜      |
| Service                 | ⬜      |
| Repository              | ⬜      |
| Tests                   | ⬜      |
| Persistencia real       | ⬜      |
| Integración con Extract | ⬜      |
| Documentación           | ⬜      |

## 🔄 Forma de trabajo

Cada funcionalidad se desarrolla mediante:

**RED → GREEN → REFACTOR**

* [ ] 🔴 **RED:** crear el test y comprobar que falla por el motivo correcto.
* [ ] 🟢 **GREEN:** implementar lo mínimo necesario para que pase.
* [ ] 🔵 **REFACTOR:** mejorar el código sin cambiar el comportamiento.
