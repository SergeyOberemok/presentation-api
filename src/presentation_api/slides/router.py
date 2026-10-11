from typing import Annotated

from fastapi import APIRouter, Depends, Query

from .builder import build_slides
from .schemas import SlideBuildResult, SlidePage
from .service import SlideService, get_slide_service

router = APIRouter(prefix="/slides", tags=["slides"])


@router.get(
    "/",
    summary="List slides",
    description="Returns slides from the dataset, paginated in chunks of 20 items.",
)
def list_slides(
    service: Annotated[SlideService, Depends(get_slide_service)],
    page: Annotated[int, Query(ge=1, description="1-indexed page number")] = 1,
) -> SlidePage:
    return service.get_slide_page(page)


@router.post(
    "/build",
    summary="Build slides from index.md",
    description=(
        "Parses the '>' blockquote sections of slide_resources/index.md and "
        "regenerates slide_resources/slides.json."
    ),
)
def build_slides_from_index() -> SlideBuildResult:
    slides = build_slides()
    return SlideBuildResult(total_items=len(slides), items=slides)
