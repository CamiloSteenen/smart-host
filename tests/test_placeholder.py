"""Basic sanity tests for the Smart Host services."""

import sys
from pathlib import Path
import types
import unittest
from datetime import date

# Ensure src package is on sys.path
sys.path.append(str(Path(__file__).resolve().parents[1] / "src"))

from smart_host.domain import Host, Property, Room, Booking


class FakePropertyRepository:
    def __init__(self) -> None:
        self.properties: list[Property] = []
        self.next_id = 1

    def add_property(self, name: str, location: str) -> Property:
        prop = Property(id=self.next_id, name=name, location=location)
        self.next_id += 1
        self.properties.append(prop)
        return prop

    def list_properties(self) -> list[Property]:
        return list(self.properties)

    def add_room(
        self, property_id: int, beds: int = 1, *, features: str | None = None, price: float = 0.0
    ) -> Room:
        return Room(id=1, property_id=property_id, beds=beds, features=features, price=price)

    def list_rooms(self, property_id: int) -> list[Room]:
        return []


class FakeBookingRepository:
    def __init__(self) -> None:
        self.bookings: list[Booking] = []
        self.next_id = 1

    def add_booking(self, booking: Booking) -> Booking:
        booking.id = self.next_id
        self.next_id += 1
        self.bookings.append(booking)
        return booking

    def list_bookings(self) -> list[Booking]:
        return list(self.bookings)


# Provide fake infrastructure module so importing service layer succeeds without
# SQLAlchemy installed.
fake_infra = types.ModuleType("smart_host.infrastructure")
fake_infra.PropertyRepository = FakePropertyRepository
fake_infra.BookingRepository = FakeBookingRepository
fake_infra.HostRepository = lambda *a, **k: None
fake_infra.init_db = lambda: None
sys.modules["smart_host.infrastructure"] = fake_infra

from smart_host.service import HostService, PropertyService, BookingService


class HostServiceTestCase(unittest.TestCase):
    def test_host_service_to_dict(self):
        host = Host(name="Alice")
        service = HostService()
        result = service.to_dict(host)
        self.assertEqual(result, {"name": "Alice", "rating": 0.0})


class PropertyServiceTestCase(unittest.TestCase):
    def test_add_property(self):
        repo = FakePropertyRepository()
        service = PropertyService()
        prop = repo.add_property(name="Aruba House", location="Paradera")
        result = service.to_dict(prop)
        self.assertEqual(result["name"], "Aruba House")
        self.assertEqual(result["location"], "Paradera")


class BookingServiceTestCase(unittest.TestCase):
    def test_create_booking(self):
        repo = FakeBookingRepository()
        service = BookingService(repo)
        check_in = date(2024, 1, 1)
        check_out = date(2024, 1, 5)
        booking = service.create_booking(
            room_id=1,
            guest_name="Bob",
            language="nl",
            check_in=check_in,
            check_out=check_out,
        )
        result = service.to_dict(booking)
        self.assertEqual(result["id"], 1)
        self.assertEqual(result["guest_name"], "Bob")
        self.assertEqual(result["language"], "nl")

    def test_create_booking_invalid_dates(self):
        repo = FakeBookingRepository()
        service = BookingService(repo)
        with self.assertRaises(ValueError):
            service.create_booking(
                room_id=1,
                guest_name="Bob",
                language="en",
                check_in=date(2024, 1, 5),
                check_out=date(2024, 1, 1),
            )


class APIBookingValidationTestCase(unittest.TestCase):
    def test_api_returns_400_for_invalid_dates(self):
        from smart_host.interface.api import create_app
        from fastapi import HTTPException

        app = create_app()

        create_booking = next(
            route.endpoint for route in app.router.routes if route.path == "/bookings" and "POST" in route.methods
        )

        with self.assertRaises(HTTPException) as ctx:
            create_booking(
                room_id=1,
                guest_name="Bob",
                language="en",
                check_in=date(2024, 1, 5),
                check_out=date(2024, 1, 1),
            )

        self.assertEqual(ctx.exception.status_code, 400)

if __name__ == "__main__":
    unittest.main()
