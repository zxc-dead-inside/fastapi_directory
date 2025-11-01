from __future__ import annotations

from sqlalchemy import Index, Text, Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base
from app.database.mixins import UUIDPrimaryKeyMixin, TimestampMixin


class Building(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "building"

    address: Mapped[str] = mapped_column(Text, nullable=False)
    lat: Mapped[float] = mapped_column(Numeric(9, 6), nullable=False)
    lon: Mapped[float] = mapped_column(Numeric(9, 6), nullable=False)

    offices: Mapped[list["Office"]] = relationship(
        "Office", back_populates="building", cascade="all, delete-orphan"
    )

    __table_args__ = (Index("ix_building_lat_lon", "lat", "lon"),)
