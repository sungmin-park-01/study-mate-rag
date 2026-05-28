import fitz
from fastapi import HTTPException, status


def extract_text_by_page(file_bytes: bytes) -> list[dict]:
    """
    Extract text from a PDF file page by page.

    Args:
        file_bytes: The uploaded PDF file as bytes.

    Returns:
        A list of dictionaries containing page numbers and raw text.
    """

    try:
        pdf_document = fitz.open(stream=file_bytes, filetype="pdf")
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to open the PDF file."
        )

    extracted_pages = []

    try:
        for page_index in range(len(pdf_document)):
            page = pdf_document[page_index]
            raw_text = page.get_text()

            extracted_pages.append(
                {
                    "page_number": page_index + 1,
                    "raw_text": raw_text.strip()
                }
            )

    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to extract text from the PDF file."
        )

    finally:
        pdf_document.close()

    return extracted_pages