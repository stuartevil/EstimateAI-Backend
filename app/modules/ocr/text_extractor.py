from app.modules.ocr.paddle_ocr import PaddleOCRService


class TextExtractor:
    def __init__(self) -> None:
        self.ocr = PaddleOCRService()

    def extract(self, image_bytes: bytes) -> str:
        blocks = self.ocr.extract_text(image_bytes)
        return " ".join(b.get("text", "") for b in blocks)
