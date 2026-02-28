from __future__ import annotations

from nechto import (
    Edge,
    EdgeType,
    NechtoEngine,
    NodeStatus,
    SemanticAtom,
    Tag,
)


def main() -> int:
    engine = NechtoEngine()

    engine.add_atom(
        SemanticAtom(
            id="c1",
            label="clarity-of-intent",
            status=NodeStatus.ANCHORED,
            clarity=0.9,
            empathy=0.6,
            coherence=0.8,
            tags=[Tag.WITNESS, Tag.INTENT],
        )
    )
    engine.add_atom(
        SemanticAtom(
            id="c2",
            label="actionable-step",
            status=NodeStatus.ANCHORED,
            clarity=0.7,
            practicality=0.9,
            agency=0.5,
            tags=[Tag.INTENT],
        )
    )
    engine.add_edge(Edge(from_id="c1", to_id="c2", type=EdgeType.SUPPORTS))

    result = engine.run("implement", context={"intent": "implement"})

    print("gate_status:", getattr(result, "gate_status", "UNKNOWN"))
    metrics = getattr(result, "metrics", None)
    if isinstance(metrics, dict) and metrics:
        for k in ("TSC_extended", "SCAV_health", "FLOW"):
            if k in metrics:
                print(f"{k}: {metrics[k]}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
