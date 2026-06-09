from pathlib import Path

from app.modules.pdf_engine.page_renderer import PageRenderer


class PageService:
    def __init__(self) -> None:
        self.renderer = PageRenderer()

    def get_page_image(self, file_path: Path, page_number: int, dpi: int = 150) -> bytes:
        return self.renderer.render_page(file_path, page_number, dpi=dpi)
