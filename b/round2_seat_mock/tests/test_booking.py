import pytest
from booking import BookingRepository, BookingService, SeatUnavailable


@pytest.fixture
def system(tmp_path):
    repo = BookingRepository(tmp_path / "concert.sqlite")
    repo.add_seat("concert-1", "A1")
    repo.add_seat("concert-1", "A2")
    return repo, BookingService(repo)


def test_reservation_can_be_retrieved(system):
    repo, service = system
    booking_id = service.reserve_seat("concert-1", "A1", "alice")
    booking = service.get_booking(booking_id)
    assert booking.customer_id == "alice"
    assert booking.seat_label == "A1"
    assert repo.count_for_seat("concert-1", "A1") == 1


def test_sequential_duplicate_rejected(system):
    repo, service = system
    service.reserve_seat("concert-1", "A1", "alice")
    with pytest.raises(SeatUnavailable):
        service.reserve_seat("concert-1", "A1", "bob")
    assert repo.count_for_seat("concert-1", "A1") == 1


def test_different_seats_independent(system):
    repo, service = system
    assert service.reserve_seat("concert-1", "A1", "alice")
    assert service.reserve_seat("concert-1", "A2", "bob")
    assert repo.count_for_seat("concert-1", "A1") == 1
    assert repo.count_for_seat("concert-1", "A2") == 1


def test_unknown_seat_rejected(system):
    repo, service = system
    with pytest.raises(ValueError):
        service.reserve_seat("concert-1", "Z99", "alice")
    assert repo.count_for_seat("concert-1", "Z99") == 0


def test_empty_customer_rejected(system):
    repo, service = system
    with pytest.raises(ValueError):
        service.reserve_seat("concert-1", "A1", "")
    assert repo.count_for_seat("concert-1", "A1") == 0


def test_unknown_booking_returns_none(system):
    _, service = system
    assert service.get_booking("missing") is None
