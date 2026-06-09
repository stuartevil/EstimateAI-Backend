"""Project ORM model."""

import uuid
from datetime import UTC, datetime

from sqlalchemy import DateTime, ForeignKey, String, Text, Uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class Project(Base):
    __tablename__ = "projects"

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    owner_id: Mapped[uuid.UUID] = mapped_column(
        Uuid, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(UTC), nullable=False
    )

    owner: Mapped["User"] = relationship("User", back_populates="projects")  # noqa: F821
    drawings: Mapped[list["Drawing"]] = relationship(  # noqa: F821
        "Drawing", back_populates="project", cascade="all, delete-orphan"
    )
    measurements: Mapped[list["Measurement"]] = relationship(  # noqa: F821
        "Measurement", back_populates="project", cascade="all, delete-orphan"
    )
    annotations: Mapped[list["Annotation"]] = relationship(  # noqa: F821
        "Annotation", back_populates="project", cascade="all, delete-orphan"
    )
    takeoffs: Mapped[list["Takeoff"]] = relationship(  # noqa: F821
        "Takeoff", back_populates="project", cascade="all, delete-orphan"
    )
    ai_jobs: Mapped[list["AIJob"]] = relationship(  # noqa: F821
        "AIJob", back_populates="project", cascade="all, delete-orphan"
    )
