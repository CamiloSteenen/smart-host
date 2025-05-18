"""Infrastructure repository implementations backed by SQLAlchemy."""

from __future__ import annotations


from ..domain import Host, Property, Room, Booking
from .sql import SessionLocal, init_db
from .sql.models import (
    HostTable,
    PropertyTable,
    RoomTable,
    BookingTable,
)


class HostRepository:
    """Host persistence using the database."""

    def __init__(self, session_factory: type[SessionLocal] = SessionLocal) -> None:
        init_db()
        self._session_factory = session_factory

    def add(self, host: Host) -> None:
        """Persist a host."""
        with self._session_factory() as session:
            db_host = HostTable(name=host.name, rating=host.rating)
            session.add(db_host)
            session.commit()

    def list_hosts(self) -> list[Host]:
        with self._session_factory() as session:
            hosts = session.query(HostTable).all()
            return [Host(name=h.name, rating=h.rating) for h in hosts]


class PropertyRepository:
    """Property and room storage using SQLAlchemy."""

    def __init__(self, session_factory: type[SessionLocal] = SessionLocal) -> None:
        init_db()
        self._session_factory = session_factory

    def add_property(self, name: str, location: str) -> Property:
        with self._session_factory() as session:
            prop = PropertyTable(name=name, location=location)
            session.add(prop)
            session.commit()
            session.refresh(prop)
            return Property(id=prop.id, name=prop.name, location=prop.location)

    def list_properties(self) -> list[Property]:
        with self._session_factory() as session:
            props = session.query(PropertyTable).all()
            return [Property(id=p.id, name=p.name, location=p.location) for p in props]

    def add_room(
        self,
        property_id: int,
        beds: int = 1,
        *,
        features: str | None = None,
        price: float = 0.0,
    ) -> Room:
        with self._session_factory() as session:
            room = RoomTable(
                property_id=property_id,
                beds=beds,
                features=features,
                price=price,
            )
            session.add(room)
            session.commit()
            session.refresh(room)
            return Room(
                id=room.id,
                property_id=room.property_id,
                beds=room.beds,
                features=room.features,
                price=room.price,
            )

    def list_rooms(self, property_id: int | None = None) -> list[Room]:
        with self._session_factory() as session:
            query = session.query(RoomTable)
            if property_id is not None:
                query = query.filter_by(property_id=property_id)
            rooms = query.all()
            return [
                Room(
                    id=r.id,
                    property_id=r.property_id,
                    beds=r.beds,
                    features=r.features,
                    price=r.price,
                )
                for r in rooms
            ]


class BookingRepository:
    """Booking persistence using SQLAlchemy."""

    def __init__(self, session_factory: type[SessionLocal] = SessionLocal) -> None:
        init_db()
        self._session_factory = session_factory

    def add_booking(self, booking: Booking) -> Booking:
        with self._session_factory() as session:
            db_booking = BookingTable(
                room_id=booking.room_id,
                guest_name=booking.guest_name,
                language=booking.language,
                check_in=booking.check_in,
                check_out=booking.check_out,
            )
            session.add(db_booking)
            session.commit()
            session.refresh(db_booking)
            booking.id = db_booking.id
            return booking

    def list_bookings(self) -> list[Booking]:
        with self._session_factory() as session:
            bookings = session.query(BookingTable).all()
            return [
                Booking(
                    id=b.id,
                    room_id=b.room_id,
                    guest_name=b.guest_name,
                    language=b.language,
                    check_in=b.check_in,
                    check_out=b.check_out,
                )
                for b in bookings
            ]
