from math import ceil
from typing import Annotated

from fastapi import Depends

from .repository import SlideRepository, get_slide_repository
from .schemas import SlidePage

SLIDES_PAGE_SIZE = 20


class SlideService:
    def __init__(self, repository: SlideRepository) -> None:
        self._repository = repository

    def get_slide_page(self, page: int) -> SlidePage:
        slides = self._repository.list_all_slides()
        total_items = len(slides)
        total_pages = max(1, ceil(total_items / SLIDES_PAGE_SIZE))
        first_slide_index = (page - 1) * SLIDES_PAGE_SIZE
        page_slides = slides[first_slide_index : first_slide_index + SLIDES_PAGE_SIZE]
        return SlidePage(
            items=list(page_slides),
            page=page,
            page_size=SLIDES_PAGE_SIZE,
            total_items=total_items,
            total_pages=total_pages,
        )


def get_slide_service(
    repository: Annotated[SlideRepository, Depends(get_slide_repository)],
) -> SlideService:
    return SlideService(repository)
