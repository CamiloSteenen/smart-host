import os

"""Configuration for the Smart Host application."""

HOST: str = os.environ.get("HOST", "127.0.0.1")
"""Host interface to bind the web server to."""

PORT: int = int(os.environ.get("PORT", 8000))
"""Port the web server listens on."""
