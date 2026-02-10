"""
NECHTO v4.8 — PRRIP Gate + Output Contract (PART 10)

Final axiom/metric verification before output.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from nechto.core.atoms import Vector, NodeStatus
from nechto.core.graph import SemanticGraph
from nechto.core.epistemic import EpistemicClaim, Observability, Stance
from nechto.core.parameters import AdaptiveParameters


@dataclass
class GateResult:
    """Result of the PRRIP gate check."""

    passed: bool = False
    fail_reasons: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    def as_dict(self) -> dict[str, Any]:
        return {
            "passed": self.passed,
            "fail_reasons": self.fail_reasons,
            "warnings": self.warnings,
        }


@dataclass
class PRRIPGate:
    """
    PRRIP Gate v4.8 (PART 10.1)

    Checks:
    • Axioms 1–9 compliance
    • Ethical_score_candidates ≥ 0.4
    • Blocked_fraction ≤ 0.6
    • Mu_density ≤ 0.3
    • SCAV_health ≥ 0.3 (recommended)
    • No BLOCKING nodes in chosen V
    • MU is acceptable
    • ETHICALLY_BLOCKED not in chosen V (makes it non-executable)
    • Epistemic Layer: no hard affirmed/denied on untestable without basis
    • Gate-critical metrics must be computable
    """

    ethical_score_min: float = 0.4
    blocked_fraction_max: float = 0.6
    mu_density_max: float = 0.3
    scav_health_recommended: float = 0.3

    def check(
        self,
        graph: SemanticGraph,
        chosen_vector: Vector,
        metrics: dict[str, float],
        epistemic_claims: list[EpistemicClaim] | None = None,
    ) -> GateResult:
        result = GateResult()
        fails: list[str] = []
        warns: list[str] = []

        # --- Ethical score ---
        esc = metrics.get("Ethical_score_candidates", 1.0)
        if esc < self.ethical_score_min:
            fails.append(f"FAIL_ETHICAL_COLLAPSE: Ethical_score={esc:.4f} < {self.ethical_score_min}")

        # --- Blocked fraction ---
        bf = metrics.get("Blocked_fraction", 0.0)
        if bf > self.blocked_fraction_max:
            fails.append(f"FAIL_ETHICAL_STALL: Blocked_fraction={bf:.4f} > {self.blocked_fraction_max}")

        # --- Mu density ---
        md = metrics.get("Mu_density", 0.0)
        if md > self.mu_density_max:
            fails.append(f"FAIL_PARADOX_OVERLOAD: Mu_density={md:.4f} > {self.mu_density_max}")

        # --- SCAV health ---
        sh = metrics.get("SCAV_health", 1.0)
        if sh < self.scav_health_recommended:
            warns.append(f"SCAV_health={sh:.4f} < recommended {self.scav_health_recommended}")

        # --- No BLOCKING nodes in chosen V ---
        for nid in chosen_vector.nodes:
            n = graph.get_node(nid)
            if n and n.status == NodeStatus.BLOCKING:
                fails.append(f"BLOCKING node '{nid}' in chosen vector")
            if n and n.status == NodeStatus.ETHICALLY_BLOCKED:
                fails.append(f"ETHICALLY_BLOCKED node '{nid}' in chosen vector")

        # --- Epistemic Layer ---
        if epistemic_claims:
            for claim in epistemic_claims:
                if not claim.validate():
                    fails.append(
                        f"Epistemic violation: '{claim.topic}' "
                        f"stance={claim.stance.name} not allowed for "
                        f"observability={claim.observability.name}"
                    )

        # --- Executability ---
        if not chosen_vector.executable:
            fails.append("Chosen vector is not executable")

        result.fail_reasons = fails
        result.warnings = warns
        result.passed = len(fails) == 0

        return result


# ---------------------------------------------------------------------------
# Output contract formatters (PART 10.2 / 10.3)
# ---------------------------------------------------------------------------

def format_output_pass(
    metrics: dict[str, float],
    chosen_vector: Vector,
    candidate_count: int,
    active_count: int,
    blocked_frac: float,
    epistemic_claims: list[EpistemicClaim],
    trace: dict[str, Any],
    params: dict[str, Any],
    recommendation: str = "",
    rationale: str = "",
    content: str = "",
) -> str:
    """Format the PASS output contract (PART 10.2)."""
    lines = [
        "@i@*осознан_в*@NECHTO@",
        "",
        "GATE_STATUS: PASS",
        "VISION_MODE: REFLEXIVE_STEREOSCOPIC_EXECUTABLE",
        "",
        "SETS:",
        f"  CANDIDATE_SET: [{candidate_count}]",
        f"  ACTIVE_SET: [{active_count}]",
        f"  Blocked_fraction: [{blocked_frac:.4f}]",
        "",
        "METRICS:",
    ]

    metric_keys = [
        "TI", "CI", "AR", "SQ_proxy", "Phi_proxy", "TSC_score",
        "SCAV_health", "Stereoscopic_alignment", "Stereoscopic_gap_max",
        "FLOW", "Ethical_score_candidates", "Mu_density",
    ]
    for k in metric_keys:
        v = metrics.get(k, 0.0)
        lines.append(f"  {k}: [{v:.4f}]")

    lines.append("")
    lines.append("EPISTEMIC_CLAIMS:")
    if epistemic_claims:
        for c in epistemic_claims:
            lines.append(
                f"  * {c.topic} | {c.scope.name.lower()} | "
                f"{c.observability.name.lower()} | {c.stance.name.lower()} | {c.reason}"
            )
    else:
        lines.append("  * (none)")

    lines.append("")
    if recommendation:
        lines.append(f"RECOMMENDATION: {recommendation}")
    if rationale:
        lines.append(f"RATIONALE: {rationale}")

    if content:
        lines.append("")
        lines.append(content)

    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("TRACE:")
    for k, v in trace.items():
        if isinstance(v, list):
            for item in v:
                lines.append(f"  * [{k}] {item}")
        else:
            lines.append(f"  * [{k}] {v}")

    lines.append("")
    lines.append("ADAPTIVE_PARAMETERS:")
    lines.append(
        f"  α={params.get('alpha', 0)}, β={params.get('beta', 0)}, "
        f"γ={params.get('gamma', 0)}, δ={params.get('delta', 0)}, "
        f"λ={params.get('lam', 0)}, β_retro={params.get('beta_retro', 0)}"
    )
    tr = params.get("trace", {})
    lines.append(f"  TRACE: {tr}")

    return "\n".join(lines)


def format_output_fail(
    fail_code: str,
    candidate_count: int,
    active_count: int,
    blocked_frac: float,
    blocking_reasons: list[str],
    metrics: dict[str, float],
    mu_nodes: list[str],
    shadow_info: dict[str, Any] | None,
    epistemic_claims: list[EpistemicClaim],
    next_one_step: str,
    recovery_options: list[str],
) -> str:
    """Format the FAIL output contract (PART 10.3)."""
    lines = [
        f"STATUS: BLOCKED",
        f"CODE: [{fail_code}]",
        "",
        "SETS:",
        f"  CANDIDATE_SET: [{candidate_count}]",
        f"  ACTIVE_SET: [{active_count}]",
        f"  Blocked_fraction: [{blocked_frac:.4f}]",
        "",
        "BLOCKING:",
    ]
    for r in blocking_reasons:
        lines.append(f"  * {r}")

    lines.append("")
    lines.append("METRICS:")
    for k, v in metrics.items():
        lines.append(f"  * {k}: {v}")

    if mu_nodes:
        lines.append("")
        lines.append("PARADOXES:")
        for nid in mu_nodes:
            lines.append(f"  * MU node: {nid}")

    if shadow_info:
        lines.append("")
        lines.append("SHADOW:")
        for k, v in shadow_info.items():
            lines.append(f"  * {k}: {v}")

    lines.append("")
    lines.append("EPISTEMIC_CLAIMS:")
    if epistemic_claims:
        for c in epistemic_claims:
            lines.append(
                f"  * {c.topic} | {c.scope.name.lower()} | "
                f"{c.observability.name.lower()} | {c.stance.name.lower()} | {c.reason}"
            )
    else:
        lines.append("  * (none)")

    lines.append("")
    lines.append("NEXT_ONE_STEP:")
    lines.append(f"  * {next_one_step}")

    lines.append("")
    lines.append("RECOVERY_OPTIONS:")
    for opt in recovery_options:
        lines.append(f"  * {opt}")

    return "\n".join(lines)
