"""
Project ORM model.

A project groups construction drawings (PDFs), measurements, and markups
for a single estimation job — similar to a Bluebeam Studio project.
"""

import uuid
from datetime import UTC, datetime

from sqlalchemy import DateTime, ForeignKey, String, Text, Uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class Project(Base):
    """Construction estimation project."""

    __tablename__ = "projects"

    id: Mapped[uuid.UUID] = mapped_column(
        Uuid,
        primary_key=True,
        default=uuid.uuid4,
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    owner_id: Mapped[uuid.UUID] = mapped_column(
        Uuid,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
        nullable=False,
    )

    owner: Mapped["User"] = relationship("User", back_populates="projects")  # noqa: F821
    pdf_documents: Mapped[list["PDFDocument"]] = relationship(  # noqa: F821
        "PDFDocument",
        back_populates="project",
        cascade="all, delete-orphan",
    )
    measurements: Mapped[list["Measurement"]] = relationship(  # noqa: F821
        "Measurement",
        back_populates="project",
        cascade="all, delete-orphan",
    )
    markups: Mapped[list["Markup"]] = relationship(  # noqa: F821
        "Markup",
        back_populates="project",
        cascade="all, delete-orphan",
    )
