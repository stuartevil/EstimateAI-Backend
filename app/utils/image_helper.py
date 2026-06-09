import cv2
import numpy as np


def bytes_to_gray(image_bytes: bytes):
    return cv2.imdecode(np.frombuffer(image_bytes, np.uint8), cv2.IMREAD_GRAYSCALE)


def resize_to_match(image, target_shape: tuple[int, int]):
    return cv2.resize(image, (target_shape[1], target_shape[0]))
