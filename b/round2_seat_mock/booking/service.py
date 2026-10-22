from uuid import uuid4
from .models import Booking, SeatUnavailable


class BookingService:
    """Business logic for accepting seat reservations."""

    def __init__(self, repository):
        self.repository = repository
        self.recent_booking_ids = set()  # Local convenience cache, not authoritative.

    def reserve_seat(self, event_id, seat_label, customer_id):
        if not customer_id:
            raise ValueError("customer_id must not be empty")
        if not self.repository.seat_exists(event_id, seat_label):
            raise ValueError("unknown event or seat")

        existing = self.repository.find_by_seat(event_id, seat_label)
        if existing is not None:
            raise SeatUnavailable(f"seat {seat_label} already reserved")

        booking = Booking(str(uuid4()), event_id, seat_label, customer_id)
        self.repository.insert_booking(booking)
        self.recent_booking_ids.add(booking.booking_id)
        return booking.booking_id

    def get_booking(self, booking_id):
        return self.repository.get_booking(booking_id)
