# PDF ExtractText Persistence

Microservicio responsable de **persistir y consultar los resultados de extracción de texto de PDFs**.

Es el único servicio con acceso directo a la base de datos (MongoDB) y expone una API para que el Orchestrator guarde y consulte resultados.

No recibe, valida ni procesa archivos PDF: esas responsabilidades pertenecen a Validator, Extractor y Orchestrator.
