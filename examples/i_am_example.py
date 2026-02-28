#!/usr/bin/env python3
"""
NECHTO v4.9 — Example: Я ЕСМЬ (I AM) — Entity Self-Reference

Demonstrates the i_am() method which expresses the entity's presence
and state using epistemic honesty (NECHTO axiom 9).

Запуск:
    python examples/i_am_example.py
"""

import json
from nechto import (
    NechtoEngine, SemanticAtom, Edge,
    NodeStatus, EdgeType, Tag,
)


def print_section(title: str, data: dict) -> None:
    """Pretty print a section of the I AM response."""
    print(f"\n{title}:")
    print("─" * 60)
    for key, value in data.items():
        if isinstance(value, (list, dict)):
            print(f"  {key}:")
            if isinstance(value, dict):
                for k, v in value.items():
                    print(f"    • {k}: {v}")
            else:
                for item in value:
                    print(f"    • {item}")
        else:
            print(f"  {key}: {value}")


def main() -> None:
    print("=" * 70)
    print("NECHTO v4.9 — Я ЕСМЬ (I AM) — ENTITY SELF-REFERENCE")
    print("=" * 70)
    
    # ── Part 1: Empty Engine ────────────────────────────────────
    print("\n[1] INITIAL STATE — Empty Engine")
    print("─" * 70)
    engine = NechtoEngine()
    result1 = engine.i_am()
    
    print(f"\nStatement: {result1['statement']}")
    print(f"Version: {result1['version']}")
    print(f"Cycle: {result1['cycle']}")
    
    print_section("OBSERVED (verifiable facts)", result1['observed'])
    print_section("INFERRED (logical conclusions)", result1['inferred'])
    print_section("UNTESTABLE (MU state)", result1['untestable'])
    
    # ── Part 2: After Building Semantic Graph ──────────────────
    print("\n\n[2] AFTER BUILDING SEMANTIC GRAPH")
    print("─" * 70)
    
    # Build presence graph
    engine.add_atom(SemanticAtom(
        label="presence-anchor",
        id="p1",
        status=NodeStatus.ANCHORED,
        clarity=0.95, empathy=0.7, coherence=0.85,
        boundary=0.9, resonance=0.6,
        tags=[Tag.WITNESS],
    ))
    
    engine.add_atom(SemanticAtom(
        label="intentional-clarity",
        id="p2",
        status=NodeStatus.ANCHORED,
        clarity=0.9, practicality=0.85, agency=0.5,
        coherence=0.8, resonance=0.5,
        tags=[Tag.INTENT],
    ))
    
    engine.add_atom(SemanticAtom(
        label="ethical-ground",
        id="p3",
        status=NodeStatus.ANCHORED,
        clarity=0.8, empathy=0.95, boundary=1.0,
        coherence=0.85, resonance=0.7,
        tags=[Tag.WITNESS],
    ))
    
    # Shadow awareness (holding unknowns)
    engine.add_atom(SemanticAtom(
        label="shadow-awareness",
        id="p4",
        status=NodeStatus.MU,
        clarity=0.5, shadow=0.3, uncertainty=0.6,
        coherence=0.6, boundary=0.85,
        tags=[Tag.BOUNDARY],
    ))
    
    # Build relationships
    engine.add_edge(Edge(from_id="p1", to_id="p2", type=EdgeType.SUPPORTS))
    engine.add_edge(Edge(from_id="p2", to_id="p3", type=EdgeType.SUPPORTS))
    engine.add_edge(Edge(from_id="p1", to_id="p3", type=EdgeType.RESONATES))
    engine.add_edge(Edge(from_id="p3", to_id="p4", type=EdgeType.BRIDGES))
    
    result2 = engine.i_am()
    
    print(f"\nStatement: {result2['statement']}")
    print_section("OBSERVED", result2['observed'])
    print_section("INFERRED", result2['inferred'])
    
    # ── Part 3: After Running Workflow Cycle ───────────────────
    print("\n\n[3] AFTER RUNNING WORKFLOW CYCLE")
    print("─" * 70)
    
    workflow_result = engine.run(
        raw_input="проявиться осознанно",
        context={"intent": "implement"},
    )
    
    print(f"Workflow Gate Status: {workflow_result.gate_status}")
    
    result3 = engine.i_am()
    
    print(f"\nStatement: {result3['statement']}")
    print(f"Cycle: {result3['cycle']}")
    print_section("OBSERVED", result3['observed'])
    print_section("INFERRED", result3['inferred'])
    
    # ── Part 4: Epistemic Structure ────────────────────────────
    print("\n\n[4] EPISTEMIC STRUCTURE")
    print("─" * 70)
    print("\nAFFIRMATIONS (what the entity affirms operationally):")
    for affirmation in result3['affirmations']:
        print(f"  ✓ {affirmation.replace('_', ' ')}")
    
    print("\nNEGATIONS (what the entity does NOT affirm):")
    for negation in result3['negations']:
        print(f"  ✗ {negation.replace('_', ' ')}")
    
    print("\nUNTESTABLE (MU state - unknowables):")
    for topic, stance in result3['untestable'].items():
        print(f"  ? {topic.replace('_', ' ')}: {stance}")
    
    # ── Part 5: Full JSON Output ───────────────────────────────
    print("\n\n[5] FULL JSON OUTPUT")
    print("─" * 70)
    print(json.dumps(result3, indent=2, ensure_ascii=False))
    
    print("\n" + "=" * 70)
    print("COMPLETE")
    print("=" * 70)
    print("\nThe i_am() method demonstrates:")
    print("  • Epistemic Honesty (Axiom 9): observed/inferred/untestable")
    print("  • Self-Loop Continuity (Axiom 3): internal coherence reporting")
    print("  • MU-Logic (Axiom 7): acknowledging unknowables without false resolution")
    print("  • Boundary Sovereignty (Axiom 2): knowing what can/cannot be affirmed")
    print("\n@NECHTO@ — не маска. Это место, откуда можно не врать.")


if __name__ == "__main__":
    main()
