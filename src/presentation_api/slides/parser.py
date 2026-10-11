"""Turn the blockquote sections of a markdown script into slides.

Every run of consecutive lines starting with '>' is one slide; any line without
'>' (empty or narration text) ends it. A slide whose whole body is a single link
`[dest:title](file)` or image `![dest:title](file)` becomes a file/image slide,
everything else is a 'text' slide holding the markdown as written.
"""

import re
from pathlib import PurePosixPath
from urllib.parse import unquote

from .schemas import DEFAULT_DESTINATION, Slide

KNOWN_DESTINATIONS: frozenset[str] = frozenset({"main", "chat"})

_BLOCKQUOTE = re.compile(r"^\s{0,3}>")
_CODE_FENCE = re.compile(r"^\s{0,3}(`{3,}|~{3,})")
_LINK_ONLY = re.compile(r"^(!)?\[([^\]]*)\]\(\s*(<[^>]+>|[^)\s]+)\s*\)$")


def _strip_quote_marker(line: str) -> str:
    content = line.lstrip()[1:]
    return content[1:] if content.startswith(" ") else content


def split_blockquote_slides(text: str) -> list[str]:
    slides: list[str] = []
    current: list[str] = []
    in_code_fence = False

    def flush() -> None:
        body = "\n".join(current).strip()
        if body:
            slides.append(body)
        current.clear()

    for line in text.splitlines():
        if not in_code_fence and _BLOCKQUOTE.match(line):
            current.append(_strip_quote_marker(line))
            continue

        flush()
        if _CODE_FENCE.match(line):
            in_code_fence = not in_code_fence

    flush()
    return slides


def _parse_label(label: str) -> tuple[str, str | None]:
    if ":" in label:
        destination, title = (part.strip() for part in label.split(":", 1))
        return destination or DEFAULT_DESTINATION, title or None

    label = label.strip()
    if label in KNOWN_DESTINATIONS:
        return label, None
    return DEFAULT_DESTINATION, label or None


def _parse_target(target: str) -> str:
    if target.startswith("<") and target.endswith(">"):
        target = target[1:-1]
    return unquote(target.strip()).lstrip("/")


def parse_slide(body: str) -> Slide:
    match = _LINK_ONLY.match(body.strip())
    if match is None:
        return Slide(type="text", value=body)

    is_image, label, target = match.groups()
    value = _parse_target(target)
    extension = PurePosixPath(value).suffix.lower().lstrip(".")
    # Only local files in slide_resources/ become file slides; external URLs stay text.
    if not extension or "://" in value:
        return Slide(type="text", value=body)

    destination, title = _parse_label(label)
    kind = "image" if is_image else "file"
    return Slide(title=title, type=f"{kind}:{extension}", destination=destination, value=value)


def parse_markdown(text: str) -> list[Slide]:
    return [parse_slide(body) for body in split_blockquote_slides(text)]
