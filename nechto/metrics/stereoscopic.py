"""
NECHTO v4.8 — Stereoscopic alignment + gap (PART 4.13)

Rank alignment and amplitude gap between TSC and SCAV evaluations.
"""

from __future__ import annotations

from statistics import mean, stdev


def _clamp(v: float, lo: float = 0.0, hi: float = 1.0) -> float:
    return max(lo, min(hi, v))


def _rank(values: list[float]) -> list[int]:
    """Return 0-based ranks (highest value → rank 0)."""
    indexed = sorted(enumerate(values), key=lambda x: -x[1])
    ranks = [0] * len(values)
    for rank, (idx, _) in enumerate(indexed):
        ranks[idx] = rank
    return ranks


# -------------------------------------------------------------------
# 4.13 Stereoscopic_alignment (rank-based)
# Stereoscopic_alignment = 1 - |rank_TSC(V) - rank_SCAV(V)| / (n - 1)
# -------------------------------------------------------------------
def stereoscopic_alignment(rank_tsc: int, rank_scav: int, n_vectors: int) -> float:
    if n_vectors <= 1:
        return 1.0
    return 1.0 - abs(rank_tsc - rank_scav) / (n_vectors - 1)


# -------------------------------------------------------------------
# 4.13 Stereoscopic_gap (amplitude-based, z-score)
# zA = (A - mean(A)) / std(A)
# zB = (B - mean(B)) / std(B)
# gap(V) = |zA - zB|
# gap_max = max gap(V)
# -------------------------------------------------------------------
def _z_scores(values: list[float]) -> list[float]:
    if len(values) < 2:
        return [0.0] * len(values)
    m = mean(values)
    s = stdev(values)
    if s < 1e-9:
        return [0.0] * len(values)
    return [(v - m) / s for v in values]


def stereoscopic_gaps(
    tsc_values: list[float],
    scav_values: list[float],
) -> list[float]:
    """Return per-vector stereoscopic gap."""
    za = _z_scores(tsc_values)
    zb = _z_scores(scav_values)
    return [abs(a - b) for a, b in zip(za, zb)]


def stereoscopic_gap_max(tsc_values: list[float], scav_values: list[float]) -> float:
    gaps = stereoscopic_gaps(tsc_values, scav_values)
    return max(gaps) if gaps else 0.0


# -------------------------------------------------------------------
# Batch: compute alignment + gap for each vector
# -------------------------------------------------------------------
def compute_stereoscopic_batch(
    tsc_ext_scores: list[float],
    scav_mag_scores: list[float],
) -> tuple[list[float], list[float], float]:
    """
    Returns (alignments, gaps, gap_max).
    """
    n = len(tsc_ext_scores)
    if n == 0:
        return [], [], 0.0

    ranks_tsc = _rank(tsc_ext_scores)
    ranks_scav = _rank(scav_mag_scores)
    alignments = [
        stereoscopic_alignment(rt, rs, n)
        for rt, rs in zip(ranks_tsc, ranks_scav)
    ]
    gaps = stereoscopic_gaps(tsc_ext_scores, scav_mag_scores)
    gmax = max(gaps) if gaps else 0.0
    return alignments, gaps, gmax
