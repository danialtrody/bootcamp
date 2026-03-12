import asyncio
from fastapi import APIRouter, Depends, HTTPException
from typing import List, Dict, Any
from solution.services.account_service import AccountService
from solution.api.dependencies import get_account_service
from starlette.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
)


ACCOUNT_ID = "id"
ACCOUNT_NAME = "name"
ACCOUNT_OPENING_BALANCE = "opening_balance"


router = APIRouter(prefix="/accounts", tags=["Accounts"])
account_service_dependency: AccountService = Depends(get_account_service)


@router.get("/", status_code=HTTP_200_OK, response_model=None)
async def get_all_accounts(
    service: AccountService = account_service_dependency,
) -> List[Dict[str, Any]]:
    accounts = await service.get_all_accounts()
    balances = await asyncio.gather(
        *[service.get_account_balance(account["id"]) for account in accounts]
    )
    result = []
    for account, balance in zip(accounts, balances):
        result.append(
            {
                ACCOUNT_ID: account[ACCOUNT_ID],
                ACCOUNT_NAME: account[ACCOUNT_NAME],
                ACCOUNT_OPENING_BALANCE: account[ACCOUNT_OPENING_BALANCE],
                "balance": balance,
            }
        )
    return result


@router.get("/{account_id}", status_code=HTTP_200_OK, response_model=None)
async def get_account(
    account_id: int, service: AccountService = account_service_dependency
) -> Dict[str, Any]:
    try:
        account = await service.get_account(account_id)
    except ValueError as error:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail=str(error))
    try:
        balance = await service.get_account_balance(account_id)
    except ValueError as error:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail=str(error))

    return {
        ACCOUNT_ID: account[ACCOUNT_ID],
        ACCOUNT_NAME: account[ACCOUNT_NAME],
        ACCOUNT_OPENING_BALANCE: account[ACCOUNT_OPENING_BALANCE],
        "balance": balance,
    }


@router.post("/", status_code=HTTP_201_CREATED, response_model=None)
async def add_account(
    account_data: Dict[str, Any], service: AccountService = account_service_dependency
) -> Dict[str, Any]:
    try:
        return await service.add_account(account_data)
    except ValueError as error:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=str(error))


@router.put("/{account_id}", status_code=HTTP_200_OK, response_model=None)
async def update_account_name(
    account_id: int,
    updated_name: str,
    service: AccountService = account_service_dependency,
) -> Dict[str, Any]:
    try:
        return await service.update_account_name(account_id, updated_name)
    except ValueError as error:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=str(error))


@router.delete("/{account_id}", status_code=HTTP_200_OK, response_model=None)
async def delete_account(
    account_id: int, service: AccountService = account_service_dependency
) -> Dict[str, str]:
    try:
        await service.delete_account(account_id)
    except ValueError as error:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=str(error))

    return {"message": "Account deleted"}
