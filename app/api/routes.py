"""Rutas HTTP del microservicio.

Solo traducen HTTP <-> casos de uso. Sin lógica de negocio.
"""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Request, status

from app.api.schemas import ExtractionCreate, ExtractionCreated, ExtractionResponse
from app.application.services import ExtractionNotFoundError, ExtractionService

router = APIRouter()


def get_extraction_service(request: Request) -> ExtractionService:
    return request.app.state.extraction_service


@router.post(
    "/extractions",
    status_code=status.HTTP_201_CREATED,
    response_model=ExtractionCreated,
)
def create_extraction(
    payload: ExtractionCreate,
    service: Annotated[ExtractionService, Depends(get_extraction_service)],
) -> ExtractionCreated:
    extraction_id = service.create(payload.file_name, payload.text, payload.page_count)
    return ExtractionCreated(id=extraction_id)


@router.get("/extractions/{extraction_id}", response_model=ExtractionResponse)
def get_extraction(
    extraction_id: str,
    service: Annotated[ExtractionService, Depends(get_extraction_service)],
) -> ExtractionResponse:
    try:
        extraction = service.get(extraction_id)
    except ExtractionNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Extraction not found"
        )
    return ExtractionResponse(id=extraction_id, **extraction)
