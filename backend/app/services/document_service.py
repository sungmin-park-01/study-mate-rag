from uuid import uuid4


def create_document_id() -> str:
    """
    Create a unique document id.
    Example: doc_abc123
    """
    return f"doc_{uuid4().hex[:12]}"


def create_chunk_id() -> str:
    """
    Create a unique chunk ID.
    """
    return f"chunk_{uuid4().hex[:12]}"