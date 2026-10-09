from pydantic import BaseModel, Field


class Node(BaseModel):
    type: str = Field(description="Node type discriminator")
    value: str = Field(description="Node text content")


class NodePage(BaseModel):
    items: list[Node] = Field(description="Nodes on this page")
    page: int = Field(description="1-indexed page number")
    page_size: int = Field(description="Number of items per page")
    total_items: int = Field(description="Total number of nodes available")
    total_pages: int = Field(description="Total number of pages")
