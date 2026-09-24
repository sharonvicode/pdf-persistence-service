"""DTOs de entrada y salida de la API (modelos Pydantic)."""

from pydantic import BaseModel, Field


class ExtractionCreate(BaseModel):
    file_name: str = Field(min_length=1)
    text: str
    page_count: int = Field(ge=0)


class ExtractionCreated(BaseModel):
    id: str


class ExtractionResponse(BaseModel):
    id: str
    file_name: str
    text: str
    page_count: int
