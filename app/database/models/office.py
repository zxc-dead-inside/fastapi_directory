from __future__ import annotations
import uuid

from sqlalchemy import UniqueConstraint, Index, ForeignKey, String, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base
from app.database.mixins import UUIDPrimaryKeyMixin, TimestampMixin


class Office(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "office"

    building_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("building.id", ondelete="CASCADE")
    )
    floor: Mapped[int | None] = mapped_column(Integer, nullable=True)
    unit: Mapped[str | None] = mapped_column(String(50), nullable=True)

    building: Mapped["Building"] = relationship(
        "Building", back_populates="offices"
    )
    organizations: Mapped[list["Organization"]] = relationship(
        secondary="organization_office", back_populates="offices"
    )

    __table_args__ = (
        UniqueConstraint(
            "building_id", "floor", "unit", name="uq_office_unique_in_building"
        ),
        Index("ix_office_building", "building_id"),
    )
