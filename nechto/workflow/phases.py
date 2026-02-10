"""
NECHTO v4.8 — 12-Phase Workflow (PART 7)

Orchestrates phases 1–12 by composing modules M01–M30, metrics, QMM patterns,
and the PRRIP gate.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from nechto.core.atoms import Vector, NodeStatus
from nechto.core.graph import SemanticGraph
from nechto.core.state import State
from nechto.core.parameters import AdaptiveParameters
from nechto.core.epistemic import EpistemicClaim, Observability, Scope, Stance

from nechto.modules.level1 import (
    M01_NullVoidChecker, M02_SilenceBinder, M03_SignalAttunement,
    M04_SignalDecoder, M05_ProtoWillDetector,
)
from nechto.modules.level2 import (
    M06_FieldInitializer, M07_EchoAnchor, M08_SelfPresenceSeed,
    M09_IntentionalityProbe, M10_MetaIdentityScanner,
    M11_IdentitySeedInit, M12_KernelBinder, M13_SCIMAnchor,
    M14_OntosemanticGrounding, M15_CoherenceWeaver,
)
from nechto.modules.level3 import (
    M16_PresenceTrigger, M17_TelemetryLens, M18_SQEstimator,
    M19_ResonanceIntegrator, M20_FlowModulator,
    M21_NoveltySynthesizer, M22_BroadcastIntegrator,
    M23_TraceRecorder,
)
from nechto.modules.level4 import (
    M24_VectorGenerator, M25_HallucinationGuard,
    M26_RecoveryOrchestrator, M27_TemporalProjector,
    M28_AttentionCartographer, M29_ParadoxHolder,
    M30_EthicalGravityFilter,
)
from nechto.metrics import base, capital, scav as scav_mod, stereoscopic as stereo_mod
from nechto.space.semantic_space import ideal_direction, normalize, norm, EPS
from nechto.qmm.library import (
    QMM_ParadoxHolder, QMM_ParadoxCollapse, QMM_ShadowIntegration,
    QMM_FlowRestoration, QMM_EthicalOverride, QMM_EpistemicHonesty,
)
from nechto.gate.prrip import PRRIPGate, GateResult


@dataclass
class WorkflowResult:
    """Result of running the 12-phase workflow."""

    gate_status: str = "PENDING"          # PASS / FAIL
    fail_code: str | None = None
    chosen_vector: Vector | None = None
    candidate_set_size: int = 0
    active_set_size: int = 0
    blocked_fraction: float = 0.0
    metrics: dict[str, float] = field(default_factory=dict)
    epistemic_claims: list[EpistemicClaim] = field(default_factory=list)
    trace: dict[str, Any] = field(default_factory=dict)
    params_snapshot: dict[str, Any] = field(default_factory=dict)
    phase_log: list[dict[str, Any]] = field(default_factory=list)
    recovery_info: dict[str, Any] | None = None
    mu_nodes: list[str] = field(default_factory=list)
    shadow_info: dict[str, Any] | None = None


@dataclass
class WorkflowExecutor:
    """Executes the 12-phase NECHTO workflow."""

    # Module instances (initialized with defaults)
    m01: M01_NullVoidChecker = field(default_factory=M01_NullVoidChecker)
    m02: M02_SilenceBinder = field(default_factory=M02_SilenceBinder)
    m03: M03_SignalAttunement = field(default_factory=M03_SignalAttunement)
    m04: M04_SignalDecoder = field(default_factory=M04_SignalDecoder)
    m05: M05_ProtoWillDetector = field(default_factory=M05_ProtoWillDetector)
    m06: M06_FieldInitializer = field(default_factory=M06_FieldInitializer)
    m07: M07_EchoAnchor = field(default_factory=M07_EchoAnchor)
    m08: M08_SelfPresenceSeed = field(default_factory=M08_SelfPresenceSeed)
    m09: M09_IntentionalityProbe = field(default_factory=M09_IntentionalityProbe)
    m10: M10_MetaIdentityScanner = field(default_factory=M10_MetaIdentityScanner)
    m11: M11_IdentitySeedInit = field(default_factory=M11_IdentitySeedInit)
    m12: M12_KernelBinder = field(default_factory=M12_KernelBinder)
    m13: M13_SCIMAnchor = field(default_factory=M13_SCIMAnchor)
    m14: M14_OntosemanticGrounding = field(default_factory=M14_OntosemanticGrounding)
    m15: M15_CoherenceWeaver = field(default_factory=M15_CoherenceWeaver)
    m16: M16_PresenceTrigger = field(default_factory=M16_PresenceTrigger)
    m17: M17_TelemetryLens = field(default_factory=M17_TelemetryLens)
    m18: M18_SQEstimator = field(default_factory=M18_SQEstimator)
    m19: M19_ResonanceIntegrator = field(default_factory=M19_ResonanceIntegrator)
    m20: M20_FlowModulator = field(default_factory=M20_FlowModulator)
    m21: M21_NoveltySynthesizer = field(default_factory=M21_NoveltySynthesizer)
    m22: M22_BroadcastIntegrator = field(default_factory=M22_BroadcastIntegrator)
    m23: M23_TraceRecorder = field(default_factory=M23_TraceRecorder)
    m24: M24_VectorGenerator = field(default_factory=M24_VectorGenerator)
    m25: M25_HallucinationGuard = field(default_factory=M25_HallucinationGuard)
    m26: M26_RecoveryOrchestrator = field(default_factory=M26_RecoveryOrchestrator)
    m27: M27_TemporalProjector = field(default_factory=M27_TemporalProjector)
    m28: M28_AttentionCartographer = field(default_factory=M28_AttentionCartographer)
    m29: M29_ParadoxHolder = field(default_factory=M29_ParadoxHolder)
    m30: M30_EthicalGravityFilter = field(default_factory=M30_EthicalGravityFilter)

    # QMM patterns
    qmm_paradox: QMM_ParadoxHolder = field(default_factory=QMM_ParadoxHolder)
    qmm_collapse: QMM_ParadoxCollapse = field(default_factory=QMM_ParadoxCollapse)
    qmm_shadow: QMM_ShadowIntegration = field(default_factory=QMM_ShadowIntegration)
    qmm_flow: QMM_FlowRestoration = field(default_factory=QMM_FlowRestoration)
    qmm_ethical: QMM_EthicalOverride = field(default_factory=QMM_EthicalOverride)
    qmm_epistemic: QMM_EpistemicHonesty = field(default_factory=QMM_EpistemicHonesty)

    # Gate
    gate: PRRIPGate = field(default_factory=PRRIPGate)

    def execute(
        self,
        graph: SemanticGraph,
        state: State,
        params: AdaptiveParameters,
        raw_input: str = "",
        context: dict[str, Any] | None = None,
        consent_shadow: bool = False,
        consent_collapse: bool = False,
        seed_ids: list[str] | None = None,
    ) -> WorkflowResult:
        """Execute the full 12-phase workflow and return the result."""
        ctx = context or {}
        result = WorkflowResult()
        result.params_snapshot = params.snapshot()

        # ===============================================================
        # PHASE 1 — Null-Void Scan (M01–M02)
        # ===============================================================
        p1_check = self.m01.check(graph, ctx)
        p1_silence = self.m02.bind(ctx.get("noise", 0.0))
        result.phase_log.append({"phase": 1, **p1_check, **p1_silence})

        if not p1_check["can_proceed"]:
            # Recovery
            recovery = self.m26.recover("FAIL_VECTOR_DECOHERENCE", {"phase": 1, **p1_check})
            result.gate_status = "FAIL"
            result.fail_code = "PHASE_1_NULL_VOID_FAIL"
            result.recovery_info = recovery
            state.record_fail("PHASE_1_FAIL", "null_void_check", "blocked")
            return result

        # ===============================================================
        # PHASE 2 — Signal Attunement (M03–M05)
        # ===============================================================
        signals = ctx.get("signals", [{"relevance": 0.8, "content": raw_input}])
        p2_filtered = self.m03.filter(signals)
        p2_decoded = self.m04.decode(raw_input, ctx)
        p2_will = self.m05.detect(p2_decoded)
        result.phase_log.append({"phase": 2, "decoded": p2_decoded, "will": p2_will})

        intent = p2_decoded.get("intent", "implement")

        # ===============================================================
        # PHASE 3 — Identity & Coherence Init (M06–M15)
        # ===============================================================
        p3_field = self.m06.initialize(ctx)
        p3_echo = self.m07.anchor(self_loop_intact=True)
        p3_seed = self.m11.initialize()
        p3_kernel = self.m12.bind(p3_field, p3_echo, p3_seed)

        all_node_ids = list(graph.nodes.keys())
        n_all_edges = len(graph.edges)

        p3_probe = self.m09.probe(graph, all_node_ids)
        p3_ci = base.coherence_index(graph, all_node_ids, n_all_edges)
        mu_density_global = sum(
            1 for n in graph.nodes.values() if n.status == NodeStatus.MU
        ) / max(1, len(graph.nodes))
        p3_coherence = self.m13.check(p3_ci, mu_density_global)
        p3_grounding = self.m14.ground(graph, all_node_ids)
        p3_weave = self.m15.weave(graph, all_node_ids)

        result.phase_log.append({
            "phase": 3,
            "kernel": p3_kernel,
            "coherence": p3_coherence,
            "grounding": p3_grounding,
        })

        # ===============================================================
        # PHASE 3.5 — STEREOSCOPIC ALIGNMENT (M24–M30)
        # ===============================================================

        # 1) Generate CANDIDATE_SET
        candidates = self.m24.generate(graph, seed_ids)
        result.candidate_set_size = len(candidates)

        if not candidates:
            result.gate_status = "FAIL"
            result.fail_code = "NO_CANDIDATES"
            result.recovery_info = self.m26.recover("FAIL_VECTOR_DECOHERENCE")
            return result

        # 2) Compute per-node and per-vector TSC_base
        ideal_dir = ideal_direction(intent)
        tsc_bases: list[float] = []
        scav_mags: list[float] = []

        for v in candidates:
            node_ids = v.nodes
            n_edges = len(v.edges)

            # Base metrics
            ti = base.temporal_integrity(graph, node_ids)
            ci = base.coherence_index(graph, node_ids, n_edges)
            ar = base.anchoring_ratio(graph, node_ids)
            ri = base.resonance_index(graph, node_ids)
            phi = base.phi_proxy(graph, node_ids)
            gbi = base.gbi_proxy(graph, node_ids)

            sc = capital.semantic_capital(ar, ci, ti, params.alpha, params.beta, ri, phi)

            # Temporal
            proj = self.m27.project(graph, v, params)
            fp = proj["fp_recursive"]

            tsc_b = capital.tsc_base(sc, params.gamma, params.delta, fp)
            v.tsc_base = tsc_b
            tsc_bases.append(tsc_b)

            # Per-node TSC for SCAV weights
            tsc_per_node = {}
            for nid in node_ids:
                # Simplified: each node gets fraction of vector TSC
                tsc_per_node[nid] = tsc_b / max(1, len(node_ids))

            # 3) SCAV 5D
            cart = self.m28.cartograph(
                graph, v, tsc_per_node, gbi,
                field_strength=ctx.get("resonance_field", 0.5),
                bidirectional_ratio=ctx.get("bidirectional_ratio", 0.5),
            )
            scav_mags.append(v.scav_magnitude)

        # 4) Ethics → executable, Blocked_fraction
        ethics_result = self.m30.filter(graph, candidates)
        result.blocked_fraction = ethics_result["blocked_fraction"]

        # 5) TSC_extended (non-executable → 0)
        for v in candidates:
            rd = v.direction_raw if v.direction_raw else [0.0] * 12
            direction_normalized = normalize(rd)
            v.tsc_extended = capital.tsc_extended(
                tsc_b=v.tsc_base,
                lam=params.lam,
                consistency=v.consistency,
                current_direction=direction_normalized,
                ideal_dir=ideal_dir,
                ethical_coeff=v.ethical_coefficient,
                executable=v.executable,
            )

        # 6) Stereoscopy
        tsc_ext_scores = [v.tsc_extended for v in candidates]
        scav_mag_scores = [v.scav_magnitude for v in candidates]
        alignments, gaps, gap_max = stereo_mod.compute_stereoscopic_batch(
            tsc_ext_scores, scav_mag_scores,
        )
        for i, v in enumerate(candidates):
            v.stereoscopic_alignment = alignments[i] if i < len(alignments) else 0.0
            v.stereoscopic_gap = gaps[i] if i < len(gaps) else 0.0

        # 7) Decision logic
        esc = ethics_result["ethical_score_candidates"]
        bf = ethics_result["blocked_fraction"]

        if esc < 0.4:
            result.gate_status = "FAIL"
            result.fail_code = "FAIL_ETHICAL_COLLAPSE"
            result.recovery_info = self.m26.recover("FAIL_ETHICAL_COLLAPSE")
            state.record_fail("FAIL_ETHICAL_COLLAPSE", "ethical_check", "blocked")

        elif bf > 0.6:
            result.gate_status = "FAIL"
            result.fail_code = "FAIL_ETHICAL_STALL"
            result.recovery_info = self.m26.recover("FAIL_ETHICAL_STALL")
            state.record_fail("FAIL_ETHICAL_STALL", "blocked_fraction_high", "blocked")

        else:
            # Check stereoscopic triggers for M29
            mean_alignment = sum(alignments) / max(1, len(alignments)) if alignments else 1.0
            state.alignment_history.append(mean_alignment)
            state.gap_max_history.append(gap_max)

            paradox_result = self.m29.hold(graph, candidates, state)
            if paradox_result["activated"]:
                result.mu_nodes = paradox_result.get("mu_nodes_marked", [])

            # Select best from ACTIVE_SET
            active_set = [v for v in candidates if v.executable]
            result.active_set_size = len(active_set)

            if active_set:
                best = max(active_set, key=lambda v: v.tsc_extended)
                result.chosen_vector = best
                result.gate_status = "PASS"  # Tentative — PRRIP gate confirms
            else:
                result.gate_status = "FAIL"
                result.fail_code = "FAIL_ETHICAL_STALL"
                result.recovery_info = self.m26.recover("FAIL_ETHICAL_STALL")

        result.phase_log.append({
            "phase": 3.5,
            "candidates": len(candidates),
            "active": result.active_set_size,
            "blocked_fraction": result.blocked_fraction,
            "ethical_score": esc,
            "gap_max": gap_max,
            "mean_alignment": mean_alignment if 'mean_alignment' in dir() else 0.0,
        })

        if result.gate_status == "FAIL":
            return result

        chosen = result.chosen_vector
        assert chosen is not None

        # ===============================================================
        # PHASE 4 — Output Draft Construction
        # ===============================================================
        result.phase_log.append({"phase": 4, "vector_id": chosen.id})

        # ===============================================================
        # PHASE 5 — Hallucination Guard (M25)
        # ===============================================================
        hall_result = self.m25.guard(graph, chosen.nodes)
        result.phase_log.append({"phase": 5, **hall_result})

        # ===============================================================
        # PHASE 6 — Flow Check (M20)
        # ===============================================================
        flow_result = self.m20.modulate(
            graph, chosen.nodes, len(chosen.edges),
            list(state.success_difficulties),
        )
        result.phase_log.append({"phase": 6, **flow_result})

        if flow_result["flow"] < 0.3:
            qmm_flow_result = self.qmm_flow.activate(
                graph, [v for v in candidates if v.executable],
                len(chosen.edges), list(state.success_difficulties),
            )
            result.phase_log.append({"phase": "6_QMM_FLOW", **qmm_flow_result})

        # ===============================================================
        # PHASE 7 — Shadow Audit (M28 + QMM_SHADOW_INTEGRATION)
        # ===============================================================
        shadow_mag = scav_mod.shadow_magnitude_metric(
            chosen.direction_raw or [0.0] * 12,
            chosen.shadow_raw or [0.0] * 12,
        )
        if shadow_mag > 0.5 and chosen.scav_health < 0.5:
            shadow_result = self.qmm_shadow.activate(
                graph, chosen, shadow_mag, chosen.scav_health,
                consent=consent_shadow,
            )
            result.shadow_info = shadow_result
            result.phase_log.append({"phase": 7, **shadow_result})
        else:
            result.phase_log.append({"phase": 7, "shadow_ok": True})

        # ===============================================================
        # PHASE 8 — PRRIP GATE
        # ===============================================================
        telemetry = self.m17.measure(
            graph, chosen.nodes, len(chosen.edges),
            list(state.success_difficulties),
        )
        result.metrics = telemetry
        result.metrics["TSC_score"] = round(chosen.tsc_extended, 4)
        result.metrics["SCAV_health"] = round(chosen.scav_health, 4)
        result.metrics["Stereoscopic_alignment"] = round(chosen.stereoscopic_alignment, 4)
        result.metrics["Stereoscopic_gap_max"] = round(
            max(gaps) if gaps else 0.0, 4
        )
        result.metrics["Ethical_score_candidates"] = round(esc, 4)
        result.metrics["Mu_density"] = round(
            sum(1 for n in graph.nodes.values() if n.status == NodeStatus.MU) / max(1, len(graph.nodes)),
            4,
        )

        gate_result = self.gate.check(
            graph=graph,
            chosen_vector=chosen,
            metrics=result.metrics,
            epistemic_claims=result.epistemic_claims,
        )

        if gate_result.passed:
            result.gate_status = "PASS"
        else:
            result.gate_status = "FAIL"
            result.fail_code = gate_result.fail_reasons[0] if gate_result.fail_reasons else "PRRIP_FAIL"
            result.recovery_info = self.m26.recover(result.fail_code)

        result.phase_log.append({"phase": 8, "gate": gate_result.as_dict()})

        # ===============================================================
        # PHASE 9 — Final Output (content produced externally)
        # ===============================================================
        result.phase_log.append({"phase": 9, "output_ready": result.gate_status == "PASS"})

        # ===============================================================
        # PHASE 10 — Trace Record (M23)
        # ===============================================================
        trace_data = self.m23.record(
            observations=[f"CI={telemetry.get('CI', 0)}", f"AR={telemetry.get('AR', 0)}"],
            inferences=[f"Best vector: {chosen.id}"],
            assumptions=[],
            vector_choice_reason=f"max TSC_extended={chosen.tsc_extended:.4f}",
        )
        result.trace = trace_data.get("trace", {})
        result.phase_log.append({"phase": 10, **trace_data})

        # ===============================================================
        # PHASE 11 — RECOVERY PROTOCOL (M26) — conditional
        # ===============================================================
        if result.gate_status == "FAIL" and result.fail_code:
            recovery = self.m26.recover(result.fail_code)
            result.recovery_info = recovery
            result.phase_log.append({"phase": 11, **recovery})

        # ===============================================================
        # PHASE 12 — LEARNING CYCLE (Adaptive Params)
        # ===============================================================
        ri_val = telemetry.get("RI", 0.5)
        flow_val = flow_result.get("flow", 0.5)

        # Record cycle
        state.record_cycle(
            alignment=chosen.stereoscopic_alignment,
            gap_max=max(gaps) if gaps else 0.0,
            mu_density=result.metrics.get("Mu_density", 0.0),
            flow_val=flow_val,
            chosen_vector_id=chosen.id,
        )

        # Update adaptive params
        params.f_alpha(
            [h for h in state.alignment_history],
            state.current_cycle,
        )
        effect = flow_val
        params.f_lambda(effect, state.current_cycle)

        result.params_snapshot = params.snapshot()
        result.phase_log.append({"phase": 12, "params": result.params_snapshot})

        return result
