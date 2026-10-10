import json
from functools import lru_cache
from pathlib import Path

from .schemas import Slide

SLIDES_FILE = Path(__file__).resolve().parents[2] / "core" / "slides.json"


@lru_cache(maxsize=1)
def _load_slides() -> tuple[Slide, ...]:
    data = json.loads(SLIDES_FILE.read_text(encoding="utf-8"))
    return tuple(Slide(**item) for item in data)


class SlideRepository:
    def list_all_slides(self) -> tuple[Slide, ...]:
        return _load_slides()


def get_slide_repository() -> SlideRepository:
    return SlideRepository()
