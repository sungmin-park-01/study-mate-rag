import chromadb

from app.core.config import settings
from app.services.embedding_service import EmbeddingService


class VectorStoreService:
    def __init__(self) -> None:
        """
        Initialize a local persistent Chroma client.

        PersistentClient stores the vector database on disk, which is useful
        for local development because uploaded document chunks remain available
        after the server restarts.
        """
        self.client = chromadb.PersistentClient(path=settings.CHROMA_DB_PATH)
        self.collection = self.client.get_or_create_collection(
            name=settings.CHROMA_COLLECTION_NAME
        )
        self.embedding_service = EmbeddingService()

    def add_chunks(
        self,
        document_id: str,
        filename: str,
        chunks: list[dict],
    ) -> int:
        """
        Store document chunks in Chroma with embeddings and metadata.

        Each chunk is stored with:
        - unique chunk ID
        - original text content
        - embedding vector
        - metadata for source-grounded retrieval
        """
        valid_chunks = [
            chunk for chunk in chunks
            if chunk.get("content") and chunk["content"].strip()
        ]

        if not valid_chunks:
            return 0

        documents = [chunk["content"] for chunk in valid_chunks]
        embeddings = self.embedding_service.create_embeddings(documents)

        ids = [
            f"{document_id}_chunk_{chunk['chunk_index']}"
            for chunk in valid_chunks
        ]

        metadatas = [
            {
                "document_id": document_id,
                "filename": filename,
                "page_number": chunk["page_number"],
                "chunk_index": chunk["chunk_index"],
            }
            for chunk in valid_chunks
        ]

        self.collection.upsert(
            ids=ids,
            documents=documents,
            embeddings=embeddings,
            metadatas=metadatas,
        )

        return len(valid_chunks)

    def retrieve_chunks(
        self,
        document_id: str,
        question: str,
        top_k: int = 5,
    ) -> list[dict]:
        """
        Retrieve the most relevant chunks for a user question.

        The search is filtered by document_id so the answer only uses
        chunks from the selected uploaded document.
        """
        clean_question = question.strip()

        if not clean_question:
            raise ValueError("Question cannot be empty.")

        query_embedding = self.embedding_service.create_embedding(clean_question)

        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k,
            where={"document_id": document_id},
            include=["documents", "metadatas", "distances"],
        )

        retrieved_chunks = []

        documents = results.get("documents", [[]])[0]
        metadatas = results.get("metadatas", [[]])[0]
        distances = results.get("distances", [[]])[0]

        for content, metadata, distance in zip(documents, metadatas, distances):
            retrieved_chunks.append(
                {
                    "content": content,
                    "filename": metadata.get("filename"),
                    "page_number": metadata.get("page_number"),
                    "chunk_index": metadata.get("chunk_index"),
                    "score": self._distance_to_score(distance),
                }
            )

        return retrieved_chunks

    def _distance_to_score(self, distance: float) -> float:
        """
        Convert Chroma distance into a simple similarity-style score.

        Lower distance means more similar. This conversion makes the API
        easier to read for portfolio demos.
        """
        return round(1 / (1 + distance), 4)