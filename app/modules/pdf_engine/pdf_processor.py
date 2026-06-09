from pathlib import Path

import fitz
from loguru import logger

from app.shared.exceptions import BadRequestError, ValidationError


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
            logger.warning("Invalid PDF: {}", file_path)
            raise BadRequestError("Invalid or corrupted PDF file") from exc

    @staticmethod
    def extract_page_count(file_path: Path) -> int:
        PDFProcessor.validate_pdf(file_path)
        with fitz.open(file_path) as doc:
            return doc.page_count
