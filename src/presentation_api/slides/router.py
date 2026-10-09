from collections.abc import AsyncIterable
from typing import Annotated

from asyncer import asyncify
from fastapi import APIRouter, Depends, Header, Path, Query
from fastapi.sse import EventSourceResponse, ServerSentEvent

from .service import ChunkResult, SlideService, get_slide_service

router = APIRouter(prefix="/slides", tags=["slides"])

SlideServiceDep = Annotated[SlideService, Depends(get_slide_service)]


def _done_event_id(result: ChunkResult) -> str | None:
    if result.resolved_index is None:
        return None
    if result.lines:
        return str(result.start_line + len(result.lines) - 1)
    return str(max(result.start_line - 1, 0))


@router.get(
    "/{filename}",
    response_class=EventSourceResponse,
    summary="Stream one chunk of a slide resource file",
    description=(
        "Streams a single chunk of a file from slide_resources/ line by line as "
        "Server-Sent Events. Chunks are delimited by standalone '---' lines "
        "(markdown table separators, lines inside fenced code blocks, and a leading "
        "YAML front matter block are never treated as delimiters). "
        "Clients choose which chunk to stream explicitly via the 'chunk' query "
        "parameter (0-based) — read chunk_index/total_chunks/has_more off the "
        "previous 'done' event to decide the next value. Requesting a chunk index "
        "past the end is clamped to the last chunk. "
        "Each line event's id is the line's index within the requested chunk. "
        "'Last-Event-ID' is only for the browser's own automatic reconnect after a "
        "dropped connection — it resumes mid-chunk from that line index; clients "
        "driving pagination themselves never need to set it. "
        "A final event with event='done' reports chunk_index, total_chunks, and "
        "has_more — clients should stop requesting once has_more is false. "
        "Allowed extensions: .md, .json, .js, .ts."
    ),
)
async def stream_slide_file(
    filename: Annotated[str, Path(description="Filename inside slide_resources/")],
    service: SlideServiceDep,
    chunk: Annotated[
        int,
        Query(ge=0, description="0-based chunk index to stream"),
    ] = 0,
    last_event_id: Annotated[
        int | None,
        Header(description="Line index within the requested chunk to resume from"),
    ] = None,
    delay_ms: Annotated[
        int, Query(ge=0, description="Per-line delay in milliseconds (0 = no delay)")
    ] = 0,
) -> AsyncIterable[ServerSentEvent]:
    result = await asyncify(service.get_chunk)(filename, chunk, last_event_id or 0)

    offset = 0
    async for line in service.iter_chunk_lines(result.lines, delay_ms=delay_ms):
        yield ServerSentEvent(raw_data=line, id=str(result.start_line + offset))
        offset += 1

    yield ServerSentEvent(
        event="done",
        id=_done_event_id(result),
        data={
            "chunk_index": result.resolved_index,
            "total_chunks": result.total_chunks,
            "has_more": result.has_more,
        },
    )
