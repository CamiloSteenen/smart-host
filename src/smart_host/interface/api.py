"""Minimal FastAPI application."""

from fastapi import FastAPI

from ..service import HostService
from ..infrastructure import HostRepository
from ..domain import Host

app = FastAPI()
repository = HostRepository()
service = HostService()


@app.get("/hosts")
def list_hosts() -> list[dict]:
    """Return all hosts in repository."""
    hosts = repository.list_hosts()
    return [service.to_dict(host) for host in hosts]


@app.post("/hosts")
def add_host(name: str) -> dict:
    """Add a host by name and return it."""
    host = Host(name=name)
    repository.add(host)
    return service.to_dict(host)
