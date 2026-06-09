from typing import Any


class HighlightMarkup:
    def build(self, rect: dict[str, float], **style: Any) -> dict[str, Any]:
        return {"type": "highlight", "rect": rect, "style": style}
