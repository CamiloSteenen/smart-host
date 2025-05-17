"""Domain models for Smart Host."""

from dataclasses import dataclass
from datetime import date
from typing import Optional


@dataclass
class Host:
    """Represents a host entity."""

    name: str
    rating: float = 0.0


@dataclass
class Property:
    """Rental property that may contain multiple rooms."""

    id: int
    name: str
    location: str


@dataclass
class Room:
    """Individual room within a property."""

    id: int
    property_id: int
    beds: int = 1
    features: Optional[str] = None
    price: float = 0.0


@dataclass
class Booking:
    """Booking for a room by a travel group."""

    id: int
    room_id: int
    guest_name: str
    language: str
    check_in: date
    check_out: date
