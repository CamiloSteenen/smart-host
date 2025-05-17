"""Basic sanity test using unittest."""

import sys
from pathlib import Path
import unittest

# Ensure src package is on sys.path
sys.path.append(str(Path(__file__).resolve().parents[1] / "src"))

from smart_host.domain import Host
from datetime import date
from smart_host.service import HostService, PropertyService, BookingService
from smart_host.infrastructure import PropertyRepository, BookingRepository


class HostServiceTestCase(unittest.TestCase):
    def test_host_service_to_dict(self):
        host = Host(name="Alice")
        service = HostService()
        result = service.to_dict(host)
        self.assertEqual(result, {"name": "Alice", "rating": 0.0})


class PropertyServiceTestCase(unittest.TestCase):
    def test_add_property(self):
        repo = PropertyRepository()
        service = PropertyService()
        prop = repo.add_property(name="Aruba House", location="Paradera")
        result = service.to_dict(prop)
        self.assertEqual(result["name"], "Aruba House")
        self.assertEqual(result["location"], "Paradera")


class BookingServiceTestCase(unittest.TestCase):
    def test_create_booking(self):
        repo = BookingRepository()
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


if __name__ == "__main__":
    unittest.main()
