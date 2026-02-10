"""
NECHTO v4.8 — Fail Codes catalog (PART 8)

Structured definitions for all FAIL codes with causes and next steps.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum, auto


class FailCode(Enum):
    FAIL_ETHICAL_COLLAPSE = auto()
    FAIL_ETHICAL_STALL = auto()
    FAIL_PARADOX_OVERLOAD = auto()
    FAIL_SHADOW_AVOIDANCE_CRITICAL = auto()
    FAIL_FLOW_IMPOSSIBLE = auto()
    FAIL_STEREOSCOPIC_MISMATCH = auto()
    FAIL_VECTOR_DECOHERENCE = auto()
    FAIL_TEMPORAL_COLLAPSE = auto()
    FAIL_OPERATIONALIZATION_MISSING = auto()


FAIL_DESCRIPTIONS: dict[FailCode, dict[str, str]] = {
    FailCode.FAIL_ETHICAL_COLLAPSE: {
        "cause": "Ethical_score_candidates < 0.4",
        "next": "Reformulate task within non-harm boundaries; propose high-ethics vectors.",
    },
    FailCode.FAIL_ETHICAL_STALL: {
        "cause": "Blocked_fraction > 0.6",
        "next": "Narrow space, replace candidates, reduce risk/harm potential.",
    },
    FailCode.FAIL_PARADOX_OVERLOAD: {
        "cause": "Mu_density > 0.3",
        "next": "QMM_PARADOX_COLLAPSE / simplification.",
    },
    FailCode.FAIL_SHADOW_AVOIDANCE_CRITICAL: {
        "cause": "shadow_magnitude > 0.7 and SCAV_health < 0.3",
        "next": "Request consent for shadow exploration or change vector.",
    },
    FailCode.FAIL_FLOW_IMPOSSIBLE: {
        "cause": "FLOW < 0.1 (5 cycles)",
        "next": "Pause / change activity / change difficulty.",
    },
    FailCode.FAIL_STEREOSCOPIC_MISMATCH: {
        "cause": "alignment < 0.3 or gap_max > 1.5 sustained, without integration",
        "next": "Activate M29 (MU), propose third integrating vector.",
    },
    FailCode.FAIL_VECTOR_DECOHERENCE: {
        "cause": "CI/consistency below threshold",
        "next": "Vector stabilization or reassembly.",
    },
    FailCode.FAIL_TEMPORAL_COLLAPSE: {
        "cause": "TI low / FP unreliable / chaotic bifurcations",
        "next": "Lower temporal_resolution, narrow horizon, update candidates.",
    },
    FailCode.FAIL_OPERATIONALIZATION_MISSING: {
        "cause": "Runnable definitions A–E missing for gate-critical metrics",
        "next": "Connect PART 11 REFERENCE IMPLEMENTATION or mark SIMULATION_ONLY.",
    },
}


def get_fail_description(code: str) -> dict[str, str]:
    """Look up a fail code by its string name."""
    try:
        fc = FailCode[code]
        return FAIL_DESCRIPTIONS.get(fc, {"cause": "unknown", "next": "diagnose and propose ONE_STEP"})
    except KeyError:
        return {"cause": code, "next": "diagnose and propose ONE_STEP"}
