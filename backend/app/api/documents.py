from fastapi import APIRouter, UploadFile, File, HTTPException, status

from app.core.config import MAX_UPLOAD_SIZE_BYTES, ALLOWED_PDF_CONTENT_TYPES
from app.services.document_service import create_document_id
from app.services.pdf_service import extract_text_by_page
from app.services.chunk_service import chunk_pages
from app.services.vector_store_service import VectorStoreService

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

      # 8. Extract text from the PDF page by page.
    pages = extract_text_by_page(file_bytes)

    # 9. Convert extracted pages into chunks.
    chunks = chunk_pages(document_id=document_id, pages=pages)

    # 10. Store chunks in the vector database for later retrieval.
    vector_store_service = VectorStoreService()
    stored_chunk_count = vector_store_service.add_chunks(
        document_id=document_id,
        filename=file.filename,
        chunks=chunks
    )

    # 11. Return the upload and processing result.
    return {
        "document_id": document_id,
        "filename": file.filename,
        "status": "processed",
        "page_count": len(pages),
        "chunk_count": len(chunks),
        "stored_chunk_count": stored_chunk_count,
        "pages": pages,
        "chunks": chunks
    }

