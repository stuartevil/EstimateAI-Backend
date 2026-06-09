"""Application-wide constants."""

# API versioning prefix — keeps routes stable as the platform evolves
API_V1_PREFIX = "/api/v1"

# Supported markup types for construction takeoff annotations
MARKUP_TYPES = ("highlight", "text", "line", "rectangle", "ellipse", "polygon", "cloud")

# Supported measurement types for quantity takeoff
MEASUREMENT_TYPES = ("length", "area", "count", "volume")

# Allowed PDF MIME types for upload validation
ALLOWED_PDF_MIME_TYPES = ("application/pdf",)
