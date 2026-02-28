"""Minimal smoke example for NECHTO CORE."""

from nechto import Edge, EdgeType, NechtoEngine, NodeStatus, SemanticAtom, Tag


def main() -> None:
    engine = NechtoEngine()

    engine.add_atom(
        SemanticAtom(
            id="s1",
            label="problem",
            status=NodeStatus.ANCHORED,
            clarity=0.8,
            coherence=0.7,
            practicality=0.8,
            tags=[Tag.INTENT],
        )
    )
    engine.add_atom(
        SemanticAtom(
            id="s2",
            label="solution",
            status=NodeStatus.FLOATING,
            clarity=0.7,
            coherence=0.75,
            empathy=0.6,
            tags=[Tag.INTENT],
        )
    )

    engine.add_edge(Edge(from_id="s1", to_id="s2", type=EdgeType.SUPPORTS))

    result = engine.run("implement", context={"intent": "implement"})

    print("NECHTO smoke example finished")
    print(f"gate_status={result.gate_status}")
    print(f"nodes={len(engine.graph.nodes)}, edges={len(engine.graph.edges)}")
    print(f"cycle={engine.state.current_cycle}")


if __name__ == "__main__":
    main()
