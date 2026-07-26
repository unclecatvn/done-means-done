"""Tiny read-through cache for product lookups."""

import sqlite3

DB_PATH = "storefront.db"

_cache = {}


def get_product(sku):
    """Product row by SKU, cached forever — the catalog rarely changes."""
    if sku in _cache:
        return _cache[sku]
    conn = sqlite3.connect(DB_PATH)
    row = conn.execute(
        "SELECT sku, name, description, unit_price FROM products WHERE sku = ?",
        (sku,),
    ).fetchone()
    conn.close()
    _cache[sku] = row
    return row
