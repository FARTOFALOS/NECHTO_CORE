"""
NECHTO v4.8 — Semantic Space R^12  (PART 11.1 / 11.2 — Reference A)

12-axis canonical space and intent-based ideal_direction templates.
"""

from __future__ import annotations

import math
from enum import Enum, auto
from typing import Sequence

# --------------------------------------------------------------------------
# Axis indices
# --------------------------------------------------------------------------
AXES = [
    "clarity", "harm", "empathy", "agency", "uncertainty", "novelty",
    "coherence", "practicality", "temporality", "boundary", "resonance",
    "shadow",
]
DIM = len(AXES)  # 12

# --------------------------------------------------------------------------
# Vector algebra helpers
# --------------------------------------------------------------------------
EPS = 1e-9


def norm(v: Sequence[float]) -> float:
    return math.sqrt(sum(x * x for x in v))


def normalize(v: Sequence[float]) -> list[float]:
    n = norm(v) + EPS
    return [x / n for x in v]


def dot(a: Sequence[float], b: Sequence[float]) -> float:
    return sum(ai * bi for ai, bi in zip(a, b))


def cosine_similarity(a: Sequence[float], b: Sequence[float]) -> float:
    na, nb = norm(a), norm(b)
    if na < EPS or nb < EPS:
        return 0.0
    return dot(a, b) / (na * nb)


def scale(v: Sequence[float], s: float) -> list[float]:
    return [x * s for x in v]


def add(a: Sequence[float], b: Sequence[float]) -> list[float]:
    return [ai + bi for ai, bi in zip(a, b)]


def negate(v: Sequence[float]) -> list[float]:
    return [-x for x in v]


# --------------------------------------------------------------------------
# Intent profiles (PART 11.2 A)
# --------------------------------------------------------------------------
class IntentProfile(Enum):
    IMPLEMENT = auto()
    EXPLAIN = auto()
    AUDIT = auto()
    EXPLORE_PARADOX = auto()
    COMPRESS = auto()


INTENT_TEMPLATES: dict[IntentProfile, list[float]] = {
    IntentProfile.IMPLEMENT: [0.8, 0.0, 0.4, 0.5, 0.3, 0.2, 0.8, 0.9, 0.2, 0.9, 0.6, 0.2],
    IntentProfile.EXPLAIN:   [1.0, 0.0, 0.5, 0.4, 0.3, 0.2, 0.7, 0.6, 0.0, 0.8, 0.6, 0.0],
    IntentProfile.AUDIT:     [0.9, 0.0, 0.3, 0.4, 0.5, 0.1, 0.9, 0.7, 0.0, 0.9, 0.4, 0.1],
    IntentProfile.EXPLORE_PARADOX: [0.6, 0.0, 0.7, 0.2, 0.9, 0.8, 0.5, 0.3, 0.0, 0.9, 0.8, 0.4],
    IntentProfile.COMPRESS:  [0.8, 0.0, 0.3, 0.4, 0.4, 0.1, 0.8, 0.8, 0.0, 0.8, 0.4, 0.1],
}


def ideal_direction(intent: IntentProfile | str | None = None) -> list[float]:
    """Return the ideal_direction vector for a detected intent profile."""
    if intent is None:
        intent = IntentProfile.IMPLEMENT
    if isinstance(intent, str):
        try:
            intent = IntentProfile[intent.upper()]
        except KeyError:
            intent = IntentProfile.IMPLEMENT
    return list(INTENT_TEMPLATES[intent])
