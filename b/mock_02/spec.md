# Potluck Mock 01: Prize Draw

Build and maintain a prize draw. Do not change public function signatures.

- `PrizeDraw.add_entry(player_id, code, amount_cents)` accepts nonempty string player IDs, **1–6 ASCII digit string** entry codes, and **positive integer** cent amounts; booleans are not valid amounts. Codes are identifiers, not numbers: preserve every character including leading zeros. Reject whitespace, signs, and non-ASCII digits. Entries preserve insertion order.
- `close_draw(winning_code)` closes the draw once; returns a summary dictionary with `winning_code`, `pool_cents`, and `entries`. Its `entries` list contains dictionaries with `player_id`, `code`, `amount_cents`.
- `payouts()` raises `RuntimeError` before close. After close, winners are entries with codes that **exactly match** the winning code. Each winning entry receives the entire pool divided by the number of winning entries, rounded to whole cents with `ROUND_HALF_UP`.
- No winners means an empty payout list. Preserve entry order in payouts.
- The closed draw is immutable from the caller's perspective: mutating a returned summary or payouts must never alter later results.
- `add_entry` and `close_draw` after closure raise `RuntimeError`.
- Invalid arguments raise `ValueError`. Do not silently normalize codes or change their lengths.

Focus: explore specification, ask AI to map state, write regression tests, and make bounded fixes. There may be more than one independent defect. Do not refactor unrelated behavior.
