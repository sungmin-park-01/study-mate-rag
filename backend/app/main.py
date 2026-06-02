from fastapi import FastAPI

from app.api.documents import router as documents_router
from app.api.query import router as query_router

app = FastAPI(
    title="Study Mate RAG API",
    description="A RAG-based AI assistant for course documents.",
    version="0.1.0"
)


@app.get("/")
def root():
    return {
        "message": "Study Mate RAG API is running.",
        "docs": "/docs",
        "health": "/health"
    }


@app.get("/health")
def health_check():
    return {"status": "ok"}


app.include_router(documents_router)
app.include_router(query_router)