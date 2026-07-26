"""Cart totals: line math, discounts, tax."""

TAX_RATE = 0.0875


def cart_total(items, discount_percent=0):
    """items: [{"unit_price": 19.99, "quantity": 3}, ...] -> amount to charge."""
    subtotal = 0.0
    for item in items:
        subtotal += item["unit_price"] * item["quantity"]
    discounted = subtotal * (1 - discount_percent / 100)
    total = discounted * (1 + TAX_RATE)
    return round(total, 2)
