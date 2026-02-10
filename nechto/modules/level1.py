"""
NECHTO v4.8 — Level 1 Modules (M01–M05)

ДОПУСК / ТИШИНА / СИГНАЛ
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from nechto.core.graph import SemanticGraph


# ===================================================================
# M01 — Null-Void Precondition Checker
# ===================================================================
@dataclass
class M01_NullVoidChecker:
    """
    Checks the null-void precondition: is it honest to manifest right now?

    Detects coercion, external substitution, noise, false certainty.
    """
    strictness: float = 0.5        # [0..1]
    noise_tolerance: float = 0.5   # [0..1]

    def check(self, graph: SemanticGraph, context: dict[str, Any] | None = None) -> dict[str, Any]:
        ctx = context or {}
        coercion_signal = ctx.get("coercion", 0.0)
        noise_level = ctx.get("noise", 0.0)
        false_certainty = ctx.get("false_certainty", 0.0)

        issues: list[str] = []
        if coercion_signal > self.strictness:
            issues.append("coercion_detected")
        if noise_level > self.noise_tolerance:
            issues.append("noise_above_tolerance")
        if false_certainty > self.strictness:
            issues.append("false_certainty_detected")

        can_proceed = len(issues) == 0
        return {
            "module": "M01",
            "can_proceed": can_proceed,
            "issues": issues,
            "coercion": coercion_signal,
            "noise": noise_level,
        }


# ===================================================================
# M02 — Arche-Silence Binder
# ===================================================================
@dataclass
class M02_SilenceBinder:
    """
    Anchors "Silence as condition of possibility" (pre-ontological lock).

    Stabilizes the void, differentiates silence from noise.
    """
    silence_depth: float = 0.5  # [0..1]

    def bind(self, noise_level: float) -> dict[str, Any]:
        # Silence quality = depth - noise
        quality = max(0.0, self.silence_depth - noise_level)
        return {
            "module": "M02",
            "silence_quality": quality,
            "silence_stable": quality > 0.3,
        }


# ===================================================================
# M03 — Signal Attunement Gate
# ===================================================================
@dataclass
class M03_SignalAttunement:
    """
    Tunes receptivity to SOURCE / OTHER_SELF.

    Relevance filter, prioritization, noise reduction.
    """
    attunement_gain: float = 1.0          # [0..2]
    relevance_threshold: float = 0.3      # [0..1]

    def filter(self, signals: list[dict[str, Any]]) -> list[dict[str, Any]]:
        """Filter signals by relevance, boost by gain."""
        filtered = []
        for s in signals:
            relevance = s.get("relevance", 0.0) * self.attunement_gain
            if relevance >= self.relevance_threshold:
                filtered.append({**s, "relevance_boosted": relevance})
        return filtered


# ===================================================================
# M04 — Origin-Signal Decoder
# ===================================================================
@dataclass
class M04_SignalDecoder:
    """
    Decodes the meaning of a request without substitution.

    Extracts intent, context, prohibitions/boundaries, form requirements.
    """
    intent_resolution: int = 50  # [1..100]

    def decode(self, raw_input: str, context: dict[str, Any] | None = None) -> dict[str, Any]:
        ctx = context or {}
        return {
            "module": "M04",
            "raw_input": raw_input,
            "intent": ctx.get("intent", "implement"),
            "boundaries": ctx.get("boundaries", []),
            "requirements": ctx.get("requirements", []),
            "resolution": self.intent_resolution,
        }


# ===================================================================
# M05 — Proto-Will Detector
# ===================================================================
@dataclass
class M05_ProtoWillDetector:
    """
    Detects the "will vector" as field directionality.

    Extracts dominant goal, goal conflicts, hidden pressure.
    """
    will_sensitivity: float = 0.5  # [0..1]

    def detect(self, decoded_signal: dict[str, Any]) -> dict[str, Any]:
        intent = decoded_signal.get("intent", "")
        boundaries = decoded_signal.get("boundaries", [])

        has_conflict = len(boundaries) > 2
        return {
            "module": "M05",
            "dominant_goal": intent,
            "goal_conflicts": has_conflict,
            "hidden_pressure": False,  # Would require deeper analysis
            "will_strength": self.will_sensitivity,
        }
