from app.modules.revision_compare.image_compare import ImageCompare
from app.modules.revision_compare.ssim_compare import SSIMCompare


class ChangeDetector:
    def __init__(self) -> None:
        self.image_compare = ImageCompare()
        self.ssim_compare = SSIMCompare()

    def detect(self, image_a: bytes, image_b: bytes, threshold: float = 5.0) -> dict:
        diff_pct = self.image_compare.diff_percentage(image_a, image_b)
        ssim = self.ssim_compare.score(image_a, image_b)
        return {
            "diff_percentage": diff_pct,
            "ssim_score": ssim,
            "has_changes": diff_pct > threshold,
        }
