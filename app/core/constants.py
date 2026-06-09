"""Application-wide constants."""

API_V1_PREFIX = "/api/v1"

MARKUP_TYPES = ("highlight", "text", "line", "rectangle", "ellipse", "polygon", "cloud", "arrow")
MEASUREMENT_TYPES = ("length", "area", "count", "volume", "perimeter")
ALLOWED_PDF_MIME_TYPES = ("application/pdf",)

TAKEOFF_STATUSES = ("draft", "in_progress", "completed", "archived")
AI_JOB_STATUSES = ("pending", "running", "completed", "failed")
AI_JOB_TYPES = ("markup_generation", "takeoff_generation", "ocr", "object_detection", "revision_compare")
