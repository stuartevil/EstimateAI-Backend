"""Shared enumerations."""

from enum import StrEnum


class MarkupType(StrEnum):
    HIGHLIGHT = "highlight"
    TEXT = "text"
    LINE = "line"
    RECTANGLE = "rectangle"
    ELLIPSE = "ellipse"
    POLYGON = "polygon"
    CLOUD = "cloud"
    ARROW = "arrow"


class MeasurementType(StrEnum):
    LENGTH = "length"
    AREA = "area"
    COUNT = "count"
    VOLUME = "volume"
    PERIMETER = "perimeter"


class TakeoffStatus(StrEnum):
    DRAFT = "draft"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    ARCHIVED = "archived"


class AIJobStatus(StrEnum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"


class AIJobType(StrEnum):
    MARKUP_GENERATION = "markup_generation"
    TAKEOFF_GENERATION = "takeoff_generation"
    OCR = "ocr"
    OBJECT_DETECTION = "object_detection"
    REVISION_COMPARE = "revision_compare"
