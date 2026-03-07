from fastapi import APIRouter, Depends, HTTPException


from solution.services.net_worth_service import NetWorth
from solution.api.dependencies import get_net_worth_service

router = APIRouter(prefix="/net_worth", tags=["Net Worth"])



@router.get("/")
def get_all_account_net_worth(
    service: NetWorth = Depends(get_net_worth_service)
    ):
        
    try:
        return service.calculate_net_worth()
    except Exception  as error:
        raise HTTPException(status_code=400, detail=str(error))
    
