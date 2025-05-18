"""Infrastructure repository implementations."""

from ..domain import Host, Property, Room, Booking


class HostRepository:
    """Placeholder in-memory host store."""

    def __init__(self) -> None:
        self._hosts: list[Host] = []

    def add(self, host: Host) -> None:
        self._hosts.append(host)

    def list_hosts(self) -> list[Host]:
        return list(self._hosts)


class PropertyRepository:
    """In-memory storage for properties and rooms."""

    def __init__(self) -> None:
        self._properties: dict[int, Property] = {}
        self._rooms: dict[int, Room] = {}
        self._next_property_id = 1
        self._next_room_id = 1

    def add_property(self, name: str, location: str) -> Property:
        prop = Property(id=self._next_property_id, name=name, location=location)
        self._properties[prop.id] = prop
        self._next_property_id += 1
        return prop

    def list_properties(self) -> list[Property]:
        return list(self._properties.values())

    def add_room(
        self,
        property_id: int,
        beds: int = 1,
        *,
        features: str | None = None,
        price: float = 0.0,
    ) -> Room:
        if property_id not in self._properties:
            raise ValueError(f"Property {property_id} does not exist")
        room = Room(
            id=self._next_room_id,
            property_id=property_id,
            beds=beds,
            features=features,
            price=price,
        )
        self._rooms[room.id] = room
        self._next_room_id += 1
        return room

    def list_rooms(self, property_id: int | None = None) -> list[Room]:
        rooms = list(self._rooms.values())
        if property_id is not None:
            rooms = [r for r in rooms if r.property_id == property_id]
        return rooms


class BookingRepository:
    """Simple booking storage."""

    def __init__(self) -> None:
        self._bookings: dict[int, Booking] = {}
        self._next_booking_id = 1

    def add_booking(self, booking: Booking) -> Booking:
        booking.id = self._next_booking_id
        self._bookings[booking.id] = booking
        self._next_booking_id += 1
        return booking

    def list_bookings(self) -> list[Booking]:
        return list(self._bookings.values())
