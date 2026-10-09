from math import ceil
from typing import Annotated

from fastapi import Depends

from .repository import NodeRepository, get_node_repository
from .schemas import NodePage

PAGE_SIZE = 20


class NodeService:
    def __init__(self, repository: NodeRepository) -> None:
        self._repository = repository

    def get_page(self, page: int) -> NodePage:
        nodes = self._repository.list_all()
        total_items = len(nodes)
        total_pages = max(1, ceil(total_items / PAGE_SIZE))
        start = (page - 1) * PAGE_SIZE
        selected = nodes[start : start + PAGE_SIZE]
        return NodePage(
            items=list(selected),
            page=page,
            page_size=PAGE_SIZE,
            total_items=total_items,
            total_pages=total_pages,
        )


def get_node_service(
    repository: Annotated[NodeRepository, Depends(get_node_repository)],
) -> NodeService:
    return NodeService(repository)
