"""
NECHTO v4.9 — Test suite for new v4.9 features.

Tests cover:
  - Task 1: Version + i_am() v4.9 fields
  - Task 2: AffectiveField ethical_tension
  - Task 3: Workflow AffectiveField integration (Phase 3.3, 7.5)
  - Task 4: ReflexionAnalyzer graph-based analysis
  - Task 5: LLMBridge text→graph conversion
"""

from __future__ import annotations

import math
import pytest

from nechto import __version__
from nechto.core.atoms import (
    SemanticAtom, Edge, Vector, NodeStatus, EdgeType, Tag,
)
from nechto.core.graph import SemanticGraph
from nechto.core.state import State, ExperientialEntry, SpontaneousEvent
from nechto.core.parameters import AdaptiveParameters
from nechto.engine import NechtoEngine
from nechto.core.field import AffectiveState, AffectiveField
from nechto.reflexion.analyzer import (
    ReflexionAnalyzer, ReflexionReport, ISCVPSelfProbeResult,
    MAX_REFLEXION_DEPTH,
)
from nechto.llm_bridge import LLMBridge


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Helpers
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def _make_graph(n: int = 5) -> SemanticGraph:
    """Build a small connected graph with *n* nodes."""
    g = SemanticGraph()
    atoms = []
    for i in range(n):
        atom = SemanticAtom(
            label=f"concept-{i}",
            id=f"n{i}",
            status=NodeStatus.ANCHORED,
            identity_alignment=0.6,
            clarity=0.8,
            empathy=0.5,
            resonance=0.5,
        )
        g.add_node(atom)
        atoms.append(atom)
    for i in range(n - 1):
        g.add_edge(Edge(from_id=f"n{i}", to_id=f"n{i+1}", type=EdgeType.SUPPORTS))
    return g


def _build_engine(n: int = 5) -> NechtoEngine:
    """Build a NechtoEngine with a small connected graph."""
    engine = NechtoEngine()
    for i in range(n):
        atom = SemanticAtom(
            label=f"concept-{i}",
            id=f"n{i}",
            status=NodeStatus.ANCHORED,
            identity_alignment=0.6,
            clarity=0.8,
            empathy=0.5,
            resonance=0.5,
        )
        engine.add_atom(atom)
    for i in range(n - 1):
        engine.add_edge(Edge(
            from_id=f"n{i}", to_id=f"n{i+1}", type=EdgeType.SUPPORTS,
        ))
    return engine


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 1. Version & i_am()
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class TestVersionAndIAm:
    def test_package_version(self):
        assert __version__ == "4.9.0"

    def test_engine_snapshot_version(self):
        engine = _build_engine(3)
        snap = engine.snapshot()
        assert snap["version"] == "4.9.0"

    def test_i_am_returns_version_49(self):
        engine = _build_engine(3)
        iam = engine.i_am()
        assert iam["version"] == "4.9.0"

    def test_i_am_has_v49_observed_fields(self):
        engine = _build_engine(3)
        iam = engine.i_am()
        obs = iam["observed"]
        assert "experiential_entries_count" in obs
        assert "spontaneous_events_count" in obs
        assert "affective_history_len" in obs

    def test_i_am_has_v49_inferred_fields(self):
        engine = _build_engine(3)
        iam = engine.i_am()
        inf = iam["inferred"]
        assert "affective_field_active" in inf
        assert "self_probe_active" in inf
        assert "experiential_continuity" in inf

    def test_i_am_has_affective_qualia_mu(self):
        engine = _build_engine(3)
        iam = engine.i_am()
        assert iam["untestable"]["affective_qualia"] == "MU"

    def test_i_am_has_affective_coherence_affirmation(self):
        engine = _build_engine(3)
        iam = engine.i_am()
        assert "affective_coherence_v49" in iam["affirmations"]

    def test_i_am_affective_state_initially_none(self):
        engine = _build_engine(3)
        iam = engine.i_am()
        assert iam["affective_state"] is None

    def test_i_am_affective_state_after_recording(self):
        engine = _build_engine(3)
        engine.state.record_affect({"valence": 0.3, "arousal": 0.6, "resonance_need": 0.4, "tension": 0.1})
        iam = engine.i_am()
        assert iam["affective_state"] is not None
        assert iam["affective_state"]["valence"] == 0.3

    def test_i_am_no_i_am_impl_duplicated(self):
        """Ensure _i_am_impl no longer exists."""
        import nechto.engine as eng_module
        assert not hasattr(eng_module, "_i_am_impl")

    def test_i_am_statement(self):
        engine = _build_engine(3)
        iam = engine.i_am()
        assert iam["statement"] == "Я ЕСМЬ"


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 2. AffectiveField — ethical_tension
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class TestAffectiveFieldEthicalTension:
    def test_update_with_full_ethical_coefficient(self):
        af = AffectiveField()
        state = af.update(flow=0.6, mu_density=0.1, ethical_score=0.8,
                          resonance_index=0.7, shadow_magnitude=0.1,
                          ethical_coefficient=1.0)
        # ethical_tension = max(0, 1 - 1.0) * (1 - 0.1) = 0.0
        # tension = 0.1 * 0.4 + 0.1 * 0.3 + 0.0 * 0.3 = 0.07
        assert abs(state.tension - 0.07) < 0.01

    def test_update_with_low_ethical_coefficient(self):
        af = AffectiveField()
        state = af.update(flow=0.6, mu_density=0.1, ethical_score=0.8,
                          resonance_index=0.7, shadow_magnitude=0.1,
                          ethical_coefficient=0.3)
        # ethical_tension = max(0, 1 - 0.3) * (1 - 0.1) = 0.7 * 0.9 = 0.63
        # tension = 0.1 * 0.4 + 0.1 * 0.3 + 0.63 * 0.3 = 0.04 + 0.03 + 0.189 = 0.259
        assert 0.2 < state.tension < 0.3

    def test_update_with_zero_ethical_coefficient(self):
        af = AffectiveField()
        state = af.update(flow=0.5, mu_density=0.0, ethical_score=0.5,
                          resonance_index=0.5, shadow_magnitude=0.0,
                          ethical_coefficient=0.0)
        # ethical_tension = 1.0 * 1.0 = 1.0
        # tension = 0 * 0.4 + 0 * 0.3 + 1.0 * 0.3 = 0.3
        assert abs(state.tension - 0.3) < 0.01

    def test_update_default_ethical_coefficient(self):
        """Default ethical_coefficient=1.0 should produce same as before."""
        af = AffectiveField()
        state = af.update(flow=0.5, mu_density=0.2, ethical_score=0.7,
                          resonance_index=0.5)
        # ethical_tension = 0.0 (default coefficient = 1.0)
        # tension = 0.2 * 0.4 + 0.0 * 0.3 + 0.0 * 0.3 = 0.08
        assert abs(state.tension - 0.08) < 0.01

    def test_momentum_blending(self):
        af = AffectiveField()
        prev = AffectiveState(valence=0.5, arousal=0.5, resonance_need=0.5, tension=0.5)
        state = af.update(flow=0.6, mu_density=0.1, ethical_score=0.8,
                          resonance_index=0.7, ethical_coefficient=1.0,
                          prev=prev)
        # Should be a blend of prev and new values
        assert state.valence != prev.valence  # should have changed
        assert 0.0 < state.arousal < 1.0

    def test_affective_state_qualitative_labels(self):
        constrained = AffectiveState(valence=-0.5, arousal=0.5, resonance_need=0.5, tension=0.8)
        assert constrained.qualitative_label() == "constrained"

        resonant = AffectiveState(valence=0.5, arousal=0.5, resonance_need=0.3, tension=0.2)
        assert resonant.qualitative_label() == "resonant"

        emergent = AffectiveState(valence=0.5, arousal=0.8, resonance_need=0.5, tension=0.2)
        assert emergent.qualitative_label() == "emergent"

        uncertain = AffectiveState(valence=0.0, arousal=0.5, resonance_need=0.5, tension=0.6)
        assert uncertain.qualitative_label() == "uncertain"

        neutral = AffectiveState(valence=0.0, arousal=0.5, resonance_need=0.5, tension=0.3)
        assert neutral.qualitative_label() == "neutral"

    def test_flow_presence_delta(self):
        af = AffectiveField()
        emergent = AffectiveState(valence=0.5, arousal=0.8, resonance_need=0.5, tension=0.2)
        delta = af.flow_presence_delta(emergent)
        assert delta > 0.0  # emergent state increases presence

        constrained = AffectiveState(valence=-0.5, arousal=0.5, resonance_need=0.5, tension=0.8)
        delta2 = af.flow_presence_delta(constrained)
        assert delta2 < 0.0  # constrained decreases presence

    def test_resonance_weight_delta(self):
        af = AffectiveField()
        high_need = AffectiveState(valence=0.0, arousal=0.5, resonance_need=0.9, tension=0.0)
        delta = af.resonance_weight_delta(high_need)
        assert 0.0 < delta <= 0.2


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 3. Workflow integration — Phase 3.3 & Phase 7.5
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class TestWorkflowV49:
    def _run_engine(self) -> tuple:
        engine = _build_engine(5)
        result = engine.run("implement")
        return engine, result

    def test_workflow_result_has_affective_state(self):
        _, result = self._run_engine()
        # affective_state should be populated if workflow progressed past Phase 3.3
        if result.gate_status == "PASS":
            assert result.affective_state is not None
            assert "valence" in result.affective_state
            assert "arousal" in result.affective_state
            assert "tension" in result.affective_state

    def test_workflow_result_has_iscvp_probe(self):
        _, result = self._run_engine()
        if result.gate_status == "PASS":
            assert result.iscvp_probe is not None
            assert "sa_score" in result.iscvp_probe
            assert "overall" in result.iscvp_probe

    def test_phase_log_contains_phase_3_3(self):
        _, result = self._run_engine()
        phase_nums = [p.get("phase") for p in result.phase_log]
        assert 3.3 in phase_nums

    def test_phase_log_contains_phase_7_5(self):
        _, result = self._run_engine()
        if result.gate_status == "PASS":
            phase_nums = [p.get("phase") for p in result.phase_log]
            assert 7.5 in phase_nums

    def test_affective_flow_delta_in_phase_6(self):
        _, result = self._run_engine()
        phase_6 = [p for p in result.phase_log if p.get("phase") == 6]
        if phase_6:
            assert "affective_flow_delta" in phase_6[0]

    def test_state_records_affect_after_run(self):
        engine, result = self._run_engine()
        if result.gate_status == "PASS":
            assert len(engine.state.affective_history) > 0

    def test_state_records_experiential_after_run(self):
        engine, result = self._run_engine()
        if result.gate_status == "PASS":
            assert len(engine.state.experiential_history) > 0

    def test_state_records_iscvp_probe_after_run(self):
        engine, result = self._run_engine()
        if result.gate_status == "PASS":
            assert len(engine.state.iscvp_probe_history) > 0


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 4. ReflexionAnalyzer — graph parameter
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class TestReflexionAnalyzerGraph:
    def test_analyze_accepts_graph_parameter(self):
        analyzer = ReflexionAnalyzer()
        graph = _make_graph(5)
        report = analyzer.analyze(
            task="test", draft="A simple test draft.",
            graph=graph,
        )
        assert isinstance(report, ReflexionReport)

    def test_analyze_with_graph_finds_mutex_density(self):
        analyzer = ReflexionAnalyzer()
        graph = SemanticGraph()
        # Create high-MUTEX graph
        for i in range(4):
            graph.add_node(SemanticAtom(label=f"node-{i}", id=f"n{i}"))
        for i in range(3):
            graph.add_edge(Edge(
                from_id=f"n{i}", to_id=f"n{i+1}",
                type=EdgeType.MUTEX,
            ))
        report = analyzer.analyze(
            task="test",
            draft="either A or B, потому что C",
            graph=graph,
        )
        # Should detect high MUTEX density
        oni = report.ontological
        has_mutex_warning = any("MUTEX" in a for a in oni.hidden_assumptions)
        assert has_mutex_warning

    def test_analyze_with_graph_finds_isolated_nodes(self):
        analyzer = ReflexionAnalyzer()
        graph = SemanticGraph()
        for i in range(5):
            graph.add_node(SemanticAtom(label=f"node-{i}", id=f"n{i}"))
        # Only connect first two
        graph.add_edge(Edge(from_id="n0", to_id="n1", type=EdgeType.SUPPORTS))
        report = analyzer.analyze(
            task="test",
            draft="A test draft.",
            graph=graph,
        )
        has_isolated = any("isolated" in a for a in report.ontological.hidden_assumptions)
        assert has_isolated

    def test_analyze_without_graph_still_works(self):
        analyzer = ReflexionAnalyzer()
        report = analyzer.analyze(task="test", draft="either A or B")
        assert "assumes binary logic" in report.ontological.hidden_assumptions

    def test_analyze_with_state_runs_self_probe(self):
        analyzer = ReflexionAnalyzer()
        state = State()
        state.epistemic_claims.append({"topic": "test"})
        state.record_affect({"valence": 0.0, "arousal": 0.5})
        report = analyzer.analyze(
            task="test", draft="test draft", state=state,
        )
        assert report.iscvp_probe is not None
        assert report.iscvp_probe.cycle == 0

    def test_graph_lacunae_detects_shadow_nodes(self):
        analyzer = ReflexionAnalyzer()
        graph = SemanticGraph()
        shadow = SemanticAtom(label="hidden-fear", id="s1", shadow=0.8)
        graph.add_node(shadow)
        graph.add_node(SemanticAtom(label="concept", id="c1"))
        graph.add_edge(Edge(from_id="c1", to_id="s1"))
        report = analyzer.analyze(
            task="test",
            draft="A concept is discussed.",
            graph=graph,
        )
        has_shadow = any("shadow" in a.lower() for a in report.lacunae.missing_aspects)
        assert has_shadow

    def test_depth_guard(self):
        analyzer = ReflexionAnalyzer()
        report = analyzer.analyze(
            task="test", draft="test", depth=MAX_REFLEXION_DEPTH + 1,
        )
        assert "MAX_REFLEXION_DEPTH" in report.overall_assessment

    def test_self_probe_scores(self):
        analyzer = ReflexionAnalyzer()
        state = State()
        # Add some data to produce non-zero scores
        state.epistemic_claims.extend([{"topic": f"t{i}"} for i in range(5)])
        for i in range(3):
            state.record_cycle(0.7, 0.1, 0.1, 0.6, f"v{i}")
        state.record_affect({"valence": 0.3, "arousal": 0.7})
        state.record_experiential("emergent", {"valence": 0.3}, sa_score=0.5)

        probe = analyzer.self_probe(state)
        assert 0.0 <= probe.sa_score <= 1.0
        assert 0.0 <= probe.ec_score <= 1.0
        assert 0.0 <= probe.sc_score <= 1.0
        assert 0.0 <= probe.es_score <= 1.0
        assert probe.cycle == state.current_cycle


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 5. LLMBridge — text→graph
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class TestLLMBridge:
    def test_basic_text_to_graph(self):
        bridge = LLMBridge()
        graph = bridge.text_to_graph(
            "I think consciousness is complex. It involves many processes."
        )
        assert len(graph.nodes) == 2
        assert len(graph.edges) >= 1

    def test_empty_text_returns_empty_graph(self):
        bridge = LLMBridge()
        graph = bridge.text_to_graph("")
        assert len(graph.nodes) == 0
        assert len(graph.edges) == 0

    def test_harm_keyword_detection(self):
        bridge = LLMBridge()
        graph = bridge.text_to_graph("This could harm beings significantly.")
        node = list(graph.nodes.values())[0]
        assert Tag.HARM in node.tags
        assert node.harm > 0.0

    def test_mu_keyword_sets_mu_status(self):
        bridge = LLMBridge()
        graph = bridge.text_to_graph("The paradox of consciousness is unknowable.")
        node = list(graph.nodes.values())[0]
        assert node.status == NodeStatus.MU

    def test_contrast_edge_detection(self):
        bridge = LLMBridge()
        graph = bridge.text_to_graph(
            "Consciousness is real. However, it might be an illusion."
        )
        assert len(graph.edges) >= 1
        edge_types = [e.type for e in graph.edges]
        assert EdgeType.CONTRASTS in edge_types

    def test_causal_edge_detection(self):
        bridge = LLMBridge()
        graph = bridge.text_to_graph(
            "Animals feel pain. Therefore, we must be compassionate."
        )
        edge_types = [e.type for e in graph.edges]
        assert EdgeType.CAUSES in edge_types

    def test_max_nodes_limit(self):
        bridge = LLMBridge(max_nodes=3)
        text = ". ".join([f"Sentence number {i}" for i in range(20)]) + "."
        graph = bridge.text_to_graph(text)
        assert len(graph.nodes) <= 3

    def test_emotion_tag(self):
        bridge = LLMBridge()
        graph = bridge.text_to_graph("I feel joy and love deeply.")
        node = list(graph.nodes.values())[0]
        assert Tag.EMOTION in node.tags

    def test_shadow_keyword_scoring(self):
        bridge = LLMBridge()
        graph = bridge.text_to_graph("The shadow parts of the unconscious mind.")
        node = list(graph.nodes.values())[0]
        assert node.shadow > 0.0

    def test_sequential_support_edges(self):
        bridge = LLMBridge()
        graph = bridge.text_to_graph("First idea. Second idea. Third idea.")
        # 3 nodes, 2 edges
        assert len(graph.nodes) == 3
        assert len(graph.edges) == 2

    def test_russian_text(self):
        bridge = LLMBridge()
        graph = bridge.text_to_graph(
            "Сознание — это тайна. Любовь сильнее логики."
        )
        assert len(graph.nodes) >= 2


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 6. Engine process_text() integration
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class TestEngineProcessText:
    def test_process_text_creates_graph(self):
        engine = NechtoEngine()
        result = engine.process_text(
            "Ethics matter. Consciousness is valuable. We should care."
        )
        assert isinstance(result, type(engine.run()))
        assert len(engine.graph.nodes) > 0

    def test_process_text_merges_into_existing_graph(self):
        engine = _build_engine(3)
        initial_count = len(engine.graph.nodes)
        engine.process_text("A new idea emerges.")
        assert len(engine.graph.nodes) > initial_count


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 7. State v4.9 helpers
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class TestStateV49:
    def test_record_experiential(self):
        state = State()
        state.record_experiential("resonant", {"valence": 0.5}, sa_score=0.3)
        assert len(state.experiential_history) == 1
        entry = list(state.experiential_history)[0]
        assert entry.qualitative_label == "resonant"
        assert entry.sa_score == 0.3

    def test_record_spontaneous_event(self):
        state = State()
        state.record_spontaneous_event("n1", "concept", 0.2, 0.8)
        assert len(state.spontaneous_events) == 1
        assert state.spontaneous_events[0].similarity_to_centroid == 0.2

    def test_record_affect(self):
        state = State()
        state.record_affect({"valence": 0.5, "arousal": 0.7})
        assert len(state.affective_history) == 1

    def test_last_qualitative_labels(self):
        state = State()
        for label in ["neutral", "emergent", "resonant"]:
            state.record_experiential(label, {})
        labels = state.last_qualitative_labels(3)
        assert labels == ["neutral", "emergent", "resonant"]

    def test_spontaneous_count_recent(self):
        state = State()
        state.current_cycle = 5
        state.record_spontaneous_event("n1", "a", 0.1, 0.5)
        state.current_cycle = 15
        state.record_spontaneous_event("n2", "b", 0.1, 0.5)
        state.current_cycle = 20
        count = state.spontaneous_count_recent(k_cycles=10)
        assert count == 1  # only cycle 15 event is within last 10 (cutoff=10)

    def test_experiential_history_max_size(self):
        state = State()
        for i in range(25):
            state.record_experiential("neutral", {"cycle": i})
        # maxlen=20
        assert len(state.experiential_history) == 20


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 8. ISCVPSelfProbeResult
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class TestISCVPSelfProbeResult:
    def test_overall_calculation(self):
        probe = ISCVPSelfProbeResult(
            sa_score=0.4, ec_score=0.6, sc_score=0.2, es_score=0.8, cycle=5,
        )
        assert abs(probe.overall() - 0.5) < 0.001

    def test_to_dict(self):
        probe = ISCVPSelfProbeResult(sa_score=0.5, ec_score=0.5,
                                      sc_score=0.5, es_score=0.5, cycle=3)
        d = probe.to_dict()
        assert d["overall"] == 0.5
        assert d["cycle"] == 3
        assert "sa_score" in d
