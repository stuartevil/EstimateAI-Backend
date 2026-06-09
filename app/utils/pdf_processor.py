"""PDF processing utilities using PyMuPDF."""

from pathlib import Path

import fitz
from loguru import logger

from app.utils.exceptions import BadRequestError, ValidationError


class PDFProcessor:
    @staticmethod
    def validate_pdf(file_path: Path) -> None:
        if not file_path.exists():
            raise BadRequestError("PDF file not found on disk")

        try:
            with fitz.open(file_path) as doc:
                if doc.page_count == 0:
                    raise ValidationError("PDF has no pages")
                doc.load_page(0)
        except fitz.FileDataError as exc:
            logger.warning("Invalid PDF file: {}", file_path)
            raise BadRequestError("Invalid or corrupted PDF file") from exc
        except Exception as exc:
            logger.error("PDF validation failed: {}", exc)
            raise BadRequestError("Unable to process PDF file") from exc

    @staticmethod
    def extract_page_count(file_path: Path) -> int:
        PDFProcessor.validate_pdf(file_path)
        with fitz.open(file_path) as doc:
            return doc.page_count

    @staticmethod
    def extract_page_as_image(file_path: Path, page_number: int, dpi: int = 150) -> bytes:
        with fitz.open(file_path) as doc:
            if page_number < 0 or page_number >= doc.page_count:
                raise ValidationError(f"Page {page_number} out of range (0-{doc.page_count - 1})")
            page = doc.load_page(page_number)
            pixmap = page.get_pixmap(dpi=dpi)
            return pixmap.tobytes("png")
