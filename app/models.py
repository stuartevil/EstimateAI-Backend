"""
ORM model registry for Alembic autogenerate.

Import all models here so Alembic can discover metadata.
"""

from app.modules.markups.model import Markup  # noqa: F401
from app.modules.measurements.model import Measurement  # noqa: F401
from app.modules.pdf.model import PDFDocument  # noqa: F401
from app.modules.projects.model import Project  # noqa: F401
from app.modules.users.model import User  # noqa: F401
