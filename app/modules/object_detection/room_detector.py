from app.modules.object_detection.yolo_detector import YOLODetector


class RoomDetector:
    def __init__(self) -> None:
        self.detector = YOLODetector()

    def detect_rooms(self, image_bytes: bytes) -> list[dict]:
        return self.detector.detect(image_bytes)
