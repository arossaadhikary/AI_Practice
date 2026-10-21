from decimal import Decimal, ROUND_HALF_UP


class PrizeDraw:
    def __init__(self):
        self._entries = []
        self._closed = None

    def add_entry(self, player_id, code, amount_cents):
        if self._closed is not None:
            raise RuntimeError("draw closed")
        if not isinstance(player_id, str) or not player_id.strip():
            raise ValueError("invalid player")
        if not isinstance(code, str) or not 1 <= len(code) <= 6 or not code.isascii() or not code.isdigit():
            raise ValueError("invalid code")
        if isinstance(amount_cents, bool) or not isinstance(amount_cents, int) or amount_cents <= 0:
            raise ValueError("invalid amount")
        
        self._entries.append({"player_id": player_id, "code": str(code), "amount_cents": amount_cents})

    def close_draw(self, winning_code):
        if self._closed is not None:
            raise RuntimeError("already closed")
        if not isinstance(winning_code, str) or not winning_code or not winning_code.isdigit():
            raise ValueError("invalid winning code")
        self._closed = {
            "winning_code": winning_code,
            "pool_cents": sum(entry["amount_cents"] for entry in self._entries),
            "entries": self._entries,
        }
        return dict(self._closed)

    def payouts(self):
        if self._closed is None:
            raise RuntimeError("not closed")
        winners = [entry for entry in self._closed["entries"] if entry["code"] in self._closed["winning_code"]]
        if not winners:
            return []
        share = int((Decimal(self._closed["pool_cents"]) / Decimal(len(winners))).quantize(Decimal("1"), rounding=ROUND_HALF_UP))
        return [{"player_id": entry["player_id"], "amount_cents": share} for entry in winners]
