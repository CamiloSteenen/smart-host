"""Minimal FastAPI application."""

from fastapi import FastAPI
from datetime import date

from ..service import HostService, PropertyService, BookingService
from ..infrastructure import (
    HostRepository,
    PropertyRepository,
    BookingRepository,
)
from ..domain import Host


def create_app() -> FastAPI:
    """Create and return the FastAPI application."""

    app = FastAPI()
    repository = HostRepository()
    prop_repo = PropertyRepository()
    booking_repo = BookingRepository()
    host_service = HostService()
    property_service = PropertyService()
    booking_service = BookingService(booking_repo)

    @app.get("/hosts")
    def list_hosts() -> list[dict]:
        """Return all hosts in repository."""
        hosts = repository.list_hosts()
        return [host_service.to_dict(host) for host in hosts]

    @app.post("/hosts")
    def add_host(name: str) -> dict:
        """Add a host by name and return it."""
        host = Host(name=name)
        repository.add(host)
        return host_service.to_dict(host)

    @app.post("/properties")
    def add_property(name: str, location: str) -> dict:
        """Create a property and return it."""
        prop = prop_repo.add_property(name=name, location=location)
        return property_service.to_dict(prop)

    @app.get("/properties")
    def list_properties() -> list[dict]:
        """List all properties."""
        props = prop_repo.list_properties()
        return [property_service.to_dict(p) for p in props]

    @app.post("/properties/{property_id}/rooms")
    def add_room(
        property_id: int,
        beds: int = 1,
        features: str | None = None,
        price: float = 0.0,
    ) -> dict:
        """Add a room to a property."""
        room = prop_repo.add_room(property_id, beds, features=features, price=price)
        return property_service.to_dict(room)

    @app.get("/properties/{property_id}/rooms")
    def list_rooms(property_id: int) -> list[dict]:
        """List rooms for a property."""
        rooms = prop_repo.list_rooms(property_id)
        return [property_service.to_dict(r) for r in rooms]

    @app.post("/bookings")
    def create_booking(
        room_id: int,
        guest_name: str,
        language: str,
        check_in: date,
        check_out: date,
    ) -> dict:
        """Create a booking for a room."""
        booking = booking_service.create_booking(
            room_id,
            guest_name,
            language,
            check_in,
            check_out,
        )
        return booking_service.to_dict(booking)

    @app.get("/bookings")
    def list_bookings() -> list[dict]:
        """Return all bookings."""
        bookings = booking_service.list_bookings()
        return [booking_service.to_dict(b) for b in bookings]

    return app


app = create_app()
