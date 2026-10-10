from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from presentation_api.slide_resources.router import router as slide_resources_router
from presentation_api.slides.router import router as slides_router

app = FastAPI(title="Presentation API")
app.include_router(slides_router)
app.include_router(slide_resources_router)

app.mount(
    "/slide-resources",
    StaticFiles(directory="slide_resources"),
    name="slide_resources",
)
