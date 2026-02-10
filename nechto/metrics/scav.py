"""
NECHTO v4.8 — SCAV 5D metrics (PARTS 4.6–4.8, 4.12)

direction, magnitude, consistency, resonance, shadow — raw + normalized.
attention_entropy, shadow_magnitude, SCAV_health.
"""

from __future__ import annotations

import math
from typing import Sequence

from nechto.core.atoms import SemanticAtom, AvoidedMarker, NodeStatus
from nechto.core.graph import SemanticGraph
from nechto.space.semantic_space import normalize, norm, negate, EPS


def _clamp(v: float, lo: float = 0.0, hi: float = 1.0) -> float:
    return max(lo, min(hi, v))


# -------------------------------------------------------------------
# Weighted gravity: w_i = TSC_base(i) / Σ TSC_base(j)
# -------------------------------------------------------------------
def compute_weights(tsc_values: dict[str, float]) -> dict[str, float]:
    total = sum(tsc_values.values())
    if total < EPS:
        n = len(tsc_values)
        return {k: 1.0 / max(1, n) for k in tsc_values}
    return {k: v / total for k, v in tsc_values.items()}


# -------------------------------------------------------------------
# 4.6 raw_direction
# raw_direction(V,t) = Σ[w_i × semantic_gravity_vector(i)]
# -------------------------------------------------------------------
def raw_direction(
    graph: SemanticGraph,
    node_ids: list[str],
    weights: dict[str, float],
) -> list[float]:
    dim = 12
    result = [0.0] * dim
    for nid in node_ids:
        n = graph.get_node(nid)
        if n is None:
            continue
        w = weights.get(nid, 0.0)
        sgv = n.semantic_gravity_vector()
        for d in range(dim):
            result[d] += w * sgv[d]
    return result


# -------------------------------------------------------------------
# 4.6 shadow raw + normalized
# shadow_gate(i) = 1 if identity_alignment(i) < 0 OR status(i) = AVOIDED else 0
# s_i = norm_weight(i) × shadow_gate(i)
# raw_shadow = Σ[s_i × (-semantic_gravity_vector(i))]
# -------------------------------------------------------------------
def shadow_gate(atom: SemanticAtom) -> float:
    if atom.identity_alignment < 0:
        return 1.0
    if atom.avoided_marker == AvoidedMarker.AVOIDED:
        return 1.0
    return 0.0


def raw_shadow(
    graph: SemanticGraph,
    node_ids: list[str],
    weights: dict[str, float],
) -> list[float]:
    dim = 12
    result = [0.0] * dim
    for nid in node_ids:
        n = graph.get_node(nid)
        if n is None:
            continue
        gate = shadow_gate(n)
        if gate == 0.0:
            continue
        w = weights.get(nid, 0.0)
        sgv = n.semantic_gravity_vector()
        neg = negate(sgv)
        for d in range(dim):
            result[d] += w * gate * neg[d]
    return result


# -------------------------------------------------------------------
# 4.6 magnitude
# magnitude(V,t) = GBI_proxy × max_{i∈active}(TSC_base(i,t))
# -------------------------------------------------------------------
def scav_magnitude(gbi: float, tsc_values: dict[str, float]) -> float:
    if not tsc_values:
        return 0.0
    return gbi * max(tsc_values.values())


# -------------------------------------------------------------------
# 4.6 consistency
# consistency = AR_coef(direction_history, lag=5) × focus_stability
# focus_stability = time_on_seed / total_time
# (Simplified: AR_coef ≈ autocorrelation proxy from direction-norm history)
# -------------------------------------------------------------------
def consistency_metric(
    direction_norms: list[float],
    time_on_seed: float = 1.0,
    total_time: float = 1.0,
) -> float:
    focus = time_on_seed / max(total_time, EPS) if total_time > 0 else 1.0
    if len(direction_norms) < 2:
        return _clamp(focus)
    # Lag-1 autocorrelation as AR proxy
    mean_v = sum(direction_norms) / len(direction_norms)
    var = sum((x - mean_v) ** 2 for x in direction_norms)
    if var < EPS:
        return _clamp(focus)
    cov = sum(
        (direction_norms[i] - mean_v) * (direction_norms[i + 1] - mean_v)
        for i in range(len(direction_norms) - 1)
    )
    ar_coef = _clamp(cov / var, 0.0, 1.0)
    return _clamp(ar_coef * focus)


# -------------------------------------------------------------------
# 4.6 resonance
# resonance = resonance_field_strength × bidirectional_attention_ratio
# -------------------------------------------------------------------
def resonance_metric(
    field_strength: float = 0.5,
    bidirectional_ratio: float = 0.5,
) -> float:
    return _clamp(field_strength * bidirectional_ratio)


# -------------------------------------------------------------------
# 4.7 attention_entropy
# p_i = w_i / Σ w_j
# H(p) = - Σ p_i log(p_i)
# attention_entropy = H(p) / log(N_active)  ∈ [0..1]
# if N_active <= 1 → 0
# -------------------------------------------------------------------
def attention_entropy(weights: dict[str, float]) -> float:
    n = len(weights)
    if n <= 1:
        return 0.0
    total = sum(weights.values())
    if total < EPS:
        return 0.0
    probs = [w / total for w in weights.values() if w > 0]
    if not probs:
        return 0.0
    h = -sum(p * math.log(p) for p in probs if p > 0)
    return _clamp(h / math.log(n))


# -------------------------------------------------------------------
# 4.8 shadow_magnitude (RAW-based)
# shadow_magnitude = ||raw_shadow|| / (||raw_direction|| + ||raw_shadow|| + ε)
# -------------------------------------------------------------------
def shadow_magnitude_metric(raw_dir: Sequence[float], raw_shd: Sequence[float]) -> float:
    nd = norm(raw_dir)
    ns = norm(raw_shd)
    return ns / (nd + ns + EPS)


# -------------------------------------------------------------------
# 4.12 SCAV_health
# (consistency × resonance × (1 - attention_entropy) × (1 - shadow_magnitude))^(1/4)
# -------------------------------------------------------------------
def scav_health(
    consistency_val: float,
    resonance_val: float,
    entropy_val: float,
    shadow_mag: float,
) -> float:
    product = (
        max(consistency_val, 0.0)
        * max(resonance_val, 0.0)
        * max(1.0 - entropy_val, 0.0)
        * max(1.0 - shadow_mag, 0.0)
    )
    return product ** 0.25
