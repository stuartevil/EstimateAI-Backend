from typing import Any


class ArrowMarkup:
    def build(self, start: dict[str, float], end: dict[str, float], **style: Any) -> dict[str, Any]:
        return {"type": "arrow", "start": start, "end": end, "style": style}
