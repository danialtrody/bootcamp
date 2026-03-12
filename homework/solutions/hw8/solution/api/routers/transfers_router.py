from fastapi import APIRouter, Depends, HTTPException
from solution.services.transfer_service import TransferService
from solution.api.dependencies import get_transfer_service
from typing import List, Dict, Any
from starlette.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_201_CREATED,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK,
)

router = APIRouter(prefix="/transfer", tags=["Transfer"])
transfer_service_dependency: TransferService = Depends(get_transfer_service)


@router.get("/", status_code=HTTP_200_OK, response_model=None)
async def get_all_transfers(
    service: TransferService = transfer_service_dependency,
) -> List[Dict[str, Any]]:
    try:
        return await service.get_all_transfers()
    except ValueError as error:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail=str(error))


@router.post("/", status_code=HTTP_201_CREATED, response_model=None)
async def add_transfer(
    transfer_data: Dict[str, Any], service: TransferService = transfer_service_dependency
) -> Dict[str, Any]:

    try:
        return await service.add_transfer(transfer_data)
    except ValueError as error:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=str(error))


@router.delete("/{transfer_id}", status_code=HTTP_200_OK, response_model=None)
async def delete_transfer(
    transfer_id: int, service: TransferService = transfer_service_dependency
) -> Dict[str, str]:
    try:
        await service.delete_transfer(transfer_id)
    except ValueError as error:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=str(error))

    return {"message": "Transfer deleted"}
