from http.client import HTTPException

from fastapi import Depends, Security
from fastapi.security import APIKeyHeader
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from app.core.config import settings
from app.database.database import get_db_session
from app.repositories.org_repo import OrganizationRepository
from app.services.org_service import OrganizationService

api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)


async def get_db() -> AsyncSession:
    async with get_db_session() as session:
        yield session


async def get_organization_repository(
        session: AsyncSession = Depends(get_db),
) -> OrganizationRepository:
    return OrganizationRepository(session)


async def get_organization_service(
        repository: OrganizationRepository = Depends(
            get_organization_repository),
) -> OrganizationService:
    return OrganizationService(repository)


async def verify_api_key(api_key: str = Security(api_key_header)):
    if not api_key or api_key != settings.api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing API key",
        )
    return api_key
