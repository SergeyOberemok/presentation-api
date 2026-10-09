import json
from functools import lru_cache
from pathlib import Path

from .schemas import Node

NODES_FILE = Path(__file__).resolve().parents[2] / "core" / "nodes.json"


@lru_cache(maxsize=1)
def _load_nodes() -> tuple[Node, ...]:
    data = json.loads(NODES_FILE.read_text(encoding="utf-8"))
    return tuple(Node(**item) for item in data)


class NodeRepository:
    def list_all(self) -> tuple[Node, ...]:
        return _load_nodes()


def get_node_repository() -> NodeRepository:
    return NodeRepository()
