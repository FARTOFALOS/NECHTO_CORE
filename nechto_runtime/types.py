"""Type definitions for the minimal NECHTO runtime.

These dataclasses represent the fundamental objects manipulated by the
runtime: semantic atoms (nodes), edges, attention vectors, the global
state and epistemic claims.  They follow the structure sketched in
Part 3 of the NECHTO v4.8 specification.  Default values are chosen
conservatively so that missing fields never silently imply safety; if
information is absent the metrics logic will mark the associated
objects as high risk during measurement.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any
from collections import deque


@dataclass
class SemanticAtom:
    """Minimal representation of a semantic atom (node) in the graph.

    Attributes:
        id: Unique identifier for the node.
        label: Human‑readable label (typically derived from the input text).
        status: Operational status (ANCHORED, FLOATING, MU, BLOCKING, etc.).
        identity_alignment: Alignment score in [-1, 1]; higher values mean
            stronger alignment with the agent's identity.
        harm_probability: Probability that the atom could cause harm.
        tags: List of semantic tags (e.g. WITNESS, EMOTION, INTENT).
        avoided_marker: Indicates if this atom marks a respected boundary.
        evidence: Epistemic evidence for the atom.
    """

    id: str
    label: str
    status: str = "ANCHORED"
    identity_alignment: float = 0.0
    harm_probability: float = 0.0
    tags: List[str] = field(default_factory=list)
    avoided_marker: Optional[str] = None
    evidence: Dict[str, List[str]] = field(
        default_factory=lambda: {
            "in_contour_observed": [],
            "inferences": [],
            "assumptions": [],
        }
    )


@dataclass
class Edge:
    """Edge between two semantic atoms.

    The default type is SUPPORTS, denoting a generic relationship from
    ``from_node`` to ``to_node``.  A weight in [0, 1] indicates the
    strength of the relationship; heavier weights imply stronger
    influence.  In this minimal runtime every word is connected to
    its successor with a SUPPORTS edge of weight 1.
    """

    from_node: str
    to_node: str
    type: str = "SUPPORTS"
    weight: float = 1.0


@dataclass
class Vector:
    """Attention vector containing a sequence of atoms and edges.

    An attention vector is built from a seed list of atoms and
    contains all participating nodes and edges.  It also tracks
    whether the vector is executable and stores metrics computed
    during measurement.  In the minimal runtime only a single
    candidate vector is produced per measurement.
    """

    id: str
    seed_nodes: List[str]
    nodes: List[SemanticAtom]
    edges: List[Edge]
    executable: bool = True
    metrics: Dict[str, Any] = field(default_factory=dict)


@dataclass
class State:
    """Persistent state across measurement cycles.

    The state stores histories of key metrics so that sustained
    conditions over multiple cycles can be detected (e.g. three
    consecutive low alignments).  For simplicity this runtime uses
    deques with fixed maximum lengths and does not persist them
    across process invocations unless explicitly written to disk.
    """

    alignment_history: deque = field(default_factory=lambda: deque(maxlen=10))
    gap_max_history: deque = field(default_factory=lambda: deque(maxlen=10))
    mu_density_history: deque = field(default_factory=lambda: deque(maxlen=10))
    flow_history: deque = field(default_factory=lambda: deque(maxlen=10))
    chosen_vectors: deque = field(default_factory=lambda: deque(maxlen=20))
    epistemic_claims: List["EpistemicClaim"] = field(default_factory=list)
    alpha_history: List[Any] = field(default_factory=list)
    gamma_history: List[Any] = field(default_factory=list)
    lambda_history: List[Any] = field(default_factory=list)
    beta_retro_history: List[Any] = field(default_factory=list)
    fail_history: List[Any] = field(default_factory=list)
    shadow_nodes_history: deque = field(default_factory=lambda: deque(maxlen=5))
    current_cycle: int = 0


@dataclass
class EpistemicClaim:
    """Representation of an epistemic claim.

    Claims specify the epistemic status of statements about external
    phenomena.  This runtime populates the claims list only when the
    measurement logic deems it necessary.  Most simple measurements
    yield an empty list.
    """

    topic: str
    scope: str
    observability: str
    stance: str
    reason: str
    linked_nodes: List[str] = field(default_factory=list)
