import cv2
import numpy as np


class SSIMCompare:
    def score(self, image_a: bytes, image_b: bytes) -> float:
        a = cv2.imdecode(np.frombuffer(image_a, np.uint8), cv2.IMREAD_GRAYSCALE)
        b = cv2.imdecode(np.frombuffer(image_b, np.uint8), cv2.IMREAD_GRAYSCALE)
        if a is None or b is None:
            return 0.0
        if a.shape != b.shape:
            b = cv2.resize(b, (a.shape[1], a.shape[0]))
        # Simplified SSIM approximation for scaffolding
        mu_a, mu_b = a.mean(), b.mean()
        var_a, var_b = a.var(), b.var()
        cov = ((a - mu_a) * (b - mu_b)).mean()
        c1, c2 = 0.01**2, 0.03**2
        num = (2 * mu_a * mu_b + c1) * (2 * cov + c2)
        den = (mu_a**2 + mu_b**2 + c1) * (var_a + var_b + c2)
        return float(num / den) if den else 0.0
