from fastapi import APIRouter, Depends, HTTPException
from solution.services.transaction_service import TransactionService
from solution.models.transaction import Transaction
from solution.api.dependencies import get_transaction_service
from typing import List, Optional, Dict
from starlette.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_201_CREATED,
    HTTP_200_OK,
)

router = APIRouter(prefix="/transactions", tags=["Transactions"])
account_service_dependency: TransactionService = Depends(get_transaction_service)


@router.get("/", status_code=HTTP_200_OK)
def get_all_transactions(
    account_id: Optional[int] = None,
    month: Optional[int] = None,
    year: Optional[int] = None,
    service: TransactionService = account_service_dependency,
) -> List[Transaction]:

    return service.get_all_transactions(account_id, month, year)


@router.post("/income", status_code=HTTP_201_CREATED)
def add_income(
    transaction: Transaction, service: TransactionService = account_service_dependency
) -> Transaction:
        try:
            return service.add_income(transaction)
        except ValueError as error:
            raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=str(error))


@router.post("/expense", status_code=HTTP_201_CREATED)
def add_income(
    transaction: Transaction, service: TransactionService = account_service_dependency
) -> Transaction:
        try:
            return service.add_expense(transaction)
        except ValueError as error:
            raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=str(error))


@router.delete("/{transaction_id}", status_code=HTTP_200_OK)
def delete_transaction(
    transaction_id: int, service: TransactionService = account_service_dependency
) -> Dict[str, str]:
    try:
        service.delete_transaction(transaction_id)
    except ValueError as error:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=str(error))
    return {"message": "Transaction deleted"}
