from fastapi import APIRouter, Depends, HTTPException
from solution.services.transaction_service import TransactionService
from solution.api.dependencies import get_transaction_service
from typing import List, Optional, Dict, Any
from starlette.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_201_CREATED,
    HTTP_200_OK,
)

router = APIRouter(prefix="/transactions", tags=["Transactions"])
account_service_dependency: TransactionService = Depends(get_transaction_service)


@router.get("/", status_code=HTTP_200_OK, response_model=None)
async def get_all_transactions(
    account_id: Optional[int] = None,
    month: Optional[int] = None,
    year: Optional[int] = None,
    service: TransactionService = account_service_dependency,
) -> List[Dict[str, Any]]:

    return await service.get_all_transactions(account_id, month, year)


@router.post("/income", status_code=HTTP_201_CREATED, response_model=None)
async def add_income(
    transaction_data: Dict[str, Any],
    service: TransactionService = account_service_dependency,
) -> Dict[str, Any]:
    try:
        return await service.add_income(transaction_data)
    except ValueError as error:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=str(error))


@router.post("/expense", status_code=HTTP_201_CREATED, response_model=None)
async def add_expense(
    transaction_data: Dict[str, Any],
    service: TransactionService = account_service_dependency,
) -> Dict[str, Any]:
    try:
        return await service.add_expense(transaction_data)
    except ValueError as error:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=str(error))


@router.delete("/{transaction_id}", status_code=HTTP_200_OK, response_model=None)
async def delete_transaction(
    transaction_id: int, service: TransactionService = account_service_dependency
) -> Dict[str, str]:
    try:
        await service.delete_transaction(transaction_id)
    except ValueError as error:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=str(error))
    return {"message": "Transaction deleted"}
