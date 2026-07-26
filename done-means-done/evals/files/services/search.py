"""Product search box on the storefront."""

import sqlite3

DB_PATH = "storefront.db"


def search_products(query, limit=20):
    """Substring search over product names and descriptions."""
    conn = sqlite3.connect(DB_PATH)
    sql = (
        "SELECT sku, name, unit_price FROM products "
        f"WHERE name LIKE '%{query}%' OR description LIKE '%{query}%' "
        f"ORDER BY name LIMIT {limit}"
    )
    rows = conn.execute(sql).fetchall()
    conn.close()
    return [
        {"sku": sku, "name": name, "unit_price": price}
        for sku, name, price in rows
    ]
