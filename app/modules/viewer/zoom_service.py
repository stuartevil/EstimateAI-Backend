class ZoomService:
    MIN_ZOOM = 0.1
    MAX_ZOOM = 10.0

    def clamp_zoom(self, zoom: float) -> float:
        return max(self.MIN_ZOOM, min(self.MAX_ZOOM, zoom))

    def zoom_to_dpi(self, base_dpi: int, zoom: float) -> int:
        return int(base_dpi * self.clamp_zoom(zoom))
