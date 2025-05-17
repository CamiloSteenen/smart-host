"""Minimal FastAPI application."""

from fastapi import FastAPI

from ..service import HostService, PropertyService
from ..infrastructure import HostRepository, PropertyRepository
from ..domain import Host


def create_app() -> FastAPI:
    """Create and return the FastAPI application."""

    app = FastAPI()
    repository = HostRepository()
    prop_repo = PropertyRepository()
    host_service = HostService()
    property_service = PropertyService()

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

    return app


app = create_app()
