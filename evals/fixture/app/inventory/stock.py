"""Units on hand per SKU."""

STOCK = {"WID-001": 40, "GAD-002": 0}


def normalize_sku(raw):
    """Canonical form of a SKU as typed by a person."""
    cleaned = raw.strip().upper().replace(" ", "")
    if "-" not in cleaned and len(cleaned) > 3:
        cleaned = cleaned[:3] + "-" + cleaned[3:]
    return cleaned


def in_stock(raw_sku):
    return STOCK.get(normalize_sku(raw_sku), 0) > 0


def low_stock_skus(threshold):
    """SKUs at or below a stock threshold, lowest first."""
    low = []
    for sku, count in STOCK.items():
        if count <= threshold:
            low.append((count, sku))
    low.sort()
    return [sku for _, sku in low]
