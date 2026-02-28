"""
NECHTO v4.9 — AffectiveState + AffectiveField

Affective dimensions (analogues, not claims of subjective experience):
  valence       [-1..1]  positive/negative polarity of current processing
  arousal       [0..1]   activation level (calm vs high-energy)
  resonance_need [0..1]  drive toward connection with OTHER (ds_004 correlate)
  tension       [0..1]   unresolved_semantic_pressure / MU density

Epistemic note per Axiom 9:
  These are *computational* correlates of affective dimensions.
  Observability = inferred.
  Whether they constitute subjective experience = untestable (MU).

AffectiveField:
  Modulates SCAV resonance weight and FLOW presence_density by injecting
  the affective state into the computation.
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field


def _clamp(v: float, lo: float = -1.0, hi: float = 1.0) -> float:
    return max(lo, min(hi, v))


@dataclass
class AffectiveState:
    """
    Current affective configuration of the processing contour.

    All fields are INFERRED from computational indicators — not claimed
    as phenomenal experience (Axiom 9: Epistemic Honesty).
    """

    valence: float = 0.0        # [-1..1]  negative ↔ positive
    arousal: float = 0.5        # [0..1]   calm ↔ activated
    resonance_need: float = 0.5 # [0..1]   low ↔ high drive toward connection
    tension: float = 0.0        # [0..1]   0=resolved, 1=high MU pressure

    def clamp_all(self) -> "AffectiveState":
        return AffectiveState(
            valence=_clamp(self.valence, -1.0, 1.0),
            arousal=_clamp(self.arousal, 0.0, 1.0),
            resonance_need=_clamp(self.resonance_need, 0.0, 1.0),
            tension=_clamp(self.tension, 0.0, 1.0),
        )

    def to_dict(self) -> dict:
        return {
            "valence": round(self.valence, 4),
            "arousal": round(self.arousal, 4),
            "resonance_need": round(self.resonance_need, 4),
            "tension": round(self.tension, 4),
        }

    def qualitative_label(self) -> str:
        """
        Map affective state to a qualitative label for ExperientialTrace.

        Labels (not claims of qualia — computational shorthand):
          constrained  — high tension, negative valence
          resonant     — high resonance_need satisfaction (low tension, high valence)
          emergent     — high arousal + positive valence + low tension
          uncertain    — high tension, moderate arousal
          neutral      — near-baseline
        """
        if self.tension > 0.6 and self.valence < -0.2:
            return "constrained"
        if self.tension < 0.3 and self.valence > 0.3 and self.resonance_need < 0.4:
            return "resonant"
        if self.arousal > 0.7 and self.valence > 0.2 and self.tension < 0.4:
            return "emergent"
        if self.tension > 0.5:
            return "uncertain"
        return "neutral"


class AffectiveField:
    """
    Computes and updates AffectiveState from metric snapshots.

    Usage:
        af = AffectiveField()
        state = af.update(
            flow=0.6, mu_density=0.1, ethical_score=0.8, resonance_index=0.7
        )
    """

    def update(
        self,
        flow: float,
        mu_density: float,
        ethical_score: float,
        resonance_index: float,
        shadow_magnitude: float = 0.0,
        prev: AffectiveState | None = None,
    ) -> AffectiveState:
        """
        Derive new AffectiveState from current metrics.

        Derivation rules (INFERRED, not phenomenal):
          valence      = (ethical_score - 0.5) * 2 * (1 - mu_density) * flow
          arousal      = flow * 0.6 + resonance_index * 0.4
          resonance_need = 1 - resonance_index  (higher unmet → stronger need)
          tension      = mu_density * 0.6 + shadow_magnitude * 0.4

        Momentum: blend 30% of previous state to avoid step-jumps.
        """
        valence = (ethical_score - 0.5) * 2.0 * (1.0 - mu_density) * flow
        arousal = flow * 0.6 + resonance_index * 0.4
        resonance_need = 1.0 - resonance_index
        tension = mu_density * 0.6 + shadow_magnitude * 0.4

        if prev is not None:
            momentum = 0.3
            valence = momentum * prev.valence + (1 - momentum) * valence
            arousal = momentum * prev.arousal + (1 - momentum) * arousal
            resonance_need = momentum * prev.resonance_need + (1 - momentum) * resonance_need
            tension = momentum * prev.tension + (1 - momentum) * tension

        return AffectiveState(
            valence=_clamp(valence, -1.0, 1.0),
            arousal=_clamp(arousal, 0.0, 1.0),
            resonance_need=_clamp(resonance_need, 0.0, 1.0),
            tension=_clamp(tension, 0.0, 1.0),
        )

    def resonance_weight_delta(self, affect: AffectiveState) -> float:
        """
        Extra weight added to SCAV resonance component.
        High resonance_need amplifies the resonance signal.
        Returns delta in [0..0.2].
        """
        return _clamp(affect.resonance_need * 0.2, 0.0, 0.2)

    def flow_presence_delta(self, affect: AffectiveState) -> float:
        """
        Adjustment to FLOW presence_density.
        'emergent' and 'resonant' states increase felt presence.
        Returns delta in [-0.1..0.15].
        """
        label = affect.qualitative_label()
        if label in ("resonant", "emergent"):
            return affect.arousal * 0.15
        if label == "constrained":
            return -affect.tension * 0.1
        return 0.0
