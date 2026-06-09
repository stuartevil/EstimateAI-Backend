import cv2
import numpy as np


class ImageCompare:
    def diff_percentage(self, image_a: bytes, image_b: bytes) -> float:
        a = cv2.imdecode(np.frombuffer(image_a, np.uint8), cv2.IMREAD_GRAYSCALE)
        b = cv2.imdecode(np.frombuffer(image_b, np.uint8), cv2.IMREAD_GRAYSCALE)
        if a is None or b is None:
            return 100.0
        if a.shape != b.shape:
            b = cv2.resize(b, (a.shape[1], a.shape[0]))
        diff = cv2.absdiff(a, b)
        return float(np.count_nonzero(diff)) / diff.size * 100.0
