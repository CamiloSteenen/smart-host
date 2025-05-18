import sqlite3
from datetime import date

from ..domain import Host, Property, Room, Booking


class SqliteHostRepository:
    """SQLite-backed repository for hosts."""

    def __init__(self, db_path: str = ":memory:") -> None:
        self._conn = sqlite3.connect(db_path)
        self._conn.execute(
            "CREATE TABLE IF NOT EXISTS hosts (name TEXT, rating REAL)"
        )
        self._conn.commit()

    def add(self, host: Host) -> None:
        self._conn.execute(
            "INSERT INTO hosts (name, rating) VALUES (?, ?)",
            (host.name, host.rating),
        )
        self._conn.commit()

    def list_hosts(self) -> list[Host]:
        cur = self._conn.execute("SELECT name, rating FROM hosts")
        return [Host(name=row[0], rating=row[1]) for row in cur.fetchall()]


class SqlitePropertyRepository:
    """SQLite-backed repository for properties and rooms."""

    def __init__(self, db_path: str = ":memory:") -> None:
        self._conn = sqlite3.connect(db_path)
        self._conn.execute(
            """
            CREATE TABLE IF NOT EXISTS properties (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                location TEXT
            )
            """
        )
        self._conn.execute(
            """
            CREATE TABLE IF NOT EXISTS rooms (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                property_id INTEGER,
                beds INTEGER,
                features TEXT,
                price REAL
            )
            """
        )
        self._conn.commit()

    def add_property(self, name: str, location: str) -> Property:
        cur = self._conn.execute(
            "INSERT INTO properties (name, location) VALUES (?, ?)",
            (name, location),
        )
        self._conn.commit()
        return Property(id=cur.lastrowid, name=name, location=location)

    def list_properties(self) -> list[Property]:
        cur = self._conn.execute("SELECT id, name, location FROM properties")
        return [
            Property(id=row[0], name=row[1], location=row[2])
            for row in cur.fetchall()
        ]

    def add_room(
        self,
        property_id: int,
        beds: int = 1,
        *,
        features: str | None = None,
        price: float = 0.0,
    ) -> Room:
        cur = self._conn.execute(
            "INSERT INTO rooms (property_id, beds, features, price) VALUES (?, ?, ?, ?)",
            (property_id, beds, features, price),
        )
        self._conn.commit()
        return Room(
            id=cur.lastrowid,
            property_id=property_id,
            beds=beds,
            features=features,
            price=price,
        )

    def list_rooms(self, property_id: int | None = None) -> list[Room]:
        query = "SELECT id, property_id, beds, features, price FROM rooms"
        params: tuple = ()
        if property_id is not None:
            query += " WHERE property_id = ?"
            params = (property_id,)
        cur = self._conn.execute(query, params)
        return [
            Room(
                id=row[0],
                property_id=row[1],
                beds=row[2],
                features=row[3],
                price=row[4],
            )
            for row in cur.fetchall()
        ]


class SqliteBookingRepository:
    """SQLite-backed repository for bookings."""

    def __init__(self, db_path: str = ":memory:") -> None:
        self._conn = sqlite3.connect(db_path)
        self._conn.execute(
            """
            CREATE TABLE IF NOT EXISTS bookings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                room_id INTEGER,
                guest_name TEXT,
                language TEXT,
                check_in TEXT,
                check_out TEXT
            )
            """
        )
        self._conn.commit()

    def add_booking(self, booking: Booking) -> Booking:
        cur = self._conn.execute(
            "INSERT INTO bookings (room_id, guest_name, language, check_in, check_out) VALUES (?, ?, ?, ?, ?)",
            (
                booking.room_id,
                booking.guest_name,
                booking.language,
                booking.check_in.isoformat(),
                booking.check_out.isoformat(),
            ),
        )
        self._conn.commit()
        booking.id = cur.lastrowid
        return booking

    def list_bookings(self) -> list[Booking]:
        cur = self._conn.execute(
            "SELECT id, room_id, guest_name, language, check_in, check_out FROM bookings"
        )
        rows = cur.fetchall()
        return [
            Booking(
                id=row[0],
                room_id=row[1],
                guest_name=row[2],
                language=row[3],
                check_in=date.fromisoformat(row[4]),
                check_out=date.fromisoformat(row[5]),
            )
            for row in rows
        ]
