# Smart Host

Skeleton project demonstrating a simple layered architecture.

```
smart-host/
├── src/
│   └── smart_host/
│       ├── domain/          # business models
│       ├── service/         # service layer operating on models
│       ├── infrastructure/  # persistence and gateways
│       └── interface/       # web/API layer
└── tests/                   # pytest test suite
```

This repository contains placeholder modules with minimal functionality.

## Installation

Create a virtual environment and install the dependencies listed in
`requirements.txt`:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Running the API

Start the FastAPI app (example using Uvicorn). Since the code lives inside the
``src`` directory you need to include it in the ``PYTHONPATH``. The server host
and port can be configured via the ``HOST`` and ``PORT`` environment variables:

```bash
HOST=0.0.0.0 PORT=8000 PYTHONPATH=src \
    uvicorn smart_host.interface.api:app
```

The module also exposes a ``create_app`` function which can be used when
embedding the application within another project.

## Environment Configuration

When running locally or inside Docker the following environment variables may be
set:

- ``HOST`` – network interface Uvicorn binds to (default ``127.0.0.1``)
- ``PORT`` – port number for the API (default ``8000``)
- ``PYTHONPATH`` – must include ``src`` when executing modules from the
  repository

## Generating Sample Data

Use the helper script to create a property in Paradera, Aruba with a couple of rooms:

```bash
python scripts/generate_test_data.py
```

## Running Tests

After installing the dependencies you can run the unit tests with ``pytest``:

```bash
pytest
```

The ``generate_test_data.py`` script can be used to populate example data while
developing or testing the application.

## Docker

Build the Docker image and run the container exposing port ``8000``:

```bash
docker build -t smart-host .
docker run -p 8000:8000 smart-host
```

The ``HOST`` and ``PORT`` variables may be supplied to ``docker run`` to adjust
the network settings.

## API Endpoints

The API exposes basic CRUD-style operations for hosts, properties, rooms and bookings. New in this version are endpoints for creating and listing bookings:

```text
POST /bookings       # create a booking
GET  /bookings       # list all bookings
```
