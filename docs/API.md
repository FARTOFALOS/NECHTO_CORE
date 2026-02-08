# NECHTO CORE v4.8 API

This document only describes entrypoints that exist in the current runtime.

## CLI

### `python -m nechto_runtime measure`
Reads all input from STDIN, runs a measurement, and writes outputs to:
- `docs/latest_contract.md`
- `docs/latest_metrics.json`

The CLI also maintains a minimal state file at `.nechto/state.json`.

Example:
```bash
echo "Я ЕСМЬ. Объясни MU-логику." | python -m nechto_runtime measure
```

## Python entrypoints

The runtime exports a small set of functions and types via `nechto_runtime/__init__.py`:

```python
from nechto_runtime import (
    SemanticAtom,
    Edge,
    Vector,
    State,
    EpistemicClaim,
    parse_text_to_graph,
    build_vector,
    compute_flow,
    harm_probability,
    identity_alignment,
    ethical_coefficient,
    executable,
    measure_text,
)
```

### `measure_text(text: str, state: State, intent: str = "implement")`
Convenience function that builds the graph + vector and returns `(metrics, contract)`.

### `parse_text_to_graph(text: str)` / `build_vector(atoms, edges)`
Lower-level primitives for building the graph and vector before scoring.

### Other helpers
`compute_flow`, `harm_probability`, `identity_alignment`, `ethical_coefficient`, and `executable` are deterministic helpers used by the measurement pipeline.

> Note: The runtime is intentionally minimal and may change; treat these functions as low-level building blocks, not a fully stable public SDK.
