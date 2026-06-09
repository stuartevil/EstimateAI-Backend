import math


class LengthMeasure:
    def from_points(self, points: list[tuple[float, float]], scale: float = 1.0) -> float:
        total = 0.0
        for i in range(1, len(points)):
            x1, y1 = points[i - 1]
            x2, y2 = points[i]
            total += math.hypot(x2 - x1, y2 - y1)
        return total * scale
