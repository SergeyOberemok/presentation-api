from pydantic import BaseModel, Field


class SlideResourceLine(BaseModel):
    text: str = Field(description="A single line of text from the slide resource file")
