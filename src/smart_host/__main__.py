"""Entry point for running the Smart Host API using Uvicorn."""

from .config import HOST, PORT
from .interface.api import app

import uvicorn

if __name__ == "__main__":
    uvicorn.run(app, host=HOST, port=PORT)
