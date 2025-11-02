import uuid

from pydantic import BaseModel, Field

from app.schemas.activity import ActivityRead
from app.schemas.building import BuildingRead


class OfficeRead(BaseModel):
    id: uuid.UUID
    floor: int | None = Field(None, example=3)
    unit: str | None = Field(None, example="12A")
    building: BuildingRead

    class Config:
        from_attributes = True


class OrganizationBase(BaseModel):
    name: str = Field(..., example="ООО 'Рога и Копыта'")


class OrganizationPhone(BaseModel):
    phone_number: str = Field(..., example="8-923-666-13-13")

    class Config:
        from_attributes = True


class OrganizationReadShort(OrganizationBase):
    id: uuid.UUID
    phones: list[OrganizationPhone] = []
    offices: list[OfficeRead] = []

    class Config:
        from_attributes = True


class OrganizationReadDetail(OrganizationReadShort):
    offices: list[OfficeRead] = []
    activities: list[ActivityRead] = []

    class Config:
        from_attributes = True
