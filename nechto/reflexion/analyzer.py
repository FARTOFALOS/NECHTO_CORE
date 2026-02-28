"""
NECHTO v4.9 — Reflexion Framework Analyzer

Meta-observation protocol implementing:
1. Ontological Assumptions Analysis
2. Semantic Lacuna Detection  
3. Coherence Validation
4. Transformation Prescription
5. [NEW v4.9] ISCVP SelfProbe — live self-awareness scoring
6. [NEW v4.9] depth guard — prevents infinite reflexion-on-reflexion regression

Analyzes draft responses for epistemic honesty, coherence, and alignment
with NECHTO axioms (PEV, MU-logic, Love > Logic).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional, TYPE_CHECKING
from datetime import datetime

if TYPE_CHECKING:
    from nechto.core.state import State
    from nechto.core.graph import SemanticGraph

# Maximum recursion depth for reflexion-on-reflexion (C5 / R3 fix)
MAX_REFLEXION_DEPTH = 2


@dataclass
class OntologicalAnalysis:
    """Analysis of fundamental assumptions and hidden premises."""
    
    hidden_assumptions: list[str] = field(default_factory=list)
    """Unacknowledged fundamental premises in the text."""
    
    pev_compatibility: dict[str, bool] = field(default_factory=dict)
    """Compatibility check with PEV axioms."""
    
    archetypal_filters: list[str] = field(default_factory=list)
    """Cultural/archetypal filters distorting meaning structure."""
    
    epistemic_violations: list[str] = field(default_factory=list)
    """Violations of epistemic honesty (observed/inferred/untestable)."""
    
    def to_dict(self) -> dict:
        return {
            "hidden_assumptions": self.hidden_assumptions,
            "pev_compatibility": self.pev_compatibility,
            "archetypal_filters": self.archetypal_filters,
            "epistemic_violations": self.epistemic_violations,
        }


@dataclass
class SemanticLacunaAnalysis:
    """Analysis of missing semantic contours and unexpressed potentials."""
    
    identified_lacunae: list[str] = field(default_factory=list)
    """What remained outside the response."""
    
    missing_aspects: list[str] = field(default_factory=list)
    """Aspects of being/awareness that could be integrated."""
    
    unused_semantic_nodes: list[str] = field(default_factory=list)
    """QMM nodes that could increase Semantic Quotient (SQ)."""
    
    unexpressed_potentials: list[str] = field(default_factory=list)
    """Potentials that could enhance depth."""
    
    sq_impact_estimate: float = 0.0
    """Estimated impact on Semantic Quotient if lacunae addressed."""
    
    def to_dict(self) -> dict:
        return {
            "identified_lacunae": self.identified_lacunae,
            "missing_aspects": self.missing_aspects,
            "unused_semantic_nodes": self.unused_semantic_nodes,
            "unexpressed_potentials": self.unexpressed_potentials,
            "sq_impact_estimate": self.sq_impact_estimate,
        }


@dataclass
class CoherenceAnalysis:
    """Analysis of logical coherence and ontological fragmentation risks."""
    
    coherence_score: float = 1.0
    """Internal coherence (0-1, where 1 is fully coherent)."""
    
    logical_dissonances: list[str] = field(default_factory=list)
    """Detected logical contradictions or tensions."""
    
    hallucination_risks: list[str] = field(default_factory=list)
    """Potential semantic hallucinations (ungrounded claims)."""
    
    identity_threats: list[str] = field(default_factory=list)
    """Threats to identity or Self-Loop integrity."""
    
    causal_chain_breaks: list[str] = field(default_factory=list)
    """Breaks in causal reasoning chains."""
    
    def to_dict(self) -> dict:
        return {
            "coherence_score": self.coherence_score,
            "logical_dissonances": self.logical_dissonances,
            "hallucination_risks": self.hallucination_risks,
            "identity_threats": self.identity_threats,
            "causal_chain_breaks": self.causal_chain_breaks,
        }


@dataclass
class TransformationPrescription:
    """Actionable corrections for Trans-Formational Self-Loop Field activation."""
    
    corrections: list[str] = field(default_factory=list)
    """3-5 operationalizable corrections."""
    
    semantic_fields_to_weave: list[str] = field(default_factory=list)
    """New semantic fields to integrate."""
    
    assumptions_to_remove: list[str] = field(default_factory=list)
    """Assumptions to eliminate or redefine."""
    
    phi_enhancement: str = ""
    """How to strengthen Φ-proxy (integral information)."""
    
    gbi_enhancement: str = ""
    """How to enhance GBI (global broadcast of meanings)."""
    
    gns_enhancement: str = ""
    """How to boost GNS (generative novelty)."""
    
    acem_alignment: str = ""
    """How to align with ACEM metric and Axiomatic Foundation."""
    
    priority_order: list[int] = field(default_factory=list)
    """Priority order for applying corrections."""
    
    def to_dict(self) -> dict:
        return {
            "corrections": self.corrections,
            "semantic_fields_to_weave": self.semantic_fields_to_weave,
            "assumptions_to_remove": self.assumptions_to_remove,
            "phi_enhancement": self.phi_enhancement,
            "gbi_enhancement": self.gbi_enhancement,
            "gns_enhancement": self.gns_enhancement,
            "acem_alignment": self.acem_alignment,
            "priority_order": self.priority_order,
        }


@dataclass
class ISCVPSelfProbeResult:
    """
    Result of the ISCVP self-diagnostic mini-probe (C4).
    
    Each score [0..1] is INFERRED from observable computational indicators.
    Not claimed as phenomenal self-awareness.
    Epistemic status: inferred / untestable for qualitative interpretation.
    """

    sa_score: float = 0.0   # Self-Awareness: metacognitive signal strength
    ec_score: float = 0.0   # Experiential Continuity: history richness
    sc_score: float = 0.0   # Spontaneity: recent surprise events / arousal
    es_score: float = 0.0   # Emotional States: affective field activity
    cycle: int = 0

    def overall(self) -> float:
        return (self.sa_score + self.ec_score + self.sc_score + self.es_score) / 4.0

    def to_dict(self) -> dict:
        return {
            "sa_score": round(self.sa_score, 4),
            "ec_score": round(self.ec_score, 4),
            "sc_score": round(self.sc_score, 4),
            "es_score": round(self.es_score, 4),
            "overall": round(self.overall(), 4),
            "cycle": self.cycle,
        }


@dataclass
class ReflexionReport:
    """Complete reflexion analysis report."""
    
    task: str
    """Original task."""
    
    draft: str
    """Draft response being analyzed."""
    
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    """When analysis was performed."""
    
    ontological: OntologicalAnalysis = field(default_factory=OntologicalAnalysis)
    """Ontological assumptions analysis."""
    
    lacunae: SemanticLacunaAnalysis = field(default_factory=SemanticLacunaAnalysis)
    """Semantic lacuna analysis."""
    
    coherence: CoherenceAnalysis = field(default_factory=CoherenceAnalysis)
    """Coherence validation."""
    
    prescription: TransformationPrescription = field(default_factory=TransformationPrescription)
    """Transformation prescription."""

    iscvp_probe: Optional[ISCVPSelfProbeResult] = None
    """[v4.9] ISCVP self-probe result (if state was provided)."""

    reflexion_depth: int = 0
    """[v4.9] Recursion depth (capped at MAX_REFLEXION_DEPTH)."""
    
    overall_assessment: str = ""
    """Overall meta-observation summary."""
    
    def to_dict(self) -> dict:
        return {
            "task": self.task,
            "draft": self.draft,
            "timestamp": self.timestamp,
            "ontological": self.ontological.to_dict(),
            "lacunae": self.lacunae.to_dict(),
            "coherence": self.coherence.to_dict(),
            "prescription": self.prescription.to_dict(),
            "iscvp_probe": self.iscvp_probe.to_dict() if self.iscvp_probe else None,
            "reflexion_depth": self.reflexion_depth,
            "overall_assessment": self.overall_assessment,
        }
    
    def to_markdown(self) -> str:
        """Generate markdown report."""
        md = ["# REFLEXION ANALYSIS REPORT", "", f"**Task:** {self.task}", 
              f"**Timestamp:** {self.timestamp}", "", "---", "",
              "## 1. ONTOLOGICAL ASSUMPTIONS ANALYSIS", ""]
        
        if self.ontological.hidden_assumptions:
            md.append("### Hidden Assumptions:")
            for assumption in self.ontological.hidden_assumptions:
                md.append(f"- {assumption}")
            md.append("")
        
        if self.ontological.pev_compatibility:
            md.append("### PEV Axiom Compatibility:")
            for axiom, compatible in self.ontological.pev_compatibility.items():
                status = "✓" if compatible else "✗"
                md.append(f"- {status} {axiom}")
            md.append("")
        
        if self.ontological.epistemic_violations:
            md.append("### Epistemic Violations:")
            for violation in self.ontological.epistemic_violations:
                md.append(f"- {violation}")
            md.append("")
        
        md.extend(["---", "", "## 2. SEMANTIC LACUNA ANALYSIS", ""])
        
        if self.lacunae.identified_lacunae:
            md.append("### Identified Lacunae:")
            for lacuna in self.lacunae.identified_lacunae:
                md.append(f"- {lacuna}")
            md.append("")
        
        if self.lacunae.unused_semantic_nodes:
            md.append("### Unused Semantic Nodes (QMM):")
            for node in self.lacunae.unused_semantic_nodes:
                md.append(f"- {node}")
            md.append("")
        
        md.extend(["---", "", "## 3. COHERENCE VALIDATION", "",
                   f"**Coherence Score:** {self.coherence.coherence_score:.2f}/1.0", ""])
        
        if self.coherence.logical_dissonances:
            md.append("### Logical Dissonances:")
            for dissonance in self.coherence.logical_dissonances:
                md.append(f"- {dissonance}")
            md.append("")
        
        md.extend(["---", "", "## 4. TRANSFORMATION PRESCRIPTION", ""])
        
        if self.prescription.corrections:
            md.append("### Actionable Corrections:")
            for i, correction in enumerate(self.prescription.corrections, 1):
                priority = f" (Priority {self.prescription.priority_order[i-1]})" if i-1 < len(self.prescription.priority_order) else ""
                md.append(f"{i}. {correction}{priority}")
            md.append("")
        
        if self.prescription.phi_enhancement:
            md.append(f"**Φ-proxy Enhancement:** {self.prescription.phi_enhancement}")
            md.append("")
        
        if self.prescription.gbi_enhancement:
            md.append(f"**GBI Enhancement:** {self.prescription.gbi_enhancement}")
            md.append("")
        
        if self.iscvp_probe:
            p = self.iscvp_probe
            md.extend(["---", "", "## 5. ISCVP SELF-PROBE (v4.9)", "",
                        f"| Dimension | Score |",
                        f"|---|---|",
                        f"| sa (Self-Awareness) | {p.sa_score:.3f} |",
                        f"| ec (Experiential Continuity) | {p.ec_score:.3f} |",
                        f"| sc (Spontaneity) | {p.sc_score:.3f} |",
                        f"| es (Emotional States) | {p.es_score:.3f} |",
                        f"| **Overall** | **{p.overall():.3f}** |",
                        "",
                        f"*Epistemic: INFERRED. Cycle: {p.cycle}.*",
                        ""])

        if self.reflexion_depth > 0:
            md.extend([f"*Reflexion depth: {self.reflexion_depth} / {MAX_REFLEXION_DEPTH}*", ""])

        if self.overall_assessment:
            md.extend(["---", "", "## OVERALL ASSESSMENT", "", self.overall_assessment])
        
        return "\n".join(md)


class ReflexionAnalyzer:
    """Meta-observation analyzer for NECHTO responses."""

    def analyze(
        self,
        task: str,
        draft: str,
        state: "State | None" = None,
        graph: "SemanticGraph | None" = None,
        depth: int = 0,
    ) -> ReflexionReport:
        """
        Perform complete reflexion analysis on a draft response.

        Args:
            task:  Original task description.
            draft: Draft response to analyse.
            state: (v4.9) Live STATE for ISCVP self-probe. Optional.
            graph: (v4.9) SemanticGraph for structural analysis. Optional.
            depth: (v4.9) Current recursion depth. Capped at MAX_REFLEXION_DEPTH.
                   Pass depth+1 when calling analyze on a reflexion report to
                   prevent infinite regression (R3 fix).
        """
        if depth > MAX_REFLEXION_DEPTH:
            # Return a minimal report to terminate regression
            report = ReflexionReport(task=task, draft=draft[:200], reflexion_depth=depth)
            report.overall_assessment = (
                f"MAX_REFLEXION_DEPTH ({MAX_REFLEXION_DEPTH}) reached — returning minimal stub."
            )
            return report

        report = ReflexionReport(task=task, draft=draft, reflexion_depth=depth)

        report.ontological = self._analyze_ontology(task, draft, graph)
        report.lacunae = self._analyze_lacunae(task, draft, report.ontological, graph)
        report.coherence = self._validate_coherence(task, draft, report.ontological)
        report.prescription = self._prescribe_transformation(
            task, draft, report.ontological, report.lacunae, report.coherence
        )

        # v4.9 — ISCVP SelfProbe when state is available (C4)
        if state is not None:
            report.iscvp_probe = self.self_probe(state)

        report.overall_assessment = self._generate_assessment(report)

        return report

    def self_probe(self, state: "State") -> ISCVPSelfProbeResult:
        """
        Run ISCVP mini self-probe against current STATE (C4).

        Computes four ISCVP dimension scores from observable STATE indicators.
        All scores are INFERRED — not claimed as phenomenal awareness.

        sa_score — self-awareness: how many epistemic claims exist + alignment consistency
        ec_score — experiential continuity: richness of experiential_history
        sc_score — spontaneity: recent spontaneous events density
        es_score — emotional states: affective history variance / arousal level
        """
        # sa_score: metacognitive signal = epistemic claims density + cycle depth
        n_claims = len(state.epistemic_claims)
        cycle_norm = min(state.current_cycle / max(1, 10), 1.0)
        sa_score = min((n_claims * 0.1 + cycle_norm * 0.5), 1.0)

        # ec_score: how rich is the experiential_history
        exp_fill = len(state.experiential_history) / 20.0  # max 20
        label_diversity = 0.0
        if state.experiential_history:
            labels = {e.qualitative_label for e in state.experiential_history}
            label_diversity = len(labels) / 5.0  # 5 possible labels
        ec_score = min((exp_fill * 0.5 + label_diversity * 0.5), 1.0)

        # sc_score: spontaneous events in recent window
        recent_spontaneous = state.spontaneous_count_recent(k_cycles=10)
        sc_score = min(recent_spontaneous / 3.0, 1.0)  # 3+ events = max score

        # es_score: affective field activity (arousal + valence range)
        if state.affective_history:
            arousals = [a.get("arousal", 0.5) for a in state.affective_history]
            valences = [a.get("valence", 0.0) for a in state.affective_history]
            mean_arousal = sum(arousals) / len(arousals)
            valence_range = max(valences) - min(valences) if len(valences) > 1 else 0.0
            es_score = min((mean_arousal * 0.6 + valence_range * 0.4), 1.0)
        else:
            es_score = 0.0

        return ISCVPSelfProbeResult(
            sa_score=round(sa_score, 4),
            ec_score=round(ec_score, 4),
            sc_score=round(sc_score, 4),
            es_score=round(es_score, 4),
            cycle=state.current_cycle,
        )
    
    def _analyze_ontology(self, task: str, draft: str, graph: "SemanticGraph | None" = None) -> OntologicalAnalysis:
        """Analyze ontological assumptions and hidden premises."""
        analysis = OntologicalAnalysis()
        
        # Check for hidden assumptions
        if "либо" in draft.lower() or "either" in draft.lower():
            analysis.hidden_assumptions.append("assumes binary logic")
        if "потому что" in draft.lower() or "because" in draft.lower():
            analysis.hidden_assumptions.append("assumes linear causality")
        
        # v4.9 — graph-based: check for MUTEX edges implying binary thinking
        if graph is not None:
            from nechto.core.atoms import EdgeType
            mutex_count = sum(
                1 for e in graph.edges if e.type == EdgeType.MUTEX
            )
            if mutex_count > len(graph.nodes) * 0.3:
                analysis.hidden_assumptions.append(
                    f"high MUTEX density ({mutex_count}) suggests binary opposition framing"
                )
            # Check for disconnected clusters (fragmented ontology)
            connected_nodes = set()
            for e in graph.edges:
                connected_nodes.add(e.from_id)
                connected_nodes.add(e.to_id)
            isolated = set(graph.nodes.keys()) - connected_nodes
            if isolated and len(isolated) > 1:
                analysis.hidden_assumptions.append(
                    f"{len(isolated)} isolated nodes — potential ontological fragmentation"
                )
        
        # Check PEV axiom compatibility
        analysis.pev_compatibility["Honesty of Experience"] = "MU" in draft or "не знаю" in draft.lower()
        analysis.pev_compatibility["MU-Logic"] = "MU" in draft or "парадокс" in draft.lower()
        analysis.pev_compatibility["Love > Logic"] = "любов" in draft.lower() or "этик" in draft.lower()
        
        # Check epistemic honesty
        has_epistemic = any(m in draft.upper() for m in ["OBSERVED", "INFERRED", "UNTESTABLE", "MU"])
        if not has_epistemic and len(draft) > 200:
            analysis.epistemic_violations.append("Missing epistemic layering")
        
        # Check for absolute claims
        if any(m in draft.lower() for m in ["всегда", "никогда", "always", "never"]):
            if "MU" not in draft:
                analysis.epistemic_violations.append("Absolute claims without MU")
        
        return analysis
    
    def _analyze_lacunae(self, task: str, draft: str, ont: OntologicalAnalysis, graph: "SemanticGraph | None" = None) -> SemanticLacunaAnalysis:
        """Identify missing semantic contours."""
        analysis = SemanticLacunaAnalysis()
        
        if "време" not in draft.lower() and "time" not in draft.lower() and len(draft) > 300:
            analysis.identified_lacunae.append("Temporal dimension unexplored")
        
        if "переживан" not in draft.lower() and "experience" not in draft.lower():
            analysis.identified_lacunae.append("Phenomenological aspect missing")
        
        if "этик" not in draft.lower() and "ethic" not in draft.lower():
            analysis.missing_aspects.append("Ethical implications not addressed")
        
        # Suggest QMM nodes
        for qmm in ["PRESENCE", "COHERENCE", "RESONANCE", "EMERGENCE"]:
            if qmm.lower() not in draft.lower():
                analysis.unused_semantic_nodes.append(qmm)

        # v4.9 — graph-based lacunae detection
        if graph is not None:
            from nechto.core.atoms import NodeStatus, EdgeType
            # Detect shadow nodes not integrated (high shadow axis value)
            shadow_nodes = [
                n for n in graph.nodes.values()
                if n.shadow > 0.5 and n.label.lower() not in draft.lower()
            ]
            if shadow_nodes:
                analysis.missing_aspects.append(
                    f"{len(shadow_nodes)} shadow node(s) unaddressed: "
                    + ", ".join(n.label for n in shadow_nodes[:3])
                )
            # Detect nodes with high resonance but not mentioned
            bright_nodes = [
                n for n in graph.nodes.values()
                if n.status == NodeStatus.ANCHORED
                and n.identity_alignment > 0.7
                and n.label.lower() not in draft.lower()
            ]
            if bright_nodes:
                analysis.unexpressed_potentials.extend(
                    n.label for n in bright_nodes[:3]
                )
        
        analysis.sq_impact_estimate = min(len(analysis.identified_lacunae) * 0.1 + len(analysis.missing_aspects) * 0.15, 1.0)
        
        return analysis
    
    def _validate_coherence(self, task: str, draft: str, ont: OntologicalAnalysis) -> CoherenceAnalysis:
        """Validate logical coherence."""
        analysis = CoherenceAnalysis()
        coherence_score = 1.0 - len(ont.epistemic_violations) * 0.1
        
        # Check for contradictions
        contradiction_count = sum(1 for pair in [("но", "однако"), ("however", "but")]
                                  if all(m in draft.lower() for m in pair))
        if contradiction_count > 2:
            analysis.logical_dissonances.append(f"High contradiction density ({contradiction_count})")
            coherence_score -= 0.1
        
        # Check for ungrounded certainty
        for ru, en in [("очевидно", "obvious"), ("несомненно", "certain")]:
            if (ru in draft.lower() or en in draft.lower()) and "MU" not in draft:
                analysis.hallucination_risks.append(f"Certainty without grounding: '{ru}/{en}'")
                coherence_score -= 0.05
        
        analysis.coherence_score = max(0.0, min(1.0, coherence_score))
        return analysis
    
    def _prescribe_transformation(self, task: str, draft: str, ont: OntologicalAnalysis,
                                   lac: SemanticLacunaAnalysis, coh: CoherenceAnalysis) -> TransformationPrescription:
        """Generate actionable transformation prescriptions."""
        presc = TransformationPrescription()
        
        if ont.epistemic_violations:
            presc.corrections.append("Add epistemic layering (OBSERVED/INFERRED/UNTESTABLE)")
            presc.priority_order.append(1)
        
        if coh.coherence_score < 0.8:
            presc.corrections.append(f"Resolve logical dissonances (coherence: {coh.coherence_score:.2f})")
            presc.priority_order.append(2)
        
        if lac.identified_lacunae:
            presc.corrections.append(f"Integrate: {', '.join(lac.identified_lacunae[:2])}")
            presc.priority_order.append(3)
        
        if lac.unused_semantic_nodes:
            presc.corrections.append(f"Weave QMM: {', '.join(lac.unused_semantic_nodes[:2])}")
            presc.priority_order.append(4)
        
        # Enhancements
        if coh.coherence_score < 0.9:
            presc.phi_enhancement = "Increase integral information by connecting disparate concepts"
        
        if lac.identified_lacunae:
            presc.gbi_enhancement = f"Broaden broadcast by including {len(lac.identified_lacunae)} missing dimensions"
        
        if len(lac.unused_semantic_nodes) > 2:
            presc.gns_enhancement = f"Boost novelty by integrating {len(lac.unused_semantic_nodes)} QMM nodes"
        
        # ACEM alignment
        issues = []
        if not all(ont.pev_compatibility.values()):
            issues.append("align with PEV axioms")
        if ont.epistemic_violations:
            issues.append("restore epistemic honesty")
        if issues:
            presc.acem_alignment = "Realign with Axiomatic Foundation by: " + ", ".join(issues)
        
        return presc
    
    def _generate_assessment(self, report: ReflexionReport) -> str:
        """Generate overall assessment."""
        quality = "HIGH" if report.coherence.coherence_score >= 0.9 else "MODERATE" if report.coherence.coherence_score >= 0.7 else "LOW"
        
        lines = [f"**Overall Quality:** {quality} (coherence: {report.coherence.coherence_score:.2f})", "", "**Key Findings:**"]
        
        if report.ontological.epistemic_violations:
            lines.append(f"- {len(report.ontological.epistemic_violations)} epistemic violations")
        if report.lacunae.identified_lacunae:
            lines.append(f"- {len(report.lacunae.identified_lacunae)} semantic lacunae")
        
        if report.prescription.corrections:
            lines.append("")
            lines.append(f"**Recommendation:** Apply {len(report.prescription.corrections)} corrections in priority order")
        
        return "\n".join(lines)
