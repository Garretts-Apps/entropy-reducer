"""Run from the app directory: python3 -m unittest discover -s tests -t ."""
import unittest

from inventory import catalog, exporters, pricing, stock, views

ROWS = [{"sku": "WID-001", "name": "Widget", "price": 8.55}]


class CatalogTest(unittest.TestCase):
    def test_find_item_normalizes_the_sku(self):
        self.assertEqual(catalog.find_item(" wid001 ")["name"], "Widget")

    def test_unknown_sku_raises(self):
        with self.assertRaises(KeyError):
            catalog.find_item("nope")


class PricingTest(unittest.TestCase):
    def test_discount_applies(self):
        self.assertEqual(pricing.price_for("WID-001", 9.5), 8.55)

    def test_no_discount(self):
        self.assertEqual(pricing.price_for("GAD-002", 24.0), 24.0)


class StockTest(unittest.TestCase):
    def test_in_stock_normalizes_the_sku(self):
        self.assertTrue(stock.in_stock("wid 001"))
        self.assertFalse(stock.in_stock("GAD-002"))


class ExportTest(unittest.TestCase):
    def test_every_enabled_format_exports(self):
        expected = {
            "csv": "sku,name,price\nWID-001,Widget,8.55",
            "json": '[{"sku": "WID-001", "name": "Widget", "price": 8.55}]',
            "ndjson": '{"sku": "WID-001", "price": 8.55}',
        }
        for fmt, text in expected.items():
            self.assertEqual(exporters.run_export(fmt, ROWS), text)

    def test_unknown_format_raises(self):
        with self.assertRaises(ValueError):
            exporters.run_export("xml", ROWS)


class ViewsTest(unittest.TestCase):
    def test_page_markup(self):
        self.assertEqual(
            views.render_page(catalog.ITEMS),
            '<ul><li class="item featured"><span class="price">$9.50</span>'
            "<strong>Widget</strong></li>"
            '<li class="item"><span class="name">Gadget</span> '
            '<span class="price">$24.00</span></li></ul>',
        )


if __name__ == "__main__":
    unittest.main()
