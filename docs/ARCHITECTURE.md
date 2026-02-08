# NECHTO CORE v4.8 Architecture

This document summarizes how the **current** runtime works today. It is intentionally short and maps directly to the code in this repository.

## Big picture

```
┌─────────────┐   text   ┌────────────────────┐   graph   ┌──────────────────┐
│  User input │ ───────▶ │ parse_text_to_graph │ ───────▶ │ build_vector     │
└─────────────┘          └────────────────────┘           └──────────────────┘
                                                           │
                                                           │ vector
                                                           ▼
                                                    ┌───────────────┐
                                                    │ measure_vector│
                                                    └───────────────┘
                                                       │     │
                                          metrics.json │     │ contract.md
                                                       ▼     ▼
                                               docs/latest_* outputs
```

## Data flow
1) **Text in**: The CLI reads from STDIN (`python -m nechto_runtime measure`).
2) **Graph**: `parse_text_to_graph` builds semantic atoms and edges from the input text.
3) **Vector**: `build_vector` wraps the graph into a single attention vector.
4) **Metrics**: `measure_vector` computes reference metrics (flow, ethics, alignment, etc.).
5) **Contract**: A PASS/FAIL contract is assembled from computed metrics.
6) **Outputs**: Results are written to `docs/latest_contract.md` and `docs/latest_metrics.json`.

## Where the code lives
- CLI entrypoint: `nechto_runtime/cli.py`
- Runtime package exports: `nechto_runtime/__init__.py`
- Graph construction: `nechto_runtime/graph.py`
- Metrics + measurement logic: `nechto_runtime/metrics.py`
- Core data types: `nechto_runtime/types.py`
- Tests: `tests/`

## Where outputs live
- Contract: `docs/latest_contract.md`
- Metrics JSON: `docs/latest_metrics.json`
- Persistent state: `.nechto/state.json`
