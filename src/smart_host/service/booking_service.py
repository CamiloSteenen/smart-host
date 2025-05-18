"""Service layer for booking operations."""

from dataclasses import asdict
from datetime import date

from ..domain import Booking
from ..infrastructure import BookingRepository


class BookingService:
    """Business logic around bookings."""

    def __init__(self, repository: BookingRepository) -> None:
        self._repository = repository

    def create_booking(
        self,
        room_id: int,
        guest_name: str,
        language: str,
        check_in: date,
        check_out: date,
    ) -> Booking:
        """Create and persist a booking."""
        if check_out <= check_in:
            raise ValueError("check_out must be after check_in")
        booking = Booking(
            id=0,
            room_id=room_id,
            guest_name=guest_name,
            language=language,
            check_in=check_in,
            check_out=check_out,
        )
        return self._repository.add_booking(booking)

    def list_bookings(self) -> list[Booking]:
        """Return all stored bookings."""
        return self._repository.list_bookings()

    def to_dict(self, booking: Booking) -> dict:
        """Return booking as serializable dict."""
        return asdict(booking)
