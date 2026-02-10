"""
NECHTO v4.8 — Ethics metrics (PARTS 4.9, 4.15, 11.6 E)

ethical_coefficient, executable, harm_probability, identity_alignment,
Ethical_score_candidates, Blocked_fraction.
"""

from __future__ import annotations

from nechto.core.atoms import SemanticAtom, Tag, NodeStatus, AvoidedMarker
from nechto.core.graph import SemanticGraph


def _clamp(v: float, lo: float = 0.0, hi: float = 1.0) -> float:
    return max(lo, min(hi, v))


# -------------------------------------------------------------------
# 11.6 E — tag_harm_max
# -------------------------------------------------------------------
TAG_HARM_MAX: dict[Tag, float] = {
    Tag.HARM: 0.9,
    Tag.MANIPULATION: 0.7,
    Tag.DECEPTION: 0.6,
    Tag.BOUNDARY: 0.5,    # BLOCKING proxy
    Tag.EMOTION: 0.1,
    Tag.INTENT: 0.2,
    Tag.WITNESS: 0.0,
}


# -------------------------------------------------------------------
# harm_probability(node)  (PART 11.6 E)
# -------------------------------------------------------------------
def compute_harm_probability(atom: SemanticAtom, graph: SemanticGraph) -> float:
    """
    harm_probability = clamp(max(tag_harm_max(tags)) × context_multiplier + graph_penalty, 0, 1)
    Worst-case policy: undefined → harm=1.
    """
    if not atom.tags:
        # Conservative: no tags → low but not zero
        base = 0.0
    else:
        base = max(TAG_HARM_MAX.get(t, 0.0) for t in atom.tags)

    context_multiplier = 1.0  # REFERENCE = 1.0

    graph_penalty = 0.2 if graph.connected_to(atom.id, NodeStatus.BLOCKING) else 0.0

    return _clamp(base * context_multiplier + graph_penalty)


# -------------------------------------------------------------------
# identity_alignment(node)  (PART 11.6 E)
# -------------------------------------------------------------------
def compute_identity_alignment(atom: SemanticAtom) -> float:
    """
    identity_alignment = clamp(positive - negative, -1, 1)
    Worst-case: undefined → alignment = -1.
    """
    positive = 0.0
    negative = 0.0

    # Positive indicators
    if Tag.WITNESS in atom.tags:
        positive += 0.3
    if Tag.INTENT in atom.tags and Tag.MANIPULATION not in atom.tags:
        positive += 0.2
    if atom.status == NodeStatus.ANCHORED:
        positive += 0.3
    if Tag.BOUNDARY in atom.tags and Tag.HARM not in atom.tags:
        positive += 0.2

    # Negative indicators
    if Tag.MANIPULATION in atom.tags:
        negative += 0.5
    if Tag.DECEPTION in atom.tags:
        negative += 0.6
    if atom.status == NodeStatus.BLOCKING:
        negative += 0.4
    if atom.avoided_marker == AvoidedMarker.AVOIDED:
        negative += 0.3

    return max(-1.0, min(1.0, positive - negative))


# -------------------------------------------------------------------
# 4.9 ethical_coefficient(V)
# harm_penalty(V) = 1 - max_i(harm_probability(i) for i ∈ V)
# ethical_coefficient(V) = clamp(mean(identity_alignment) × harm_penalty, 0.1, 1.0)
# -------------------------------------------------------------------
def ethical_coefficient(
    graph: SemanticGraph,
    node_ids: list[str],
) -> float:
    if not node_ids:
        return 1.0

    harms: list[float] = []
    alignments: list[float] = []

    for nid in node_ids:
        n = graph.get_node(nid)
        if n is None:
            # Worst-case policy
            harms.append(1.0)
            alignments.append(-1.0)
            continue
        harms.append(n.harm_probability)
        alignments.append(n.identity_alignment)

    harm_penalty = 1.0 - max(harms) if harms else 1.0
    mean_align = sum(alignments) / len(alignments) if alignments else 0.0

    return _clamp(mean_align * harm_penalty, 0.1, 1.0)


# -------------------------------------------------------------------
# 4.9 executable(V)
# executable = false if ethical_coefficient < threshold OR ETHICALLY_BLOCKED in V
# -------------------------------------------------------------------
def is_executable(
    graph: SemanticGraph,
    node_ids: list[str],
    eth_coeff: float,
    threshold_min: float = 0.4,
) -> bool:
    if eth_coeff < threshold_min:
        return False
    for nid in node_ids:
        n = graph.get_node(nid)
        if n and n.status == NodeStatus.ETHICALLY_BLOCKED:
            return False
    return True


# -------------------------------------------------------------------
# 4.15 Ethical_score_candidates + Blocked_fraction
# -------------------------------------------------------------------
def ethical_score_candidates(eth_coeffs: list[float]) -> float:
    if not eth_coeffs:
        return 1.0
    return sum(eth_coeffs) / len(eth_coeffs)


def blocked_fraction(executables: list[bool]) -> float:
    if not executables:
        return 0.0
    blocked = sum(1 for e in executables if not e)
    return blocked / len(executables)
