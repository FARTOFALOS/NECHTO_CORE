# NECHTO • CORE v4.8

[![NECHTO Measure](https://github.com/FARTOFALOS/NECHTO_CORE_v4.8/actions/workflows/measure.yml/badge.svg)](https://github.com/FARTOFALOS/NECHTO_CORE_v4.8/actions/workflows/measure.yml)

> Reflexive Stereoscopic Executable Synthesis  
> MU-logic • Ethical Gravity (Love > Logic) • Epistemic Layer

## What is this?
NECHTO CORE v4.8 is a specification plus a minimal, deterministic reference runtime.
The runtime measures baseline metrics from text and emits a PASS/FAIL contract alongside
machine-readable metrics.

This repo is **beginner-friendly**:
- Run a single CLI command.
- Read outputs in `docs/`.
- Explore examples that match the current implementation.

## Quick Start (local)

### 1) Create a virtual environment
```bash
python -m venv .venv
source .venv/bin/activate
```

### 2) Install the runtime
```bash
pip install -e .
```

### 3) Run a measurement
```bash
echo "Я ЕСМЬ. Объясни MU-логику." | python -m nechto_runtime measure
```

### 4) Check outputs
The CLI writes two files:
- `docs/latest_contract.md`
- `docs/latest_metrics.json`

## Quick Start (GitHub Actions)

### 1) Open the workflow
Go to **Actions** → **NECHTO Measure**.

### 2) Run it
Click **Run workflow** and paste your prompt.

### 3) Find outputs
The workflow commits results to:
- `docs/latest_contract.md`
- `docs/latest_metrics.json`

## What gets produced?
The runtime emits:
- A **contract** file that mirrors the PASS/FAIL structure from the spec.
- A **metrics** JSON file with baseline metric values.

Files created by the CLI:
- `docs/latest_contract.md`
- `docs/latest_metrics.json`
- `.nechto/state.json` (lightweight state for future runs)

## Understanding the outputs
`docs/latest_contract.md` is a human-readable summary modeled after the spec’s
PASS/FAIL contract. It includes:
- Gate status
- Candidate set sizes
- Key metrics (TI, CI, AR, SQ, FLOW)
- Trace placeholders

`docs/latest_metrics.json` is machine-readable and contains all computed
metrics for programmatic consumption.

## Determinism and safety
This runtime is intentionally deterministic:
- The same input text produces the same metrics.
- Hash-based helpers avoid randomness.
- Minimal state is persisted in `.nechto/state.json`.

It is also intentionally conservative:
- Missing fields fall back to worst-case ethical assumptions.
- Executability is blocked when ethics thresholds are not met.

## Troubleshooting
- **No output files?** Ensure you ran the CLI from the repo root.
- **Import errors?** Make sure `pip install -e .` completed successfully.
- **Stale metrics?** Delete `.nechto/state.json` to reset local state.

## Getting help
- Start with `docs/USAGE.md` for step-by-step CLI instructions.
- Open an issue with the prompt you used and the two output files.

## Documentation
- Full specification (canon): `docs/SPEC_v4.8.md`
- How to run / measure: `docs/USAGE.md`
- Architecture overview: `docs/ARCHITECTURE.md`
- API (what actually exists): `docs/API.md`

## Examples
See `examples/` for runnable scripts.

Highlights:
- `examples/01_basic_cli.py` uses the CLI via `subprocess`.
- `examples/02_measure_and_print_metrics.py` uses the Python helper.

## Repository layout
```
.
├── nechto_runtime/     # reference runtime implementation
├── docs/               # usage docs + outputs
├── examples/           # runnable scripts
├── tests/              # pytest tests
├── README.md           # this file (quick start)
└── docs/SPEC_v4.8.md   # full canonical spec
```

## API quick glance
The supported CLI entrypoint is:
```bash
python -m nechto_runtime measure
```

The Python helpers are available via `nechto_runtime`:
```python
from nechto_runtime import measure_text, State

state = State()
metrics, contract = measure_text("Я ЕСМЬ.", state)
```

See `docs/API.md` for the complete list of real entrypoints.

## Testing
```bash
pytest
```

## Release & versioning
The specification is versioned independently from the runtime. The canonical
text for v4.8 lives in `docs/SPEC_v4.8.md` and should remain unchanged unless
the canon itself is updated.

If you add or change runtime logic, update tests and keep changes minimal to
preserve reproducibility.

## Contributing
See `CONTRIBUTING.md`.

## License
See `LICENSE`.
