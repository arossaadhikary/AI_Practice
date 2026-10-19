from decimal import Decimal
from ledger import normalize_order_id, calculate_total, OrderLedger


def test_normalize_regular_id():
    assert normalize_order_id(123456) == "123456"


def test_total_without_discount():
    assert calculate_total([Decimal("2.00"), Decimal("3.00")], 0) == Decimal("5.00")


def test_add_order():
    ledger = OrderLedger()
    assert ledger.add_order(123456, Decimal("10.00")) == "123456"
    assert ledger.orders["123456"] == Decimal("10.00")
