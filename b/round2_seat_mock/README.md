# Round 2 Practice: SeatReserve

**Scenario:** You joined a team maintaining a concert-seat reservation service. An incident report says the same seat was sold twice when two checkout requests overlapped.

This is a simulated Bloomberg-style codebase exercise, not an actual Bloomberg question.

## Candidate workflow
1. Read `SPEC.md` and `TICKET.md`. Restate the acceptance criteria and what is out of scope.
2. Trace `BookingService.reserve_seat` through the repository and SQLite persistence.
3. Name the invariant and the layer that must enforce it.
4. Run existing tests: `python -m pytest -q` (install pytest if needed).
5. Design a focused regression test that reproduces the overlapping-request failure. Avoid tests that rely on arbitrary sleeps.
6. Ask an AI assistant for a minimal plan; critique its assumptions and its ability to handle multiple service instances.
7. Make a narrow patch, rerun tests, inspect the diff, and explain remaining risks.

**Do not read the coach key until you've attempted the exercise.**

## Starter prompts
- "Summarize SPEC.md and TICKET.md into acceptance criteria, invariants, and explicit exclusions. Do not modify code."
- "Trace reserve_seat from service through repository to SQLite, naming files, methods, and the exact read/write boundary. Do not propose a fix yet."
- "Propose a deterministic test for two overlapping reservations of one seat. Explain why sequential tests cannot prove concurrency safety. Do not modify files."
- "Review a proposed process-local lock: does it preserve the invariant across independent service instances? What should the database enforce?"

## Interview pacing (about 70 minutes)
10m requirements + constructor structures; 15m trace; 15m failing test; 15m patch; 15m validation + explanation.
