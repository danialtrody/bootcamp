from solution.exercise1 import Product
from solution.exercise1 import DigitalProduct


def test_product_mro_order() -> None:
    mro = Product.mro()

    assert mro[0].__name__ == "Product"
    assert mro[1].__name__ == "DiscountMixin"
    assert mro[2].__name__ == "ShippingMixin"
    assert mro[3].__name__ == "Item"


def test_get_info_override() -> None:
    product = Product("Laptop", 1000.0, 2.0, discount_percent=10)

    info = product.get_info()
    assert "Item:" not in info
    assert "Product:" in info
    assert "Total:" in info


def test_total_cost_with_discount_and_shipping() -> None:
    product = Product("Phone", 500.0, 1.0, discount_percent=20)

    assert product.get_price() == 400
    assert product.get_shipping_cost() == 5
    assert product.get_total_cost() == 405


def test_digital_product_no_shipping() -> None:
    ebook = DigitalProduct("Python Guide", 100.0, discount_percent=10)

    assert ebook.get_price() == 90
    assert ebook.weight == 0
