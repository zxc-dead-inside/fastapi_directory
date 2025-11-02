from pydantic import BaseModel, Field
from app.schemas.organization import OrganizationReadShort, OrganizationReadDetail


class OrganizationListResponse(BaseModel):
    total: int = Field(..., example=100)
    items: list[OrganizationReadShort]

    class Config:
        from_attributes = True


class OrganizationDetailResponse(BaseModel):
    organization: OrganizationReadDetail | None = None

    class Config:
        from_attributes = True
