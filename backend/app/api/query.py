from pydantic import BaseModel, Field
from fastapi import APIRouter, HTTPException

from app.services.vector_store_service import VectorStoreService

router = APIRouter(prefix="/query", tags=["query"])


class RetrieveRequest(BaseModel):
    document_id: str = Field(..., min_length=1)
    question: str = Field(..., min_length=1)
    top_k: int = Field(default=5, ge=1, le=20)


class RetrievedChunk(BaseModel):
    content: str
    filename: str | None
    page_number: int | None
    chunk_index: int | None
    score: float


class RetrieveResponse(BaseModel):
    document_id: str
    question: str
    top_k: int
    results: list[RetrievedChunk]


@router.post("/retrieve", response_model=RetrieveResponse)
def retrieve_relevant_chunks(request: RetrieveRequest):
    """
    Retrieve the most relevant chunks for a question from a specific document.
    """
    document_id = request.document_id.strip()
    question = request.question.strip()

    if not document_id:
        raise HTTPException(status_code=400, detail="document_id cannot be empty.")

    if not question:
        raise HTTPException(status_code=400, detail="question cannot be empty.")

    vector_store_service = VectorStoreService()

    try:
        results = vector_store_service.retrieve_chunks(
            document_id=document_id,
            question=question,
            top_k=request.top_k,
        )
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error))

    return {
        "document_id": document_id,
        "question": question,
        "top_k": request.top_k,
        "results": results,
    }