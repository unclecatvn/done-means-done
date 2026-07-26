"""Apply warehouse deltas to the stock table."""

import sqlite3

DB_PATH = "storefront.db"


def apply_delta(sku, delta):
    """Called concurrently by the warehouse scanners' sync workers."""
    conn = sqlite3.connect(DB_PATH)
    current = conn.execute(
        "SELECT stock FROM inventory WHERE sku = ?", (sku,)
    ).fetchone()[0]
    new_stock = current + delta
    conn.execute(
        "UPDATE inventory SET stock = ? WHERE sku = ?", (new_stock, sku)
    )
    conn.commit()
    conn.close()
    return new_stock
