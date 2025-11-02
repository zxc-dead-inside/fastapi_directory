from fastapi import APIRouter
from app.api.v1.org_router import router as organization_router

api_router = APIRouter()
api_router.include_router(organization_router)
