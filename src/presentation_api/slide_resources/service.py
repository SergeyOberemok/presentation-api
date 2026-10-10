import asyncio
import re
from collections.abc import AsyncIterator
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path

from fastapi import HTTPException

SLIDE_RESOURCES_DIR = Path("slide_resources")

ALLOWED_EXTENSIONS: frozenset[str] = frozenset({
    ".md",
    ".json",
    ".js",
    ".ts",
})

_CHUNK_DELIMITER = re.compile(r"^-{3,}$")
_CODE_FENCE = re.compile(r"^(`{3,}|~{3,})")


@dataclass(frozen=True)
class ResourceChunk:
    lines: list[str]
    first_line_index: int
    chunk_index: int | None
    total_chunks: int
    has_more: bool


class SlideResourceService:
    def __init__(self) -> None:
        self._chunks_cache: dict[Path, tuple[float, list[list[str]]]] = {}

    def _resolve_resource_path(self, filename: str) -> Path:
        path = Path(filename)

        if path.suffix not in ALLOWED_EXTENSIONS:
            raise HTTPException(
                status_code=400,
                detail=f"Extension '{path.suffix}' is not allowed. "
                       f"Allowed: {sorted(ALLOWED_EXTENSIONS)}",
            )

        resolved = (SLIDE_RESOURCES_DIR / path).resolve()
        base = SLIDE_RESOURCES_DIR.resolve()

        if not resolved.is_relative_to(base):
            raise HTTPException(status_code=400, detail="Invalid file path.")

        if not resolved.exists():
            raise HTTPException(status_code=404, detail=f"File '{filename}' not found.")

        return resolved

    def _parse_chunks(self, resolved: Path) -> list[list[str]]:
        chunks: list[list[str]] = []
        current: list[str] = []
        in_code_fence = False
        in_front_matter = False

        with resolved.open(encoding="utf-8") as fh:
            for index, raw_line in enumerate(fh):
                line = raw_line.rstrip("\n")
                stripped = line.strip()

                if _CODE_FENCE.match(stripped):
                    in_code_fence = not in_code_fence
                    current.append(line)
                    continue

                if index == 0 and stripped == "---":
                    in_front_matter = True
                    current.append(line)
                    continue

                if in_front_matter:
                    current.append(line)
                    if stripped == "---":
                        in_front_matter = False
                    continue

                if not in_code_fence and _CHUNK_DELIMITER.match(stripped):
                    chunks.append(current)
                    current = []
                else:
                    current.append(line)

        chunks.append(current)
        return [chunk for chunk in chunks if any(line.strip() for line in chunk)]

    def _load_chunks(self, filename: str) -> list[list[str]]:
        resolved = self._resolve_resource_path(filename)
        mtime = resolved.stat().st_mtime

        cached = self._chunks_cache.get(resolved)
        if cached is not None and cached[0] == mtime:
            return cached[1]

        chunks = self._parse_chunks(resolved)
        self._chunks_cache[resolved] = (mtime, chunks)
        return chunks

    def get_resource_chunk(self, filename: str, chunk_index: int, first_line_index: int = 0) -> ResourceChunk:
        """Resolve the slice of lines to send for an explicitly requested chunk.

        `chunk_index` is the chunk the client wants (clamped into range). `first_line_index`
        resumes mid-chunk — the browser's own automatic SSE reconnect resends the last
        line index it saw via `Last-Event-ID`, so a dropped connection continues from
        where it left off instead of restarting the whole chunk.
        """
        chunks = self._load_chunks(filename)

        if not chunks:
            return ResourceChunk(
                lines=[], first_line_index=0, chunk_index=None, total_chunks=0, has_more=False
            )

        chunk_idx = max(0, min(chunk_index, len(chunks) - 1))
        line_idx = max(0, min(first_line_index, len(chunks[chunk_idx])))

        lines = chunks[chunk_idx][line_idx:]
        has_more = chunk_idx < len(chunks) - 1

        return ResourceChunk(
            lines=lines,
            first_line_index=line_idx,
            chunk_index=chunk_idx,
            total_chunks=len(chunks),
            has_more=has_more,
        )

    async def iter_chunk_lines(self, lines: list[str], delay_ms: int = 0) -> AsyncIterator[str]:
        delay_s = delay_ms / 1000
        for line in lines:
            yield line
            await asyncio.sleep(delay_s)


@lru_cache
def get_slide_resource_service() -> SlideResourceService:
    return SlideResourceService()
