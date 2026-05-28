from app.core.config import DEFAULT_CHUNK_SIZE, DEFAULT_CHUNK_OVERLAP, MIN_CHUNK_LENGTH
from app.services.document_service import create_chunk_id


def split_text_into_chunks(
    text: str,
    chunk_size: int = DEFAULT_CHUNK_SIZE,
    chunk_overlap: int = DEFAULT_CHUNK_OVERLAP
) -> list[str]:
    """
    Split a long text into smaller overlapping chunks.

    Args:
        text: The text to split.
        chunk_size: The maximum number of characters per chunk.
        chunk_overlap: The number of overlapping characters between chunks.

    Returns:
        A list of text chunks.
    """

    if not text:
        return []

    cleaned_text = " ".join(text.split())

    if len(cleaned_text) < MIN_CHUNK_LENGTH:
        return []

    chunks = []
    start = 0

    while start < len(cleaned_text):
        end = start + chunk_size
        chunk = cleaned_text[start:end].strip()

        if len(chunk) >= MIN_CHUNK_LENGTH:
            chunks.append(chunk)

        start += chunk_size - chunk_overlap

    return chunks


def chunk_pages(document_id: str, pages: list[dict]) -> list[dict]:
    """
    Convert extracted PDF pages into searchable chunks.

    Args:
        document_id: The unique document ID.
        pages: A list of extracted page dictionaries.

    Returns:
        A list of chunk dictionaries.
    """

    all_chunks = []
    chunk_index = 0

    for page in pages:
        page_number = page["page_number"]
        raw_text = page["raw_text"]

        page_chunks = split_text_into_chunks(raw_text)

        for chunk_content in page_chunks:
            all_chunks.append(
                {
                    "chunk_id": create_chunk_id(),
                    "document_id": document_id,
                    "page_number": page_number,
                    "chunk_index": chunk_index,
                    "content": chunk_content
                }
            )

            chunk_index += 1

    return all_chunks