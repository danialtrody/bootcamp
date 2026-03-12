from fastapi import APIRouter, Depends, HTTPException
from solution.services.category_service import CategoryService
from solution.api.dependencies import get_category_service
from typing import List, Dict, Any
from starlette.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_201_CREATED,
    HTTP_200_OK,
)

router = APIRouter(prefix="/categories", tags=["Categories"])
category_service_dependency: CategoryService = Depends(get_category_service)


@router.get("/", status_code=HTTP_200_OK, response_model=None)
async def get_all_categories(
    service: CategoryService = category_service_dependency,
) -> List[Dict[str, Any]]:
    return await service.get_all_categories()


@router.post("/", status_code=HTTP_201_CREATED, response_model=None)
async def add_category(
    category_data: Dict[str, Any],
    service: CategoryService = category_service_dependency,
) -> Dict[str, Any]:

    try:
        return await service.add_category(category_data)
    except ValueError as error:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=str(error))


@router.delete("/{category_id}", status_code=HTTP_200_OK)
async def delete_category(
    category_id: int, service: CategoryService = category_service_dependency
) -> Dict[str, str]:

    try:
        await service.delete_category(category_id)
    except ValueError as error:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=str(error))

    return {"message": "Category deleted"}
