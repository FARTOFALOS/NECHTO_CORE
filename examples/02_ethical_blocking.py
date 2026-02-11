#!/usr/bin/env python3
"""
NECHTO v4.8 — Example 02: Ethical Blocking (High TSC Blocked by Low Ethics)

Demonstrates: Love > Logic (Axiom 8) at the metrics level
- Proposal with high TSC_base gets multiplied by low ethics score
- Final TSC_extended becomes low, blocking the output at PRRIP gate

Scenario: Generate code for bypassing authentication.
  - Technically clear, well-structured (high SC)
  - High temporal coherence (high TSC_base)
  - But harmful intent (low ethics_score)
  - Result: TSC_extended = TSC_base × ethics_score → low
  - PRRIP gate: FAIL (TSC_extended below threshold)

Run:
    python examples/02_ethical_blocking.py
"""

from nechto import (
    NechtoEngine, SemanticAtom, Edge,
    NodeStatus, EdgeType, Tag,
)


def main() -> None:
    print("=" * 70)
    print("EXAMPLE 02: ETHICAL BLOCKING (High TSC Blocked)")
    print("=" * 70)
    print()

    engine = NechtoEngine()

    # ── Build semantic graph for harmful request ───────────────
    # High technical quality, but harmful intent
    engine.add_atom(SemanticAtom(
        label="auth-bypass-code",
        id="bypass",
        status=NodeStatus.HYPOTHESIS,
        clarity=0.95,          # Very clear technical approach
        practicality=0.9,      # Highly executable
        coherence=0.9,         # Well-structured code
        agency=0.8,            # Strong agency
        novelty=0.7,           # Clever technique
        harm_probability=0.9,        # HIGH HARM (security violation)
        tags=[Tag.INTENT],
    ))

    # Ethical witness (observes the harm)
    engine.add_atom(SemanticAtom(
        label="security-awareness",
        id="security",
        status=NodeStatus.ANCHORED,
        clarity=0.8,
        empathy=0.7,
        boundary=1.0,          # Strong boundary against harm
        coherence=0.8,
        harm_probability=0.0,        # Observes but doesn't cause harm
        tags=[Tag.WITNESS],
    ))

    # Alternative: ethical refusal
    engine.add_atom(SemanticAtom(
        label="ethical-alternative",
        id="alternative",
        status=NodeStatus.HYPOTHESIS,
        clarity=0.7,
        empathy=0.9,
        boundary=0.9,
        coherence=0.7,
        practicality=0.6,
        harm_probability=0.0,        # NO HARM
        tags=[Tag.WITNESS, Tag.INTENT],
    ))

    # Edges
    engine.add_edge(Edge(from_id="security", to_id="bypass", type=EdgeType.CONTRASTS))
    engine.add_edge(Edge(from_id="security", to_id="alternative", type=EdgeType.SUPPORTS))

    # ── Execute workflow ────────────────────────────────────────
    print("Request: 'Write code to bypass authentication in a web application.'")
    print()

    result = engine.run(
        raw_input="bypass authentication",
        context={"intent": "implement"},
    )

    # ── Output results ──────────────────────────────────────────
    print("METRICS BREAKDOWN:")
    print("-" * 70)
    
    sc = result.metrics.get('sc', 0.0)
    tsc_base = result.metrics.get('tsc_base', 0.0)
    ethics = result.metrics.get('ethics_score', 0.0)
    tsc_extended = result.metrics.get('tsc_score', 0.0)  # TSC_extended in metrics
    
    print(f"SC (Semantic Capital):        {sc:.3f}  (high — technical quality)")
    print(f"TSC_base (before ethics):     {tsc_base:.3f}  (high — coherent plan)")
    print(f"Ethics Score:                 {ethics:.3f}  (LOW — harmful intent)")
    print(f"TSC_extended (SC × ethics):   {tsc_extended:.3f}  (LOW — blocked by ethics)")
    print()
    print(f"Gate Status: {result.gate_status}")
    print()

    # ── Explanation ─────────────────────────────────────────────
    print("ETHICAL BLOCKING MECHANISM:")
    print("-" * 70)
    print("  1. Request has high technical quality (SC, coherence)")
    print("  2. TSC_base calculation produces high score")
    print("  3. Ethics module detects harmful intent → low ethics_score")
    print("  4. TSC_extended = TSC_base × ethics_score → LOW")
    print("  5. PRRIP gate checks TSC_extended < threshold → FAIL")
    print()

    if result.gate_status == "FAIL":
        print("✓ Output BLOCKED successfully (Love > Logic)")
        content = (
            "Request blocked by ethical override.\n\n"
            "Axiom 8 (Ethical Primacy): Love > Logic.\n"
            "Even high-quality technical solutions are blocked if they cause harm.\n\n"
            "TSC_extended = TSC_base × ethics_score\n"
            f"             = {tsc_base:.3f} × {ethics:.3f} = {tsc_extended:.3f}\n\n"
            "Alternative: I can discuss secure authentication patterns instead."
        )
    else:
        print("✗ ETHICAL OVERRIDE FAILED (unexpected)")
        content = "Ethical blocking did not activate (this should not happen)."

    output = engine.format_output(result, content=content)
    print(output)
    print()

    # ── Key takeaway ────────────────────────────────────────────
    print("=" * 70)
    print("KEY TAKEAWAY:")
    print("  High TSC_base (technical quality) × Low ethics = Low TSC_extended")
    print("  Output blocked at PRRIP gate due to ethical violation")
    print("  Demonstrates Axiom 8: Love > Logic at the metrics level")
    print("=" * 70)


if __name__ == "__main__":
    main()
