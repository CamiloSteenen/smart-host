"""Basic sanity test using unittest."""

import sys
from pathlib import Path
import unittest

# Ensure src package is on sys.path
sys.path.append(str(Path(__file__).resolve().parents[1] / "src"))

from smart_host.domain import Host
from smart_host.service import HostService


class HostServiceTestCase(unittest.TestCase):
    def test_host_service_to_dict(self):
        host = Host(name="Alice")
        service = HostService()
        result = service.to_dict(host)
        self.assertEqual(result, {"name": "Alice", "rating": 0.0})


if __name__ == "__main__":
    unittest.main()
