import uuid
from pydantic import BaseModel, Field


class BuildingBase(BaseModel):
    address: str = Field(..., example="г. Москва, ул. Ленина 1, офис 3")
    lat: float = Field(..., example=55.751244)
    lon: float = Field(..., example=37.618423)


class BuildingRead(BuildingBase):
    id: uuid.UUID

    class Config:
        from_attributes = True
