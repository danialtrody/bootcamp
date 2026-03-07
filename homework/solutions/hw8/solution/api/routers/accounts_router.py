from fastapi import APIRouter, Depends, HTTPException
from solution.services.account_service import AccountService
from solution.models.account import Account
from solution.api.dependencies import get_account_service
from starlette.status import(
    HTTP_400_BAD_REQUEST,
    HTTP_201_CREATED ,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK
    ) 



router = APIRouter(prefix="/accounts", tags=["Accounts"])


@router.get("/", status_code=HTTP_200_OK)
def get_all_account_balance(
    service: AccountService = Depends(get_account_service)
    ):
    
    accounts = service.get_all_accounts()
    result = []
    
    for account in accounts:
        result.append(
             {
            "id": account.id,
            "name": account.name,
            "balance": service.get_account_balance(account.id),
             }
        )

    return result

@router.get("/{account_id}", status_code=HTTP_200_OK)
def get_single_account_balance(
    account_id: int,
    service: AccountService = Depends(get_account_service)
    ):
    
    try:
        account = service.get_account(account_id)
    except ValueError   as error:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail=str(error)
            )
    
    return(
             {
            "id": account.id,
            "name": account.name,
            "balance": service.get_account_balance(account.id),
             }
        )

     
       
@router.post("/" , status_code=HTTP_201_CREATED)
def add_account(
    account: Account,
    service: AccountService = Depends(get_account_service),
):
    try:
        return service.add_account(account)
    except ValueError   as error:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail=str(error)
            )


@router.put("/{account_id}", status_code=HTTP_200_OK)
def update_account_name(
    account_id: int,
    updated_name: str,
    service: AccountService = Depends(get_account_service),
):
    try:
        return service.update_account_name(account_id, updated_name)
    except ValueError   as error:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail=str(error)
            )


@router.delete("/{account_id}" ,status_code=HTTP_200_OK)
def delete_account(
    account_id: int,
    service: AccountService = Depends(get_account_service),
):
    try:
        service.delete_account(account_id)
    except ValueError   as error:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail=str(error)
            )
    
    return {"message": "Account deleted"}

