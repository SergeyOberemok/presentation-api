from typing import Annotated

from fastapi import APIRouter, Depends, Query

from .schemas import SlidePage
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
