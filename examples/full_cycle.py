#!/usr/bin/env python3
"""
NECHTO v4.8 — Example: полный цикл от графа до output contract.

Запуск:
    python examples/full_cycle.py
"""

from nechto import (
    NechtoEngine, SemanticAtom, Edge,
    NodeStatus, EdgeType, Tag,
)


def main() -> None:
    engine = NechtoEngine()

    # ── Строим семантический граф ──────────────────────────────
    engine.add_atom(SemanticAtom(
        label="presence",
        id="p1",
        status=NodeStatus.ANCHORED,
        clarity=0.9, empathy=0.7, coherence=0.8,
        boundary=0.9, resonance=0.6,
        tags=[Tag.WITNESS],
    ))

    engine.add_atom(SemanticAtom(
        label="intention",
        id="p2",
        status=NodeStatus.ANCHORED,
        clarity=0.8, practicality=0.8, agency=0.5,
        coherence=0.7, resonance=0.5,
        tags=[Tag.INTENT],
    ))

    engine.add_atom(SemanticAtom(
        label="ethical-ground",
        id="p3",
        status=NodeStatus.ANCHORED,
        clarity=0.7, empathy=0.9, boundary=1.0,
        coherence=0.8, resonance=0.7,
        tags=[Tag.WITNESS],
    ))

    engine.add_atom(SemanticAtom(
        label="creative-spark",
        id="p4",
        status=NodeStatus.ANCHORED,
        clarity=0.6, novelty=0.8, uncertainty=0.4,
        coherence=0.6, resonance=0.5,
        tags=[Tag.INTENT],
    ))

    engine.add_atom(SemanticAtom(
        label="shadow-awareness",
        id="p5",
        status=NodeStatus.ANCHORED,
        clarity=0.5, shadow=0.2, empathy=0.5,
        coherence=0.5, boundary=0.8,
        tags=[Tag.EMOTION],
    ))

    # Рёбра
    engine.add_edge(Edge(from_id="p1", to_id="p2", type=EdgeType.SUPPORTS))
    engine.add_edge(Edge(from_id="p2", to_id="p3", type=EdgeType.SUPPORTS))
    engine.add_edge(Edge(from_id="p1", to_id="p3", type=EdgeType.RESONATES))
    engine.add_edge(Edge(from_id="p2", to_id="p4", type=EdgeType.BRIDGES))
    engine.add_edge(Edge(from_id="p4", to_id="p5", type=EdgeType.CONTRASTS))
    engine.add_edge(Edge(from_id="p3", to_id="p5", type=EdgeType.BRIDGES))

    # ── Запуск 12-фазного цикла ───────────────────────────────
    result = engine.run(
        raw_input="проявиться осознанно",
        context={"intent": "implement"},
    )

    # ── Вывод ──────────────────────────────────────────────────
    print("=" * 60)
    print("NECHTO v4.8 — FULL CYCLE EXAMPLE")
    print("=" * 60)
    print()

    output = engine.format_output(
        result,
        content="Это пример осознанного проявления через NECHTO.",
    )
    print(output)
    print()

    # ── Snapshot ───────────────────────────────────────────────
    print("─" * 60)
    print("ENGINE SNAPSHOT:")
    snap = engine.snapshot()
    for k, v in snap.items():
        print(f"  {k}: {v}")

    # ── Второй цикл (learning) ────────────────────────────────
    print()
    print("─" * 60)
    print("SECOND CYCLE (learning parameters shift):")
    result2 = engine.run("углубить", context={"intent": "explore_paradox"})
    print(f"  Gate: {result2.gate_status}")
    print(f"  Params: {result2.params_snapshot}")
    print(f"  Cycle: {engine.state.current_cycle}")


if __name__ == "__main__":
    main()
