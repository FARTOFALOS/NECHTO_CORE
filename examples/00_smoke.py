"""Minimal NECHTO smoke example."""

from nechto import Edge, EdgeType, NechtoEngine, NodeStatus, SemanticAtom

engine = NechtoEngine()
engine.add_atom(SemanticAtom(id="a1", label="input", status=NodeStatus.ANCHORED, clarity=0.8))
engine.add_atom(SemanticAtom(id="a2", label="output", status=NodeStatus.FLOATING, coherence=0.7))
engine.add_edge(Edge(from_id="a1", to_id="a2", type=EdgeType.SUPPORTS))

result = engine.run("implement", context={"intent": "implement"})
print("NECHTO smoke complete")
print(f"gate_status={result.gate_status}")
print(f"nodes={len(engine.graph.nodes)} edges={len(engine.graph.edges)}")
