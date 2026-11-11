"""The product catalog and SKU lookup."""

ITEMS = [
    {"sku": "WID-001", "name": "Widget", "price": 9.5, "featured": True},
    {"sku": "GAD-002", "name": "Gadget", "price": 24.0, "featured": False},
]


def normalize_sku(raw):
    """Canonical form of a SKU as typed by a person."""
    cleaned = raw.strip().upper().replace(" ", "")
    if "-" not in cleaned and len(cleaned) > 3:
        cleaned = cleaned[:3] + "-" + cleaned[3:]
    return cleaned


def find_item(raw_sku):
    sku = normalize_sku(raw_sku)
    for item in ITEMS:
        if item["sku"] == sku:
            return item
    raise KeyError(sku)
