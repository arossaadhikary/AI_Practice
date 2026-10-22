from dataclasses import dataclass


@dataclass(frozen=True)
class Booking:
    booking_id: str
    event_id: str
    seat_label: str
    customer_id: str


class SeatUnavailable(Exception):
    """Raised when a valid seat is already reserved."""
