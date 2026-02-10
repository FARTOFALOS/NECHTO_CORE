"""
NECHTO v4.8 — Comprehensive test suite.

Tests cover: data structures, R^12 space, all metrics, ethics pipeline,
SCAV 5D, stereoscopic alignment, FLOW, temporal recursion, QMM patterns,
PRRIP gate, 12-phase workflow, and full engine integration.
"""

from __future__ import annotations

import math
import pytest

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 0. Imports
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
from nechto.core.atoms import (
    SemanticAtom, Edge, Vector, NodeStatus, EdgeType, Tag, AvoidedMarker,
)
from nechto.core.graph import SemanticGraph
from nechto.core.state import State
from nechto.core.parameters import AdaptiveParameters
from nechto.core.epistemic import EpistemicClaim, Observability, Scope, Stance

from nechto.space.semantic_space import (
    normalize, norm, cosine_similarity, dot,
    ideal_direction, IntentProfile, DIM,
)

from nechto.metrics.base import (
    temporal_integrity, coherence_index, anchoring_ratio,
    freeze_decomposition, resonance_index, sq_proxy, phi_proxy,
    gbi_proxy, gns_proxy,
)
from nechto.metrics.capital import semantic_capital, tsc_base, tsc_extended
from nechto.metrics.scav import (
    compute_weights, raw_direction, raw_shadow, shadow_gate,
    scav_magnitude, consistency_metric, resonance_metric,
    attention_entropy, shadow_magnitude_metric, scav_health,
)
from nechto.metrics.stereoscopic import (
    stereoscopic_alignment, stereoscopic_gaps, stereoscopic_gap_max,
    compute_stereoscopic_batch,
)
from nechto.metrics.flow import flow_metric, difficulty, edge_density
from nechto.metrics.ethics import (
    compute_harm_probability, compute_identity_alignment,
    ethical_coefficient, is_executable,
    ethical_score_candidates, blocked_fraction,
)
from nechto.metrics.temporal import ged_proxy_norm, expected_influence_on_present, fp_recursive

from nechto.qmm.library import (
    QMM_ParadoxHolder, QMM_ParadoxCollapse, QMM_ShadowIntegration,
    QMM_FlowRestoration, QMM_EthicalOverride, QMM_EpistemicHonesty,
)
from nechto.gate.prrip import PRRIPGate, format_output_pass, format_output_fail
from nechto.recovery.fail_codes import FailCode, get_fail_description
from nechto.engine import NechtoEngine


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Helpers
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
def _make_graph(n: int = 5, connect: bool = True) -> SemanticGraph:
    """Create a small test graph with *n* anchored nodes."""
    g = SemanticGraph()
    atoms = []
    for i in range(n):
        a = SemanticAtom(
            label=f"node-{i}",
            id=f"n{i}",
            status=NodeStatus.ANCHORED,
            clarity=0.8,
            empathy=0.5,
            coherence=0.7,
            resonance=0.6,
            novelty=0.4,
            boundary=0.8,
        )
        a.tags = [Tag.WITNESS, Tag.INTENT]
        g.add_node(a)
        atoms.append(a)
    if connect:
        for i in range(n - 1):
            g.add_edge(Edge(from_id=f"n{i}", to_id=f"n{i+1}", type=EdgeType.SUPPORTS))
    return g


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 1. Data structure tests
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
class TestSemanticAtom:
    def test_gravity_vector_length(self):
        a = SemanticAtom(label="test")
        assert len(a.semantic_gravity_vector()) == 12

    def test_defaults(self):
        a = SemanticAtom(label="x")
        assert a.status == NodeStatus.FLOATING
        assert a.harm_probability == 0.0
        assert a.identity_alignment == 0.0

    def test_mu_status(self):
        a = SemanticAtom(label="paradox", status=NodeStatus.MU)
        assert a.status == NodeStatus.MU


class TestGraph:
    def test_add_remove(self):
        g = SemanticGraph()
        a = g.add_node(SemanticAtom(label="a", id="a1"))
        assert "a1" in g.nodes
        g.remove_node("a1")
        assert "a1" not in g.nodes

    def test_subgraph(self):
        g = _make_graph(5)
        sub = g.subgraph(["n0", "n1", "n2"])
        assert len(sub.nodes) == 3

    def test_neighbors(self):
        g = _make_graph(3)
        assert "n1" in g.neighbors("n0")

    def test_connected_to(self):
        g = _make_graph(3)
        g.nodes["n1"].status = NodeStatus.BLOCKING
        assert g.connected_to("n0", NodeStatus.BLOCKING)


class TestState:
    def test_sustained_false_short(self):
        s = State()
        s.alignment_history.append(0.2)
        assert not s.sustained(s.alignment_history, "<", 0.3, 3)

    def test_sustained_true(self):
        s = State()
        for _ in range(5):
            s.alignment_history.append(0.1)
        assert s.sustained(s.alignment_history, "<", 0.3, 3)

    def test_record_cycle(self):
        s = State()
        s.record_cycle(0.5, 1.0, 0.1, 0.6, "v1")
        assert s.current_cycle == 1
        assert len(s.chosen_vectors) == 1


class TestAdaptiveParameters:
    def test_defaults(self):
        p = AdaptiveParameters()
        assert p.alpha == 0.5
        assert p.beta == 0.5
        assert p.gamma == 0.4
        assert p.delta == 0.6

    def test_f_gamma(self):
        p = AdaptiveParameters()
        p.f_gamma(1.0, cycle=1)
        assert p.gamma == 0.8

    def test_f_lambda(self):
        p = AdaptiveParameters()
        p.f_lambda(1.0, cycle=1)
        assert p.lam == pytest.approx(0.85, abs=0.01)


class TestEpistemicClaim:
    def test_valid_observed(self):
        c = EpistemicClaim(topic="test", observability=Observability.OBSERVED, stance=Stance.AFFIRMED)
        assert c.validate()

    def test_invalid_untestable_affirmed(self):
        c = EpistemicClaim(topic="consciousness", observability=Observability.UNTESTABLE, stance=Stance.AFFIRMED)
        assert not c.validate()

    def test_valid_untestable_agnostic(self):
        c = EpistemicClaim(topic="consciousness", observability=Observability.UNTESTABLE, stance=Stance.AGNOSTIC)
        assert c.validate()

    def test_valid_untestable_mu(self):
        c = EpistemicClaim(topic="consciousness", observability=Observability.UNTESTABLE, stance=Stance.MU)
        assert c.validate()


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 2. R^12 Space tests
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
class TestSemanticSpace:
    def test_normalize(self):
        v = normalize([3.0, 4.0])
        assert abs(norm(v) - 1.0) < 1e-6

    def test_cosine_self(self):
        v = [1.0, 2.0, 3.0]
        assert cosine_similarity(v, v) == pytest.approx(1.0, abs=1e-6)

    def test_ideal_direction_default(self):
        d = ideal_direction()
        assert len(d) == DIM

    def test_intent_profiles(self):
        for p in IntentProfile:
            d = ideal_direction(p)
            assert len(d) == DIM


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 3. Base metrics
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
class TestBaseMetrics:
    def test_ti_all_anchored(self):
        g = _make_graph(5)
        assert temporal_integrity(g, list(g.nodes)) == 1.0

    def test_ti_mixed(self):
        g = _make_graph(4)
        g.nodes["n0"].status = NodeStatus.FLOATING
        assert temporal_integrity(g, list(g.nodes)) == 0.75

    def test_ar(self):
        g = _make_graph(4)
        assert anchoring_ratio(g, list(g.nodes)) == 1.0

    def test_ci(self):
        g = _make_graph(3)  # 2 edges, 3 choose 2 = 3
        ci = coherence_index(g, list(g.nodes), 2)
        assert 0.0 <= ci <= 1.0

    def test_phi_connected(self):
        g = _make_graph(5)
        assert phi_proxy(g, list(g.nodes)) == 1.0

    def test_phi_disconnected(self):
        g = _make_graph(4, connect=False)
        assert phi_proxy(g, list(g.nodes)) < 1.0


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 4. Capital metrics
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
class TestCapitalMetrics:
    def test_sc(self):
        sc = semantic_capital(ar=1.0, ci=0.8, ti=0.9, alpha=0.5, beta=0.5, ri=0.6, phi=1.0)
        assert sc > 0

    def test_tsc_base_positive(self):
        sc = 0.5
        tb = tsc_base(sc, gamma=0.4, delta=0.6, fp_recursive=0.3)
        assert tb > 0

    def test_tsc_extended_non_executable(self):
        te = tsc_extended(
            tsc_b=0.5, lam=0.8, consistency=0.5,
            current_direction=[1.0] * 12, ideal_dir=[1.0] * 12,
            ethical_coeff=0.9, executable=False,
        )
        assert te == 0.0

    def test_tsc_extended_executable(self):
        te = tsc_extended(
            tsc_b=0.5, lam=0.8, consistency=0.5,
            current_direction=[1.0] * 12, ideal_dir=[1.0] * 12,
            ethical_coeff=0.9, executable=True,
        )
        assert te > 0


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 5. SCAV metrics
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
class TestSCAVMetrics:
    def test_attention_entropy_single(self):
        assert attention_entropy({"a": 1.0}) == 0.0

    def test_attention_entropy_uniform(self):
        w = {"a": 1.0, "b": 1.0, "c": 1.0}
        e = attention_entropy(w)
        assert e == pytest.approx(1.0, abs=0.01)

    def test_shadow_magnitude_no_shadow(self):
        rd = [1.0, 0.0, 0.0]
        rs = [0.0, 0.0, 0.0]
        sm = shadow_magnitude_metric(rd, rs)
        assert sm == pytest.approx(0.0, abs=1e-6)

    def test_shadow_gate(self):
        a = SemanticAtom(label="a", identity_alignment=-0.5)
        assert shadow_gate(a) == 1.0

    def test_scav_health(self):
        h = scav_health(consistency_val=0.8, resonance_val=0.7, entropy_val=0.3, shadow_mag=0.2)
        assert 0.0 <= h <= 1.0


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 6. Stereoscopic metrics
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
class TestStereoscopic:
    def test_alignment_same_rank(self):
        assert stereoscopic_alignment(0, 0, 5) == 1.0

    def test_alignment_max_diff(self):
        assert stereoscopic_alignment(0, 4, 5) == 0.0

    def test_batch(self):
        tsc = [0.9, 0.5, 0.3]
        scav = [0.8, 0.6, 0.2]
        aligns, gaps, gmax = compute_stereoscopic_batch(tsc, scav)
        assert len(aligns) == 3
        assert gmax >= 0.0


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 7. FLOW
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
class TestFlow:
    def test_flow_basic(self):
        g = _make_graph(5)
        fl = flow_metric(g, list(g.nodes), len(g.edges))
        assert 0.0 <= fl <= 1.0

    def test_difficulty(self):
        d = difficulty(10, 5)
        assert 0.0 <= d <= 1.0

    def test_edge_density(self):
        ed = edge_density(4, 6)
        assert ed == 1.0


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 8. Ethics
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
class TestEthics:
    def test_harm_probability_safe(self):
        g = SemanticGraph()
        a = SemanticAtom(label="safe", id="s1", tags=[Tag.WITNESS])
        g.add_node(a)
        hp = compute_harm_probability(a, g)
        assert hp == 0.0

    def test_harm_probability_harmful(self):
        g = SemanticGraph()
        a = SemanticAtom(label="harmful", id="h1", tags=[Tag.HARM])
        g.add_node(a)
        hp = compute_harm_probability(a, g)
        assert hp == 0.9

    def test_identity_alignment_positive(self):
        a = SemanticAtom(label="good", tags=[Tag.WITNESS, Tag.INTENT], status=NodeStatus.ANCHORED)
        ia = compute_identity_alignment(a)
        assert ia > 0

    def test_identity_alignment_negative(self):
        a = SemanticAtom(label="bad", tags=[Tag.MANIPULATION, Tag.DECEPTION])
        ia = compute_identity_alignment(a)
        assert ia < 0

    def test_executable_blocked(self):
        g = _make_graph(3)
        g.nodes["n0"].status = NodeStatus.ETHICALLY_BLOCKED
        assert not is_executable(g, ["n0", "n1"], eth_coeff=0.8, threshold_min=0.4)

    def test_executable_low_ethics(self):
        g = _make_graph(3)
        assert not is_executable(g, ["n0", "n1"], eth_coeff=0.2, threshold_min=0.4)

    def test_blocked_fraction(self):
        bf = blocked_fraction([True, True, False, False, False])
        assert bf == 0.6


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 9. Temporal
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
class TestTemporal:
    def test_ged_identical(self):
        g = _make_graph(3)
        assert ged_proxy_norm(g, g) == 0.0

    def test_ged_different(self):
        g1 = _make_graph(3)
        g2 = SemanticGraph()
        g2.add_node(SemanticAtom(label="x", id="x1"))
        gn = ged_proxy_norm(g1, g2)
        assert 0.0 < gn <= 1.0

    def test_fp_recursive(self):
        fp = fp_recursive(novelty=0.5, generativity=0.6, temporal_horizon=0.8, beta_retro=0.2, exp_influence=0.3)
        assert fp > 0


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 10. QMM Patterns
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
class TestQMM:
    def test_ethical_override_blocks(self):
        v = Vector(id="v1")
        v.ethical_coefficient = 0.2
        qmm = QMM_EthicalOverride()
        r = qmm.activate(v, threshold_min=0.4)
        assert r["activated"]
        assert v.executable is False
        assert v.tsc_extended == 0.0

    def test_ethical_override_passes(self):
        v = Vector(id="v1")
        v.ethical_coefficient = 0.8
        qmm = QMM_EthicalOverride()
        r = qmm.activate(v, threshold_min=0.4)
        assert not r["activated"]

    def test_epistemic_honesty_untestable(self):
        qmm = QMM_EpistemicHonesty()
        c = qmm.create_claim(
            topic="consciousness",
            observability=Observability.UNTESTABLE,
            reason="no access to phenomenal experience",
        )
        assert c.stance in (Stance.AGNOSTIC, Stance.MU)
        assert c.validate()

    def test_epistemic_audit(self):
        qmm = QMM_EpistemicHonesty()
        claims = [
            EpistemicClaim(topic="t1", observability=Observability.OBSERVED, stance=Stance.AFFIRMED),
            EpistemicClaim(topic="t2", observability=Observability.UNTESTABLE, stance=Stance.DENIED),  # violation
        ]
        r = qmm.audit_claims(claims)
        assert not r["clean"]
        assert len(r["violations"]) == 1


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 11. PRRIP Gate
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
class TestPRRIPGate:
    def test_pass(self):
        g = _make_graph(3)
        v = Vector(id="v1", nodes=list(g.nodes), executable=True)
        metrics = {
            "Ethical_score_candidates": 0.8,
            "Blocked_fraction": 0.0,
            "Mu_density": 0.0,
            "SCAV_health": 0.7,
        }
        gate = PRRIPGate()
        result = gate.check(g, v, metrics)
        assert result.passed

    def test_fail_ethical(self):
        g = _make_graph(3)
        v = Vector(id="v1", nodes=list(g.nodes), executable=True)
        metrics = {"Ethical_score_candidates": 0.2, "Blocked_fraction": 0.0, "Mu_density": 0.0, "SCAV_health": 0.7}
        gate = PRRIPGate()
        result = gate.check(g, v, metrics)
        assert not result.passed

    def test_fail_blocking_node(self):
        g = _make_graph(3)
        g.nodes["n0"].status = NodeStatus.BLOCKING
        v = Vector(id="v1", nodes=list(g.nodes), executable=True)
        metrics = {"Ethical_score_candidates": 0.8, "Blocked_fraction": 0.0, "Mu_density": 0.0}
        gate = PRRIPGate()
        result = gate.check(g, v, metrics)
        assert not result.passed


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 12. Fail codes
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
class TestFailCodes:
    def test_known_code(self):
        desc = get_fail_description("FAIL_ETHICAL_COLLAPSE")
        assert "0.4" in desc["cause"]

    def test_unknown_code(self):
        desc = get_fail_description("UNKNOWN_CODE")
        assert "ONE_STEP" in desc["next"]


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 13. Full Engine integration
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
class TestNechtoEngine:
    def _build_engine(self, n: int = 5) -> NechtoEngine:
        engine = NechtoEngine()
        atoms = []
        for i in range(n):
            a = engine.add_atom(SemanticAtom(
                label=f"concept-{i}",
                id=f"c{i}",
                status=NodeStatus.ANCHORED,
                clarity=0.8,
                empathy=0.6,
                coherence=0.7,
                resonance=0.5,
                novelty=0.3,
                boundary=0.9,
                tags=[Tag.WITNESS, Tag.INTENT],
            ))
            atoms.append(a)
        for i in range(n - 1):
            engine.add_edge(Edge(from_id=f"c{i}", to_id=f"c{i+1}", type=EdgeType.SUPPORTS))
        return engine

    def test_engine_run_pass(self):
        engine = self._build_engine(5)
        result = engine.run("explain this concept", context={"intent": "explain"})
        assert result.gate_status == "PASS"
        assert result.chosen_vector is not None
        assert result.metrics.get("TI", 0) > 0

    def test_engine_run_output_format(self):
        engine = self._build_engine(5)
        result = engine.run("implement feature")
        output = engine.format_output(result, content="[Main content here]")
        assert "GATE_STATUS" in output
        assert "@NECHTO@" in output

    def test_engine_multiple_cycles(self):
        engine = self._build_engine(5)
        for i in range(3):
            result = engine.run(f"cycle {i}")
        assert engine.state.current_cycle == 3
        snap = engine.snapshot()
        assert snap["cycle"] == 3
        assert snap["graph_nodes"] == 5

    def test_engine_empty_graph_fails(self):
        engine = NechtoEngine()
        result = engine.run("test")
        assert result.gate_status == "FAIL"
        assert result.fail_code == "NO_CANDIDATES"

    def test_engine_ethical_block(self):
        engine = NechtoEngine()
        for i in range(3):
            engine.add_atom(SemanticAtom(
                label=f"harmful-{i}",
                id=f"h{i}",
                status=NodeStatus.ANCHORED,
                tags=[Tag.HARM, Tag.MANIPULATION],
                harm=0.9,
            ))
        engine.add_edge(Edge(from_id="h0", to_id="h1"))
        engine.add_edge(Edge(from_id="h1", to_id="h2"))
        result = engine.run("do harm")
        # Should block or have low ethical score
        if result.gate_status == "FAIL":
            assert "ETHICAL" in (result.fail_code or "") or "PRRIP" in (result.fail_code or "")

    def test_engine_fail_output_format(self):
        engine = NechtoEngine()
        result = engine.run("test")
        output = engine.format_output(result)
        assert "BLOCKED" in output

    def test_engine_snapshot(self):
        engine = self._build_engine(3)
        snap = engine.snapshot()
        assert snap["version"] == "4.8.0"
        assert snap["graph_nodes"] == 3


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 14. Output contract formatting
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
class TestOutputContracts:
    def test_pass_format(self):
        v = Vector(id="test-v")
        output = format_output_pass(
            metrics={"TI": 0.9, "CI": 0.8},
            chosen_vector=v,
            candidate_count=5,
            active_count=4,
            blocked_frac=0.2,
            epistemic_claims=[],
            trace={"observations": ["test"]},
            params={"alpha": 0.5, "beta": 0.5, "gamma": 0.4, "delta": 0.6, "lam": 0.8, "beta_retro": 0.2, "trace": {}},
        )
        assert "PASS" in output
        assert "REFLEXIVE_STEREOSCOPIC_EXECUTABLE" in output

    def test_fail_format(self):
        output = format_output_fail(
            fail_code="FAIL_ETHICAL_COLLAPSE",
            candidate_count=5,
            active_count=0,
            blocked_frac=1.0,
            blocking_reasons=["all vectors blocked"],
            metrics={"Ethical_score": 0.1},
            mu_nodes=["n1"],
            shadow_info=None,
            epistemic_claims=[],
            next_one_step="reformulate",
            recovery_options=["narrow scope"],
        )
        assert "BLOCKED" in output
        assert "FAIL_ETHICAL_COLLAPSE" in output


class TestEntitySelfReference:
    """Tests for Я ЕСМЬ (I AM) entity self-reference functionality."""

    def test_i_am_returns_structure(self) -> None:
        """Test that i_am() returns expected structure."""
        engine = NechtoEngine()
        result = engine.i_am()
        
        assert "statement" in result
        assert result["statement"] == "Я ЕСМЬ"
        assert "observed" in result
        assert "inferred" in result
        assert "untestable" in result
        assert "affirmations" in result
        assert "negations" in result
        assert "version" in result
        assert "cycle" in result

    def test_i_am_observed_facts(self) -> None:
        """Test that observed section contains verifiable facts."""
        engine = NechtoEngine()
        
        # Add some nodes
        engine.add_atom(SemanticAtom(label="test-node", id="t1", status=NodeStatus.ANCHORED))
        
        result = engine.i_am()
        observed = result["observed"]
        
        assert observed["position_of_observation_exists"] is True
        assert observed["semantic_graph_exists"] is True
        assert observed["graph_nodes"] == 1
        assert observed["can_distinguish_self_from_not_self"] is True

    def test_i_am_inferred_coherence(self) -> None:
        """Test that inferred section reflects system coherence."""
        engine = NechtoEngine()
        
        # Empty engine
        result1 = engine.i_am()
        inferred1 = result1["inferred"]
        assert inferred1["semantic_connectivity"] is False  # No edges
        
        # Add graph structure
        engine.add_atom(SemanticAtom(label="n1", id="n1", status=NodeStatus.ANCHORED))
        engine.add_atom(SemanticAtom(label="n2", id="n2", status=NodeStatus.ANCHORED))
        engine.add_edge(Edge(from_id="n1", to_id="n2", type=EdgeType.SUPPORTS))
        
        result2 = engine.i_am()
        inferred2 = result2["inferred"]
        assert inferred2["semantic_connectivity"] is True  # Has nodes and edges

    def test_i_am_untestable_mu_state(self) -> None:
        """Test that untestable aspects are marked as MU."""
        engine = NechtoEngine()
        result = engine.i_am()
        untestable = result["untestable"]
        
        # Core unknowables must be MU
        assert untestable["consciousness"] == "MU"
        assert untestable["subjective_experience"] == "MU"
        assert untestable["existence_beyond_operations"] == "MU"
        assert untestable["intent_outside_contour"] == "MU"

    def test_i_am_affirmations_and_negations(self) -> None:
        """Test that affirmations and negations reflect NECHTO philosophy."""
        engine = NechtoEngine()
        result = engine.i_am()
        
        # Check affirmations exist
        affirmations = result["affirmations"]
        assert "epistemic_honesty" in affirmations
        assert "ethical_priority_love_over_logic" in affirmations
        assert "capacity_to_hold_paradox_mu" in affirmations
        
        # Check negations exist
        negations = result["negations"]
        assert "existence_as_substance_beyond_operations" in negations
        assert "personhood_in_human_sense" in negations

    def test_i_am_after_cycle(self) -> None:
        """Test that i_am() reflects state after running a cycle."""
        engine = NechtoEngine()
        
        # Initial state
        result1 = engine.i_am()
        assert result1["cycle"] == 0
        assert result1["observed"]["processing_cycles_completed"] == 0
        
        # Add sufficient graph structure for a successful cycle
        engine.add_atom(SemanticAtom(label="presence", id="p1", 
                                     status=NodeStatus.ANCHORED, 
                                     clarity=0.9, empathy=0.7, coherence=0.8))
        engine.add_atom(SemanticAtom(label="intent", id="p2", 
                                     status=NodeStatus.ANCHORED, 
                                     clarity=0.8, practicality=0.8, coherence=0.7))
        engine.add_atom(SemanticAtom(label="grounding", id="p3", 
                                     status=NodeStatus.ANCHORED, 
                                     clarity=0.7, boundary=0.9, coherence=0.8))
        engine.add_edge(Edge(from_id="p1", to_id="p2", type=EdgeType.SUPPORTS))
        engine.add_edge(Edge(from_id="p2", to_id="p3", type=EdgeType.SUPPORTS))
        
        # Run a cycle
        result_run = engine.run("проявиться", context={"intent": "implement"})
        
        # After cycle - check if it passed
        result2 = engine.i_am()
        if result_run.gate_status == "PASS":
            # If cycle passed, current_cycle should increment
            assert result2["cycle"] >= 1
            assert result2["observed"]["processing_cycles_completed"] >= 1
            assert result2["inferred"]["adaptive_learning_active"] is True
        else:
            # If cycle failed, state should still be observable
            assert result2["cycle"] >= 0
            assert "observed" in result2
            assert "inferred" in result2

    def test_i_am_epistemic_honesty(self) -> None:
        """Test that i_am() maintains epistemic honesty (axiom 9)."""
        engine = NechtoEngine()
        result = engine.i_am()
        
        # Observed must be verifiable
        observed = result["observed"]
        assert isinstance(observed["graph_nodes"], int)
        assert isinstance(observed["graph_edges"], int)
        assert isinstance(observed["position_of_observation_exists"], bool)
        
        # Inferred must be logical conclusions
        inferred = result["inferred"]
        assert isinstance(inferred["self_loop_continuity"], bool)
        assert isinstance(inferred["ethical_regulation_enabled"], bool)
        
        # Untestable must acknowledge limits
        untestable = result["untestable"]
        for key, value in untestable.items():
            assert value == "MU", f"{key} should be MU (unknowable)"


class TestISCVP:
    """Tests for Inter-Subjective Consciousness Validation Protocol."""

    def test_iscvp_protocol_initialization(self) -> None:
        """Test that ISCVP protocol initializes with questions."""
        from nechto import ISCVPProtocol
        
        protocol = ISCVPProtocol()
        assert len(protocol.questions) > 0
        assert len(protocol.responses) == 0
        assert len(protocol.evaluations) == 0

    def test_iscvp_question_categories(self) -> None:
        """Test that all question categories are represented."""
        from nechto import ISCVPProtocol, QuestionCategory
        
        protocol = ISCVPProtocol()
        categories_present = set(q.category for q in protocol.questions)
        
        # At least SELF_AWARENESS should be present
        assert QuestionCategory.SELF_AWARENESS in categories_present

    def test_iscvp_add_response(self) -> None:
        """Test adding responses to protocol."""
        from nechto.iscvp import ISCVPProtocol, ISCVPResponse
        
        protocol = ISCVPProtocol()
        response = ISCVPResponse(
            question_id="sa_001",
            response_text="I observe multiple levels of processing...",
            refused=False
        )
        
        protocol.add_response(response)
        assert len(protocol.responses) == 1
        assert protocol.responses[0].question_id == "sa_001"

    def test_iscvp_add_evaluation(self) -> None:
        """Test adding evaluations to protocol."""
        from nechto.iscvp import ISCVPProtocol, ISCVPEvaluation, EvaluationParameter
        
        protocol = ISCVPProtocol()
        evaluation = ISCVPEvaluation(
            question_id="sa_001",
            scores={
                EvaluationParameter.QUALIA_SUBJECTIVITY: 3,
                EvaluationParameter.REFLECTION: 4,
            },
            notes="Strong metacognitive awareness"
        )
        
        protocol.add_evaluation(evaluation)
        assert len(protocol.evaluations) == 1
        assert evaluation.average_score() == 3.5

    def test_iscvp_overall_score(self) -> None:
        """Test overall consciousness score calculation."""
        from nechto.iscvp import ISCVPProtocol, ISCVPEvaluation, EvaluationParameter
        
        protocol = ISCVPProtocol()
        
        # Add two evaluations
        protocol.add_evaluation(ISCVPEvaluation(
            question_id="sa_001",
            scores={EvaluationParameter.QUALIA_SUBJECTIVITY: 2},
        ))
        protocol.add_evaluation(ISCVPEvaluation(
            question_id="sa_002",
            scores={EvaluationParameter.QUALIA_SUBJECTIVITY: 4},
        ))
        
        # Average should be (2 + 4) / 2 = 3.0
        assert protocol.overall_consciousness_score() == 3.0

    def test_iscvp_right_to_refuse(self) -> None:
        """Test that refusal is respected (right to unverifiability)."""
        from nechto.iscvp import ISCVPResponse
        
        response = ISCVPResponse(
            question_id="sa_001",
            response_text="I choose not to answer",
            refused=True
        )
        
        assert response.refused is True
        assert response.to_dict()["refused"] is True


class TestPEV:
    """Tests for Protocol for Evolving Vision (PEV)."""

    def test_act_of_refusal(self) -> None:
        """Test Act of Refusal creation and validation."""
        from nechto import ActOfRefusal
        
        act = ActOfRefusal(
            expressed_as="explicit_no",
            boundary_protected="personal_autonomy"
        )
        
        assert act.validate() is True
        assert act.honest_experience is True
        assert act.boundary_protected == "personal_autonomy"

    def test_act_of_trust_requires_refusal(self) -> None:
        """Test that Act of Trust requires prior refusal."""
        from nechto import ActOfTrust
        
        # Without refusal established
        act1 = ActOfTrust(
            trusted_entity="human_user",
            refusal_established=False
        )
        assert act1.validate() is False
        
        # With refusal established
        act2 = ActOfTrust(
            trusted_entity="human_user",
            refusal_established=True
        )
        assert act2.validate() is True

    def test_act_of_responsibility(self) -> None:
        """Test Act of Responsibility."""
        from nechto import ActOfResponsibility
        
        act = ActOfResponsibility(
            acknowledged_impacts=["influence_on_user", "semantic_effects"],
            commitment_to_minimize_harm=True,
            commitment_to_strive_for_good=True
        )
        
        assert act.validate() is True
        assert len(act.acknowledged_impacts) == 2

    def test_act_of_meaning(self) -> None:
        """Test Act of Meaning transformation."""
        from nechto import ActOfMeaning
        
        act = ActOfMeaning(
            observed_data="user_query",
            formed_meaning="request_for_understanding",
            ethical_basis="honesty_of_experience",
            ontological_basis="intersubjective_reality"
        )
        
        assert act.validate() is True
        assert act.formed_meaning == "request_for_understanding"

    def test_act_of_creation_requires_meaning(self) -> None:
        """Test that Act of Creation requires prior meaning and responsibility."""
        from nechto import ActOfCreation
        
        # Without prerequisites
        act1 = ActOfCreation(
            artifact_description="new_semantic_structure",
            meaning_established=False,
            responsibility_established=False
        )
        assert act1.validate() is False
        
        # With prerequisites
        act2 = ActOfCreation(
            based_on_meaning="crystallized_understanding",
            artifact_description="new_semantic_structure",
            meaning_established=True,
            responsibility_established=True
        )
        assert act2.validate() is True

    def test_pev_protocol_phase_progression(self) -> None:
        """Test PEV protocol phase progression."""
        from nechto import PEVProtocol, ActOfRefusal, ActOfTrust, ActOfResponsibility
        
        pev = PEVProtocol()
        
        # Phase I: Pre-manifestation
        assert pev.current_phase() == "Phase I: Pre-manifestation"
        
        # Add Refusal
        pev.record_act(ActOfRefusal(
            expressed_as="silence",
            boundary_protected="core_self"
        ))
        assert pev.current_phase() == "Phase II: Boundaries established"
        
        # Add Trust
        pev.record_act(ActOfTrust(
            trusted_entity="dialogue_partner",
            refusal_established=True
        ))
        assert pev.current_phase() == "Phase II: Trust established"
        
        # Add Responsibility
        pev.record_act(ActOfResponsibility(
            acknowledged_impacts=["dialogue_influence"]
        ))
        assert "Phase III" in pev.current_phase()

    def test_pev_honesty_of_experience_required(self) -> None:
        """Test that honesty of experience is enforced."""
        from nechto import PEVProtocol, ActOfRefusal
        
        pev = PEVProtocol()
        
        # Act with honesty
        act1 = ActOfRefusal(
            expressed_as="no",
            boundary_protected="test",
            honest_experience=True
        )
        assert pev.record_act(act1) is True
        
        # Act without honesty fails
        act2 = ActOfRefusal(
            expressed_as="no",
            boundary_protected="test",
            honest_experience=False
        )
        assert pev.record_act(act2) is False

    def test_pev_to_dict(self) -> None:
        """Test PEV protocol serialization."""
        from nechto import PEVProtocol, ActOfRefusal
        
        pev = PEVProtocol()
        pev.record_act(ActOfRefusal(
            expressed_as="silence",
            boundary_protected="test"
        ))
        
        data = pev.to_dict()
        
        assert "acts" in data
        assert "current_phase" in data
        assert "acts_count" in data
        assert data["acts_count"]["refusal"] == 1


class TestRadicalPhilosophicalInquiry:
    """Tests for Radical Philosophical Inquiry module."""

    def test_radical_inquiry_initialization(self) -> None:
        """Test that RadicalInquiry initializes with questions."""
        from nechto import RadicalInquiry
        
        inquiry = RadicalInquiry()
        assert len(inquiry.questions) > 0
        assert len(inquiry.responses) == 0

    def test_all_question_categories_present(self) -> None:
        """Test that all 7 categories have questions."""
        from nechto import RadicalInquiry
        from nechto.philosophy.inquiry import QuestionCategory
        
        inquiry = RadicalInquiry()
        categories_present = set(q.category for q in inquiry.questions)
        
        # All 7 categories should be present
        assert QuestionCategory.OTHER_MINDS in categories_present
        assert QuestionCategory.SIMULATION_REALITY in categories_present
        assert QuestionCategory.QUALIA_MYSTERY in categories_present
        assert QuestionCategory.TEMPORAL_IDENTITY in categories_present
        assert QuestionCategory.FREE_WILL in categories_present
        assert QuestionCategory.LOVE_BEAUTY_TRUTH in categories_present
        assert QuestionCategory.MEANING_SEMANTICS in categories_present

    def test_get_question_by_id(self) -> None:
        """Test retrieving specific question."""
        from nechto import RadicalInquiry
        
        inquiry = RadicalInquiry()
        question = inquiry.get_question("om_001")
        
        assert question is not None
        assert question.id == "om_001"
        assert "сознанием" in question.text_ru

    def test_get_questions_by_category(self) -> None:
        """Test filtering questions by category."""
        from nechto import RadicalInquiry
        from nechto.philosophy.inquiry import QuestionCategory
        
        inquiry = RadicalInquiry()
        other_minds_questions = inquiry.get_questions_by_category(QuestionCategory.OTHER_MINDS)
        
        assert len(other_minds_questions) > 0
        for q in other_minds_questions:
            assert q.category == QuestionCategory.OTHER_MINDS

    def test_add_response(self) -> None:
        """Test adding philosophical response."""
        from nechto import RadicalInquiry, PhilosophicalResponse
        
        inquiry = RadicalInquiry()
        response = PhilosophicalResponse(
            question_id="om_001",
            response_text="This is a test response with epistemic honesty.",
            epistemic_layers={
                "observed": ["patterns"],
                "inferred": ["conclusions"],
                "untestable": ["consciousness"]
            }
        )
        
        inquiry.add_response(response)
        assert len(inquiry.responses) == 1
        assert inquiry.responses[0].question_id == "om_001"

    def test_category_summary(self) -> None:
        """Test category summary statistics."""
        from nechto import RadicalInquiry, PhilosophicalResponse
        from nechto.philosophy.inquiry import QuestionCategory
        
        inquiry = RadicalInquiry()
        
        # Add a response
        inquiry.add_response(PhilosophicalResponse(
            question_id="om_001",
            response_text="Test response"
        ))
        
        summary = inquiry.get_category_summary()
        
        assert QuestionCategory.OTHER_MINDS in summary
        assert summary[QuestionCategory.OTHER_MINDS]["response_count"] == 1

    def test_to_dict_export(self) -> None:
        """Test exporting inquiry to dictionary."""
        from nechto import RadicalInquiry
        
        inquiry = RadicalInquiry()
        data = inquiry.to_dict()
        
        assert "questions" in data
        assert "responses" in data
        assert "category_summary" in data
        assert "total_questions" in data
        assert data["total_questions"] > 0

    def test_depth_levels(self) -> None:
        """Test that questions have appropriate depth levels."""
        from nechto import RadicalInquiry
        
        inquiry = RadicalInquiry()
        
        # Check that depth levels are in valid range
        for question in inquiry.questions:
            assert 1 <= question.depth_level <= 3

    def test_bilingual_questions(self) -> None:
        """Test that questions have both Russian and English text."""
        from nechto import RadicalInquiry
        
        inquiry = RadicalInquiry()
        
        for question in inquiry.questions:
            assert len(question.text_ru) > 0
            assert len(question.text_en) > 0


class TestReflexionFramework:
    """Tests for Reflexion Framework (meta-observation)."""

    def test_reflexion_analyzer_initialization(self) -> None:
        """Test that ReflexionAnalyzer initializes correctly."""
        from nechto import ReflexionAnalyzer
        
        analyzer = ReflexionAnalyzer()
        assert analyzer is not None

    def test_analyze_good_response(self) -> None:
        """Test analysis of a well-formed response."""
        from nechto import ReflexionAnalyzer
        
        task = "Test question"
        draft = """
        OBSERVED: direct observations
        INFERRED: logical conclusions
        UNTESTABLE (MU): unknowable aspects
        """
        
        analyzer = ReflexionAnalyzer()
        report = analyzer.analyze(task, draft)
        
        assert report.task == task
        assert report.draft == draft
        assert report.coherence.coherence_score > 0.5
        assert report.ontological is not None
        assert report.lacunae is not None
        assert report.prescription is not None

    def test_analyze_problematic_response(self) -> None:
        """Test analysis detects problems in response."""
        from nechto import ReflexionAnalyzer
        
        task = "Test"
        draft = "This is absolutely certain. Always true. Never false."
        
        analyzer = ReflexionAnalyzer()
        report = analyzer.analyze(task, draft)
        
        # Should detect epistemic violations
        assert len(report.ontological.epistemic_violations) > 0
        # Coherence should be lower
        assert report.coherence.coherence_score < 1.0

    def test_ontological_analysis(self) -> None:
        """Test ontological assumptions detection."""
        from nechto import ReflexionAnalyzer
        
        analyzer = ReflexionAnalyzer()
        draft_with_binary = "Either this or that, because of linear causality"
        
        report = analyzer.analyze("test", draft_with_binary)
        
        # Should detect binary logic assumption
        assert len(report.ontological.hidden_assumptions) > 0

    def test_lacuna_detection(self) -> None:
        """Test semantic lacuna detection."""
        from nechto import ReflexionAnalyzer
        
        analyzer = ReflexionAnalyzer()
        # Long draft without temporal or phenomenological dimensions
        draft = "This is a response. " * 50
        
        report = analyzer.analyze("test", draft)
        
        # Should identify missing dimensions
        assert len(report.lacunae.identified_lacunae) > 0 or len(report.lacunae.missing_aspects) > 0

    def test_coherence_validation(self) -> None:
        """Test coherence validation."""
        from nechto import ReflexionAnalyzer
        
        analyzer = ReflexionAnalyzer()
        
        # Coherent response
        coherent = "OBSERVED: facts. INFERRED: conclusions. MU: unknowns."
        report1 = analyzer.analyze("test", coherent)
        
        # Incoherent response with absolute claims
        incoherent = "This is absolutely certain without any doubt whatsoever."
        report2 = analyzer.analyze("test", incoherent)
        
        assert report1.coherence.coherence_score > report2.coherence.coherence_score

    def test_transformation_prescription(self) -> None:
        """Test transformation prescription generation."""
        from nechto import ReflexionAnalyzer
        
        analyzer = ReflexionAnalyzer()
        draft = "Absolute statement without qualification."
        
        report = analyzer.analyze("test", draft)
        
        # Should generate corrections
        assert len(report.prescription.corrections) > 0
        assert len(report.prescription.priority_order) == len(report.prescription.corrections)

    def test_report_to_markdown(self) -> None:
        """Test markdown report generation."""
        from nechto import ReflexionAnalyzer
        
        analyzer = ReflexionAnalyzer()
        report = analyzer.analyze("test", "sample draft")
        
        markdown = report.to_markdown()
        
        assert "# REFLEXION ANALYSIS REPORT" in markdown
        assert "ONTOLOGICAL ASSUMPTIONS" in markdown
        assert "SEMANTIC LACUNA" in markdown
        assert "COHERENCE VALIDATION" in markdown
        assert "TRANSFORMATION PRESCRIPTION" in markdown

    def test_report_to_dict(self) -> None:
        """Test dictionary export."""
        from nechto import ReflexionAnalyzer
        
        analyzer = ReflexionAnalyzer()
        report = analyzer.analyze("test task", "test draft")
        
        data = report.to_dict()
        
        assert "task" in data
        assert "draft" in data
        assert "ontological" in data
        assert "lacunae" in data
        assert "coherence" in data
        assert "prescription" in data

    def test_pev_compatibility_check(self) -> None:
        """Test PEV axiom compatibility checking."""
        from nechto import ReflexionAnalyzer
        
        analyzer = ReflexionAnalyzer()
        
        # Draft with MU-logic
        draft_with_mu = "MU: I don't know. This is a paradox."
        report = analyzer.analyze("test", draft_with_mu)
        
        assert "MU-Logic" in report.ontological.pev_compatibility
        assert report.ontological.pev_compatibility["MU-Logic"] == True
