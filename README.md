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

Use the helper script to create a property in Paradera, Aruba with a couple of rooms:

```bash
python scripts/generate_test_data.py
```
