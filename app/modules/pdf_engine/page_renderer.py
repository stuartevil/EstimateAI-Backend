from pathlib import Path

import fitz

from app.shared.exceptions import ValidationError


class PageRenderer:
    @staticmethod
    def render_page(file_path: Path, page_number: int, dpi: int = 150) -> bytes:
        with fitz.open(file_path) as doc:
            if page_number < 0 or page_number >= doc.page_count:
                raise ValidationError(f"Page {page_number} out of range")
            return doc.load_page(page_number).get_pixmap(dpi=dpi).tobytes("png")
