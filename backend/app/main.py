from fastapi import FastAPI

from app.api.health import router as health_router

app = FastAPI(title="Study Mate RAG API")

app.include_router(health_router)