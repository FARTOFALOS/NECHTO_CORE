"""
NECHTO v4.8 — Adaptive Parameters (PART 3.5)

α, β=1-α, γ, δ=1-γ, λ, β_retro with learning functions.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from statistics import mean
from typing import Any


def _clamp(v: float, lo: float, hi: float) -> float:
    return max(lo, min(hi, v))


@dataclass
class AdaptiveParameters:
    """Mutable adaptive parameters with learning rules."""

    alpha: float = 0.5
    gamma: float = 0.4
    lam: float = 0.8          # λ in spec
    beta_retro: float = 0.2

    trace: dict[str, int] = field(default_factory=lambda: {
        "alpha": 0, "gamma": 0, "lam": 0, "beta_retro": 0,
    })

    # ----- derived
    @property
    def beta(self) -> float:
        return 1.0 - self.alpha

    @property
    def delta(self) -> float:
        return 1.0 - self.gamma

    # ----- learning functions (PART 3.5)
    def f_alpha(self, ri_history: list[float], cycle: int) -> None:
        """Moving average of impact of RI, window=10."""
        window = ri_history[-10:]
        if window:
            self.alpha = _clamp(mean(window), 0.0, 1.0)
            self.trace["alpha"] = cycle

    def f_gamma(self, urgency_score: float, cycle: int) -> None:
        self.gamma = _clamp(0.2 + 0.6 * urgency_score, 0.2, 0.8)
        self.trace["gamma"] = cycle

    def f_lambda(self, effect: float, cycle: int) -> None:
        self.lam = _clamp(self.lam + 0.1 * (effect - 0.5), 0.5, 1.0)
        self.trace["lam"] = cycle

    def f_retro(self, observed: float, max_effects: float, cycle: int) -> None:
        if max_effects > 0:
            self.beta_retro = _clamp(observed / max_effects, 0.0, 0.5)
        self.trace["beta_retro"] = cycle

    def snapshot(self) -> dict[str, Any]:
        return {
            "alpha": round(self.alpha, 4),
            "beta": round(self.beta, 4),
            "gamma": round(self.gamma, 4),
            "delta": round(self.delta, 4),
            "lam": round(self.lam, 4),
            "beta_retro": round(self.beta_retro, 4),
            "trace": dict(self.trace),
        }
