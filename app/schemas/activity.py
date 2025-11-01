import uuid
from pydantic import BaseModel, Field


class ActivityBase(BaseModel):
    name: str = Field(..., example="Еда")


class ActivityRead(ActivityBase):
    id: uuid.UUID
    parent_id: uuid.UUID | None = None

    class Config:
        from_attributes = True


class ActivityTree(ActivityRead):
    children: list["ActivityTree"] = []

    class Config:
        from_attributes = True
        arbitrary_types_allowed = True


ActivityTree.model_rebuild()
