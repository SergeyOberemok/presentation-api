# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project state

This is a freshly scaffolded FastAPI project (`presentation-api`) managed with `uv`. There is no API code yet beyond the `main()` entrypoint stub in `src/presentation_api/__init__.py`. Package layout, routers, and dependencies will take shape as the project grows — don't assume structure that isn't there yet.

## Commands

This project uses `uv` for all dependency and environment management (Python >=3.13, pinned via `.python-version`).

- Install dependencies: `uv sync`
- Run the CLI entrypoint: `uv run presentation-api`
- Run the FastAPI dev server (once an `app` object exists): `uv run fastapi dev src/presentation_api/<module>.py`
- Add a dependency: `uv add <package>`

There are no lint, type-check, or test commands configured yet (no Ruff/pytest config in `pyproject.toml`).

## Architecture

- `src/presentation_api/` — the package root (`src` layout, per `pyproject.toml`'s `uv_build` backend).
- `pyproject.toml` — declares the `presentation-api` CLI entrypoint (`presentation_api:main`) and the single current dependency, `fastapi[standard]`.

## FastAPI conventions

A FastAPI skill is available (`.agents/skills/fastapi/`, symlinked into `.claude/skills/` and `.bob/skills/`) and should be consulted when writing API code. Key conventions it specifies:

- Use `Annotated[...]` for parameter declarations and dependencies (`Depends()`), not bare defaults.
- Prefer a return type annotation over `response_model` unless the public schema differs from the internal return value.
- Don't use `...` (Ellipsis) as a default in path operations or Pydantic models; don't use Pydantic `RootModel`.
- Declare router-level `prefix`, `tags`, and shared `dependencies` on the `APIRouter` itself, not in `include_router()`.
- One HTTP operation per function.
- Default to `def` (sync) path operations unless the body is confirmed async-safe; never run blocking code inside `async def`.
- Use `app.frontend()` / `router.frontend()` to serve built frontend assets instead of mounting `StaticFiles` manually.
- For streaming/SSE, use `response_class=EventSourceResponse` with `yield`.
- Don't use `ORJSONResponse`/`UJSONResponse` (deprecated) — rely on Pydantic's Rust-side serialization via return types.
- Prefer `uv`, Ruff, `ty`, Asyncer, SQLModel, and HTTPX over their respective alternatives when those needs arise.

See `.agents/skills/fastapi/references/` for detailed guidance on dependencies, path operations, Pydantic models, responses, and streaming.
