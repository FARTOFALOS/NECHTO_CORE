"""
NECHTO v4.8 — Semantic Atoms, Edges, Vectors (PART 3)

Canonical data structures: SEMANTIC_ATOM, EDGE, VECTOR.
"""

from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Optional


# ---------------------------------------------------------------------------
# 3.1 Node status
# ---------------------------------------------------------------------------
class NodeStatus(Enum):
    ANCHORED = auto()
    FLOATING = auto()
    HYPOTHESIS = auto()
    BLOCKING = auto()
    MU = auto()
    ETHICALLY_BLOCKED = auto()


# ---------------------------------------------------------------------------
# Tags
# ---------------------------------------------------------------------------
class Tag(Enum):
    WITNESS = auto()
    EMOTION = auto()
    INTENT = auto()
    HARM = auto()
    MANIPULATION = auto()
    DECEPTION = auto()
    BOUNDARY = auto()


# ---------------------------------------------------------------------------
# Avoided marker
# ---------------------------------------------------------------------------
class AvoidedMarker(Enum):
    NONE = auto()
    AVOIDED = auto()
    RESPECTED_BOUNDARY = auto()


# ---------------------------------------------------------------------------
# 3.1 SEMANTIC_ATOM
# ---------------------------------------------------------------------------
@dataclass
class Evidence:
    """Epistemic provenance of a node."""
    in_contour_observed: list[str] = field(default_factory=list)
    inferences: list[str] = field(default_factory=list)
    assumptions: list[str] = field(default_factory=list)


@dataclass
class SemanticAtom:
    """Minimal semantic unit with status, valence, ethics, connectivity."""

    label: str
    id: str = field(default_factory=lambda: uuid.uuid4().hex[:12])
    status: NodeStatus = NodeStatus.FLOATING
    identity_alignment: float = 0.0          # [-1..1]
    harm_probability: float = 0.0            # [0..1]
    tags: list[Tag] = field(default_factory=list)
    avoided_marker: AvoidedMarker = AvoidedMarker.NONE
    evidence: Evidence = field(default_factory=Evidence)

    # --- R^12 semantic-gravity axes (PART 11.1) ---
    clarity: float = 0.5
    harm: float = 0.0
    empathy: float = 0.5
    agency: float = 0.0
    uncertainty: float = 0.5
    novelty: float = 0.5
    coherence: float = 0.5
    practicality: float = 0.5
    temporality: float = 0.0
    boundary: float = 0.5
    resonance: float = 0.5
    shadow: float = 0.0

    # --- computed (set externally) ---
    _harm_computed: Optional[float] = field(default=None, repr=False)
    _alignment_computed: Optional[float] = field(default=None, repr=False)

    def semantic_gravity_vector(self) -> list[float]:
        """Return the 12-D gravity vector for this atom (PART 11.1 A)."""
        return [
            self.clarity,
            self.harm,
            self.empathy,
            self.agency,
            self.uncertainty,
            self.novelty,
            self.coherence,
            self.practicality,
            self.temporality,
            self.boundary,
            self.resonance,
            self.shadow,
        ]


# ---------------------------------------------------------------------------
# 3.2 EDGE
# ---------------------------------------------------------------------------
class EdgeType(Enum):
    SUPPORTS = auto()
    CONTRASTS = auto()
    MUTEX = auto()
    CAUSES = auto()
    BRIDGES = auto()
    RESONATES = auto()


@dataclass
class Edge:
    """Directed typed edge with weight."""
    from_id: str
    to_id: str
    type: EdgeType = EdgeType.SUPPORTS
    weight: float = 1.0


# ---------------------------------------------------------------------------
# 3.3 VECTOR (Attention Vector)
# ---------------------------------------------------------------------------
@dataclass
class Vector:
    """Attention trajectory: seed → expansion, evaluated by TSC/SCAV/ETHICS/FLOW."""

    id: str = field(default_factory=lambda: uuid.uuid4().hex[:12])
    seed_nodes: list[str] = field(default_factory=list)
    nodes: list[str] = field(default_factory=list)
    edges: list[Edge] = field(default_factory=list)
    executable: bool = True

    # Metrics (populated during evaluation)
    tsc_base: float = 0.0
    tsc_extended: float = 0.0
    ethical_coefficient: float = 1.0
    scav_magnitude: float = 0.0
    scav_health: float = 0.0
    flow_score: float = 0.0
    alignment_score: float = 0.0
    stereoscopic_alignment: float = 0.0
    stereoscopic_gap: float = 0.0

    # SCAV 5D raw
    direction_raw: list[float] = field(default_factory=list)
    shadow_raw: list[float] = field(default_factory=list)
    consistency: float = 0.0
    resonance_score: float = 0.0

    def __hash__(self) -> int:
        return hash(self.id)
