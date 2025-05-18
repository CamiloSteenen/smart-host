"""Integration tests for FastAPI endpoints."""

import sys
from pathlib import Path
from datetime import date
import unittest

# Ensure src package is on sys.path
sys.path.append(str(Path(__file__).resolve().parents[1] / "src"))

try:
    from fastapi.testclient import TestClient
except Exception:  # pragma: no cover - dependency missing
    TestClient = None
from smart_host.interface.api import create_app


class ApiIntegrationTestCase(unittest.TestCase):
    def setUp(self):
        if TestClient is None:
            self.skipTest("fastapi.testclient not available")
        self.client = TestClient(create_app())

    def test_hosts_endpoints(self):
        # Initially empty
        response = self.client.get("/hosts")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), [])

        # Add a host
        response = self.client.post("/hosts", params={"name": "Alice"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["name"], "Alice")

        # List hosts
        response = self.client.get("/hosts")
        self.assertEqual(len(response.json()), 1)

    def test_property_and_room_endpoints(self):
        # Add property
        resp = self.client.post("/properties", params={"name": "Beach", "location": "Aruba"})
        self.assertEqual(resp.status_code, 200)
        prop_id = resp.json()["id"]

        # List properties
        resp = self.client.get("/properties")
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(resp.json()), 1)

        # Add room
        resp = self.client.post(f"/properties/{prop_id}/rooms", params={"beds": 2})
        self.assertEqual(resp.status_code, 200)
        room_id = resp.json()["id"]

        # List rooms
        resp = self.client.get(f"/properties/{prop_id}/rooms")
        self.assertEqual(len(resp.json()), 1)
        self.assertEqual(resp.json()[0]["id"], room_id)

    def test_booking_endpoints(self):
        # Add property and room for booking
        prop = self.client.post("/properties", params={"name": "House", "location": "Aruba"}).json()
        room = self.client.post(f"/properties/{prop['id']}/rooms").json()

        # Create booking
        payload = {
            "room_id": room["id"],
            "guest_name": "Bob",
            "language": "en",
            "check_in": date(2024, 1, 1).isoformat(),
            "check_out": date(2024, 1, 5).isoformat(),
        }
        resp = self.client.post("/bookings", params=payload)
        self.assertEqual(resp.status_code, 200)
        booking_id = resp.json()["id"]

        # List bookings
        resp = self.client.get("/bookings")
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(resp.json()), 1)
        self.assertEqual(resp.json()[0]["id"], booking_id)


if __name__ == "__main__":
    unittest.main()
