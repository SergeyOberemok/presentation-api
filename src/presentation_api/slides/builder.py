import json
import logging
from pathlib import Path

from presentation_api.slide_resources.service import SLIDE_RESOURCES_DIR

from .parser import parse_markdown
from .schemas import Slide

logger = logging.getLogger(__name__)

SLIDES_SOURCE_FILE = SLIDE_RESOURCES_DIR / "index.md"
SLIDES_FILE = SLIDE_RESOURCES_DIR / "slides.json"


def build_slides(source: Path = SLIDES_SOURCE_FILE, target: Path = SLIDES_FILE) -> list[Slide]:
    """Parse the markdown script at `source` and write the slides to `target` as JSON."""
    slides = parse_markdown(source.read_text(encoding="utf-8"))

    for slide in slides:
        if slide.type != "text" and not (target.parent / slide.value).exists():
            logger.warning("Slide resource '%s' referenced in %s does not exist", slide.value, source)

    # An empty title and the default 'main' destination are left out of the file.
    data = [slide.model_dump(exclude_defaults=True) for slide in slides]

    tmp = target.with_suffix(target.suffix + ".tmp")
    tmp.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    tmp.replace(target)

    logger.info("Built %d slides from %s into %s", len(slides), source, target)
    return slides
