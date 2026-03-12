from decimal import Decimal
from fastapi import APIRouter, Depends, HTTPException
from solution.services.net_worth_service import NetWorth
from solution.api.dependencies import get_net_worth_service
from starlette.status import HTTP_400_BAD_REQUEST, HTTP_200_OK

router = APIRouter(prefix="/net-worth", tags=["Net Worth"])
net_worth_service_dependency: NetWorth = Depends(get_net_worth_service)


@router.get("/", status_code=HTTP_200_OK)
def get_all_account_net_worth(
    service: NetWorth = net_worth_service_dependency,
) -> Decimal:

    try:
        return service.calculate_net_worth()
    except ValueError as error:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=str(error))
