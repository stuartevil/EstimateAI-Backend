class AreaMeasure:
    def from_polygon(self, points: list[tuple[float, float]], scale: float = 1.0) -> float:
        if len(points) < 3:
            return 0.0
        area = 0.0
        for i in range(len(points)):
            x1, y1 = points[i]
            x2, y2 = points[(i + 1) % len(points)]
            area += x1 * y2 - x2 * y1
        return abs(area / 2.0) * (scale**2)
