from fastapi import APIRouter, Depends

from app.api.v1.endpoints import banks, dashboard, imports, maintenance, outages, statistics
from app.core.rate_limit import enforce_rate_limit
from app.core.security import verify_basic_auth


api_router = APIRouter(dependencies=[Depends(verify_basic_auth), Depends(enforce_rate_limit)])
api_router.include_router(banks.router, prefix="/banks", tags=["banks"])
api_router.include_router(outages.router, prefix="/outages", tags=["outages"])
api_router.include_router(maintenance.router, prefix="/maintenance", tags=["maintenance"])
api_router.include_router(statistics.router, prefix="/statistics", tags=["statistics"])
api_router.include_router(imports.router, prefix="/imports", tags=["imports"])
api_router.include_router(dashboard.router, prefix="/dashboard", tags=["dashboard"])
