class ScaleCalibrator:
    def calibrate(self, known_length: float, pixel_length: float) -> float:
        if pixel_length <= 0:
            raise ValueError("Pixel length must be positive")
        return known_length / pixel_length
