# NECHTO v5.0 — Public Surface (Backwards-Compatible Re-Exports)
#
# Goal:
#   Keep stable imports working:
#     from nechto import NechtoEngine, SemanticAtom, Edge, EdgeType, NodeStatus, Tag
#
# Notes:
#   - This file should stay SMALL and stable.
#   - Internal modules may move; update imports here to preserve user code.
#   - Avoid importing heavy modules at import-time if possible.

from __future__ import annotations

# Version (keep)
try:
    from ._version import __version__  # optional if you keep a version module
except Exception:
    try:
        from importlib.metadata import version as _pkg_version

        __version__ = _pkg_version("nechto")
    except Exception:
        __version__ = "0.0.0"

# =========================
# Public API — Engine
# =========================
try:
    # v5 location
    from .api.engine import NechtoEngine
except Exception:
    # v4 fallback (during migration)
    from .engine import NechtoEngine  # type: ignore


# =========================
# Public API — Core Types
# =========================
# Graph/domain types (v5 preferred, v4 fallback)
try:
    from .domain.graph.atom import SemanticAtom
    from .domain.graph.edge import Edge, EdgeType
    from .domain.graph.status import NodeStatus
except Exception:
    # v4 fallback
    from .core.atoms import SemanticAtom, Edge, EdgeType, NodeStatus  # type: ignore

# Tags / enums (wherever you keep them)
try:
    from .domain.graph.atom import Tag  # if Tag is defined alongside SemanticAtom
except Exception:
    try:
        from .core.atoms import Tag  # type: ignore
    except Exception:
        Tag = None  # type: ignore


# =========================
# Optional convenience API
# =========================
# Keep these light: only import if they exist.
try:
    from .api.ingest import process_text
except Exception:
    process_text = None  # type: ignore

try:
    from .api.run import run
except Exception:
    run = None  # type: ignore


__all__ = [
    "__version__",
    "NechtoEngine",
    "SemanticAtom",
    "Edge",
    "EdgeType",
    "NodeStatus",
    "Tag",
    "process_text",
    "run",
]


# =========================
# Legacy public exports (v4 compatibility)
# =========================
try:
    from .core.atoms import Vector
except Exception:
    Vector = None  # type: ignore

try:
    from .core.graph import SemanticGraph
except Exception:
    SemanticGraph = None  # type: ignore

try:
    from .core.state import State
except Exception:
    State = None  # type: ignore

try:
    from .core.parameters import AdaptiveParameters
except Exception:
    AdaptiveParameters = None  # type: ignore

try:
    from .core.epistemic import EpistemicClaim, Observability, Scope, Stance
except Exception:
    EpistemicClaim = Observability = Scope = Stance = None  # type: ignore

try:
    from .iscvp import ISCVPProtocol, QuestionCategory, EvaluationParameter
except Exception:
    ISCVPProtocol = QuestionCategory = EvaluationParameter = None  # type: ignore

try:
    from .pev import (
        ActOfRefusal,
        ActOfTrust,
        ActOfResponsibility,
        ActOfMeaning,
        ActOfCreation,
        PEVProtocol,
    )
except Exception:
    ActOfRefusal = ActOfTrust = ActOfResponsibility = None  # type: ignore
    ActOfMeaning = ActOfCreation = PEVProtocol = None  # type: ignore

try:
    from .philosophy import RadicalInquiry, PhilosophicalQuestion, PhilosophicalResponse
except Exception:
    RadicalInquiry = PhilosophicalQuestion = PhilosophicalResponse = None  # type: ignore

try:
    from .reflexion import ReflexionAnalyzer, ReflexionReport
except Exception:
    ReflexionAnalyzer = ReflexionReport = None  # type: ignore

try:
    from .llm_bridge import LLMBridge
except Exception:
    LLMBridge = None  # type: ignore

__all__.extend(
    [
        "Vector",
        "SemanticGraph",
        "State",
        "AdaptiveParameters",
        "EpistemicClaim",
        "Observability",
        "Scope",
        "Stance",
        "ISCVPProtocol",
        "QuestionCategory",
        "EvaluationParameter",
        "ActOfRefusal",
        "ActOfTrust",
        "ActOfResponsibility",
        "ActOfMeaning",
        "ActOfCreation",
        "PEVProtocol",
        "RadicalInquiry",
        "PhilosophicalQuestion",
        "PhilosophicalResponse",
        "ReflexionAnalyzer",
        "ReflexionReport",
        "LLMBridge",
    ]
)
