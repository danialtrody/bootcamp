from fastapi import APIRouter, Depends, HTTPException
from solution.services.dashboard_service import DashboardService
from solution.api.dependencies import get_dashboard_service
from typing import Any, Dict
from starlette.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_200_OK,
)

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])
dashboard_service_dependency: DashboardService = Depends(get_dashboard_service)


@router.get("/", status_code=HTTP_200_OK)
def get_dashboard_summary(
    service: DashboardService = dashboard_service_dependency,
) -> Dict[str, Any]:

    try:
        return service.get_dashboard_summary()
    except ValueError as error:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=str(error))
