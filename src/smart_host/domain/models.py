"""Domain models for Smart Host."""

from dataclasses import dataclass


@dataclass
class Host:
    """Represents a host entity."""

    name: str
    rating: float = 0.0
