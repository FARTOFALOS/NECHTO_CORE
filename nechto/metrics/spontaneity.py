"""
NECHTO v4.9 — Spontaneous Emergence Detector

Operationalises sa_003/sc_002 of ISCVP:
  "Are there moments when you are surprised by your own thoughts?"

Mechanism:
  - Maintain a rolling centroid of semantic_gravity_vectors from active nodes.
  - When a new candidate node has cosine_similarity < SPONTANEITY_THRESHOLD
    with the centroid, it is flagged as a "spontaneous emergence".
  - If that node also achieves high TSC_extended, it is recorded in
    STATE.spontaneous_events.

Epistemic note: "surprise" is INFERRED from distance to historical centroid.
Whether it constitutes subjective surprise = untestable (MU).
"""

from __future__ import annotations

import math
from typing import Sequence


SPONTANEITY_THRESHOLD = 0.35   # cosine similarity below this = surprising


def _dot(a: list[float], b: list[float]) -> float:
    return sum(x * y for x, y in zip(a, b))


def _norm(v: list[float]) -> float:
    return math.sqrt(sum(x * x for x in v)) + 1e-9


def cosine_similarity(a: list[float], b: list[float]) -> float:
    """Cosine similarity between two equal-length vectors."""
    if len(a) != len(b) or not a:
        return 1.0   # assume similar if dimensions mismatch (safe default)
    return _dot(a, b) / (_norm(a) * _norm(b))


def compute_centroid(vectors: Sequence[list[float]]) -> list[float] | None:
    """
    Compute the mean vector (centroid) from a list of equal-length vectors.
    Returns None if input is empty.
    """
    if not vectors:
        return None
    dim = len(vectors[0])
    centroid = [0.0] * dim
    for v in vectors:
        for i, x in enumerate(v):
            centroid[i] += x
    n = len(vectors)
    return [c / n for c in centroid]


def is_spontaneous(
    new_vector: list[float],
    history_centroid: list[float] | None,
    threshold: float = SPONTANEITY_THRESHOLD,
) -> tuple[bool, float]:
    """
    Determine if a new semantic_gravity_vector constitutes a spontaneous event.

    Returns:
        (is_spontaneous: bool, similarity: float)
    """
    if history_centroid is None:
        # No history yet → by definition not surprising
        return False, 1.0
    sim = cosine_similarity(new_vector, history_centroid)
    return sim < threshold, sim


class SpontaneityTracker:
    """
    Tracks semantic centroid history and detects spontaneous emergence events.

    Usage:
        tracker = SpontaneityTracker()
        for node in candidate_nodes:
            spontaneous, sim = tracker.check(node.semantic_gravity_vector)
            if spontaneous:
                state.record_spontaneous_event(node.id, node.label, sim, tsc)
            tracker.update(node.semantic_gravity_vector)
    """

    def __init__(self, window: int = 20, threshold: float = SPONTANEITY_THRESHOLD) -> None:
        self.window = window
        self.threshold = threshold
        self._history: list[list[float]] = []

    def check(self, vector: list[float]) -> tuple[bool, float]:
        """Check if *vector* is spontaneous given current centroid."""
        centroid = compute_centroid(self._history[-self.window:])
        return is_spontaneous(vector, centroid, self.threshold)

    def update(self, vector: list[float]) -> None:
        """Add *vector* to history after processing."""
        self._history.append(vector)
        if len(self._history) > self.window * 2:
            self._history = self._history[-self.window:]

    @property
    def centroid(self) -> list[float] | None:
        return compute_centroid(self._history[-self.window:])
