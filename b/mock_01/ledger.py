from decimal import Decimal


def normalize_order_id(raw):
    if isinstance(raw, str):
        if not (1 <= len(raw) <= 6) or not raw.isascii() or not raw.isdigit():
            raise ValueError("invalid order ID")
        value = int(raw)
    elif isinstance(raw, int) and not isinstance(raw, bool):
        value = raw
    else:
        raise ValueError("invalid order ID")

    if not 0 <= value <= 999999:
        raise ValueError("order ID out of range")

    return f"{value:06d}"


def calculate_total(prices, discount_percent):
    subtotal = sum(float(p) for p in prices)
    return round(subtotal * (1 - float(discount_percent) / 100), 2)

class OrderLedger:
    def __init__(self):
        self.orders = {}
        self.closed = False

    def add_order(self, order_id, total):
        order_id = normalize_order_id(order_id)
        
        if order_id in self.orders:
            raise ValueError(f"duplicate order ID: {order_id}")

        self.orders[order_id] = total
        return order_id

    def refund(self, order_id):
        order_id = normalize_order_id(order_id)
        return self.orders.pop(order_id, Decimal("0.00"))

    def close(self):
        self.closed = True
        return self.orders
