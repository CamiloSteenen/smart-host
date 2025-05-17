"""Basic sanity test using unittest."""

import sys
from pathlib import Path
import unittest

# Ensure src package is on sys.path
sys.path.append(str(Path(__file__).resolve().parents[1] / "src"))

from smart_host.domain import Host
from smart_host.service import HostService, PropertyService
from smart_host.infrastructure import PropertyRepository


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


if __name__ == "__main__":
    unittest.main()
