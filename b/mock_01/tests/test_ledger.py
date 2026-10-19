from decimal import Decimal
from ledger import normalize_order_id, calculate_total, OrderLedger
import pytest


def test_normalize_regular_id():
    assert normalize_order_id(123456) == "123456"


def test_total_without_discount():
    assert calculate_total([Decimal("2.00"), Decimal("3.00")], 0) == Decimal("5.00")


def test_add_order():
    ledger = OrderLedger()
    assert ledger.add_order(123456, Decimal("10.00")) == "123456"
    assert ledger.orders["123456"] == Decimal("10.00")

def test_add_order_rejects_duplicate_id():
    ledger = OrderLedger()

    first = ledger.add_order("123456", Decimal("10.00"))
    assert first == "123456"

    with pytest.raises(ValueError):
        ledger.add_order("123456", Decimal("20.00"))

@pytest.mark.parametrize(
    ("raw", "expected"),
    [
        (0, "000000"),           # lowest accepted number
        (1, "000001"),
        (999999, "999999"),      # highest accepted number
        ("0", "000000"),         # shortest valid string
        ("00001", "000001"),     # leading zeros are preserved in the output
        ("123456", "123456"),    # longest valid string
    ],
)
def test_normalize_order_id_returns_six_ascii_digits(raw, expected):
    result = normalize_order_id(raw)

    assert result == expected
    assert len(result) == 6
    assert result.isascii()
    assert result.isdigit()


@pytest.mark.parametrize(
    "raw",
    [
        -1,             # below numeric range
        1000000,        # above numeric range
        "",             # string too short
        "1234567",      # string too long
        "12a",          # contains a non-digit
        "+1",           # sign is not an ASCII digit
        " 1 ",          # whitespace is not an ASCII digit
        "１２",          # Unicode digits, not ASCII digits
    ],
)
def test_normalize_order_id_rejects_invalid_inputs(raw):
    with pytest.raises(ValueError):
        normalize_order_id(raw)