import logging
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from presentation_api.slide_resources.router import router as slide_resources_router
from presentation_api.slides.builder import build_slides
from presentation_api.slides.router import router as slides_router

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    try:
        build_slides()
    except Exception:
        logger.exception("Failed to build slides from index.md; keeping the existing slides.json")
    yield


app = FastAPI(title="Presentation API", lifespan=lifespan)
app.include_router(slides_router)
app.include_router(slide_resources_router)

app.mount(
    "/slide-resources",
    StaticFiles(directory="slide_resources"),
    name="slide_resources",
)
