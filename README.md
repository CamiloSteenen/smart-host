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

## Running the API

Install dependencies and start the FastAPI app (example using Uvicorn). Since
the code lives inside the ``src`` directory you need to include it in the
``PYTHONPATH`` when running ``uvicorn``:

```bash
PYTHONPATH=src uvicorn smart_host.interface.api:app
```

The module also exposes a ``create_app`` function which can be used when
embedding the application within another project.

## Generating Sample Data

Run the helper script to populate ``smart_host.db`` with a few example hosts,
one property and two rooms. The script is idempotent so it can be executed
multiple times without duplicating entries.

```bash
python scripts/generate_test_data.py
```

## API Endpoints

The API exposes basic CRUD-style operations for hosts, properties, rooms and bookings. New in this version are endpoints for creating and listing bookings:

```text
POST /bookings       # create a booking
GET  /bookings       # list all bookings
```
