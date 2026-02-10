"""
NECHTO v4.8 — Reflexion Framework Analyzer

Meta-observation protocol implementing:
1. Ontological Assumptions Analysis
2. Semantic Lacuna Detection  
3. Coherence Validation
4. Transformation Prescription

Analyzes draft responses for epistemic honesty, coherence, and alignment
with NECHTO axioms (PEV, MU-logic, Love > Logic).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional
from datetime import datetime


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
        
        if self.overall_assessment:
            md.extend(["---", "", "## OVERALL ASSESSMENT", "", self.overall_assessment])
        
        return "\n".join(md)


class ReflexionAnalyzer:
    """Meta-observation analyzer for NECHTO responses."""
    
    def analyze(self, task: str, draft: str) -> ReflexionReport:
        """Perform complete reflexion analysis on a draft response."""
        report = ReflexionReport(task=task, draft=draft)
        
        report.ontological = self._analyze_ontology(task, draft)
        report.lacunae = self._analyze_lacunae(task, draft, report.ontological)
        report.coherence = self._validate_coherence(task, draft, report.ontological)
        report.prescription = self._prescribe_transformation(
            task, draft, report.ontological, report.lacunae, report.coherence
        )
        report.overall_assessment = self._generate_assessment(report)
        
        return report
    
    def _analyze_ontology(self, task: str, draft: str) -> OntologicalAnalysis:
        """Analyze ontological assumptions and hidden premises."""
        analysis = OntologicalAnalysis()
        
        # Check for hidden assumptions
        if "либо" in draft.lower() or "either" in draft.lower():
            analysis.hidden_assumptions.append("assumes binary logic")
        if "потому что" in draft.lower() or "because" in draft.lower():
            analysis.hidden_assumptions.append("assumes linear causality")
        
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
    
    def _analyze_lacunae(self, task: str, draft: str, ont: OntologicalAnalysis) -> SemanticLacunaAnalysis:
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
