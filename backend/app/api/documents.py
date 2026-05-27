from fastapi import APIRouter, UploadFile, File, HTTPException, status

from app.core.config import MAX_UPLOAD_SIZE_BYTES, ALLOWED_PDF_CONTENT_TYPES
from app.services.document_service import create_document_id

router = APIRouter(
    prefix="/documents",
    tags=["documents"]
)


@router.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    """
    Upload a PDF document.
    """

    # 1. Validate that the file has a filename.
    if not file.filename:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Filename is missing."
        )

    # 2. Validate that the uploaded file has a PDF extension.
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only PDF files are allowed."
        )

    # 3. Validate the file content type.
    if file.content_type not in ALLOWED_PDF_CONTENT_TYPES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid file type. Please upload a PDF file."
        )

    # 4. Read the uploaded file into memory.
    file_bytes = await file.read()

    # 5. Reject empty files.
    if len(file_bytes) == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Uploaded file is empty."
        )

    # 6. Reject files that exceed the maximum upload size.
    if len(file_bytes) > MAX_UPLOAD_SIZE_BYTES:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail="File is too large. Maximum upload size is 10 MB."
        )

    # 7. Generate a unique document ID.
    document_id = create_document_id()

    return {
        "document_id": document_id,
        "filename": file.filename,
        "status": "uploaded"
    }