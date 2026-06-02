import time

from pydantic import BaseModel, Field
from fastapi import APIRouter, HTTPException

from app.services.embedding_service import EmbeddingService
from app.services.vector_store_service import VectorStoreService
from app.services.llm_service import LLMService


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


class AskRequest(BaseModel):
    document_id: str = Field(..., min_length=1)
    question: str = Field(..., min_length=1)
    top_k: int = Field(default=3, ge=1, le=10)


class Source(BaseModel):
    filename: str | None
    page_number: int | None
    content_preview: str


class AskResponse(BaseModel):
    answer: str
    sources: list[Source]
    latency_ms: int


embedding_service = EmbeddingService()
llm_service = LLMService()


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


@router.post("/ask", response_model=AskResponse)
def ask_question(request: AskRequest):
    """
    Generate a source-grounded answer using retrieved chunks from a specific document.
    """
    start_time = time.time()

    document_id = request.document_id.strip()
    question = request.question.strip()

    if not document_id:
        raise HTTPException(status_code=400, detail="document_id cannot be empty.")

    if not question:
        raise HTTPException(status_code=400, detail="question cannot be empty.")

    vector_store_service = VectorStoreService()

    try:
        retrieved_chunks = vector_store_service.retrieve_chunks(
            document_id=document_id,
            question=question,
            top_k=request.top_k,
        )
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error))

    if not retrieved_chunks:
        latency_ms = int((time.time() - start_time) * 1000)

        return {
            "answer": "The answer could not be found in the document.",
            "sources": [],
            "latency_ms": latency_ms,
        }

    context = build_context(retrieved_chunks)

    try:
        answer = llm_service.generate_answer(
            question=question,
            context=context,
        )
    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate answer: {str(error)}",
        )

    sources = build_sources(retrieved_chunks)

    latency_ms = int((time.time() - start_time) * 1000)

    return {
        "answer": answer,
        "sources": sources,
        "latency_ms": latency_ms,
    }


def build_context(chunks: list[dict]) -> str:
    """
    Convert retrieved chunks into a prompt-friendly context string.
    """
    context_parts = []

    for index, chunk in enumerate(chunks, start=1):
        filename = chunk.get("filename")
        page_number = chunk.get("page_number")
        content = chunk.get("content", "")

        context_parts.append(
            f"""
        Source {index}
        Filename: {filename}
        Page: {page_number}
        Content:
        {content}
        """
        )

    return "\n".join(context_parts)


def build_sources(chunks: list[dict]) -> list[Source]:
    """
    Build source objects from retrieved chunks.
    """
    sources = []

    for chunk in chunks:
        content = chunk.get("content", "")

        preview = content[:200]

        if len(content) > 200:
            preview += "..."

        sources.append(
            Source(
                filename=chunk.get("filename"),
                page_number=chunk.get("page_number"),
                content_preview=preview,
            )
        )

    return sources