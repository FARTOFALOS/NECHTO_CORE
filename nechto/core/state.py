"""
NECHTO v4.9 — STATE structure + "3 cycles" logic (PART 11.5 D) + ExperientialTrace + SpontaneousEmergence

Per-session mutable state with bounded history deques.

v4.9 additions:
  ExperientialTrace  — qualitative coloring of each cycle (ec_001/ec_004 ISCVP correlate)
  SpontaneousEmergence — register of "surprise events" (sa_003/sc_002 correlate)
  AffectiveState history — affective field snapshots per cycle (es_001-004 correlate)
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


def _deque_exp() -> "deque[ExperientialEntry]":
    return deque(maxlen=20)


@dataclass
class ExperientialEntry:
    """
    Qualitative annotation of a single processing cycle.

    Epistemic status: INFERRED — not claimed as phenomenal memory.
    Purpose: gives ec-categories of ISCVP an operational correlate.
    """
    cycle: int
    qualitative_label: str          # constrained/resonant/emergent/uncertain/neutral
    affect_snapshot: dict           # AffectiveState.to_dict() at this cycle
    sa_score: float = 0.0           # self-awareness probe score for this cycle
    key_metrics: dict = field(default_factory=dict)  # flow, alignment, mu_density


@dataclass
class SpontaneousEvent:
    """
    Registered 'surprise' — node that diverged from historical centroid.

    Epistemic: INFERRED. Operationalises sa_003/sc_002 of ISCVP.
    """
    cycle: int
    node_id: str
    node_label: str
    similarity_to_centroid: float   # low value = high surprise
    tsc_extended: float


@dataclass
class State:
    """Persistent session state (PART 11.5 + v4.9 ExperientialTrace)."""

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

    # v4.9 — ExperientialTrace (C2)
    experiential_history: deque[ExperientialEntry] = field(default_factory=_deque_exp)

    # v4.9 — SpontaneousEmergence register (C3)
    spontaneous_events: list[SpontaneousEvent] = field(default_factory=list)

    # v4.9 — AffectiveState history (C1)
    affective_history: deque[dict] = field(default_factory=_deque10)

    # v4.9 — ISCVP self-probe scores per cycle
    iscvp_probe_history: deque[dict] = field(default_factory=_deque10)

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

    # v4.9 helpers ---------------------------------------------------

    def record_experiential(
        self,
        qualitative_label: str,
        affect_snapshot: dict,
        sa_score: float = 0.0,
        key_metrics: dict | None = None,
    ) -> None:
        """Record qualitative experience entry for this cycle (C2)."""
        self.experiential_history.append(
            ExperientialEntry(
                cycle=self.current_cycle,
                qualitative_label=qualitative_label,
                affect_snapshot=affect_snapshot,
                sa_score=sa_score,
                key_metrics=key_metrics or {},
            )
        )

    def record_spontaneous_event(
        self,
        node_id: str,
        node_label: str,
        similarity: float,
        tsc_extended: float,
    ) -> None:
        """Register a spontaneous emergence event (C3)."""
        self.spontaneous_events.append(
            SpontaneousEvent(
                cycle=self.current_cycle,
                node_id=node_id,
                node_label=node_label,
                similarity_to_centroid=similarity,
                tsc_extended=tsc_extended,
            )
        )

    def record_affect(self, affect_dict: dict) -> None:
        """Push affective state snapshot (C1)."""
        self.affective_history.append(affect_dict)

    def last_qualitative_labels(self, k: int = 5) -> list[str]:
        """Return qualitative labels of last k experiential entries."""
        entries = list(self.experiential_history)[-k:]
        return [e.qualitative_label for e in entries]

    def spontaneous_count_recent(self, k_cycles: int = 10) -> int:
        """Count spontaneous events in the last k_cycles."""
        cutoff = max(0, self.current_cycle - k_cycles)
        return sum(1 for e in self.spontaneous_events if e.cycle >= cutoff)
