from decimal import Decimal, ROUND_HALF_UP


def normalize_order_id(raw):
    value = int(raw)
    if value < 0 or value > 999999:
        raise ValueError("order ID out of range")
    return f"{value:06d}"

def calculate_total(prices, discount_percent):
    decimal_prices = [Decimal(str(price)) for price in prices]
    if any(price < 0 for price in decimal_prices):
        raise ValueError("prices must be nonnegative")

    subtotal = sum(decimal_prices, Decimal("0"))
    discount = Decimal(str(discount_percent))

    if not discount.is_finite() or not Decimal("0") <= discount <= Decimal("100"):
        raise ValueError("discount must be between 0 and 100")

    total = subtotal * (Decimal("100") - discount) / Decimal("100")
    return total.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

class OrderLedger:
    def __init__(self):
        self.orders = {}
        self.closed = False

    def add_order(self, order_id, total):
        if self.closed:
            raise RuntimeError("cannot add orders to closed ledger")

        order_id = normalize_order_id(order_id)
        self.orders[order_id] = total
        return order_id

    def refund(self, order_id):
        if self.closed:
            raise RuntimeError("cannot refund from closed ledger")

        order_id = normalize_order_id(order_id)
        return self.orders.pop(order_id)

    def close(self):
        self.closed = True
        return self.orders.copy()
