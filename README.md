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
| `GET` | `/slides/` | List slides, paginated in chunks of 20. Use `?page=` (1-indexed) to navigate. |
| `GET` | `/slide-resources/{filename}/stream` | Stream one chunk of a slide resource file as Server-Sent Events. |

## Project structure

```
src/
└── presentation_api/
    ├── app.py          # FastAPI application entry point
    ├── slides/            # Slide list (paginated)
    │   ├── router.py
    │   ├── service.py
    │   ├── repository.py
    │   └── schemas.py
    └── slide_resources/   # Chunked SSE streaming of slide_resources/ files
        ├── router.py
        ├── service.py
        └── schemas.py
```
