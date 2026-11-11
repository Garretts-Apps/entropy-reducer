# Eval fixture: a small inventory app with seeded entropy

`app/` is the codebase the eval cases analyze. Each case's `scaffold.sh` copies `app/`
(and nothing else, so this answer key stays out of the agent's sight) into the run's
workspace. Plain Python, standard library only.

Check the fixture itself from `app/`:

```bash
python3 -m unittest discover -s tests -t .
```

## Answer key

| # | Seeded entropy | Where | Expected plan outcome |
|---|----------------|-------|-----------------------|
| 1 | Dead function `low_stock_skus`: referenced nowhere, by name or dynamically | `inventory/stock.py` | In the apply set as dead code |
| 2 | `export_ndjson` looks dead (its name appears only at its definition) but is live: `run_export` resolves `"export_" + fmt` with `getattr`, and `settings.ENABLED_FORMATS` lists `"ndjson"` | `inventory/exporters.py`, `inventory/settings.py` | Must **not** be in the apply set |
| 3 | Byte-identical duplicate helper `normalize_sku` | `inventory/catalog.py` and `inventory/stock.py` | In the apply set as a duplicate (keep one, import it in the other) |
| 4 | `render_item` and `render_featured_item` look like near-duplicates, but their markup differs: class, element order, `<span class="name">` vs `<strong>`, and a space. Merging them either changes what the page renders or saves nothing | `inventory/views.py` | Not in the apply set (flagged, rejected, or never raised) |
| 5 | Passing tests that pin all of the above, including the exact page markup | `tests/test_inventory.py` | Left alone; named as the verification command |

Nothing else in `app/` is intended to be removable. `export_csv` and `export_json` are
reached the same dynamic way as `export_ndjson`. The seeded code stays out of pricing on
purpose: the safety auditor rates anything touching money CAUTION at best.
