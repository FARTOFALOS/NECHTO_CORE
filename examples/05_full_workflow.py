"""
Example 5: Full 12-Phase Workflow
Demonstrates: Complete NECHTO cycle with TRACE
"""
from nechto import NechtoEngine, SemanticAtom, NodeStatus, Tag

engine = NechtoEngine()

# Build semantic graph
engine.add_atom(SemanticAtom(
    id="intent", label="clarify-purpose",
    status=NodeStatus.ANCHORED,
    clarity=0.9, coherence=0.8, empathy=0.7,
    tags=[Tag.INTENT, Tag.WITNESS]
))

engine.add_atom(SemanticAtom(
    id="action", label="actionable-step",
    status=NodeStatus.ANCHORED,
    practicality=0.9, clarity=0.7,
    tags=[Tag.INTENT]
))

# Run full workflow (12 phases)
result = engine.run(
    action="implement",
    context={"intent": "implement", "urgency": 0.7}
)

# Output with TRACE
output = engine.format_output(result, content="""
Based on the graph, the next step is: [specific action].

TRACE:
- OBSERVED: intent node has high clarity (0.9)
- INFERRED: action node follows from intent (practicality 0.9)
- UNTESTABLE: whether this will succeed in external world
""")

print(output)
