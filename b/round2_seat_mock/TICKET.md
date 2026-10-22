# BOOK-218: Two customers reserved the same seat

**Reported behavior:** Two checkout requests for seat `A1` on the same event arrived almost simultaneously. Both customers received a booking confirmation, and the database contained two bookings for the same seat.

**Expected behavior:** Exactly one reservation succeeds. The other gets `SeatUnavailable`. Exactly one booking row is stored for the seat, even if separate `BookingService` instances share the database.

**Acceptance checks:**
- Normal single reservation still succeeds and can be retrieved.
- A sequential second reservation is rejected.
- Two overlapping reservations from separate service instances produce one success, one `SeatUnavailable`, and exactly one stored row.
- Different seats may be booked independently.

**Out of scope:** Payments, cancellation, retry/idempotency keys, new endpoints, broad refactoring.
