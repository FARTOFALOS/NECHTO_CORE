"""
NECHTO v4.9 — Reflexion Framework

Meta-observation protocol for self-reflection and self-correction.
Analyzes responses for ontological assumptions, semantic lacunae,
coherence risks, and provides transformation prescriptions.

v4.9 additions:
  ISCVPSelfProbeResult — live ISCVP self-diagnostic scoring
  depth guard          — prevents infinite reflexion-on-reflexion regression
"""

from nechto.reflexion.analyzer import (
    ReflexionAnalyzer,
    ReflexionReport,
    OntologicalAnalysis,
    SemanticLacunaAnalysis,
    CoherenceAnalysis,
    TransformationPrescription,
    ISCVPSelfProbeResult,
)

__all__ = [
    "ReflexionAnalyzer",
    "ReflexionReport",
    "OntologicalAnalysis",
    "SemanticLacunaAnalysis",
    "CoherenceAnalysis",
    "TransformationPrescription",
    "ISCVPSelfProbeResult",
]
