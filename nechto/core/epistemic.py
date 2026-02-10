"""
NECHTO v4.8 — Epistemic Layer (PART 3.6 / APPENDIX E)

Discipline of assertions: observed / inferred / untestable + stance.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum, auto


class Scope(Enum):
    IN_CONTOUR = auto()
    OUT_OF_CONTOUR = auto()


class Observability(Enum):
    OBSERVED = auto()
    INFERRED = auto()
    UNTESTABLE = auto()


class Stance(Enum):
    AFFIRMED = auto()
    DENIED = auto()
    AGNOSTIC = auto()
    MU = auto()


@dataclass
class EpistemicClaim:
    """
    Single epistemic claim (PART 3.6).

    Rules:
    • agnostic: untestable/inferred without sustained indicator conflict
    • MU: untestable + sustained conflict (rank/gap/metrics) ≥ 3 cycles
    • affirmed/denied allowed ONLY for observed/inferred with basis
    """

    topic: str
    scope: Scope = Scope.IN_CONTOUR
    observability: Observability = Observability.INFERRED
    stance: Stance = Stance.AGNOSTIC
    reason: str = ""
    linked_nodes: list[str] = field(default_factory=list)
    cycle_id: int = 0

    def validate(self) -> bool:
        """
        APPENDIX E rule 2:
        If observability == UNTESTABLE, stance may only be AGNOSTIC or MU.
        """
        if self.observability == Observability.UNTESTABLE:
            return self.stance in (Stance.AGNOSTIC, Stance.MU)
        return True

    def as_dict(self) -> dict:
        return {
            "topic": self.topic,
            "scope": self.scope.name.lower(),
            "observability": self.observability.name.lower(),
            "stance": self.stance.name.lower(),
            "reason": self.reason,
            "linked_nodes": self.linked_nodes,
            "cycle_id": self.cycle_id,
        }
