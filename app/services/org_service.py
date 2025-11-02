from uuid import UUID

from app.repositories.org_repo import OrganizationRepository
from app.schemas.org_response import OrganizationListResponse, \
    OrganizationDetailResponse
from app.schemas.organization import OrganizationReadShort, \
    OrganizationReadDetail


class OrganizationService:
    def __init__(self, repository: OrganizationRepository):
        self.repository = repository

    async def get_by_building(self, building_id: UUID) -> OrganizationListResponse:
        organizations = await self.repository.get_by_building(building_id)
        return OrganizationListResponse(
            total=len(organizations),
            items=[OrganizationReadShort.from_orm(org) for org in organizations],
        )

    async def get_by_activity(self, activity_id: UUID, max_depth: int = 3) -> OrganizationListResponse:
        if max_depth > 3:
            raise ValueError("Максимальная глубина вложенности видов деятельности — 3")
        organizations = await self.repository.get_by_activity(activity_id)
        return OrganizationListResponse(
            total=len(organizations),
            items=[OrganizationReadShort.from_orm(org) for org in organizations],
        )

    async def get_in_area(
            self, lat_min: float, lat_max: float,
            lon_min: float, lon_max: float
    ) -> OrganizationListResponse:
        organizations = await self.repository.get_in_area(
            lat_min, lat_max, lon_min, lon_max
        )
        return OrganizationListResponse(
            total=len(organizations),
            items=[OrganizationReadShort.from_orm(org) for org in organizations],
        )

    async def search_by_name(self, query: str) -> OrganizationListResponse:
        query = query.strip()
        if len(query) < 2:
            raise ValueError("Минимальная длина запроса — 2 символа")
        organizations = await self.repository.search_by_name(query)
        return OrganizationListResponse(
            total=len(organizations),
            items=[OrganizationReadShort.from_orm(org) for org in organizations],
        )

    async def get_by_id(
            self, organization_id: UUID
    ) -> OrganizationDetailResponse | None:
        org = await self.repository.get_by_id(organization_id)
        if not org:
            return None
        return OrganizationDetailResponse(
            organization=OrganizationReadDetail.from_orm(org)
        )
