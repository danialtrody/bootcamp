from fastapi import APIRouter, Depends, HTTPException
from solution.services.category_service import CategoryService
from solution.models.categories import Category
from solution.api.dependencies import get_category_service
from typing import List, Dict
from starlette.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_201_CREATED,
    HTTP_200_OK,
)

router = APIRouter(prefix="/categories", tags=["Categories"])
category_service_dependency: CategoryService = Depends(get_category_service)


@router.get("/", status_code=HTTP_200_OK)
def get_all_categories(
    service: CategoryService = category_service_dependency,
) -> List[Category]:
    return service.get_all_categories()


@router.post("/", status_code=HTTP_201_CREATED)
def add_category(
    category: Category, service: CategoryService = category_service_dependency
) -> Category:

    try:
        return service.add_category(category)
    except ValueError as error:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=str(error))


@router.delete("/{category_id}", status_code=HTTP_200_OK)
def delete_category(
    category_id: int, service: CategoryService = category_service_dependency
) -> Dict:

    try:
        service.delete_category(category_id)
    except ValueError as error:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=str(error))

    return {"message": "Account deleted"}
