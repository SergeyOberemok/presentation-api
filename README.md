# Presentation API

A FastAPI project built with Python 3.13 and managed by [uv](https://docs.astral.sh/uv/).

## Prerequisites

- Python 3.13+
- [uv](https://docs.astral.sh/uv/getting-started/installation/)

## Setup

Install dependencies:

```bash
uv sync
```

## Running the development server

```bash
uv run presentation-api
```

Hot-reload is enabled by default. The API will be available at `http://localhost:8000`.

## Running in production

```bash
ENV=production uv run presentation-api
```

Set `ENV=production` to disable hot-reload.

## Interactive docs

| URL | Description |
|---|---|
| `http://localhost:8000/docs` | Swagger UI |
| `http://localhost:8000/redoc` | ReDoc |

## API

| Method | Path | Description |
|---|---|---|
| `GET` | `/nodes/` | List nodes, paginated in chunks of 20. Use `?page=` (1-indexed) to navigate. |

## Project structure

```
src/
└── presentation_api/
    ├── app.py          # FastAPI application entry point
    └── nodes/
        ├── router.py   # Route definitions
        ├── service.py  # Business logic
        ├── repository.py  # Data access
        └── schemas.py  # Pydantic models
```
