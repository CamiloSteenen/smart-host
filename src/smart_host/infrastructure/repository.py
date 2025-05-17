"""Infrastructure repository implementations."""

from ..domain import Host


class HostRepository:
    """Placeholder in-memory host store."""

    def __init__(self) -> None:
        self._hosts: list[Host] = []

    def add(self, host: Host) -> None:
        self._hosts.append(host)

    def list_hosts(self) -> list[Host]:
        return list(self._hosts)
