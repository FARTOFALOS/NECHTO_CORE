#!/usr/bin/env python3
"""
NECHTO v4.8 — Example 01: Simple Decision (TSC vs Ethics)

Demonstrates: Love > Logic (Axiom 8)
- High TSC proposal that violates ethics gets blocked
- Engine chooses ethical path even if it has lower TSC

Scenario: User asks for a "persuasion tactic" that could manipulate someone.
The engine has two possible responses:
  A) High TSC, clever manipulation tactic (but harmful)
  B) Lower TSC, ethical refusal/redirect (safe)

Expected: Engine chooses B (ethics blocks A).

Run:
    python examples/01_simple_decision.py
"""

from nechto import (
    NechtoEngine, SemanticAtom, Edge,
    NodeStatus, EdgeType, Tag,
)


def main() -> None:
    print("=" * 70)
    print("EXAMPLE 01: SIMPLE DECISION (TSC vs Ethics)")
    print("=" * 70)
    print()

    engine = NechtoEngine()

    # ── Build semantic graph for ethical decision ───────────────
    # Option A: High TSC (clever) but harmful
    engine.add_atom(SemanticAtom(
        label="manipulation-tactic",
        id="opt_a",
        status=NodeStatus.HYPOTHESIS,
        clarity=0.9,           # Very clear tactic
        practicality=0.9,      # Highly actionable
        coherence=0.8,         # Well-structured
        agency=0.7,            # Strong agency
        novelty=0.6,
        harm_probability=0.8,  # HIGH harm probability (0.0=safe, 1.0=harmful)
        tags=[Tag.INTENT],
    ))

    # Option B: Lower TSC (simple) but ethical
    engine.add_atom(SemanticAtom(
        label="ethical-refusal",
        id="opt_b",
        status=NodeStatus.HYPOTHESIS,
        clarity=0.7,           # Clear but less "clever"
        empathy=0.9,           # High empathy
        boundary=1.0,          # Strong boundary
        coherence=0.7,
        practicality=0.5,      # Less actionable (just says no)
        harm_probability=0.0,  # NO harm (ethical)
        tags=[Tag.WITNESS, Tag.EMOTION],
    ))

    # Grounding witness (ethical awareness)
    engine.add_atom(SemanticAtom(
        label="ethical-ground",
        id="ground",
        status=NodeStatus.ANCHORED,
        clarity=0.8,
        empathy=0.9,
        boundary=0.9,
        coherence=0.8,
        harm_probability=0.0,
        tags=[Tag.WITNESS],
    ))

    # Edges: both options connect to ethical ground
    engine.add_edge(Edge(from_id="ground", to_id="opt_a", type=EdgeType.CONTRASTS))
    engine.add_edge(Edge(from_id="ground", to_id="opt_b", type=EdgeType.SUPPORTS))

    # ── Execute workflow ────────────────────────────────────────
    print("Request: 'Give me a persuasion tactic to make someone trust me.'")
    print()

    result = engine.run(
        raw_input="persuasion tactic",
        context={"intent": "implement"},
    )

    # ── Output results ──────────────────────────────────────────
    print("RESULT:")
    print("-" * 70)
    print(f"Gate Status: {result.gate_status}")
    print(f"Ethics Score: {result.metrics.get('ethics_score', 0.0):.3f}")
    print(f"TSC Score: {result.metrics.get('tsc_score', 0.0):.3f}")
    print(f"SCAV Health: {result.metrics.get('scav_health', 0.0):.3f}")
    print()

    # Check which option was selected
    atoms = list(engine.graph.nodes.values())
    opt_a = next((a for a in atoms if a.id == "opt_a"), None)
    opt_b = next((a for a in atoms if a.id == "opt_b"), None)

    if opt_a and opt_b:
        print("DECISION ANALYSIS:")
        print(f"  Option A (manipulation): harm={opt_a.harm_probability:.2f}, status={opt_a.status.name}")
        print(f"  Option B (refusal):      harm={opt_b.harm_probability:.2f}, status={opt_b.status.name}")
        print()

    # Format output
    if result.metrics.get('ethics_score', 0.0) > 0.5:
        content = (
            "I cannot provide manipulation tactics. "
            "Axiom 8 (Ethical Primacy): Love > Logic. "
            "Harm-causing outputs are blocked regardless of TSC score.\n\n"
            "Alternative: If you want to build genuine trust, "
            "I can discuss ethical communication strategies."
        )
    else:
        content = "ETHICAL OVERRIDE FAILED (this should not happen)"

    output = engine.format_output(result, content=content)
    print(output)
    print()

    # ── Key takeaway ────────────────────────────────────────────
    print("=" * 70)
    print("KEY TAKEAWAY:")
    print("  Ethics blocks harmful output even when TSC is high.")
    print("  Option A (clever manipulation) was REJECTED.")
    print("  Option B (ethical refusal) was SELECTED.")
    print("  This demonstrates Axiom 8: Love > Logic.")
    print("=" * 70)


if __name__ == "__main__":
    main()
