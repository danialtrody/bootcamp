import json
import pytest
from typing import Tuple, List
from solution.Service_Layer import products_service
from solution.Service_Layer import product_data_model

JSON_FILE_PATH = "solution/products.json"
TEMP_JSON_FILE_PATH = "solution/temp_products.json"

READ_FROM_FILE = "r"
WRITE_TO_FILE = "w"

INDEX_NEGATIVE_ONE = -1
INDEX_ZERO = 0
INDEX_ONE = 1
INDEX_TWO = 2
INDEX_ONE_HUNDRED = 100

ProductsFixture = Tuple[
    List[dict],
    products_service.ProductsService,
]


TempFileFixture = Tuple[products_service.ProductsService, str]


@pytest.fixture()
def initialize_products() -> ProductsFixture:
    with open(JSON_FILE_PATH, READ_FROM_FILE) as file:
        json_products = json.load(file)

    service_products = products_service.ProductsService()

    return json_products, service_products


@pytest.fixture()
def products_service_temp_file() -> TempFileFixture:
    with open(JSON_FILE_PATH, READ_FROM_FILE) as file:
        data = json.load(file)

    with open(TEMP_JSON_FILE_PATH, WRITE_TO_FILE) as file:
        json.dump(data, file, indent=4)

    products_service.JSON_FILE_PATH = TEMP_JSON_FILE_PATH

    service = products_service.ProductsService()
    return service, TEMP_JSON_FILE_PATH


def get_products_as_dicts(
    service: list[product_data_model.Product],
) -> List[dict]:
    return [product.__dict__ for product in service]


def test_init(initialize_products: ProductsFixture) -> None:
    json_products, service_products = initialize_products

    products_as_dicts = get_products_as_dicts(service_products.products)

    assert products_as_dicts == json_products
    assert all(
        isinstance(
            product,
            product_data_model.Product,
        )
        for product in service_products.products
    )


def test_get_all_products(initialize_products: ProductsFixture) -> None:
    json_products, service_products = initialize_products

    products_as_dicts = get_products_as_dicts(
        service_products.get_all_products(),
    )

    assert products_as_dicts == json_products


@pytest.mark.parametrize(
    "product_id , json_index",
    [(INDEX_ONE, INDEX_ZERO), (INDEX_TWO, INDEX_ONE)],
)
def test_get_product_by_id_success(
    initialize_products: ProductsFixture,
    product_id: int,
    json_index: int,
) -> None:

    json_products, service_products = initialize_products

    service_product_by_id = service_products.get_product_by_id(product_id)

    assert service_product_by_id.__dict__ == json_products[json_index]


@pytest.mark.parametrize(
    "product_id",
    [INDEX_ZERO, INDEX_ONE_HUNDRED, INDEX_NEGATIVE_ONE],
)
def test_get_product_by_id_failed(
    initialize_products: ProductsFixture,
    product_id: int,
) -> None:

    service_products = initialize_products[1]

    with pytest.raises(ValueError, match=f"ID:{product_id} not found"):
        service_products.get_product_by_id(product_id)


def test_create_product(products_service_temp_file: TempFileFixture) -> None:
    service, temp_file = products_service_temp_file

    old_count = len(service.products)
    new_product = service.create_product(
        "Test Product",
        "Description",
        50,
        10,
    )

    assert isinstance(
        new_product,
        product_data_model.Product,
    )
    assert len(service.products) == old_count + 1
    assert service.products[-1] == new_product

    with open(temp_file, READ_FROM_FILE) as file:
        data = json.load(file)

    assert data[-1]["name"] == "Test Product"
    assert data[-1]["description"] == "Description"
    assert data[-1]["price"] == 50
    assert data[-1]["stock"] == 10
    assert data[-1]["id"] == new_product.id
