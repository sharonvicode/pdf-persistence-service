"""Datos de prueba compartidos entre los tests."""

VALID_PAYLOAD = {
    "file_name": "documento.pdf",
    "text": "Texto extraído del PDF.",
    "page_count": 3,
}

# Supera el límite de 16 MB por documento de MongoDB.
OVERSIZED_TEXT = "a" * (17 * 1024 * 1024)