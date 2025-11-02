from uuid import UUID

from fastapi import APIRouter, Query, HTTPException, status, Depends

from app.api.v1.dependencies import get_organization_service, verify_api_key
from app.schemas.org_response import OrganizationListResponse, \
    OrganizationDetailResponse
from app.services.org_service import OrganizationService

router = APIRouter(
    prefix="/organizations",
    tags=["Organizations"],
    dependencies=[Depends(verify_api_key)]
)


@router.get(
    "/by-building/{building_id}",
    response_model=OrganizationListResponse,
    summary="Организации в конкретном здании",
)
async def get_by_building(
    building_id: UUID,
    service: OrganizationService = Depends(get_organization_service),
):
    return await service.get_by_building(building_id)


@router.get(
    "/by-activity/{activity_id}",
    response_model=OrganizationListResponse,
    summary="Организации по виду деятельности (включая вложенные категории)",
)
async def get_by_activity(
    activity_id: UUID,
    service: OrganizationService = Depends(get_organization_service),
):
    try:
        return await service.get_by_activity(activity_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get(
    "/geo",
    response_model=OrganizationListResponse,
    summary="Организации в заданной области по координатам",
)
async def get_in_area(
    lat_min: float = Query(..., description="Минимальная широта"),
    lat_max: float = Query(..., description="Максимальная широта"),
    lon_min: float = Query(..., description="Минимальная долгота"),
    lon_max: float = Query(..., description="Максимальная долгота"),
    service: OrganizationService = Depends(get_organization_service),
):
    return await service.get_in_area(lat_min, lat_max, lon_min, lon_max)


@router.get(
    "/search",
    response_model=OrganizationListResponse,
    summary="Поиск организаций по названию",
)
async def search_by_name(
    q: str = Query(..., min_length=2,
                   description="Поисковый запрос (название организации)"),
    service: OrganizationService = Depends(get_organization_service),
):
    try:
        return await service.search_by_name(q)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get(
    "/{organization_id}",
    response_model=OrganizationDetailResponse,
    summary="Получить информацию об организации по ID",
)
async def get_by_id(
    organization_id: UUID,
    service: OrganizationService = Depends(get_organization_service),
):
    org = await service.get_by_id(organization_id)
    if not org:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Организация с ID={organization_id} не найдена",
        )
    return org
