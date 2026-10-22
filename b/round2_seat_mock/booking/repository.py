import sqlite3
from .models import Booking


class BookingRepository:
    """Persistence: store and retrieve event, seat, and booking records."""

    def __init__(self, db_path):
        self.db_path = str(db_path)
        with self._connect() as conn:
            conn.executescript("""
                CREATE TABLE IF NOT EXISTS seats (
                    event_id TEXT NOT NULL,
                    seat_label TEXT NOT NULL,
                    PRIMARY KEY (event_id, seat_label)
                );
                CREATE TABLE IF NOT EXISTS bookings (
                    booking_id TEXT PRIMARY KEY,
                    event_id TEXT NOT NULL,
                    seat_label TEXT NOT NULL,
                    customer_id TEXT NOT NULL
                );
            """)

    def _connect(self):
        return sqlite3.connect(self.db_path, timeout=5)

    def add_seat(self, event_id, seat_label):
        with self._connect() as conn:
            conn.execute(
                "INSERT OR IGNORE INTO seats (event_id, seat_label) VALUES (?, ?)",
                (event_id, seat_label),
            )

    def seat_exists(self, event_id, seat_label):
        with self._connect() as conn:
            return conn.execute(
                "SELECT 1 FROM seats WHERE event_id = ? AND seat_label = ?",
                (event_id, seat_label),
            ).fetchone() is not None

    def find_by_seat(self, event_id, seat_label):
        with self._connect() as conn:
            row = conn.execute(
                "SELECT booking_id, event_id, seat_label, customer_id "
                "FROM bookings WHERE event_id = ? AND seat_label = ?",
                (event_id, seat_label),
            ).fetchone()
        return Booking(*row) if row else None

    def insert_booking(self, booking):
        with self._connect() as conn:
            conn.execute(
                "INSERT INTO bookings (booking_id, event_id, seat_label, customer_id) "
                "VALUES (?, ?, ?, ?)",
                (booking.booking_id, booking.event_id, booking.seat_label, booking.customer_id),
            )

    def get_booking(self, booking_id):
        with self._connect() as conn:
            row = conn.execute(
                "SELECT booking_id, event_id, seat_label, customer_id "
                "FROM bookings WHERE booking_id = ?", (booking_id,)
            ).fetchone()
        return Booking(*row) if row else None

    def count_for_seat(self, event_id, seat_label):
        with self._connect() as conn:
            return conn.execute(
                "SELECT COUNT(*) FROM bookings WHERE event_id = ? AND seat_label = ?",
                (event_id, seat_label),
            ).fetchone()[0]
