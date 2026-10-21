import pytest
from potluck import PrizeDraw


def test_simple_payout():
    d = PrizeDraw()
    d.add_entry("ada", "1234", 100)
    d.add_entry("ben", "5678", 200)
    assert d.close_draw("1234")["pool_cents"] == 300
    assert d.payouts() == [{"player_id": "ada", "amount_cents": 300}]


def test_no_winners():
    d = PrizeDraw()
    d.add_entry("ada", "12", 100)
    d.close_draw("34")
    assert d.payouts() == []


def test_requires_close():
    with pytest.raises(RuntimeError):
        PrizeDraw().payouts()


def test_half_up():
    d = PrizeDraw()
    for i, cents in enumerate((1, 2, 2, 2)):
        d.add_entry(str(i), "1234", cents)
    d.close_draw("1234")
    assert [x["amount_cents"] for x in d.payouts()] == [2, 2, 2, 2]


def test_closed_rejects_changes():
    d = PrizeDraw()
    d.close_draw("99")
    with pytest.raises(RuntimeError):
        d.add_entry("ada", "99", 1)
    with pytest.raises(RuntimeError):
        d.close_draw("99")

# Candidate: add tests for overlooked requirements. Existing tests are not complete.

def test_add_entry_rejects_non_ascii_digits():
    draw = PrizeDraw()

    with pytest.raises(ValueError):
        draw.add_entry("ada", "\u0661", 100)

def test_add_entry_preserves_leading_zeros():
    draw = PrizeDraw()
    draw.add_entry("ada", "007", 100)

    summary = draw.close_draw("007")

    assert summary["entries"][0]["code"] == "007"

def test_add_entry_rejects_code_longer_than_six_digits():
    draw = PrizeDraw()

    with pytest.raises(ValueError):
        draw.add_entry("ada", "1234567", 100)