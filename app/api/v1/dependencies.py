from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.database import get_db_session
from app.repositories.org_repo import OrganizationRepository
from app.services.org_service import OrganizationService


async def get_db() -> AsyncSession:
    async with get_db_session() as session:
        yield session


async def get_organization_repository(
    session: AsyncSession = Depends(get_db),
) -> OrganizationRepository:
    return OrganizationRepository(session)


async def get_organization_service(
    repository: OrganizationRepository = Depends(get_organization_repository),
) -> OrganizationService:
    return OrganizationService(repository)
