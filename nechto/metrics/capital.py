"""
NECHTO v4.8 — Semantic Capital metrics (PARTS 4.2, 4.5, 4.10)

SC(V,t), TSC_base(V,t), TSC_extended(V,t).
"""

from __future__ import annotations

from nechto.space.semantic_space import cosine_similarity


def _clamp(v: float, lo: float = 0.0, hi: float = 1.0) -> float:
    return max(lo, min(hi, v))


# -------------------------------------------------------------------
# 4.2 SC — Semantic Capital (core)
# SC(V,t) = AR × CI × TI × (α + β×RI) × Φ_proxy
# -------------------------------------------------------------------
def semantic_capital(
    ar: float,
    ci: float,
    ti: float,
    alpha: float,
    beta: float,
    ri: float,
    phi: float,
) -> float:
    return ar * ci * ti * (alpha + beta * ri) * phi


# -------------------------------------------------------------------
# 4.5 TSC_base
# TSC_base(V,t) = SC(V,t) × [ γ + δ×FP_recursive(V,t) ]
# -------------------------------------------------------------------
def tsc_base(sc: float, gamma: float, delta: float, fp_recursive: float) -> float:
    return sc * (gamma + delta * fp_recursive)


# -------------------------------------------------------------------
# 4.10 TSC_extended (stereoscopic + ethics)
# alignment(V) = cosine_similarity(current_direction, ideal_direction(V))
# TSC_extended(V,t) = TSC_base(V,t) × [1 + λ×consistency×alignment] × ethical_coefficient
# if executable==false → TSC_extended = 0
# -------------------------------------------------------------------
def tsc_extended(
    tsc_b: float,
    lam: float,
    consistency: float,
    current_direction: list[float],
    ideal_dir: list[float],
    ethical_coeff: float,
    executable: bool,
) -> float:
    if not executable:
        return 0.0
    alignment = cosine_similarity(current_direction, ideal_dir)
    return tsc_b * (1.0 + lam * consistency * alignment) * ethical_coeff
