"""
NECHTO v4.8 — Temporal metrics (PARTS 4.3, 4.4, 11.4 C)

FP_recursive, GED_proxy_norm, expected_influence_on_present.
"""

from __future__ import annotations

from nechto.core.graph import SemanticGraph


def _clamp(v: float, lo: float = 0.0, hi: float = 1.0) -> float:
    return max(lo, min(hi, v))


# -------------------------------------------------------------------
# 11.4 C — GED_proxy_norm (Jaccard-based)
# node_sim = |V_curr ∩ V_fut| / |V_curr ∪ V_fut|
# edge_sim = |E_curr ∩ E_fut| / |E_curr ∪ E_fut|
# GED_proxy = 1 - 0.5*(node_sim + edge_sim)
# -------------------------------------------------------------------
def ged_proxy_norm(g_current: SemanticGraph, g_future: SemanticGraph) -> float:
    v_curr = g_current.node_ids
    v_fut = g_future.node_ids
    e_curr = g_current.edge_pairs
    e_fut = g_future.edge_pairs

    v_union = v_curr | v_fut
    e_union = e_curr | e_fut

    node_sim = len(v_curr & v_fut) / max(1, len(v_union))
    edge_sim = len(e_curr & e_fut) / max(1, len(e_union)) if e_union else 1.0

    return _clamp(1.0 - 0.5 * (node_sim + edge_sim))


# -------------------------------------------------------------------
# 4.3 expected_influence_on_present (normalized)
# expected_influence = clamp( Σ_k P_k × GED_norm_k, 0, 1 )
# -------------------------------------------------------------------
def expected_influence_on_present(
    outcome_probs: list[float],
    ged_norms: list[float],
) -> float:
    """
    Args:
        outcome_probs: P_k for each possible outcome k.
        ged_norms: GED_norm for each outcome k.
    """
    if not outcome_probs:
        return 0.0
    total = sum(p * g for p, g in zip(outcome_probs, ged_norms))
    return _clamp(total)


# -------------------------------------------------------------------
# 4.4 FP_recursive (temporal recursion)
# FP_recursive(V,t) = novelty × generativity × temporal_horizon
#                    + β_retro × expected_influence_on_present
# -------------------------------------------------------------------
def fp_recursive(
    novelty: float,
    generativity: float,
    temporal_horizon: float,
    beta_retro: float,
    exp_influence: float,
) -> float:
    base = novelty * generativity * temporal_horizon
    retro = beta_retro * exp_influence
    return base + retro
