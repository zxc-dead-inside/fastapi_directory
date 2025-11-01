from __future__ import annotations

import uuid

from sqlalchemy import String, UniqueConstraint, Index, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base
from app.database.mixins import UUIDPrimaryKeyMixin, TimestampMixin


class Organization(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "organization"

    name: Mapped[str] = mapped_column(String(300), nullable=False)

    phones: Mapped[list["OrganizationPhone"]] = relationship(
        back_populates="organization",
        cascade="all, delete-orphan"
    )
    offices: Mapped[list["Office"]] = relationship(
        secondary="organization_office",
        back_populates="organizations",
        lazy="selectin"
    )
    activities: Mapped[list["Activity"]] = relationship(
        secondary="organization_activity",
        backref="organizations",
        lazy="selectin"
    )

    __table_args__ = (Index("ix_org_name", "name"),)


class OrganizationPhone(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "organization_phone"

    phone_number: Mapped[str] = mapped_column(String(20), nullable=False)
    organization_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("organization.id", ondelete="CASCADE")
    )

    organization: Mapped["Organization"] = relationship(
        back_populates="phones")

    __table_args__ = (
        UniqueConstraint("organization_id", "phone_number",
                         name="uq_org_phone_unique"),
        Index("ix_org_phone_org", "organization_id"),
        Index("ix_org_phone_number", "phone_number"),
    )


class OrganizationOffice(Base):
    __tablename__ = "organization_office"

    organization_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("organization.id", ondelete="CASCADE"),
        primary_key=True
    )
    office_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("office.id", ondelete="CASCADE"),
        primary_key=True
    )

    __table_args__ = (Index("ix_org_office_office", "office_id"),)


class OrganizationActivity(Base):
    __tablename__ = "organization_activity"

    organization_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("organization.id", ondelete="CASCADE"), 
        primary_key=True
    )
    activity_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("activity.id", ondelete="RESTRICT"),
        primary_key=True
    )

    __table_args__ = (Index("ix_org_activity_activity", "activity_id"),)
