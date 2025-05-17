"""Script to generate sample data for Smart Host."""

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1] / "src"))

from smart_host.infrastructure import PropertyRepository


def main() -> None:
    repo = PropertyRepository()
    aruba = repo.add_property(name="Aruba House", location="Paradera")
    repo.add_room(property_id=aruba.id, beds=2, features="Sea view", price=100.0)
    repo.add_room(property_id=aruba.id, beds=1, features="Garden access", price=80.0)
    for prop in repo.list_properties():
        print(prop)
    for room in repo.list_rooms(aruba.id):
        print(room)


if __name__ == "__main__":
    main()
