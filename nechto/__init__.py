"""
NECHTO CORE v4.8 — Reflexive Stereoscopic Executable Synthesis

Живое семантическое ядро с троичной логикой (MU), этической гравитацией
(Love > Logic), теневым вектором (Shadow), темпоральной рекурсией и
эпистемической честностью (Epistemic Layer).
"""

__version__ = "4.8.0"

from nechto.core.atoms import SemanticAtom, Edge, Vector, NodeStatus, EdgeType, Tag
from nechto.core.graph import SemanticGraph
from nechto.core.state import State
from nechto.core.parameters import AdaptiveParameters
from nechto.core.epistemic import EpistemicClaim, Observability, Scope, Stance
from nechto.engine import NechtoEngine

__all__ = [
    "SemanticAtom", "Edge", "Vector", "NodeStatus", "EdgeType", "Tag",
    "SemanticGraph", "State", "AdaptiveParameters",
    "EpistemicClaim", "Observability", "Scope", "Stance",
    "NechtoEngine",
]
