from fastapi import FastAPI, HTTPException
from typing import List
from solution.Service_Layer.product_data_model import Product
from solution.Service_Layer.products_service import ProductsService
from starlette.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_404_NOT_FOUND

app = FastAPI()


product_service = ProductsService()


@app.get("/products", status_code=HTTP_200_OK)
def get_all_products() -> List[Product]:
    return product_service.get_all_products()


@app.get("/products/{products_id}", status_code=HTTP_200_OK)
def get_product_by_id(products_id: int) -> Product | None:
    try:
        return product_service.get_product_by_id(products_id)
    except ValueError as error:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail=str(error))


@app.post("/products", status_code=HTTP_201_CREATED)
def create_product(name: str, description: str, price: float, stock: int) -> Product:
    return product_service.create_product(name, description, price, stock)
