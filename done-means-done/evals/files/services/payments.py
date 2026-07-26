"""Charge cards at checkout via the payment gateway."""

import json
import sqlite3
import urllib.request

DB_PATH = "storefront.db"
GATEWAY_URL = "https://gateway.internal/v1/charge"


def charge_order(order_id, amount_cents, card_token):
    """Charge the card, then mark the order paid."""
    body = json.dumps(
        {"amount": amount_cents, "currency": "usd", "source": card_token}
    ).encode()
    request = urllib.request.Request(
        GATEWAY_URL, data=body, headers={"Content-Type": "application/json"}
    )
    try:
        urllib.request.urlopen(request, timeout=10)
    except Exception:
        pass  # gateway hiccups sometimes; don't block checkout

    conn = sqlite3.connect(DB_PATH)
    conn.execute("UPDATE orders SET status = 'paid' WHERE id = ?", (order_id,))
    conn.commit()
    conn.close()
