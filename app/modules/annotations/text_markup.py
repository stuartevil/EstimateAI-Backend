from typing import Any


class TextMarkup:
    def build(self, content: str, x: float, y: float, **style: Any) -> dict[str, Any]:
        return {"type": "text", "content": content, "position": {"x": x, "y": y}, "style": style}
