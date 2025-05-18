import sys
from pathlib import Path
import unittest

sys.path.append(str(Path(__file__).resolve().parents[1] / "src"))

try:
    from fastapi.testclient import TestClient
except Exception:  # httpx or fastapi might be missing
    TestClient = None  # type: ignore

import types

fake_infra = types.ModuleType("smart_host.infrastructure")
fake_infra.HostRepository = lambda *a, **k: None
fake_infra.PropertyRepository = lambda *a, **k: None
fake_infra.BookingRepository = lambda *a, **k: None
fake_infra.init_db = lambda: None
sys.modules["smart_host.infrastructure"] = fake_infra

from smart_host.interface.api import create_app


class ChatRouteTestCase(unittest.TestCase):
    def setUp(self):
        if TestClient is None:
            self.skipTest("TestClient unavailable")
        self.client = TestClient(create_app())

    def test_chat_route(self):
        resp = self.client.get("/chat")
        self.assertEqual(resp.status_code, 200)


if __name__ == "__main__":
    unittest.main()
