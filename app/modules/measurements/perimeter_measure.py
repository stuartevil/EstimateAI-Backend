from app.modules.measurements.length_measure import LengthMeasure


class PerimeterMeasure:
    def __init__(self) -> None:
        self._length = LengthMeasure()

    def from_polygon(self, points: list[tuple[float, float]], scale: float = 1.0) -> float:
        if len(points) < 2:
            return 0.0
        closed = points + [points[0]]
        return self._length.from_points(closed, scale=scale)
