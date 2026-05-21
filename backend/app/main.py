from fastapi import FastAPI

app = FastAPI(title="Study Mate RAG API")


@app.get("/health")
def health_check():
    return {"status": "ok"} 