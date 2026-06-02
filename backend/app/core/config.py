import os
from dotenv import load_dotenv

# Load environment variables from the .env file for local development.
load_dotenv()


# Upload validation settings.
MAX_UPLOAD_SIZE_BYTES = 10 * 1024 * 1024  # 10 MB

ALLOWED_PDF_CONTENT_TYPES = {
    "application/pdf"
}


# Chunking settings.
DEFAULT_CHUNK_SIZE = 800
DEFAULT_CHUNK_OVERLAP = 150
MIN_CHUNK_LENGTH = 50


class Settings:
    # OpenAI API configuration.
    OPENAI_API_KEY: str | None = os.getenv("OPENAI_API_KEY")
    OPENAI_EMBEDDING_MODEL: str = os.getenv(
        "OPENAI_EMBEDDING_MODEL",
        "text-embedding-3-small",
    )

    # Chroma local persistence configuration.
    CHROMA_DB_PATH: str = os.getenv("CHROMA_DB_PATH", "./chroma_db")
    CHROMA_COLLECTION_NAME: str = os.getenv(
        "CHROMA_COLLECTION_NAME",
        "study_mate_chunks",
    )


settings = Settings()