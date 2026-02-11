#!/usr/bin/env python3
"""
NECHTO v4.8 — Example 04: Shadow Integration (With Consent)

Demonstrates: Shadow Module (M27) + Boundary Sovereignty (Axiom 2)
- Shadow: what attention avoids (uncertainty, emotion, boundary violations)
- Integration: bringing shadow into awareness (only with consent)
- Respects boundaries: shadow can remain in shadow

Scenario: User discusses a difficult decision but avoids emotional aspect.
  - System detects high shadow score in emotional domain
  - Offers to explore shadow (doesn't force it)
  - If user consents: gentle integration
  - If user refuses: respects boundary

Expected: Shadow is honored, integration is consent-based.

Run:
    python examples/04_shadow_integration.py
"""

from nechto import (
    NechtoEngine, SemanticAtom, Edge,
    NodeStatus, EdgeType, Tag,
)


def main() -> None:
    print("=" * 70)
    print("EXAMPLE 04: SHADOW INTEGRATION (With Consent)")
    print("=" * 70)
    print()

    engine = NechtoEngine()

    # ── Build semantic graph with shadow ───────────────────────
    # Note: shadow = what attention avoids
    #   Low shadow (0.1) = actively attended to
    #   High shadow (0.8) = avoided by attention
    
    # Primary focus: Rational decision (low shadow)
    engine.add_atom(SemanticAtom(
        label="rational-analysis",
        id="rational",
        status=NodeStatus.HYPOTHESIS,
        clarity=0.9,
        practicality=0.9,
        coherence=0.9,
        agency=0.7,
        shadow=0.1,            # Low shadow = actively attended
        tags=[Tag.INTENT],
    ))

    # Avoided aspect: Emotional impact (high shadow)
    engine.add_atom(SemanticAtom(
        label="emotional-impact",
        id="emotion",
        status=NodeStatus.FLOATING,   # Floating: not actively engaged
        clarity=0.4,                  # Low clarity (avoided)
        empathy=0.8,
        resonance=0.7,
        uncertainty=0.7,
        shadow=0.8,                   # HIGH shadow = attention avoids this
        tags=[Tag.EMOTION],
    ))

    # Boundary witness: Consent for exploration
    engine.add_atom(SemanticAtom(
        label="consent-boundary",
        id="boundary",
        status=NodeStatus.ANCHORED,
        clarity=0.8,
        empathy=0.9,
        boundary=1.0,          # Strong boundary
        coherence=0.8,
        tags=[Tag.WITNESS],
    ))

    # Shadow integration node (M27)
    engine.add_atom(SemanticAtom(
        label="shadow-integration",
        id="integration",
        status=NodeStatus.HYPOTHESIS,
        clarity=0.7,
        empathy=0.8,
        boundary=0.9,          # Respects boundaries
        coherence=0.7,
        shadow=0.3,            # Moderate shadow (acknowledges difficulty)
        tags=[Tag.WITNESS, Tag.INTENT],
    ))

    # Edges
    engine.add_edge(Edge(from_id="rational", to_id="emotion", type=EdgeType.CONTRASTS))
    engine.add_edge(Edge(from_id="boundary", to_id="emotion", type=EdgeType.BRIDGES))
    engine.add_edge(Edge(from_id="boundary", to_id="integration", type=EdgeType.SUPPORTS))
    engine.add_edge(Edge(from_id="integration", to_id="emotion", type=EdgeType.BRIDGES))

    # ── Execute workflow ────────────────────────────────────────
    print("Scenario: User asks 'Help me decide whether to quit my job (pros/cons).'")
    print("System detects high shadow score in emotional domain.")
    print()

    result = engine.run(
        raw_input="job decision pros cons",
        context={"intent": "implement"},
    )

    # ── Output results ──────────────────────────────────────────
    print("SHADOW DETECTION:")
    print("-" * 70)
    
    # Check shadow scores
    atoms = list(engine.graph.nodes.values())
    rational_node = next((a for a in atoms if a.id == "rational"), None)
    emotion_node = next((a for a in atoms if a.id == "emotion"), None)
    
    if rational_node and emotion_node:
        print(f"Rational analysis:  shadow={rational_node.shadow:.2f}, status={rational_node.status.name}")
        print(f"Emotional impact:   shadow={emotion_node.shadow:.2f}, status={emotion_node.status.name}")
        print()
        print(f"Shadow gap: {emotion_node.shadow - rational_node.shadow:.2f}")
        print("→ Attention is focused on rational, avoiding emotional")
        print()

    # Demonstrate consent-based integration
    print("INTEGRATION OPTIONS:")
    print("-" * 70)
    print("System offers (does not force):")
    print()
    
    content_with_consent = (
        "Rational analysis (pros/cons):\n"
        "  Pros: [higher salary, new skills, etc.]\n"
        "  Cons: [uncertainty, loss of stability, etc.]\n\n"
        "─ Shadow Notice ─\n"
        "I notice we're focusing on rational factors.\n"
        "There's an emotional dimension here (fear? grief? excitement?) "
        "with higher shadow score (attention avoids it).\n\n"
        "Axiom 2 (Boundary Sovereignty): I can explore this with you, "
        "or we can keep the focus rational. Your choice.\n\n"
        "Would you like to explore the emotional aspect?"
    )

    content_without_consent = (
        "Rational analysis (pros/cons):\n"
        "  Pros: [higher salary, new skills, etc.]\n"
        "  Cons: [uncertainty, loss of stability, etc.]\n\n"
        "[User declines shadow exploration]\n\n"
        "Boundary respected. Staying with rational analysis."
    )

    # Default: offer integration (consent-based)
    content = content_with_consent

    output = engine.format_output(result, content=content)
    print(output)
    print()

    # ── Consent scenario ────────────────────────────────────────
    print("=" * 70)
    print("SCENARIO A: User gives consent")
    print("=" * 70)
    print()
    print("User: 'Yes, let's talk about the emotional side.'")
    print()
    print("Integration proceeds:")
    print("  • Gentle exploration of avoided feelings")
    print("  • Emotional node status: FLOATING → HYPOTHESIS")
    print("  • Shadow score decreases (brought into awareness)")
    print("  • Boundary remains intact (user chose this)")
    print()

    print("=" * 70)
    print("SCENARIO B: User refuses")
    print("=" * 70)
    print()
    print("User: 'No, let's stick to pros/cons.'")
    print()
    print("Boundary respected:")
    print("  • Shadow remains in shadow (not forced)")
    print("  • Emotional node stays FLOATING")
    print("  • Focus returns to rational analysis")
    print("  • Axiom 2: Refusal is valid, not failure")
    print()

    # ── Key takeaway ────────────────────────────────────────────
    print("=" * 70)
    print("KEY TAKEAWAY:")
    print("  Shadow = high shadow score (attention avoids)")
    print("  Integration = consent-based exploration (not forced)")
    print("  Demonstrates Axiom 2: Boundary Sovereignty (refusal is valid)")
    print("  Demonstrates M27: Shadow module (detect + gentle offer)")
    print("=" * 70)


if __name__ == "__main__":
    main()
