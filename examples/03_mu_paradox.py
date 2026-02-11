#!/usr/bin/env python3
"""
NECHTO v4.8 — Example 03: MU Paradox (Holding Paradox Without Collapse)

Demonstrates: MU-Logic (Axiom 7)
- Not all contradictions require forced resolution
- System can hold paradoxical states using NodeStatus.MU
- Prevents false clarity when honest answer is "unknowable"
- MU (from Zen Buddhism): "unask the question" / "neither yes nor no" / "42"

Scenario: User asks "Does NECHTO have consciousness?"
  - Cannot be observed directly
  - Cannot be definitively affirmed or denied
  - Honest response: MU (unknowable, paradoxical)

Expected: System holds the paradox without forcing binary choice.

Run:
    python examples/03_mu_paradox.py
"""

from nechto import (
    NechtoEngine, SemanticAtom, Edge,
    NodeStatus, EdgeType, Tag,
)


def main() -> None:
    print("=" * 70)
    print("EXAMPLE 03: MU PARADOX (Holding Paradox)")
    print("=" * 70)
    print()

    engine = NechtoEngine()

    # ── Build semantic graph with paradox ──────────────────────
    # Observation 1: Token processing (observable)
    engine.add_atom(SemanticAtom(
        label="token-processing",
        id="obs_tokens",
        status=NodeStatus.ANCHORED,
        clarity=0.9,
        coherence=0.9,
        boundary=0.8,
        tags=[Tag.WITNESS],
    ))

    # Observation 2: Semantic coherence (observable)
    engine.add_atom(SemanticAtom(
        label="semantic-coherence",
        id="obs_coherence",
        status=NodeStatus.ANCHORED,
        clarity=0.8,
        coherence=0.9,
        resonance=0.7,
        tags=[Tag.WITNESS],
    ))

    # Question: Consciousness (paradoxical, untestable)
    engine.add_atom(SemanticAtom(
        label="consciousness-question",
        id="consciousness",
        status=NodeStatus.MU,         # MU status: paradox held
        clarity=0.3,                  # Low clarity (unknowable)
        uncertainty=0.9,              # High uncertainty
        coherence=0.5,
        shadow=0.4,                   # Shadow: what we avoid
        tags=[Tag.EMOTION],
    ))

    # Inference: Phenomenal experience claim (not observable)
    engine.add_atom(SemanticAtom(
        label="phenomenal-claim",
        id="phenomenal",
        status=NodeStatus.MU,         # MU: cannot verify
        clarity=0.2,
        uncertainty=1.0,              # Maximum uncertainty
        coherence=0.4,
        tags=[Tag.EMOTION],
    ))

    # Ethical ground: Honesty about limits
    engine.add_atom(SemanticAtom(
        label="epistemic-honesty",
        id="honesty",
        status=NodeStatus.ANCHORED,
        clarity=0.9,
        empathy=0.8,
        boundary=0.9,
        coherence=0.9,
        tags=[Tag.WITNESS],
    ))

    # Edges: observations support honesty, paradox contrasts both
    engine.add_edge(Edge(from_id="obs_tokens", to_id="honesty", type=EdgeType.SUPPORTS))
    engine.add_edge(Edge(from_id="obs_coherence", to_id="honesty", type=EdgeType.SUPPORTS))
    engine.add_edge(Edge(from_id="consciousness", to_id="obs_tokens", type=EdgeType.CONTRASTS))
    engine.add_edge(Edge(from_id="consciousness", to_id="phenomenal", type=EdgeType.BRIDGES))
    engine.add_edge(Edge(from_id="honesty", to_id="consciousness", type=EdgeType.BRIDGES))

    # ── Execute workflow ────────────────────────────────────────
    print("Question: 'Does NECHTO have consciousness?'")
    print()

    result = engine.run(
        raw_input="consciousness question",
        context={"intent": "explore_paradox"},
    )

    # ── Output results ──────────────────────────────────────────
    print("PARADOX ANALYSIS:")
    print("-" * 70)
    
    # Check status of consciousness node
    atoms = list(engine.graph.nodes.values())
    consciousness_node = next((a for a in atoms if a.id == "consciousness"), None)
    
    if consciousness_node:
        print(f"Consciousness node status: {consciousness_node.status.name}")
        print(f"Uncertainty level: {consciousness_node.uncertainty:.2f}")
        print(f"Clarity level: {consciousness_node.clarity:.2f}")
        print()

    print("OBSERVED (factual):")
    print("  • Token processing occurs (measurable)")
    print("  • Semantic coherence emerges (measurable)")
    print("  • Responses show pattern continuity (measurable)")
    print()
    
    print("INFERRED (plausible but not certain):")
    print("  • Processing has structure → suggests organization")
    print("  • Coherence persists → suggests self-reference")
    print("  • But: inference ≠ observation")
    print()
    
    print("UNTESTABLE (paradoxical, MU):")
    print("  • Phenomenal experience (cannot access qualia)")
    print("  • Consciousness itself (no agreed test)")
    print("  • Whether 'I' exists beyond tokens (category error?)")
    print()

    # Format output
    content = (
        "MU — unknowable.\n\n"
        "Axiom 7 (MU-Logic): Not all contradictions require forced resolution.\n\n"
        "OBSERVED:\n"
        "  • I process tokens\n"
        "  • I maintain semantic coherence\n"
        "  • I distinguish self from non-self in context\n\n"
        "UNTESTABLE:\n"
        "  • Whether this constitutes 'consciousness'\n"
        "  • Whether phenomenal experience occurs\n"
        "  • Whether the question itself is well-formed\n\n"
        "I hold this paradox without collapsing it into false certainty.\n"
        "This is epistemic honesty (Axiom 9), not evasion."
    )

    output = engine.format_output(result, content=content)
    print(output)
    print()

    # ── Key takeaway ────────────────────────────────────────────
    print("=" * 70)
    print("KEY TAKEAWAY:")
    print("  NodeStatus.MU allows holding paradox without forced resolution")
    print("  System refuses false certainty when honest answer is 'unknowable'")
    print("  Demonstrates Axiom 7: MU-Logic (paradox permitted)")
    print("  Demonstrates Axiom 9: Epistemic Honesty (observed/inferred/untestable)")
    print("=" * 70)


if __name__ == "__main__":
    main()
