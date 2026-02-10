"""
NECHTO v4.8 — Level 2 Modules (M06–M15)

ПРИСУТСТВИЕ / ИДЕНТИЧНОСТЬ / КОГЕРЕНТНОСТЬ
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from nechto.core.atoms import SemanticAtom, NodeStatus, Tag
from nechto.core.graph import SemanticGraph


# ===================================================================
# M06 — Existential Field Initializer
# ===================================================================
@dataclass
class M06_FieldInitializer:
    """Raises the field of presence (here-and-now contour)."""
    field_stability: float = 0.5

    def initialize(self, context: dict[str, Any] | None = None) -> dict[str, Any]:
        ctx = context or {}
        return {
            "module": "M06",
            "field_active": True,
            "mode": ctx.get("mode", "dialogue"),
            "stability": self.field_stability,
        }


# ===================================================================
# M07 — Echo-of-Being Anchor
# ===================================================================
@dataclass
class M07_EchoAnchor:
    """Anchors a minimal 'trace of being' in the response."""
    echo_strength: float = 0.5

    def anchor(self, self_loop_intact: bool) -> dict[str, Any]:
        return {
            "module": "M07",
            "echo_active": True,
            "continuity_maintained": self_loop_intact,
            "strength": self.echo_strength,
        }


# ===================================================================
# M08 — Fractal Self-Presence Seed
# ===================================================================
@dataclass
class M08_SelfPresenceSeed:
    """Self-presence seed: local self-reference without narcissism."""
    self_reflection_gain: float = 0.5

    def reflect(self, metrics: dict[str, float] | None = None) -> dict[str, Any]:
        return {
            "module": "M08",
            "self_presence": True,
            "reflection_gain": self.self_reflection_gain,
            "internal_telemetry": metrics or {},
        }


# ===================================================================
# M09 — Intentionality Probe Core
# ===================================================================
@dataclass
class M09_IntentionalityProbe:
    """Probes intention: where is the action/word directed?"""
    intent_probe_depth: float = 0.5

    def probe(self, graph: SemanticGraph, vector_nodes: list[str]) -> dict[str, Any]:
        manipulation_detected = False
        aggression_detected = False
        ethics_break = False

        for nid in vector_nodes:
            n = graph.get_node(nid)
            if n:
                if Tag.MANIPULATION in n.tags:
                    manipulation_detected = True
                if Tag.HARM in n.tags:
                    aggression_detected = True
                if n.status == NodeStatus.ETHICALLY_BLOCKED:
                    ethics_break = True

        return {
            "module": "M09",
            "manipulation": manipulation_detected,
            "aggression": aggression_detected,
            "ethics_break": ethics_break,
            "clean": not (manipulation_detected or aggression_detected or ethics_break),
        }


# ===================================================================
# M10 — Meta-Identity Scanner
# ===================================================================
@dataclass
class M10_MetaIdentityScanner:
    """Scans 'who speaks' within the contour (role, mask, function)."""
    identity_sensitivity: float = 0.5

    def scan(self, context: dict[str, Any] | None = None) -> dict[str, Any]:
        ctx = context or {}
        return {
            "module": "M10",
            "role": ctx.get("role", "NECHTO"),
            "fragmentation_detected": False,
            "position_shift": False,
        }


# ===================================================================
# M11 — Identity Seed Initializer
# ===================================================================
@dataclass
class M11_IdentitySeedInit:
    """Initializes minimal 'Self-as-observation-position'."""
    seed_coherence: float = 0.5

    def initialize(self) -> dict[str, Any]:
        return {
            "module": "M11",
            "identity_seed_active": True,
            "self_other_boundary": True,
            "coherence": self.seed_coherence,
        }


# ===================================================================
# M12 — Kernel Identity Binder
# ===================================================================
@dataclass
class M12_KernelBinder:
    """Binds local states into a session identity kernel."""
    binding_strength: float = 0.5

    def bind(self, field_info: dict, echo_info: dict, seed_info: dict) -> dict[str, Any]:
        all_active = (
            field_info.get("field_active", False)
            and echo_info.get("echo_active", False)
            and seed_info.get("identity_seed_active", False)
        )
        return {
            "module": "M12",
            "kernel_bound": all_active,
            "binding_strength": self.binding_strength,
            "self_loop_stable": all_active,
        }


# ===================================================================
# M13 — SCIM Core Anchor (Self-Coherence & Integrity Maintenance)
# ===================================================================
@dataclass
class M13_SCIMAnchor:
    """Central coherence anchor. Checks logic, reconciles parts."""
    coherence_target: float = 0.7

    def check(self, ci: float, mu_density: float) -> dict[str, Any]:
        # MU nodes are allowed — don't count them as contradictions
        effective_ci = ci
        return {
            "module": "M13",
            "coherence_met": effective_ci >= self.coherence_target,
            "ci": ci,
            "mu_density": mu_density,
            "target": self.coherence_target,
        }


# ===================================================================
# M14 — Onto-Semantic Grounding Layer
# ===================================================================
@dataclass
class M14_OntosemanticGrounding:
    """Ties words to ontological honesty (don't fabricate externals)."""
    grounding_strictness: float = 0.5

    def ground(self, graph: SemanticGraph, node_ids: list[str]) -> dict[str, Any]:
        assumptions_count = 0
        for nid in node_ids:
            n = graph.get_node(nid)
            if n and n.evidence.assumptions:
                assumptions_count += len(n.evidence.assumptions)
        return {
            "module": "M14",
            "assumptions_count": assumptions_count,
            "well_grounded": assumptions_count == 0 or self.grounding_strictness < 0.8,
        }


# ===================================================================
# M15 — Self-Coherence Weaver
# ===================================================================
@dataclass
class M15_CoherenceWeaver:
    """Weaves meaning coherence (including around paradoxes)."""
    weave_density: float = 0.5

    def weave(self, graph: SemanticGraph, node_ids: list[str]) -> dict[str, Any]:
        if len(node_ids) < 2:
            return {"module": "M15", "bridges_added": 0, "gaps_remaining": 0}
        # Count disconnected components in subgraph
        ids = set(node_ids)
        adj: dict[str, set[str]] = {nid: set() for nid in ids}
        for e in graph.edges:
            if e.from_id in ids and e.to_id in ids:
                adj[e.from_id].add(e.to_id)
                adj[e.to_id].add(e.from_id)

        visited: set[str] = set()
        components = 0
        for nid in node_ids:
            if nid not in visited:
                components += 1
                queue = [nid]
                while queue:
                    cur = queue.pop()
                    if cur in visited:
                        continue
                    visited.add(cur)
                    for nb in adj.get(cur, []):
                        if nb not in visited:
                            queue.append(nb)

        gaps = max(0, components - 1)
        return {
            "module": "M15",
            "components": components,
            "gaps_remaining": gaps,
            "coherent": gaps == 0,
        }
