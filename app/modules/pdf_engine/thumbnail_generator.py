import uuid
from pathlib import Path

import fitz

from app.core.config import get_settings

settings = get_settings()


class ThumbnailGenerator:
    def generate(self, file_path: Path, project_id: uuid.UUID, dpi: int = 72) -> Path | None:
        thumb_dir = settings.storage_thumbnails / str(project_id)
        thumb_dir.mkdir(parents=True, exist_ok=True)
        thumb_path = thumb_dir / f"{uuid.uuid4()}.png"
        with fitz.open(file_path) as doc:
            if doc.page_count == 0:
                return None
            pixmap = doc.load_page(0).get_pixmap(dpi=dpi)
            pixmap.save(thumb_path)
        return thumb_path
