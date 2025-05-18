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
from smart_host.interface import create_app
from fastapi import HTTPException


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


class ApiErrorHandlingTestCase(unittest.TestCase):
    def setUp(self):
        app = create_app()
        self.add_room_endpoint = [
            r.endpoint
            for r in app.routes
            if r.path == "/properties/{property_id}/rooms" and "POST" in r.methods
        ][0]
        self.add_property_endpoint = [
            r.endpoint
            for r in app.routes
            if r.path == "/properties" and "POST" in r.methods
        ][0]
        self.create_booking_endpoint = [
            r.endpoint
            for r in app.routes
            if r.path == "/bookings" and "POST" in r.methods
        ][0]

    def test_add_room_invalid_property(self):
        with self.assertRaises(HTTPException) as ctx:
            self.add_room_endpoint(property_id=999)
        self.assertEqual(ctx.exception.status_code, 400)
        self.assertIn("does not exist", ctx.exception.detail)

    def test_create_booking_invalid_dates(self):
        # create property and room first
        prop = self.add_property_endpoint(name="Prop", location="Here")
        prop_id = prop["id"]
        room = self.add_room_endpoint(property_id=prop_id)
        room_id = room["id"]

        with self.assertRaises(HTTPException) as ctx:
            self.create_booking_endpoint(
                room_id=room_id,
                guest_name="Bob",
                language="en",
                check_in=date(2024, 1, 5),
                check_out=date(2024, 1, 1),
            )
        self.assertEqual(ctx.exception.status_code, 400)
        self.assertIn("check_out", ctx.exception.detail)


if __name__ == "__main__":
    unittest.main()
