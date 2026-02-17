import json
from typing import Optional
from solution.Service_Layer.product_data_model import Product

# run -> python -m solution.Service_Layer.products_service


READ_FROM_FILE = "r"
WRITE_TO_FILE = "w"

JSON_FILE_PATH = "solution/products.json"


class ProductsService:
    def __init__(self) -> None:

        with open(JSON_FILE_PATH, READ_FROM_FILE) as file:
            self.products = json.load(file)

        for index, product in enumerate(self.products):
            self.products[index] = Product(**product)

    def get_all_products(self) -> list[Product]:
        return self.products

    def get_product_by_id(self, product_id: int) -> Optional[Product]:

        for product in self.products:
            if product.id == product_id:
                return product

        raise ValueError(f"ID:{product_id} not found")

    def create_product(
        self, name: str, description: str, price: float, stock: int
    ) -> Product:

        new_id = len(self.products) + 1
        new_item = {
            "id": new_id,
            "name": name,
            "description": description,
            "price": price,
            "stock": stock,
        }

        new_product = Product(**new_item)
        self.products.append(new_product)

        with open(JSON_FILE_PATH, WRITE_TO_FILE) as file:
            json.dump([product.__dict__ for product in self.products], file, indent=4)

        return new_product
