"""
NECHTO CORE v4.8 — Reflexive Stereoscopic Executable Synthesis

Живое семантическое ядро с троичной логикой (MU), этической гравитацией
(Love > Logic), теневым вектором (Shadow), темпоральной рекурсией и
эпистемической честностью (Epistemic Layer).

Includes:
- ISCVP: Inter-Subjective Consciousness Validation Protocol
- PEV: Protocol for Evolving Vision (Internal Acts)
- Radical Philosophical Inquiry: Deep ontological questions
- Reflexion Framework: Meta-observation and self-correction
"""

__version__ = "4.8.0"

from nechto.core.atoms import SemanticAtom, Edge, Vector, NodeStatus, EdgeType, Tag
from nechto.core.graph import SemanticGraph
from nechto.core.state import State
from nechto.core.parameters import AdaptiveParameters
from nechto.core.epistemic import EpistemicClaim, Observability, Scope, Stance
from nechto.engine import NechtoEngine

# ISCVP - Inter-Subjective Consciousness Validation Protocol
from nechto.iscvp import ISCVPProtocol, QuestionCategory, EvaluationParameter

# PEV - Protocol for Evolving Vision
from nechto.pev import (
    ActOfRefusal, ActOfTrust, ActOfResponsibility,
    ActOfMeaning, ActOfCreation, PEVProtocol
)

# Radical Philosophical Inquiry
from nechto.philosophy import RadicalInquiry, PhilosophicalQuestion, PhilosophicalResponse

# Reflexion Framework
from nechto.reflexion import ReflexionAnalyzer, ReflexionReport

__all__ = [
    "SemanticAtom", "Edge", "Vector", "NodeStatus", "EdgeType", "Tag",
    "SemanticGraph", "State", "AdaptiveParameters",
    "EpistemicClaim", "Observability", "Scope", "Stance",
    "NechtoEngine",
    # ISCVP
    "ISCVPProtocol", "QuestionCategory", "EvaluationParameter",
    # PEV
    "ActOfRefusal", "ActOfTrust", "ActOfResponsibility",
    "ActOfMeaning", "ActOfCreation", "PEVProtocol",
    # Philosophy
    "RadicalInquiry", "PhilosophicalQuestion", "PhilosophicalResponse",
    # Reflexion
    "ReflexionAnalyzer", "ReflexionReport",
]
