"""PDF upload HTTP endpoints."""

from uuid import UUID

from fastapi import APIRouter, Depends, File, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.modules.pdf.schema import PDFDocumentResponse, PDFUploadResponse
from app.modules.pdf.service import PDFService
from app.modules.users.model import User
from app.shared.dependencies import get_current_active_user
from app.shared.response import APIResponse, success_response

router = APIRouter(prefix="/pdf", tags=["PDF"])


def get_pdf_service(db: AsyncSession = Depends(get_db)) -> PDFService:
    return PDFService(db)


@router.post(
    "/projects/{project_id}/upload",
    response_model=APIResponse[PDFUploadResponse],
    status_code=201,
)
async def upload_pdf(
    project_id: UUID,
    file: UploadFile = File(...),
    service: PDFService = Depends(get_pdf_service),
    current_user: User = Depends(get_current_active_user),
) -> dict:
    """Upload a construction drawing PDF to a project."""
    document = await service.upload_pdf(project_id, file, owner_id=current_user.id)
    response = PDFUploadResponse.model_validate(document)
    return success_response(data=response, message="PDF uploaded successfully")


@router.get(
    "/projects/{project_id}",
    response_model=APIResponse[list[PDFDocumentResponse]],
)
async def list_pdfs(
    project_id: UUID,
    service: PDFService = Depends(get_pdf_service),
    current_user: User = Depends(get_current_active_user),
) -> dict:
    """List all PDF documents in a project."""
    documents = await service.list_documents(project_id, owner_id=current_user.id)
    return success_response(
        data=[PDFDocumentResponse.model_validate(d) for d in documents],
        message="PDF documents retrieved",
    )


@router.get("/{document_id}", response_model=APIResponse[PDFDocumentResponse])
async def get_pdf(
    document_id: UUID,
    service: PDFService = Depends(get_pdf_service),
    current_user: User = Depends(get_current_active_user),
) -> dict:
    """Get PDF document metadata by ID."""
    document = await service.get_document(document_id, owner_id=current_user.id)
    return success_response(
        data=PDFDocumentResponse.model_validate(document),
        message="PDF document retrieved",
    )


@router.delete("/{document_id}", response_model=APIResponse[None])
async def delete_pdf(
    document_id: UUID,
    service: PDFService = Depends(get_pdf_service),
    current_user: User = Depends(get_current_active_user),
) -> dict:
    """Delete a PDF document and its file from disk."""
    await service.delete_document(document_id, owner_id=current_user.id)
    return success_response(data=None, message="PDF document deleted")
