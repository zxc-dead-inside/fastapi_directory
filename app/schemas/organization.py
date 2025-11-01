import uuid
from pydantic import BaseModel, Field

from app.schemas.building import BuildingRead
from app.schemas.activity import ActivityRead


class OrganizationBase(BaseModel):
    name: str = Field(..., example="ООО 'Рога и Копыта'")


class OrganizationPhone(BaseModel):
    number: str = Field(..., example="8-923-666-13-13")

    class Config:
        from_attributes = True


class OrganizationReadShort(OrganizationBase):
    id: uuid.UUID
    phones: list[OrganizationPhone] = []
    building_id: uuid.UUID | None = None

    class Config:
        from_attributes = True


class OrganizationReadDetail(OrganizationReadShort):
    building: BuildingRead | None
    activities: list[ActivityRead] = []

    class Config:
        from_attributes = True
