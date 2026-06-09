"""
ORM model registry for Alembic autogenerate.

Import all models here so Alembic and tests can discover metadata.
"""

from app.models.markup import Markup
from app.models.measurement import Measurement
from app.models.pdf_document import PDFDocument
from app.models.project import Project
from app.models.user import User

__all__ = ["User", "Project", "PDFDocument", "Measurement", "Markup"]
