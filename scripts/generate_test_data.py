"""Script to populate an SQLite database with sample data."""

from __future__ import annotations

import sqlite3
from pathlib import Path
from typing import Optional

DB_PATH = Path(__file__).resolve().parents[1] / "smart_host.db"


def init_db(conn: sqlite3.Connection) -> None:
    """Create tables if they do not already exist."""
    cur = conn.cursor()
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS hosts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL,
            rating REAL DEFAULT 0.0
        )
        """
    )
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS properties (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL,
            location TEXT NOT NULL
        )
        """
    )
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS rooms (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            property_id INTEGER NOT NULL,
            beds INTEGER DEFAULT 1,
            features TEXT,
            price REAL DEFAULT 0.0,
            FOREIGN KEY(property_id) REFERENCES properties(id)
        )
        """
    )
    conn.commit()


def add_host(conn: sqlite3.Connection, name: str, rating: float = 0.0) -> tuple[int, str, float]:
    cur = conn.cursor()
    cur.execute("INSERT OR IGNORE INTO hosts(name, rating) VALUES (?, ?)", (name, rating))
    conn.commit()
    cur.execute("SELECT id, name, rating FROM hosts WHERE name=?", (name,))
    return cur.fetchone()


def add_property(conn: sqlite3.Connection, name: str, location: str) -> tuple[int, str, str]:
    cur = conn.cursor()
    cur.execute(
        "INSERT OR IGNORE INTO properties(name, location) VALUES (?, ?)",
        (name, location),
    )
    conn.commit()
    cur.execute("SELECT id, name, location FROM properties WHERE name=?", (name,))
    return cur.fetchone()


def add_room(
    conn: sqlite3.Connection,
    property_id: int,
    beds: int = 1,
    *,
    features: Optional[str] = None,
    price: float = 0.0,
) -> tuple[int, int, int, Optional[str], float]:
    cur = conn.cursor()
    cur.execute(
        """
        SELECT id FROM rooms
        WHERE property_id=? AND beds=? AND features IS ? AND price=?
        """,
        (property_id, beds, features, price),
    )
    row = cur.fetchone()
    if row is None:
        cur.execute(
            "INSERT INTO rooms(property_id, beds, features, price) VALUES (?, ?, ?, ?)",
            (property_id, beds, features, price),
        )
        conn.commit()
        room_id = cur.lastrowid
    else:
        room_id = row[0]
    cur.execute("SELECT * FROM rooms WHERE id=?", (room_id,))
    return cur.fetchone()


def main() -> None:
    conn = sqlite3.connect(DB_PATH)
    init_db(conn)

    alice = add_host(conn, "Alice", rating=4.5)
    bob = add_host(conn, "Bob", rating=4.8)
    print(f"Hosts: {alice}, {bob}")

    aruba = add_property(conn, "Aruba House", "Paradera")
    room1 = add_room(conn, aruba[0], beds=2, features="Sea view", price=100.0)
    room2 = add_room(conn, aruba[0], beds=1, features="Garden access", price=80.0)

    print("Property:", aruba)
    print("Rooms:", room1, room2)

    conn.close()


if __name__ == "__main__":
    main()
