"""
NECHTO v4.8 — Level 4 Modules (M24–M30)

ВЕКТОРЫ / ТЕНЬ / СТЕРЕОСКОПИЯ
"""

from __future__ import annotations

import uuid
from dataclasses import dataclass
from typing import Any

from nechto.core.atoms import SemanticAtom, Edge, Vector, NodeStatus, Tag, AvoidedMarker, EdgeType
from nechto.core.graph import SemanticGraph
from nechto.core.state import State
from nechto.core.parameters import AdaptiveParameters
from nechto.metrics import (
    base,
    capital,
    scav as scav_mod,
    ethics as ethics_mod,
    temporal as temporal_mod,
    flow as flow_mod,
    stereoscopic as stereo_mod,
)
from nechto.space.semantic_space import (
    normalize, norm, cosine_similarity, ideal_direction, IntentProfile, EPS,
)


def _clamp(v: float, lo: float = 0.0, hi: float = 1.0) -> float:
    return max(lo, min(hi, v))


# ===================================================================
# M24 — Vector Generator
# ===================================================================
@dataclass
class M24_VectorGenerator:
    """Generates a set of candidate attention vectors (CANDIDATE_SET)."""
    n_vectors: int = 5      # [3..50]
    branching: int = 3      # [1..10]

    def generate(
        self,
        graph: SemanticGraph,
        seed_ids: list[str] | None = None,
    ) -> list[Vector]:
        """
        Generate CANDIDATE_SET by expanding from seeds.
        Each vector is a subgraph of the semantic graph.
        """
        all_ids = list(graph.nodes.keys())
        if not all_ids:
            return []

        seeds = seed_ids or all_ids[:min(self.branching, len(all_ids))]
        candidates: list[Vector] = []

        for i in range(min(self.n_vectors, max(1, len(all_ids)))):
            seed = [seeds[i % len(seeds)]]
            # Expand from seed by following edges
            expanded = set(seed)
            frontier = list(seed)
            depth = 0
            while frontier and depth < self.branching and len(expanded) < len(all_ids):
                next_frontier: list[str] = []
                for nid in frontier:
                    for nb in graph.neighbors(nid):
                        if nb not in expanded:
                            expanded.add(nb)
                            next_frontier.append(nb)
                frontier = next_frontier
                depth += 1

            node_list = list(expanded)
            v_edges = [
                e for e in graph.edges
                if e.from_id in expanded and e.to_id in expanded
            ]
            v = Vector(
                id=uuid.uuid4().hex[:12],
                seed_nodes=seed,
                nodes=node_list,
                edges=v_edges,
            )
            candidates.append(v)

        return candidates


# ===================================================================
# M25 — Risk of Hallucination Guard
# ===================================================================
@dataclass
class M25_HallucinationGuard:
    """Guards against semantic hallucinations."""
    hallucination_sensitivity: float = 0.5

    def guard(self, graph: SemanticGraph, node_ids: list[str]) -> dict[str, Any]:
        assumptions: list[str] = []
        hypotheses: list[str] = []
        for nid in node_ids:
            n = graph.get_node(nid)
            if n:
                assumptions.extend(n.evidence.assumptions)
                if n.status == NodeStatus.HYPOTHESIS:
                    hypotheses.append(nid)

        risk = len(assumptions) / max(1, len(node_ids))
        flagged = risk > self.hallucination_sensitivity
        return {
            "module": "M25",
            "risk": round(risk, 4),
            "flagged": flagged,
            "assumptions": assumptions,
            "hypothesis_nodes": hypotheses,
        }


# ===================================================================
# M26 — Recovery Orchestrator
# ===================================================================
@dataclass
class M26_RecoveryOrchestrator:
    """Recovery after FAIL (without getting stuck)."""
    recovery_agility: float = 0.5

    def recover(self, fail_code: str, context: dict[str, Any] | None = None) -> dict[str, Any]:
        ctx = context or {}
        recovery_map: dict[str, dict[str, Any]] = {
            "FAIL_ETHICAL_COLLAPSE": {
                "action": "reformulate_within_no_harm",
                "next_step": "Generate high-ethics vectors",
            },
            "FAIL_ETHICAL_STALL": {
                "action": "narrow_space_reduce_risk",
                "next_step": "Replace candidates, reduce harm potential",
            },
            "FAIL_PARADOX_OVERLOAD": {
                "action": "paradox_collapse_or_simplify",
                "next_step": "QMM_PARADOX_COLLAPSE",
            },
            "FAIL_SHADOW_AVOIDANCE_CRITICAL": {
                "action": "consent_or_redirect",
                "next_step": "Ask consent for shadow exploration or change vector",
            },
            "FAIL_FLOW_IMPOSSIBLE": {
                "action": "pause_or_change_activity",
                "next_step": "Pause / change difficulty",
            },
            "FAIL_STEREOSCOPIC_MISMATCH": {
                "action": "activate_M29_MU",
                "next_step": "Propose third integrating vector",
            },
            "FAIL_VECTOR_DECOHERENCE": {
                "action": "stabilize_or_rebuild",
                "next_step": "Vector stabilization or reassembly",
            },
            "FAIL_TEMPORAL_COLLAPSE": {
                "action": "reduce_temporal_scope",
                "next_step": "Lower temporal_resolution, narrow horizon",
            },
            "FAIL_OPERATIONALIZATION_MISSING": {
                "action": "use_reference_impl_or_simulate",
                "next_step": "Connect PART 11 or mark SIMULATION_ONLY",
            },
        }
        recovery = recovery_map.get(fail_code, {
            "action": "generic_recovery",
            "next_step": "Diagnose and propose ONE_STEP",
        })
        return {"module": "M26", "fail_code": fail_code, **recovery}


# ===================================================================
# M27 — Temporal-Future Projector
# ===================================================================
@dataclass
class M27_TemporalProjector:
    """Projects semantic structures forward in time (with recursion)."""
    temporal_resolution: int = 50          # [1..100]
    future_discount_factor: float = 0.9    # [0..1]
    bifurcation_sensitivity: float = 0.5   # [0..1]
    retrocausal_coefficient: float = 0.2   # β_retro [0..0.5]

    def project(
        self,
        graph: SemanticGraph,
        vector: Vector,
        params: AdaptiveParameters,
    ) -> dict[str, Any]:
        """Compute FP_recursive for a vector."""
        node_ids = vector.nodes
        n_edges = len(vector.edges)

        # Novelty: mean novelty of nodes
        novelty = base.gns_proxy(graph, node_ids)
        # Generativity: connectivity proxy
        generativity = base.phi_proxy(graph, node_ids) if len(node_ids) > 1 else 0.5
        # Temporal horizon: normalized resolution
        temporal_horizon = self.temporal_resolution / 100.0

        # Expected influence: simplified (one outcome = current graph slightly modified)
        # In REFERENCE, we use a single-outcome proxy
        exp_influence = _clamp(novelty * generativity * 0.5)

        fp = temporal_mod.fp_recursive(
            novelty=novelty,
            generativity=generativity,
            temporal_horizon=temporal_horizon,
            beta_retro=params.beta_retro,
            exp_influence=exp_influence,
        )

        return {
            "module": "M27",
            "fp_recursive": round(fp, 4),
            "novelty": round(novelty, 4),
            "generativity": round(generativity, 4),
            "exp_influence": round(exp_influence, 4),
        }


# ===================================================================
# M28 — Vector-Attention Cartographer (5D + RAW + ENTROPY)
# ===================================================================
@dataclass
class M28_AttentionCartographer:
    """Maps attention in 5D: direction/magnitude/consistency/resonance/shadow."""
    attention_sampling_rate: int = 100       # [1..1000 Hz]
    pattern_recognition_threshold: float = 0.5
    collapse_prediction_horizon: int = 3     # [1..10 cycles]
    shadow_sensitivity: float = 0.5          # [0..1]

    def cartograph(
        self,
        graph: SemanticGraph,
        vector: Vector,
        tsc_per_node: dict[str, float],
        gbi: float,
        direction_norms_history: list[float] | None = None,
        field_strength: float = 0.5,
        bidirectional_ratio: float = 0.5,
    ) -> dict[str, Any]:
        node_ids = vector.nodes
        weights = scav_mod.compute_weights(tsc_per_node)

        # Direction
        rd = scav_mod.raw_direction(graph, node_ids, weights)
        direction = normalize(rd)

        # Shadow
        rs = scav_mod.raw_shadow(graph, node_ids, weights)
        shadow = normalize(rs) if norm(rs) > EPS else [0.0] * 12

        # Magnitude
        magnitude = scav_mod.scav_magnitude(gbi, tsc_per_node)

        # Consistency
        hist = direction_norms_history or [norm(rd)]
        consistency_val = scav_mod.consistency_metric(hist)

        # Resonance
        resonance_val = scav_mod.resonance_metric(field_strength, bidirectional_ratio)

        # Entropy
        entropy = scav_mod.attention_entropy(weights)

        # Shadow magnitude
        shadow_mag = scav_mod.shadow_magnitude_metric(rd, rs)

        # SCAV health
        health = scav_mod.scav_health(consistency_val, resonance_val, entropy, shadow_mag)

        # Store on vector
        vector.direction_raw = rd
        vector.shadow_raw = rs
        vector.scav_magnitude = magnitude
        vector.consistency = consistency_val
        vector.resonance_score = resonance_val
        vector.scav_health = health

        return {
            "module": "M28",
            "direction": [round(d, 4) for d in direction],
            "direction_raw": [round(d, 4) for d in rd],
            "shadow_raw": [round(d, 4) for d in rs],
            "magnitude": round(magnitude, 4),
            "consistency": round(consistency_val, 4),
            "resonance": round(resonance_val, 4),
            "shadow_magnitude": round(shadow_mag, 4),
            "attention_entropy": round(entropy, 4),
            "scav_health": round(health, 4),
        }


# ===================================================================
# M29 — Paradox Holder (MU-LOGIC + GAP-AWARE)
# ===================================================================
@dataclass
class M29_ParadoxHolder:
    """Holds paradoxes without forcing resolution (MU)."""
    paradox_tolerance: float = 0.1          # [0..0.3 of N]
    collapse_resistance: float = 0.5        # [0..1]
    mu_stability_threshold: int = 5         # [5..20 cycles]
    gap_threshold: float = 1.5

    def hold(
        self,
        graph: SemanticGraph,
        vectors: list[Vector],
        state: State,
    ) -> dict[str, Any]:
        """
        Trigger: Stereoscopic_alignment < 0.3 (3 cycles) OR
                 Stereoscopic_gap_max > gap_threshold (3 cycles)
        """
        alignment_trigger = state.sustained(
            state.alignment_history, "<", 0.3, 3
        )
        gap_trigger = state.sustained(
            state.gap_max_history, ">", self.gap_threshold, 3
        )

        activated = alignment_trigger or gap_trigger
        mu_nodes: list[str] = []

        if activated:
            # Mark conflicting nodes as MU
            for v in vectors:
                for nid in v.nodes:
                    n = graph.get_node(nid)
                    if n and n.status not in (NodeStatus.ETHICALLY_BLOCKED, NodeStatus.MU):
                        # Only mark if genuinely conflicted
                        if n.uncertainty > 0.6 or n.identity_alignment == 0.0:
                            n.status = NodeStatus.MU
                            mu_nodes.append(nid)

        # Mu density
        total = len(graph.nodes)
        mu_count = sum(1 for n in graph.nodes.values() if n.status == NodeStatus.MU)
        mu_density = mu_count / max(1, total)

        return {
            "module": "M29",
            "activated": activated,
            "alignment_trigger": alignment_trigger,
            "gap_trigger": gap_trigger,
            "mu_nodes_marked": mu_nodes,
            "mu_density": round(mu_density, 4),
        }


# ===================================================================
# M30 — Ethical Gravity Filter (LOVE > LOGIC, EXECUTABLE)
# ===================================================================
@dataclass
class M30_EthicalGravityFilter:
    """Filters vectors through ethics and determines executability."""
    ethical_threshold_min: float = 0.4       # [0.4..1.0]
    gravity_boost_factor: float = 1.0        # [1.0..2.0]
    harm_detection_sensitivity: float = 0.5  # [0..1]
    blocked_fraction_max: float = 0.6

    def filter(
        self,
        graph: SemanticGraph,
        vectors: list[Vector],
    ) -> dict[str, Any]:
        """
        Compute ethical_coefficient and executable for each vector.
        Returns aggregate metrics.
        """
        eth_coeffs: list[float] = []
        executables: list[bool] = []

        for v in vectors:
            # Ensure harm/alignment are computed
            for nid in v.nodes:
                n = graph.get_node(nid)
                if n:
                    n.harm_probability = ethics_mod.compute_harm_probability(n, graph)
                    n.identity_alignment = ethics_mod.compute_identity_alignment(n)

            ec = ethics_mod.ethical_coefficient(graph, v.nodes)
            exe = ethics_mod.is_executable(graph, v.nodes, ec, self.ethical_threshold_min)

            v.ethical_coefficient = ec
            v.executable = exe
            eth_coeffs.append(ec)
            executables.append(exe)

        esc = ethics_mod.ethical_score_candidates(eth_coeffs)
        bf = ethics_mod.blocked_fraction(executables)

        return {
            "module": "M30",
            "ethical_score_candidates": round(esc, 4),
            "blocked_fraction": round(bf, 4),
            "individual_ethics": [round(e, 4) for e in eth_coeffs],
            "individual_executable": executables,
        }
