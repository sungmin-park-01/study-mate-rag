# Study Mate RAG

Study Mate RAG is a full-stack RAG-based AI assistant that allows users to upload course documents and ask source-grounded questions.

## Project Goal

The goal of this project is to build a production-style AI document assistant using PDF ingestion, text extraction, chunking, embeddings, vector retrieval, LLM answer generation, and source citation.

## Tech Stack

- Frontend: React, Vite, TypeScript
- Backend: Python, FastAPI
- PDF Processing: PyMuPDF
- Vector Database: Chroma first, PostgreSQL + pgvector later
- LLM API: OpenAI API
- Deployment: Docker
- Evaluation: Custom test set and latency measurement

## MVP Scope

- PDF upload
- Text extraction
- Chunking
- Embedding generation
- Vector search
- RAG-based answer generation
- Source citation
- Basic frontend