from fastapi import APIRouter, Depends, HTTPException
from solution.services.report_service import ReportService
from solution.api.dependencies import get_report_service
from typing import Optional
from decimal import Decimal

from starlette.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_200_OK,
)

router = APIRouter(prefix="/reports", tags=["Reports"])
reports_service_dependency: ReportService = Depends(get_report_service)


@router.get("/monthly-summary", status_code=HTTP_200_OK)
async def get_monthly_summary(
    month: int,
    year: int,
    account_id: Optional[int] = None,
    service: ReportService = reports_service_dependency,
) -> dict[str, Decimal]:

    try:
        return await service.get_monthly_summary(month, year, account_id)
    except ValueError as error:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=str(error))


@router.get("/spending-breakdown", status_code=HTTP_200_OK)
async def get_spending_breakdown_by_category(
    month: int,
    year: int,
    account_id: Optional[int] = None,
    service: ReportService = reports_service_dependency,
) -> dict[str, Decimal]:

    try:
        return await service.get_spending_breakdown_by_category(month, year, account_id)
    except ValueError as error:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=str(error))
