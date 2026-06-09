from pathlib import Path
from typing import Any

import fitz


class MetadataExtractor:
    @staticmethod
    def extract(file_path: Path) -> dict[str, Any]:
        with fitz.open(file_path) as doc:
            meta = doc.metadata or {}
            return {
                "page_count": doc.page_count,
                "title": meta.get("title"),
                "author": meta.get("author"),
                "subject": meta.get("subject"),
                "creator": meta.get("creator"),
            }
