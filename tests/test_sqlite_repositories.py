"""Unit tests for SQLite-backed repositories."""

import sys
from pathlib import Path
from datetime import date
import unittest

# Ensure src package is on sys.path
sys.path.append(str(Path(__file__).resolve().parents[1] / "src"))

from smart_host.domain import Host, Booking
from smart_host.infrastructure import (
    SqliteHostRepository,
    SqlitePropertyRepository,
    SqliteBookingRepository,
)


class SqliteHostRepositoryTestCase(unittest.TestCase):
    def setUp(self):
        self.repo = SqliteHostRepository()

    def test_add_and_list_hosts(self):
        host = Host(name="Alice")
        self.repo.add(host)
        hosts = self.repo.list_hosts()
        self.assertEqual(len(hosts), 1)
        self.assertEqual(hosts[0].name, "Alice")


class SqlitePropertyRepositoryTestCase(unittest.TestCase):
    def setUp(self):
        self.repo = SqlitePropertyRepository()

    def test_property_crud(self):
        prop = self.repo.add_property(name="Beach House", location="Aruba")
        props = self.repo.list_properties()
        self.assertEqual(props[0].name, "Beach House")
        room = self.repo.add_room(prop.id, beds=2, features="AC", price=99.0)
        rooms = self.repo.list_rooms(prop.id)
        self.assertEqual(len(rooms), 1)
        self.assertEqual(rooms[0].id, room.id)
        self.assertEqual(rooms[0].beds, 2)


class SqliteBookingRepositoryTestCase(unittest.TestCase):
    def setUp(self):
        self.repo = SqliteBookingRepository()

    def test_add_and_list_bookings(self):
        self.repo.add_booking(
            booking=Booking(
                id=0,
                room_id=1,
                guest_name="Bob",
                language="en",
                check_in=date(2024, 1, 1),
                check_out=date(2024, 1, 5),
            )
        )
        bookings = self.repo.list_bookings()
        self.assertEqual(len(bookings), 1)
        self.assertEqual(bookings[0].guest_name, "Bob")


if __name__ == "__main__":
    unittest.main()
