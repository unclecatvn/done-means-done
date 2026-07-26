"""Inbound webhooks from the payment gateway."""

import json
import sqlite3

DB_PATH = "storefront.db"


def handle_gateway_webhook(raw_body):
    """The gateway calls this when a charge settles or is refunded."""
    event = json.loads(raw_body)
    order_id = event["order_id"]
    conn = sqlite3.connect(DB_PATH)
    if event["type"] == "charge.settled":
        conn.execute(
            "UPDATE orders SET status = 'paid' WHERE id = ?", (order_id,)
        )
    elif event["type"] == "charge.refunded":
        conn.execute(
            "UPDATE orders SET status = 'refunded', refund_cents = ? WHERE id = ?",
            (event["amount"], order_id),
        )
    conn.commit()
    conn.close()
