"""Prices after discounts."""
from inventory.settings import DISCOUNTS


def price_for(sku, list_price):
    discount = DISCOUNTS.get(sku, 0.0)
    return round(list_price * (1 - discount), 2)
