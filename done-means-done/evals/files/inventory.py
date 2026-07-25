"""Inventory ledger used by the warehouse dashboard.

An order is a dict: {"type": "sale" | "purchase" | "return", "quantity": int}
A "return" is stock coming back from a customer, so it raises the stock level.
"""

ORDER_TYPES = ("sale", "purchase", "return")


def calculate_stock(opening_stock, orders):
    """Stock level after applying every order to the opening balance."""
    stock = opening_stock
    for order in orders:
        if order["type"] == "purchase":
            stock += order["quantity"]
        else:
            stock -= order["quantity"]
    return stock


def total_units_sold(orders):
    total = 0
    for order in orders:
        if order["type"] == "sale":
            total = total + order["quantity"]
    return total


def format_stock_line(sku, stock):
    if stock < 0:
        return sku + ": " + str(stock) + " (OVERSOLD)"
    else:
        return sku + ": " + str(stock)
