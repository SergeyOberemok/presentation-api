from typing import Annotated

from fastapi import APIRouter, Depends, Query

from .schemas import NodePage
from .service import NodeService, get_node_service

router = APIRouter(prefix="/nodes", tags=["nodes"])


@router.get(
    "/",
    summary="List nodes",
    description="Returns nodes from the dataset, paginated in chunks of 20 items.",
)
def list_nodes(
    service: Annotated[NodeService, Depends(get_node_service)],
    page: Annotated[int, Query(ge=1, description="1-indexed page number")] = 1,
) -> NodePage:
    return service.get_page(page)
