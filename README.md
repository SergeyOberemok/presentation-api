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
| `POST` | `/slides/build` | Regenerate `slide_resources/slides.json` from `slide_resources/index.md`. |
| `GET` | `/slides/` | List slides, paginated in chunks of 20. Use `?page=` (1-indexed) to navigate. |
| `GET` | `/slide-resources/{filename}/stream` | Stream one chunk of a slide resource file as Server-Sent Events. |

## Slide markup

Write the presentation script in `slide_resources/index.md`. When the app starts, and on `POST /slides/build`, the script is compiled into `slide_resources/slides.json`. That is the file `GET /slides/` serves.

- Only blockquote (`>`) sections become slides. Every other line is narration and is ignored.
- Consecutive `>` lines form one slide. A bare `>` line is a blank line inside the same slide.
- An empty line or a narration line between `>` blocks starts a new slide.
- A slide whose whole body is one link to a local file becomes a file slide. Anything else is a `text` slide, and its value is the markdown as written, with the `>` markers removed.

Link syntax: `[destination:title](/file.ext)` or `![destination:title](/file.ext)`

| Part | Meaning |
|---|---|
| `!` prefix | Image: `type` is `image:<ext>`. Without it, `type` is `file:<ext>`. |
| `destination` | Where the slide is shown. The default is `main`. Without a colon, a known destination (`main`, `chat`) is the destination; any other label is the title. |
| `title` | Optional. Left out of the JSON when empty. |
| `/file.ext` | A file in `slide_resources/`. `<...>` wrapping and `%20` escapes are supported. The extension sets the type. |

| Markdown | Slide |
|---|---|
| `> Main title` | `{"type": "text", "value": "Main title"}` |
| `> ### Results` + `>` + `> - Revenue up` | `{"type": "text", "value": "### Results

- Revenue up"}` |
| `> ![main: funny image](</Screenshot%20(1).png>)` | `{"title": "funny image", "type": "image:png", "value": "Screenshot (1).png"}` |
| `> ![](/diagram.svg)` | `{"type": "image:svg", "value": "diagram.svg"}` |
| `> [main:some code](/test.json)` | `{"title": "some code", "type": "file:json", "value": "test.json"}` |
| `> [some code](/test.json)` | `{"title": "some code", "type": "file:json", "value": "test.json"}` |
| `> [chat](/session.md)` | `{"type": "file:md", "destination": "chat", "value": "session.md"}` |
| `> [chat: Transcript](/session.md)` | `{"title": "Transcript", "type": "file:md", "destination": "chat", "value": "session.md"}` |

## Tests

```bash
uv run pytest
```

## Project structure

```
src/
└── presentation_api/
    ├── app.py          # FastAPI application entry point
    ├── slides/            # Slide list (paginated) + index.md -> slides.json
    │   ├── parser.py      # Markdown blockquote -> Slide parser
    │   ├── builder.py     # Writes slide_resources/slides.json
    │   ├── router.py
    │   ├── service.py
    │   ├── repository.py
    │   └── schemas.py
    └── slide_resources/   # Chunked SSE streaming of slide_resources/ files
        ├── router.py
        ├── service.py
        └── schemas.py
```
