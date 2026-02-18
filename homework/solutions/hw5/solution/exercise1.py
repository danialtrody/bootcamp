from typing import Any


class Item:
    def __init__(self, name: str, base_price: float, weight: float) -> None:
        self.name: str = name
        self.base_price: float = base_price
        self.weight: float = weight

    def get_info(self) -> str:
        return (
            f"Item: {self.name}, "
            f"Base Price: ${self.base_price:.2f}, "
            f"Weight: {self.weight}kg"
        )


class DiscountMixin:
    def __init__(self, discount_percent: float = 0, **kwargs: Any) -> None:
        self.discount_percent: float = discount_percent
        super().__init__(**kwargs)

    def get_price(self) -> float:
        return self.base_price * (1 - self.discount_percent / 100)


class ShippingMixin:
    shipping_rate_per_kg: float = 5.0

    def get_shipping_cost(self) -> float:
        return self.weight * self.shipping_rate_per_kg


class Product(DiscountMixin, ShippingMixin, Item):
    def __init__(
        self, name: str, base_price: float, weight: float, discount_percent: float = 0
    ) -> None:
        super().__init__(
            name=name,
            base_price=base_price,
            weight=weight,
            discount_percent=discount_percent,
        )

    def get_total_cost(self) -> float:
        return self.get_price() + self.get_shipping_cost()

    def get_info(self) -> str:
        price_after_discount: float = self.get_price()
        shipping_cost: float = self.get_shipping_cost()
        total: float = self.get_total_cost()

        return (
            f"Product: {self.name}, "
            f"Price after Discount: ${price_after_discount:.2f}, "
            f"Shipping: ${shipping_cost:.2f}, "
            f"Total: ${total:.2f}"
        )


class DigitalProduct(DiscountMixin, Item):
    def __init__(
        self, name: str, base_price: float, discount_percent: float = 0
    ) -> None:
        super().__init__(
            name=name,
            base_price=base_price,
            weight=0,
            discount_percent=discount_percent,
        )

    def get_info(self) -> str:
        price_after_discount: float = self.get_price()

        return (
            f"Digital Product: {self.name}, "
            f"Price after Discount: ${price_after_discount:.2f} "
            f"(no shipping)"
        )
