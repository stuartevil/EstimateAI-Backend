from typing import Any


class CloudMarkup:
    def build(self, points: list[dict[str, float]], **style: Any) -> dict[str, Any]:
        return {"type": "cloud", "points": points, "style": style}
