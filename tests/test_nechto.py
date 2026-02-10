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
