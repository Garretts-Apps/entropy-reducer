"""Command-line entry point: python3 main.py [html | stock <sku> | <export format>]"""
import sys

from inventory.catalog import ITEMS
from inventory.exporters import run_export
from inventory.pricing import price_for
from inventory.stock import in_stock
from inventory.views import render_page


def main(argv):
    fmt = argv[1] if len(argv) > 1 else "html"
    if fmt == "html":
        print(render_page(ITEMS))
        return 0
    if fmt == "stock":
        print("yes" if in_stock(argv[2]) else "no")
        return 0
    rows = [dict(item, price=price_for(item["sku"], item["price"])) for item in ITEMS]
    print(run_export(fmt, rows))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
