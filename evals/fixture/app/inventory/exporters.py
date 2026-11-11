"""Catalog exports. One function per format, selected by name at run time."""
import json
import sys

from inventory.settings import ENABLED_FORMATS

FIELDS = ["sku", "name", "price"]


def export_csv(rows):
    lines = [",".join(FIELDS)]
    for row in rows:
        lines.append(",".join(str(row[field]) for field in FIELDS))
    return "\n".join(lines)


def export_json(rows):
    return json.dumps([{field: row[field] for field in FIELDS} for row in rows])


def export_ndjson(rows):
    return "\n".join(json.dumps({"sku": row["sku"], "price": row["price"]}) for row in rows)


def run_export(fmt, rows):
    if fmt not in ENABLED_FORMATS:
        raise ValueError("unknown export format: " + fmt)
    exporter = getattr(sys.modules[__name__], "export_" + fmt)
    return exporter(rows)
