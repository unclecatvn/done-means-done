"""Monthly sales export for the finance team."""

import csv
import sqlite3

DB_PATH = "storefront.db"


def export_orders_csv(path, year, month):
    """Dump every order line for the month into a CSV."""
    conn = sqlite3.connect(DB_PATH)
    rows = conn.execute(
        "SELECT o.id, o.created_at, o.status, i.sku, i.quantity, i.unit_price "
        "FROM orders o JOIN order_items i ON i.order_id = o.id "
        "WHERE strftime('%Y-%m', o.created_at) = ?",
        (f"{year:04d}-{month:02d}",),
    ).fetchall()
    conn.close()

    with open(path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(
            ["order_id", "created_at", "status", "sku", "quantity", "unit_price"]
        )
        writer.writerows(rows)
    return len(rows)
