# SeatReserve Product Contract

The system sells numbered seats for a single concert event.

## Data and storage
- Each event has a unique event ID and a set of valid seat labels, e.g. `A1`, `A2`.
- SQLite is the shared source of truth. Multiple `BookingService` objects may use the same database file.
- A successful booking has a unique booking ID, event ID, seat label, and customer ID.
- Seat labels are identifiers, not quantities. Preserve their exact string value.

## `BookingService.reserve_seat(event_id, seat_label, customer_id)`
- Returns a booking ID on success.
- Raises `ValueError` if the event or seat does not exist, or customer ID is empty.
- Raises `SeatUnavailable` if the seat has already been reserved.
- For a given `(event_id, seat_label)`, **at most one successful booking may exist**, even if two calls overlap and originate from different service instances.
- A failed attempt must not create a booking row.
- A successful reservation remains retrievable using `get_booking(booking_id)`.

## `BookingService.get_booking(booking_id)`
- Returns a booking record, or `None` for an unknown ID.

## Scope
- Focus only on preventing duplicate successful bookings of one seat.
- Do not add payment processing, cancellations, waitlists, authentication, web APIs, or background workers.
- Preserve public function signatures and existing error behavior.
