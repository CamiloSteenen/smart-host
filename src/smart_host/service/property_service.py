"""Service operations for properties and rooms."""

from dataclasses import asdict

from ..domain import Property, Room


class PropertyService:
    """Business logic around properties and rooms."""

    def to_dict(self, obj: Property | Room) -> dict:
        """Return dataclass as dict."""
        return asdict(obj)
