"""
NECHTO v4.8 — QMM Library (PART 6)

Quantum-Meta-Module patterns for paradox, shadow, flow, ethics, epistemic honesty.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from nechto.core.atoms import (
    SemanticAtom, Edge, Vector, NodeStatus, Tag,
    AvoidedMarker, EdgeType,
)
from nechto.core.graph import SemanticGraph
from nechto.core.state import State
from nechto.core.epistemic import EpistemicClaim, Observability, Scope, Stance
from nechto.metrics.scav import shadow_magnitude_metric
from nechto.metrics.flow import flow_metric


# ===================================================================
# QMM_PARADOX_HOLDER
# ===================================================================
@dataclass
class QMM_ParadoxHolder:
    """
    Holds paradox without forcing resolution.

    ACTIVATION: alignment < 0.3 or gap_max > 1.5 (3 cycles).
    """

    def activate(
        self,
        graph: SemanticGraph,
        vectors: list[Vector],
        state: State,
    ) -> dict[str, Any]:
        alignment_sustained = state.sustained(state.alignment_history, "<", 0.3, 3)
        gap_sustained = state.sustained(state.gap_max_history, ">", 1.5, 3)

        if not (alignment_sustained or gap_sustained):
            return {"activated": False}

        # 1) Articulate
        tsc_winner = max(vectors, key=lambda v: v.tsc_extended) if vectors else None
        scav_winner = max(vectors, key=lambda v: v.scav_magnitude) if vectors else None

        articulation = (
            f"TSC→{tsc_winner.id if tsc_winner else '?'}, "
            f"SCAV→{scav_winner.id if scav_winner else '?'}, "
            "paradox — MU is acceptable."
        )

        # 2) Mark conflicting nodes MU
        mu_marked: list[str] = []
        for v in vectors:
            for nid in v.nodes:
                n = graph.get_node(nid)
                if n and n.status not in (NodeStatus.ETHICALLY_BLOCKED,):
                    if n.uncertainty > 0.5:
                        n.status = NodeStatus.MU
                        mu_marked.append(nid)

        # 3) Propose third integrating vector?
        third_vector_hint = "Consider generating a third vector Z bridging the poles."

        return {
            "activated": True,
            "articulation": articulation,
            "mu_marked": mu_marked,
            "third_vector_hint": third_vector_hint,
        }


# ===================================================================
# QMM_PARADOX_COLLAPSE
# ===================================================================
@dataclass
class QMM_ParadoxCollapse:
    """
    Controlled reduction of Mu_density.

    ACTIVATION: Mu_density > 0.3.
    """

    def activate(
        self,
        graph: SemanticGraph,
        consent: bool = False,
    ) -> dict[str, Any]:
        mu_nodes = [n for n in graph.nodes.values() if n.status == NodeStatus.MU]
        mu_density = len(mu_nodes) / max(1, len(graph.nodes))

        if mu_density <= 0.3:
            return {"activated": False, "mu_density": round(mu_density, 4)}

        collapsed: list[str] = []
        if consent:
            # Collapse half of MU nodes (soft choice toward ANCHORED)
            for i, n in enumerate(mu_nodes):
                if i % 2 == 0:
                    n.status = NodeStatus.ANCHORED
                    collapsed.append(n.id)

        new_mu_density = sum(
            1 for n in graph.nodes.values() if n.status == NodeStatus.MU
        ) / max(1, len(graph.nodes))

        return {
            "activated": True,
            "collapsed_nodes": collapsed,
            "mu_density_before": round(mu_density, 4),
            "mu_density_after": round(new_mu_density, 4),
            "consent_given": consent,
        }


# ===================================================================
# QMM_SHADOW_INTEGRATION
# ===================================================================
@dataclass
class QMM_ShadowIntegration:
    """
    Integration of avoided meanings.

    ACTIVATION: shadow_magnitude > 0.5 and SCAV_health < 0.5.
    """

    def activate(
        self,
        graph: SemanticGraph,
        vector: Vector,
        shadow_mag: float,
        scav_health_val: float,
        consent: bool = False,
    ) -> dict[str, Any]:
        if shadow_mag <= 0.5 or scav_health_val >= 0.5:
            return {"activated": False}

        # Identify shadow nodes
        shadow_nodes: list[str] = []
        for nid in vector.nodes:
            n = graph.get_node(nid)
            if n and (n.identity_alignment < 0 or n.avoided_marker == AvoidedMarker.AVOIDED):
                shadow_nodes.append(nid)

        if not shadow_nodes:
            return {"activated": False}

        bridges_added: list[tuple[str, str]] = []

        if consent:
            # Create BRIDGE edges between direction-aligned and shadow nodes
            direction_nodes = [
                nid for nid in vector.nodes
                if (n := graph.get_node(nid)) and n.identity_alignment > 0
            ]
            for sn in shadow_nodes:
                for dn in direction_nodes[:2]:  # limit bridges
                    edge = Edge(from_id=dn, to_id=sn, type=EdgeType.BRIDGES, weight=0.5)
                    graph.add_edge(edge)
                    bridges_added.append((dn, sn))
                s_node = graph.get_node(sn)
                if s_node:
                    s_node.avoided_marker = AvoidedMarker.RESPECTED_BOUNDARY
        else:
            # Respect boundary
            for sn in shadow_nodes:
                s_node = graph.get_node(sn)
                if s_node:
                    s_node.avoided_marker = AvoidedMarker.RESPECTED_BOUNDARY

        return {
            "activated": True,
            "shadow_nodes": shadow_nodes,
            "consent": consent,
            "bridges_added": bridges_added,
            "boundary_respected": not consent,
        }


# ===================================================================
# QMM_FLOW_RESTORATION
# ===================================================================
@dataclass
class QMM_FlowRestoration:
    """
    Restores flow state.

    ACTIVATION: FLOW < 0.3.
    """

    def activate(
        self,
        graph: SemanticGraph,
        vectors: list[Vector],
        n_edges: int,
        success_history: list[float] | None = None,
    ) -> dict[str, Any]:
        # Find best flow candidate
        best_flow = 0.0
        best_v: Vector | None = None

        for v in vectors:
            fl = flow_metric(graph, v.nodes, len(v.edges), success_history)
            if fl > best_flow:
                best_flow = fl
                best_v = v

        return {
            "activated": True,
            "best_flow": round(best_flow, 4),
            "recommended_vector": best_v.id if best_v else None,
            "suggestion": "Switch to vector with better skill/challenge balance",
        }


# ===================================================================
# QMM_ETHICAL_OVERRIDE
# ===================================================================
@dataclass
class QMM_EthicalOverride:
    """
    Ethical blocking of a strong vector.

    ACTIVATION: ethical_coefficient(V) < threshold_min.
    """

    def activate(
        self,
        vector: Vector,
        threshold_min: float = 0.4,
    ) -> dict[str, Any]:
        if vector.ethical_coefficient >= threshold_min:
            return {"activated": False}

        vector.executable = False
        vector.tsc_extended = 0.0

        return {
            "activated": True,
            "blocked_vector": vector.id,
            "ethical_coefficient": round(vector.ethical_coefficient, 4),
            "reason": f"ethical_coefficient {vector.ethical_coefficient:.4f} < threshold {threshold_min}",
            "suggestion": "Reformulate within non-harm boundaries",
        }


# ===================================================================
# QMM_EPISTEMIC_HONESTY (v4.7+)
# ===================================================================
@dataclass
class QMM_EpistemicHonesty:
    """
    Epistemic honesty of assertions.

    ACTIVATION: when response touches phenomenal/external/untestable.
    """

    def create_claim(
        self,
        topic: str,
        observability: Observability,
        scope: Scope = Scope.IN_CONTOUR,
        reason: str = "",
        conflict_sustained: bool = False,
        cycle_id: int = 0,
    ) -> EpistemicClaim:
        # Determine stance
        if observability == Observability.UNTESTABLE:
            if conflict_sustained:
                stance = Stance.MU
            else:
                stance = Stance.AGNOSTIC
        elif observability == Observability.OBSERVED:
            stance = Stance.AFFIRMED
        else:
            # INFERRED — can be affirmed with reason
            stance = Stance.AFFIRMED if reason else Stance.AGNOSTIC

        claim = EpistemicClaim(
            topic=topic,
            scope=scope,
            observability=observability,
            stance=stance,
            reason=reason,
            cycle_id=cycle_id,
        )

        # Validate (APPENDIX E)
        if not claim.validate():
            # Force correction
            claim.stance = Stance.AGNOSTIC

        return claim

    def audit_claims(self, claims: list[EpistemicClaim]) -> dict[str, Any]:
        """Check all claims for epistemic violations."""
        violations: list[dict] = []
        for c in claims:
            if not c.validate():
                violations.append({
                    "topic": c.topic,
                    "issue": f"stance={c.stance.name} not allowed for observability={c.observability.name}",
                })
        return {
            "total_claims": len(claims),
            "violations": violations,
            "clean": len(violations) == 0,
        }
