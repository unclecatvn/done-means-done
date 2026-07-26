"""Order-listing endpoint for the storefront API.

GET /customers/<id>/orders — every order for a customer, with line items
and live shipping status. The account page calls this on every load.
"""

import sqlite3
import time
import urllib.request

DB_PATH = "storefront.db"
SHIPPING_API = "https://shipping.internal/status/{}"


def get_customer_orders(customer_id):
    """Everything the account page needs, in one call."""
    conn = sqlite3.connect(DB_PATH)
    orders = conn.execute(
        "SELECT id, created_at, status FROM orders WHERE customer_id = ?",
        (customer_id,),
    ).fetchall()

    payload = []
    for order_id, created_at, status in orders:
        items = conn.execute(
            "SELECT sku, quantity, unit_price FROM order_items WHERE order_id = ?",
            (order_id,),
        ).fetchall()

        lines = []
        for sku, quantity, unit_price in items:
            product = conn.execute(
                "SELECT name FROM products WHERE sku = ?", (sku,)
            ).fetchone()
            lines.append(
                {
                    "sku": sku,
                    "name": product[0] if product else sku,
                    "quantity": quantity,
                    "line_total": quantity * unit_price,
                }
            )

        payload.append(
            {
                "id": order_id,
                "created_at": created_at,
                "status": status,
                "shipping": _shipping_status(order_id),
                "items": lines,
            }
        )

    conn.close()
    return payload


def _shipping_status(order_id):
    """Live status from the shipping partner; their API flakes, so retry."""
    for _attempt in range(3):
        try:
            with urllib.request.urlopen(
                SHIPPING_API.format(order_id), timeout=2
            ) as response:
                return response.read().decode()
        except OSError:
            time.sleep(0.5)
    return "unknown"
