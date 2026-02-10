"""
NECHTO v4.8 — STATE structure + "3 cycles" logic (PART 11.5 D)

Per-session mutable state with bounded history deques.
"""

from __future__ import annotations

from collections import deque
from dataclasses import dataclass, field
from typing import Any


def _deque10() -> deque[float]:
    return deque(maxlen=10)


def _deque5() -> deque[Any]:
    return deque(maxlen=5)


def _deque20() -> deque[str]:
    return deque(maxlen=20)


@dataclass
class State:
    """Persistent session state (PART 11.5)."""

    alignment_history: deque[float] = field(default_factory=_deque10)
    gap_max_history: deque[float] = field(default_factory=_deque10)
    mu_density_history: deque[float] = field(default_factory=_deque10)
    flow_history: deque[float] = field(default_factory=_deque10)
    chosen_vectors: deque[str] = field(default_factory=_deque20)

    # Epistemic claims accumulated over cycles
    epistemic_claims: list[dict[str, Any]] = field(default_factory=list)

    # Adaptive parameter traces: list[(value, cycle_id)]
    alpha_history: list[tuple[float, int]] = field(default_factory=list)
    gamma_history: list[tuple[float, int]] = field(default_factory=list)
    lambda_history: list[tuple[float, int]] = field(default_factory=list)
    beta_retro_history: list[tuple[float, int]] = field(default_factory=list)

    # Fail history: list[(code, cycle_id, action, outcome)]
    fail_history: list[tuple[str, int, str, str]] = field(default_factory=list)

    # Shadow nodes
    shadow_nodes_history: deque[list[str]] = field(default_factory=_deque5)

    # Success difficulty for current_skill tracking
    success_difficulties: deque[float] = field(default_factory=_deque10)

    current_cycle: int = 0

    # -------------------------------------------------------------- helpers
    @staticmethod
    def sustained(history: deque[float], cmp: str, threshold: float, k: int = 3) -> bool:
        """
        SUSTAINED(history, cmp, thr, k=3):
        True when the last *k* values all satisfy *cmp* w.r.t. *threshold*.
        """
        if len(history) < k:
            return False
        recent = list(history)[-k:]
        if cmp == "<":
            return all(v < threshold for v in recent)
        elif cmp == ">":
            return all(v > threshold for v in recent)
        elif cmp == "<=":
            return all(v <= threshold for v in recent)
        elif cmp == ">=":
            return all(v >= threshold for v in recent)
        return False

    def record_cycle(
        self,
        alignment: float,
        gap_max: float,
        mu_density: float,
        flow_val: float,
        chosen_vector_id: str | None = None,
    ) -> None:
        """Convenience: push one cycle's data into all histories."""
        self.alignment_history.append(alignment)
        self.gap_max_history.append(gap_max)
        self.mu_density_history.append(mu_density)
        self.flow_history.append(flow_val)
        if chosen_vector_id:
            self.chosen_vectors.append(chosen_vector_id)
        self.current_cycle += 1

    def record_fail(self, code: str, action: str, outcome: str) -> None:
        self.fail_history.append((code, self.current_cycle, action, outcome))
