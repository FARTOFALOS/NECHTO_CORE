"""
NECHTO v4.8 — Base metrics (PART 4.1)

TI, CI, AR, FZD, RI, SQ_proxy, Φ_proxy, GBI_proxy, GNS_proxy, flow_rate.
All metrics are computed from a SemanticGraph + Vector subgraph.
"""

from __future__ import annotations

from nechto.core.atoms import NodeStatus, Tag
from nechto.core.graph import SemanticGraph


def _clamp(v: float, lo: float = 0.0, hi: float = 1.0) -> float:
    return max(lo, min(hi, v))


# -------------------------------------------------------------------
# TI — Temporal Integrity  ∈ [0..1]
# Fraction of nodes whose status is stable (≠ FLOATING, ≠ HYPOTHESIS)
# -------------------------------------------------------------------
def temporal_integrity(graph: SemanticGraph, node_ids: list[str]) -> float:
    if not node_ids:
        return 0.0
    stable = sum(
        1 for nid in node_ids
        if (n := graph.get_node(nid)) and n.status not in (NodeStatus.FLOATING, NodeStatus.HYPOTHESIS)
    )
    return stable / len(node_ids)


# -------------------------------------------------------------------
# CI — Coherence Index  ∈ [0..1]
# Edge density of the subgraph
# -------------------------------------------------------------------
def coherence_index(graph: SemanticGraph, node_ids: list[str], edges_in_v: int) -> float:
    n = len(node_ids)
    if n < 2:
        return 1.0
    max_edges = n * (n - 1) / 2
    return _clamp(edges_in_v / max_edges)


# -------------------------------------------------------------------
# AR — Anchoring Ratio  ∈ [0..1]
# Fraction of ANCHORED nodes
# -------------------------------------------------------------------
def anchoring_ratio(graph: SemanticGraph, node_ids: list[str]) -> float:
    if not node_ids:
        return 0.0
    anchored = sum(
        1 for nid in node_ids
        if (n := graph.get_node(nid)) and n.status == NodeStatus.ANCHORED
    )
    return anchored / len(node_ids)


# -------------------------------------------------------------------
# FZD — Freeze/Decomposition  ∈ [0..1]
# 0 = no freeze, 1 = full.  Based on BLOCKING fraction.
# -------------------------------------------------------------------
def freeze_decomposition(graph: SemanticGraph, node_ids: list[str]) -> float:
    if not node_ids:
        return 0.0
    blocked = sum(
        1 for nid in node_ids
        if (n := graph.get_node(nid)) and n.status in (NodeStatus.BLOCKING, NodeStatus.ETHICALLY_BLOCKED)
    )
    return blocked / len(node_ids)


# -------------------------------------------------------------------
# RI — Resonance Index  ∈ [0..1]
# Mean resonance axis value across nodes
# -------------------------------------------------------------------
def resonance_index(graph: SemanticGraph, node_ids: list[str]) -> float:
    if not node_ids:
        return 0.0
    total = 0.0
    for nid in node_ids:
        n = graph.get_node(nid)
        if n:
            total += n.resonance
    return _clamp(total / len(node_ids))


# -------------------------------------------------------------------
# SQ_proxy — Semantic Quality  ∈ [0..1]
# Graph coherence × density × resonance
# -------------------------------------------------------------------
def sq_proxy(ci: float, ri: float, ar: float) -> float:
    return _clamp(ci * ri * ar)


# -------------------------------------------------------------------
# Φ_proxy — Integrated information proxy  ∈ [0..1]
# Fraction of nodes reachable from each other (connectivity proxy)
# -------------------------------------------------------------------
def phi_proxy(graph: SemanticGraph, node_ids: list[str]) -> float:
    if len(node_ids) < 2:
        return 1.0
    ids = set(node_ids)
    adj: dict[str, set[str]] = {nid: set() for nid in ids}
    for e in graph.edges:
        if e.from_id in ids and e.to_id in ids:
            adj[e.from_id].add(e.to_id)
            adj[e.to_id].add(e.from_id)

    # BFS from first node
    start = node_ids[0]
    visited: set[str] = set()
    queue = [start]
    while queue:
        cur = queue.pop(0)
        if cur in visited:
            continue
        visited.add(cur)
        for nb in adj.get(cur, []):
            if nb not in visited:
                queue.append(nb)
    return len(visited) / len(node_ids)


# -------------------------------------------------------------------
# GBI_proxy — Global Broadcast Integrator  ∈ [0..1]
# Degree centrality mean
# -------------------------------------------------------------------
def gbi_proxy(graph: SemanticGraph, node_ids: list[str]) -> float:
    if len(node_ids) < 2:
        return 1.0
    ids = set(node_ids)
    degree: dict[str, int] = {nid: 0 for nid in ids}
    for e in graph.edges:
        if e.from_id in ids and e.to_id in ids:
            degree[e.from_id] = degree.get(e.from_id, 0) + 1
            degree[e.to_id] = degree.get(e.to_id, 0) + 1
    max_deg = len(node_ids) - 1
    return _clamp(sum(degree.values()) / (len(node_ids) * max_deg))


# -------------------------------------------------------------------
# GNS_proxy — Generative Novelty  ∈ [0..1]
# Mean novelty axis
# -------------------------------------------------------------------
def gns_proxy(graph: SemanticGraph, node_ids: list[str]) -> float:
    if not node_ids:
        return 0.0
    total = sum(
        graph.get_node(nid).novelty
        for nid in node_ids
        if graph.get_node(nid)
    )
    return _clamp(total / len(node_ids))
