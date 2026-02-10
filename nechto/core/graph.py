"""
NECHTO v4.8 — Semantic Graph

Nodes + edges + evaluation functions.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional

from nechto.core.atoms import SemanticAtom, Edge, EdgeType, NodeStatus, Vector


@dataclass
class SemanticGraph:
    """Container for semantic atoms and their edges."""

    nodes: dict[str, SemanticAtom] = field(default_factory=dict)
    edges: list[Edge] = field(default_factory=list)

    # ------------------------------------------------------------------ ops
    def add_node(self, atom: SemanticAtom) -> SemanticAtom:
        self.nodes[atom.id] = atom
        return atom

    def add_edge(self, edge: Edge) -> Edge:
        self.edges.append(edge)
        return edge

    def remove_node(self, node_id: str) -> None:
        self.nodes.pop(node_id, None)
        self.edges = [e for e in self.edges if e.from_id != node_id and e.to_id != node_id]

    def get_node(self, node_id: str) -> Optional[SemanticAtom]:
        return self.nodes.get(node_id)

    def neighbors(self, node_id: str) -> list[str]:
        """Return IDs of nodes adjacent to *node_id*."""
        out: set[str] = set()
        for e in self.edges:
            if e.from_id == node_id:
                out.add(e.to_id)
            elif e.to_id == node_id:
                out.add(e.from_id)
        return list(out)

    def subgraph(self, node_ids: list[str]) -> "SemanticGraph":
        """Return a subgraph restricted to *node_ids*."""
        ids = set(node_ids)
        sub_nodes = {nid: n for nid, n in self.nodes.items() if nid in ids}
        sub_edges = [e for e in self.edges if e.from_id in ids and e.to_id in ids]
        return SemanticGraph(nodes=sub_nodes, edges=sub_edges)

    def connected_to(self, node_id: str, status: NodeStatus) -> bool:
        """True if *node_id* has a neighbor with the given *status*."""
        for nid in self.neighbors(node_id):
            n = self.nodes.get(nid)
            if n and n.status == status:
                return True
        return False

    @property
    def node_ids(self) -> set[str]:
        return set(self.nodes.keys())

    @property
    def edge_pairs(self) -> set[tuple[str, str]]:
        return {(e.from_id, e.to_id) for e in self.edges}

    def __len__(self) -> int:
        return len(self.nodes)
