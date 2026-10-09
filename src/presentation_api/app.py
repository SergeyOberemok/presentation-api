from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from presentation_api.nodes.router import router as nodes_router
from presentation_api.slides.router import router as slides_router

app = FastAPI(title="Presentation API")
app.include_router(nodes_router)
app.include_router(slides_router)

app.mount(
    "/slide-resources",
    StaticFiles(directory="slide_resources"),
    name="slide_resources",
)
