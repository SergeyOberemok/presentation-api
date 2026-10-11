from pydantic import BaseModel, Field

DEFAULT_DESTINATION = "main"


class Slide(BaseModel):
    title: str | None = Field(default=None, description="Optional slide title")
    type: str = Field(description="Slide type discriminator, e.g. 'text', 'image:png', 'file:json'")
    destination: str = Field(
        default=DEFAULT_DESTINATION,
        description="Where the slide is shown, e.g. 'main' or 'chat'",
    )
    value: str = Field(description="Slide text content or resource filename")


class SlidePage(BaseModel):
    items: list[Slide] = Field(description="Slides on this page")
    page: int = Field(description="1-indexed page number")
    page_size: int = Field(description="Number of slides per page")
    total_items: int = Field(description="Total number of slides available")
    total_pages: int = Field(description="Total number of pages")


class SlideBuildResult(BaseModel):
    total_items: int = Field(description="Number of slides generated from index.md")
    items: list[Slide] = Field(description="Generated slides")
