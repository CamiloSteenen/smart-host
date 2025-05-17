"""Basic service definitions."""

from dataclasses import asdict

from ..domain import Host


class HostService:
    """Service operations for managing hosts."""

    def to_dict(self, host: Host) -> dict:
        """Return a host as a serializable dictionary."""
        return asdict(host)
