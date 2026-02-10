"""
NECHTO v4.8 — FLOW metric (PARTS 4.11, 11.3 B)

FLOW(V,t) = (skill_match × challenge_balance × presence_density)^(1/3)
"""

from __future__ import annotations

import math
from collections import deque

from nechto.core.atoms import Tag
from nechto.core.graph import SemanticGraph


def _clamp(v: float, lo: float = 0.0, hi: float = 1.0) -> float:
    return max(lo, min(hi, v))


# Reference constants
NMAX = 60
MAX_SKILL = 1.0
SIGMA = 0.2
DEFAULT_SKILL = 0.6


# -------------------------------------------------------------------
# 11.3 B — edge_density, base_complexity, difficulty, required_skill
# -------------------------------------------------------------------
def edge_density(n_nodes: int, n_edges: int) -> float:
    max_e = n_nodes * (n_nodes - 1) / 2
    if max_e < 1:
        return 0.0
    return _clamp(n_edges / max_e)


def base_complexity(n_nodes: int) -> float:
    return _clamp(0.2 + 0.8 * (n_nodes / NMAX))


def difficulty(n_nodes: int, n_edges: int) -> float:
    bc = base_complexity(n_nodes)
    ed = edge_density(n_nodes, n_edges)
    return _clamp(bc + 0.2 * ed)


def required_skill(diff: float) -> float:
    return diff


def current_skill(success_history: deque[float] | list[float] | None = None) -> float:
    """Moving average of difficulty of prior successes, window=5."""
    if not success_history:
        return DEFAULT_SKILL
    window = list(success_history)[-5:]
    return sum(window) / len(window)


# -------------------------------------------------------------------
# 4.11 FLOW
# skill_match = 1 - |required_skill - current_skill| / max_skill
# challenge_balance = exp(-((difficulty - optimal_difficulty)^2)/(2σ^2))
# optimal_difficulty = current_skill + 0.1
# presence_density = (WITNESS + EMOTION + INTENT nodes) / max(1, N)
# FLOW = (skill_match × challenge_balance × presence_density)^(1/3)
# -------------------------------------------------------------------
def flow_metric(
    graph: SemanticGraph,
    node_ids: list[str],
    n_edges: int,
    success_history: deque[float] | list[float] | None = None,
) -> float:
    n = len(node_ids)
    if n == 0:
        return 0.0

    diff = difficulty(n, n_edges)
    cs = current_skill(success_history)
    rs = required_skill(diff)

    skill_match = _clamp(1.0 - abs(rs - cs) / MAX_SKILL)

    optimal_diff = cs + 0.1
    challenge_balance = math.exp(-((diff - optimal_diff) ** 2) / (2 * SIGMA ** 2))

    presence_tags = {Tag.WITNESS, Tag.EMOTION, Tag.INTENT}
    presence_count = sum(
        1 for nid in node_ids
        if (atom := graph.get_node(nid)) and any(t in presence_tags for t in atom.tags)
    )
    presence_density = presence_count / max(1, n)

    return _clamp((skill_match * challenge_balance * presence_density) ** (1.0 / 3.0))
