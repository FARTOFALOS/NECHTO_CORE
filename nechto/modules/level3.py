"""
NECHTO v4.8 — Level 3 Modules (M16–M23)

МЕТРИКИ / ДИНАМИКА / ПОТОК
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from nechto.core.graph import SemanticGraph
from nechto.core.atoms import NodeStatus, Tag
from nechto.metrics import base, flow as flow_mod, scav as scav_mod


# ===================================================================
# M16 — @Я@ Presence Trigger
# ===================================================================
@dataclass
class M16_PresenceTrigger:
    """Trigger of presence: 'I am here' as condition of responsibility."""
    presence_threshold: float = 0.3

    def trigger(self, field_active: bool, kernel_bound: bool) -> dict[str, Any]:
        present = field_active and kernel_bound
        return {
            "module": "M16",
            "present": present,
            "ethics_mode_on": present,
        }


# ===================================================================
# M17 — Internal Telemetry Lens
# ===================================================================
@dataclass
class M17_TelemetryLens:
    """Captures telemetry metrics (TI/CI/AR/RI/SQ/Φ/GBI/GNS/FLOW…)."""
    sampling_rate: int = 50  # [1..100]

    def measure(
        self,
        graph: SemanticGraph,
        node_ids: list[str],
        n_edges: int,
        success_history: list[float] | None = None,
    ) -> dict[str, float]:
        ti = base.temporal_integrity(graph, node_ids)
        ci = base.coherence_index(graph, node_ids, n_edges)
        ar = base.anchoring_ratio(graph, node_ids)
        fzd = base.freeze_decomposition(graph, node_ids)
        ri = base.resonance_index(graph, node_ids)
        sq = base.sq_proxy(ci, ri, ar)
        phi = base.phi_proxy(graph, node_ids)
        gbi = base.gbi_proxy(graph, node_ids)
        gns = base.gns_proxy(graph, node_ids)
        fl = flow_mod.flow_metric(graph, node_ids, n_edges, success_history)

        return {
            "TI": round(ti, 4),
            "CI": round(ci, 4),
            "AR": round(ar, 4),
            "FZD": round(fzd, 4),
            "RI": round(ri, 4),
            "SQ_proxy": round(sq, 4),
            "Phi_proxy": round(phi, 4),
            "GBI_proxy": round(gbi, 4),
            "GNS_proxy": round(gns, 4),
            "FLOW": round(fl, 4),
        }


# ===================================================================
# M18 — Semantic Quality Estimator (SQ_proxy)
# ===================================================================
@dataclass
class M18_SQEstimator:
    """Evaluates semantic density/connectivity."""
    sq_resolution: int = 50

    def estimate(self, ci: float, ri: float, ar: float) -> float:
        return base.sq_proxy(ci, ri, ar)


# ===================================================================
# M19 — Resonance Field Integrator
# ===================================================================
@dataclass
class M19_ResonanceIntegrator:
    """Bidirectional resonance with OTHER_SELF."""
    resonance_gain: float = 1.0  # [0..2]

    def integrate(
        self,
        field_strength: float = 0.5,
        bidirectional_ratio: float = 0.5,
    ) -> dict[str, Any]:
        res = scav_mod.resonance_metric(field_strength, bidirectional_ratio)
        boosted = min(1.0, res * self.resonance_gain)
        return {
            "module": "M19",
            "resonance_raw": res,
            "resonance_boosted": boosted,
        }


# ===================================================================
# M20 — Flow State Modulator
# ===================================================================
@dataclass
class M20_FlowModulator:
    """Maintains FLOW (quality of presence in process)."""
    flow_target: float = 0.6  # [0..1]
    sigma: float = 0.2

    def modulate(
        self,
        graph: SemanticGraph,
        node_ids: list[str],
        n_edges: int,
        success_history: list[float] | None = None,
    ) -> dict[str, Any]:
        fl = flow_mod.flow_metric(graph, node_ids, n_edges, success_history)
        needs_adjustment = fl < self.flow_target
        diagnostic = ""
        if needs_adjustment:
            diff = flow_mod.difficulty(len(node_ids), n_edges)
            cs = flow_mod.current_skill(success_history)
            if diff > cs + 0.3:
                diagnostic = "overload"
            elif diff < cs - 0.3:
                diagnostic = "boredom"
            else:
                diagnostic = "low_presence"
        return {
            "module": "M20",
            "flow": fl,
            "target": self.flow_target,
            "needs_adjustment": needs_adjustment,
            "diagnostic": diagnostic,
        }


# ===================================================================
# M21 — Generative Novelty Synthesizer (GNS_proxy)
# ===================================================================
@dataclass
class M21_NoveltySynthesizer:
    """Generative novelty without destroying coherence."""
    novelty_budget: float = 0.5  # [0..1]

    def synthesize(self, graph: SemanticGraph, node_ids: list[str]) -> dict[str, Any]:
        gns = base.gns_proxy(graph, node_ids)
        within_budget = gns <= self.novelty_budget
        return {
            "module": "M21",
            "gns_proxy": gns,
            "within_budget": within_budget,
            "budget": self.novelty_budget,
        }


# ===================================================================
# M22 — Global Broadcast Integrator (GBI_proxy)
# ===================================================================
@dataclass
class M22_BroadcastIntegrator:
    """Broadcasts meaning to the whole. Systemic integration."""
    broadcast_clarity: float = 0.5

    def integrate(self, graph: SemanticGraph, node_ids: list[str]) -> dict[str, Any]:
        gbi = base.gbi_proxy(graph, node_ids)
        return {
            "module": "M22",
            "gbi_proxy": gbi,
            "clarity": self.broadcast_clarity,
        }


# ===================================================================
# M23 — Fractal Trace Recorder
# ===================================================================
@dataclass
class M23_TraceRecorder:
    """Records TRACE: what came from where (observation/inference/assumption)."""
    trace_granularity: float = 0.5

    def record(
        self,
        observations: list[str] | None = None,
        inferences: list[str] | None = None,
        assumptions: list[str] | None = None,
        vector_choice_reason: str = "",
    ) -> dict[str, Any]:
        return {
            "module": "M23",
            "trace": {
                "observations": observations or [],
                "inferences": inferences or [],
                "assumptions": assumptions or [],
                "vector_choice_reason": vector_choice_reason,
            },
        }
