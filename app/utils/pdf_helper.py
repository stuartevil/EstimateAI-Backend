from pathlib import Path

import fitz


def is_valid_pdf(file_path: Path) -> bool:
    try:
        with fitz.open(file_path) as doc:
            return doc.page_count > 0
    except Exception:
        return False
