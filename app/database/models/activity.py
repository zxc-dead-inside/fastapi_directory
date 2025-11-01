from __future__ import annotations

import uuid

from sqlalchemy import (String, CheckConstraint, UniqueConstraint, Index,
                        ForeignKey, text)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base
from app.database.mixins import UUIDPrimaryKeyMixin, TimestampMixin


class Activity(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "activity"

    name: Mapped[str] = mapped_column(String(200), nullable=False)
    parent_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("activity.id", ondelete="RESTRICT"),
        nullable=True
    )
    level: Mapped[int] = mapped_column(
        nullable=False, server_default=text("0")
    )

    parent: Mapped["Activity | None"] = relationship(
        remote_side="Activity.id", backref="children"
    )

    __table_args__ = (
        UniqueConstraint("name", "parent_id", name="uq_activity_parent"),
        CheckConstraint("level BETWEEN 0 AND 2", name="ck_activity_level_0_2"),
        Index("ix_activity_parent_level","parent_id", "level"),
        Index("ix_activity_name", "name")
    )
