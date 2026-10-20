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

def test_normalize_order_id_pads_with_leading_zeros():
    assert normalize_order_id(123) == "000123"

@pytest.mark.parametrize(
    "raw",
    [" 123", "123 ", "abc", "+123", "12-3", "１２３"],
)
def test_normalize_rejects_strings_that_are_not_ascii_digits(raw):
    with pytest.raises(ValueError):
        normalize_order_id(raw)
        
def test_calculate_total_uses_half_up_and_returns_two_place_decimal():
    result = calculate_total([Decimal("1.125")], 0)

    assert isinstance(result, Decimal)
    assert result.as_tuple().exponent == -2
    assert result == Decimal("1.13")

def test_calculate_total_rejects_negative_price():
    with pytest.raises(ValueError):
        calculate_total([Decimal("-0.01")], 0)

@pytest.mark.parametrize(
    ("discount", "expected"),
    [
        (0, Decimal("10.00")),
        (100, Decimal("0.00")),
    ],
)
def test_calculate_total_accepts_inclusive_discount_bounds(discount, expected):
    assert calculate_total([Decimal("10.00")], discount) == expected

@pytest.mark.parametrize("discount", [-1, 101])
def test_calculate_total_rejects_discount_outside_bounds(discount):
    with pytest.raises(ValueError):
        calculate_total([Decimal("10.00")], discount)

def test_calculate_total_does_not_mutate_inputs():
    prices = [Decimal("3.00"), Decimal("1.00"), Decimal("2.00")]
    original_prices = prices.copy()
    discount_percent = Decimal("10")
    original_discount = discount_percent

    calculate_total(prices, discount_percent)

    assert prices == original_prices
    assert discount_percent == original_discount

def test_add_order_after_close_raises_without_changing_orders():
    ledger = OrderLedger()
    ledger.add_order("123456", Decimal("10.00"))
    orders_before = ledger.orders.copy()

    ledger.close()

    with pytest.raises(RuntimeError):
        ledger.add_order("654321", Decimal("20.00"))

    assert ledger.orders == orders_before

def test_close_snapshot_is_independent_of_ledger_orders():
    ledger = OrderLedger()
    ledger.add_order("123456", Decimal("10.00"))

    snapshot = ledger.close()
    ledger.orders.clear()

    assert snapshot == {"123456": Decimal("10.00")}

def test_refund_after_close_raises_without_removing_order():
    ledger = OrderLedger()
    ledger.add_order("123456", Decimal("10.00"))
    ledger.close()

    with pytest.raises(RuntimeError):
        ledger.refund("123456")

    assert ledger.orders == {"123456": Decimal("10.00")}

def test_refund_removes_order_and_returns_original_amount():
    ledger = OrderLedger()
    ledger.add_order("123456", Decimal("10.00"))

    refunded_amount = ledger.refund("123456")

    assert refunded_amount == Decimal("10.00")
    assert "123456" not in ledger.orders

def test_refund_unknown_order_raises_key_error():
    ledger = OrderLedger()

    with pytest.raises(KeyError):
        ledger.refund("654321")
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