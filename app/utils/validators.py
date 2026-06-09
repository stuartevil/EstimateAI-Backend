from app.core.constants import ALLOWED_PDF_MIME_TYPES, MARKUP_TYPES, MEASUREMENT_TYPES


def validate_pdf_mime(mime_type: str | None) -> bool:
    return mime_type in ALLOWED_PDF_MIME_TYPES


def validate_markup_type(markup_type: str) -> bool:
    return markup_type in MARKUP_TYPES


def validate_measurement_type(measurement_type: str) -> bool:
    return measurement_type in MEASUREMENT_TYPES
