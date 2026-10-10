from pydantic import BaseModel, Field


class Slide(BaseModel):
    type: str = Field(description="Slide type discriminator")
    value: str = Field(description="Slide text content or resource filename")


class SlidePage(BaseModel):
    items: list[Slide] = Field(description="Slides on this page")
    page: int = Field(description="1-indexed page number")
    page_size: int = Field(description="Number of slides per page")
    total_items: int = Field(description="Total number of slides available")
    total_pages: int = Field(description="Total number of pages")
