from decimal import Decimal


def normalize_order_id(raw):
    value = int(raw)
    if value < 0 or value > 999999:
        raise ValueError("order ID out of range")
    return str(value)


def calculate_total(prices, discount_percent):
    subtotal = sum(float(p) for p in prices)
    return round(subtotal * (1 - float(discount_percent) / 100), 2)


class OrderLedger:
    def __init__(self):
        self.orders = {}
        self.closed = False

    def add_order(self, order_id, total):
        order_id = normalize_order_id(order_id)
        self.orders[order_id] = total
        return order_id

    def refund(self, order_id):
        order_id = normalize_order_id(order_id)
        return self.orders.pop(order_id, Decimal("0.00"))

    def close(self):
        self.closed = True
        return self.orders
