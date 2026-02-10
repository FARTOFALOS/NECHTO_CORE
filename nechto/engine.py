"""
NECHTO v4.8 — Main Engine

Top-level API that manages graph, state, parameters, and workflow execution.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from nechto.core.atoms import SemanticAtom, Edge, Vector, NodeStatus, EdgeType, Tag, AvoidedMarker
from nechto.core.graph import SemanticGraph
from nechto.core.state import State
from nechto.core.parameters import AdaptiveParameters
from nechto.core.epistemic import EpistemicClaim, Observability, Scope, Stance
from nechto.metrics.ethics import compute_harm_probability, compute_identity_alignment
from nechto.workflow.phases import WorkflowExecutor, WorkflowResult
from nechto.gate.prrip import format_output_pass, format_output_fail


@dataclass
class NechtoEngine:
    """
    NECHTO CORE v4.8 — top-level orchestrator.

    Usage:
        engine = NechtoEngine()
        engine.add_atom(SemanticAtom(label="concept-1", ...))
        engine.add_atom(SemanticAtom(label="concept-2", ...))
        engine.add_edge(Edge(from_id=..., to_id=...))
        result = engine.run("implement", context={...})
    """

    graph: SemanticGraph = field(default_factory=SemanticGraph)
    state: State = field(default_factory=State)
    params: AdaptiveParameters = field(default_factory=AdaptiveParameters)
    workflow: WorkflowExecutor = field(default_factory=WorkflowExecutor)

    # ------------------------------------------------------------------ API
    def add_atom(self, atom: SemanticAtom) -> SemanticAtom:
        """Add a semantic atom to the graph and compute harm/alignment."""
        self.graph.add_node(atom)
        atom.harm_probability = compute_harm_probability(atom, self.graph)
        atom.identity_alignment = compute_identity_alignment(atom)
        return atom

    def add_edge(self, edge: Edge) -> Edge:
        return self.graph.add_edge(edge)

    def remove_atom(self, node_id: str) -> None:
        self.graph.remove_node(node_id)

    def run(
        self,
        raw_input: str = "",
        context: dict[str, Any] | None = None,
        consent_shadow: bool = False,
        consent_collapse: bool = False,
        seed_ids: list[str] | None = None,
    ) -> WorkflowResult:
        """
        Execute one full 12-phase cycle.

        Args:
            raw_input: The user/source request text.
            context: Optional dict with keys like 'intent', 'noise', 'coercion',
                     'resonance_field', 'bidirectional_ratio', etc.
            consent_shadow: Whether the user consents to shadow integration.
            consent_collapse: Whether the user consents to paradox collapse.
            seed_ids: Optional seed node IDs for vector generation.

        Returns:
            WorkflowResult with gate status, metrics, trace, etc.
        """
        return self.workflow.execute(
            graph=self.graph,
            state=self.state,
            params=self.params,
            raw_input=raw_input,
            context=context,
            consent_shadow=consent_shadow,
            consent_collapse=consent_collapse,
            seed_ids=seed_ids,
        )

    def format_output(self, result: WorkflowResult, content: str = "") -> str:
        """Format a WorkflowResult into the NECHTO output contract."""
        if result.gate_status == "PASS":
            return format_output_pass(
                metrics=result.metrics,
                chosen_vector=result.chosen_vector,
                candidate_count=result.candidate_set_size,
                active_count=result.active_set_size,
                blocked_frac=result.blocked_fraction,
                epistemic_claims=result.epistemic_claims,
                trace=result.trace,
                params=result.params_snapshot,
                recommendation=f"Vector {result.chosen_vector.id}" if result.chosen_vector else "",
                rationale="TSC + SCAV + Ethics + Flow + Epistemic",
                content=content,
            )
        else:
            return format_output_fail(
                fail_code=result.fail_code or "UNKNOWN",
                candidate_count=result.candidate_set_size,
                active_count=result.active_set_size,
                blocked_frac=result.blocked_fraction,
                blocking_reasons=[result.fail_code or "unknown"],
                metrics=result.metrics,
                mu_nodes=result.mu_nodes,
                shadow_info=result.shadow_info,
                epistemic_claims=result.epistemic_claims,
                next_one_step=result.recovery_info.get("next_step", "diagnose") if result.recovery_info else "diagnose",
                recovery_options=[result.recovery_info.get("action", "generic")] if result.recovery_info else [],
            )

    def snapshot(self) -> dict[str, Any]:
        """Return a serializable snapshot of the engine state."""
        return {
            "version": "4.8.0",
            "graph_nodes": len(self.graph.nodes),
            "graph_edges": len(self.graph.edges),
            "cycle": self.state.current_cycle,
            "params": self.params.snapshot(),
            "fail_history": list(self.state.fail_history),
            "epistemic_claims": [c for c in self.state.epistemic_claims],
        }
