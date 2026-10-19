# Mock 01 — Order Ledger

## Scenario
You inherited a small Python order-processing module. Use an AI coding assistant to investigate, test, and repair it. Treat this as an interview: narrate your reasoning and verify all claims against code.

## Contract
1. `normalize_order_id(raw)` returns a **six-character string** of digits. Numeric inputs from 0 through 999999 are accepted and left-padded with zeros. String inputs must contain only 1–6 ASCII digits. Invalid inputs raise `ValueError`.
2. `calculate_total(prices, discount_percent)` returns a `Decimal` rounded to two decimal places with ROUND_HALF_UP. Prices are nonnegative Decimal-compatible values. Discounts range from 0 to 100 inclusive. Do not mutate inputs.
3. `OrderLedger.add_order(order_id, total)` records an order only when the ledger is open. Duplicate order IDs are rejected. Totals must be nonnegative. Return the normalized ID.
4. `OrderLedger.close()` returns an independent snapshot of orders. After closing, attempts to add orders raise `RuntimeError`. Subsequent mutations of caller-owned objects must not change the snapshot.
5. `OrderLedger.refund(order_id)` is allowed only while open. A refund removes an existing order and returns its original amount. Unknown IDs raise `KeyError`.
6. Preserve public function names and signatures. Avoid unrelated refactoring.

## Your task
- First map requirements to functions and create a short test plan.
- Ask the agent to find potential violations with concrete counterexamples; verify the claims yourself.
- Add deterministic regression tests, observe failures, and fix one issue at a time.
- Review diffs against the contract, then run the entire test suite.
- If possible, open a second read-only agent chat for independent review.

## Commands
`python -m pip install -r requirements.txt`
`python -m pytest -q`

## Interviewer questions
- Which requirement is your current change satisfying?
- Which test fails before the change and passes afterward?
- What other behavior could your fix accidentally change?
- What evidence supports your claim that the ticket is complete?
