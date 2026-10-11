import json

from .builder import SLIDES_FILE
from .schemas import Slide

_cache: tuple[float, tuple[Slide, ...]] | None = None


def _load_slides() -> tuple[Slide, ...]:
    global _cache
    mtime = SLIDES_FILE.stat().st_mtime
    if _cache is not None and _cache[0] == mtime:
        return _cache[1]

    data = json.loads(SLIDES_FILE.read_text(encoding="utf-8"))
    slides = tuple(Slide.model_validate(item) for item in data)
    _cache = (mtime, slides)
    return slides


class SlideRepository:
    def list_all_slides(self) -> tuple[Slide, ...]:
        return _load_slides()


def get_slide_repository() -> SlideRepository:
    return SlideRepository()
