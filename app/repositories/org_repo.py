from collections.abc import Sequence
from uuid import UUID

from sqlalchemy import select, func, and_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload, selectinload

from app.database import Activity, Organization, Office, Building


class OrganizationRepository:

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_building(self, building_id: UUID) -> Sequence[Organization]:
        """organization via building"""
        stmt = (
            select(Organization)
            .join(Organization.offices)
            .join(Office.building)
            .where(Building.id == building_id)
            .options(
                selectinload(Organization.activities),
                selectinload(Organization.phones),
                selectinload(Organization.offices).selectinload(
                    Office.building),
            )
        )
        result = await self.session.execute(stmt)
        return result.scalars().unique().all()

    async def get_by_activity(
        self,
        activity_id: UUID,
    ) -> Sequence[Organization]:
        """
        Get organization via activity,
        include inner levels.
        """
        # рекурсивный CTE для поиска дочерних видов деятельности
        cte = (
            select(Activity.id, Activity.parent_id)
            .where(Activity.id == activity_id)
            .cte(name="activity_tree", recursive=True)
        )

        cte = cte.union_all(
            select(Activity.id, Activity.parent_id).where(
                Activity.parent_id == cte.c.id
            )
        )

        stmt = (
            select(Organization)
            .join(Organization.activities)
            .where(Activity.id.in_(select(cte.c.id)))
            .options(
                selectinload(Organization.activities),
                selectinload(Organization.phones),
                selectinload(Organization.offices).selectinload(
                    Office.building),
            )
        )

        result = await self.session.execute(stmt)
        return result.scalars().unique().all()

    async def search_by_name(self, query: str) -> Sequence[Organization]:
        """
        name search, ignore register.
        """
        stmt = (
            select(Organization)
            .where(func.lower(Organization.name).ilike(f"%{query.lower()}%"))
            .options(
                selectinload(Organization.activities),
                selectinload(Organization.phones),
                selectinload(Organization.offices).selectinload(
                    Office.building),
            )
        )
        result = await self.session.execute(stmt)
        return result.scalars().unique().all()

    async def get_in_area(
        self,
        lat_min: float,
        lat_max: float,
        lon_min: float,
        lon_max: float,
    ) -> Sequence[Organization]:
        """
        search organizations in area
        """
        stmt = (
            select(Organization)
            .join(Organization.offices)
            .join(Office.building)
            .where(
                and_(
                    Building.lat >= lat_min,
                    Building.lat <= lat_max,
                    Building.lon >= lon_min,
                    Building.lon <= lon_max,
                )
            )
            .options(
                selectinload(Organization.activities),
                selectinload(Organization.phones),
                selectinload(Organization.offices).selectinload(
                    Office.building),
            )
        )
        result = await self.session.execute(stmt)
        return result.scalars().unique().all()

    async def get_by_id(self, organization_id: UUID) -> Organization | None:
        stmt = (
            select(Organization)
            .where(Organization.id == organization_id)
            .options(
                selectinload(Organization.activities),
                selectinload(Organization.phones),
                selectinload(Organization.offices).selectinload(
                    Office.building),
            )
        )
        result = await self.session.execute(stmt)
        return result.scalars().first()

    async def get_all(self, limit: int = 100) -> Sequence[Organization]:
        stmt = (
            select(Organization)
            .limit(limit)
            .options(
                selectinload(Organization.activities),
                selectinload(Organization.phones),
                selectinload(Organization.offices).selectinload(
                    Office.building),
            )
        )
        result = await self.session.execute(stmt)
        return result.scalars().unique().all()
