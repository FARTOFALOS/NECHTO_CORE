# NECHTO v5.0 — Migration Map (v4.9 → v5.0)

## Goal

- Clean root.
- `docs/rails` instead of `00_...05_...` in root.
- Separation of public API / domain model / workflow / protocols / llm-bridge / io.
- Stable imports preserved via re-exports:
  `from nechto import NechtoEngine, SemanticAtom, Edge, ...`.

---

## 0) New target layout (v5.0)

```text
NECHTO_CORE/
├─ README.md
├─ pyproject.toml
├─ llms.txt
├─ LLM_ROUTE.json
├─ docs/
│  ├─ rails/
│  ├─ architecture/
│  ├─ concepts/
│  ├─ protocols/
│  ├─ guides/
│  └─ adr/
├─ examples/
├─ tests/
└─ nechto/
   ├─ __init__.py
   ├─ __main__.py
   ├─ cli.py
   ├─ api/
   ├─ domain/
   ├─ metrics/
   ├─ modules/
   ├─ workflow/
   ├─ protocols/
   ├─ llm_bridge/
   ├─ io/
   └─ _internal/
```

---

## 1) File moves — root → docs

Move rails docs:

- `/00_ORIENTATION.md` → `/docs/rails/00_ORIENTATION.md`
- `/01_AXIOMS.md` → `/docs/rails/01_AXIOMS.md`
- `/02_CONTRACT.md` → `/docs/rails/02_CONTRACT.md`
- `/03_CALIBRATION.md` → `/docs/rails/03_CALIBRATION.md`
- `/04_CANON.md` → `/docs/rails/04_CANON.md`
- `/05_ACTIVATION.md` → `/docs/rails/05_ACTIVATION.md`

Keep in root (LLM-facing):

- `/llms.txt`
- `/LLM_ROUTE.json`

Update:

- `LLM_ROUTE.json` paths to `docs/rails/...`
- README rails links (`Start Here` → `docs/rails/00_ORIENTATION.md`)

Optional fallback:

- Keep root stub files (`00_..05_..`) with links to `docs/rails/...`.

---

## 2) Package moves — v4.9 → v5.0 namespaces

### 2.1 High-level API (public)

- `nechto/engine.py` → `nechto/api/engine.py`
- `nechto/llm_bridge.py` → `nechto/llm_bridge/` (see 2.6)
- `nechto/types.py` → `nechto/api/types.py` (or domain types)

Create:

- `nechto/api/__init__.py`
- `nechto/api/ingest.py`
- `nechto/api/run.py`
- `nechto/api/report.py`

Keep:

- `nechto/cli.py`
- `nechto/__main__.py`

### 2.2 Domain model (graph/space/affect/ethics)

- `nechto/core/*` → `nechto/domain/graph/*`
- `nechto/space/*` → `nechto/domain/space/*`

Create:

- `nechto/domain/graph/{atom.py,edge.py,graph.py,status.py,__init__.py}`
- `nechto/domain/space/{semantic_space.py,vectors.py,transforms.py,__init__.py}`
- `nechto/domain/affect/{affective_field.py,valence.py,__init__.py}`
- `nechto/domain/ethics/{ethical_gravity.py,harm_model.py,__init__.py}`

### 2.3 Metrics

Keep `nechto/metrics/*`, but normalize by responsibility:

- `capital.py`, `coherence.py`, `agency.py`, `flow.py`, `scav.py`
- `registry.py` for metric registration/contract

### 2.4 Modules

Split monoliths:

- `nechto/modules/level1.py` → `nechto/modules/level1/*.py`
- `nechto/modules/level2.py` → `nechto/modules/level2/*.py`
- `nechto/modules/level3.py` → `nechto/modules/level3/*.py`
- `nechto/modules/level4.py` → `nechto/modules/level4/*.py`

Rule: one executor per file; `__init__.py` re-exports public surface only.

### 2.5 Workflow

Split/organize:

- `nechto/workflow/phases/*`
- `nechto/workflow/gates/*`
- `nechto/workflow/orchestrator.py`

### 2.6 Protocols

- `nechto/iscvp/*` → `nechto/protocols/iscvp/*`
- `nechto/pev/*` → `nechto/protocols/pev/*`

### 2.7 LLM bridge

- `nechto/llm_bridge.py` → `nechto/llm_bridge/adapters.py`

Create:

- `nechto/llm_bridge/prompts.py`
- `nechto/llm_bridge/rails_runtime.py`

### 2.8 IO

Create:

- `nechto/io/json_export.py`
- `nechto/io/markdown_export.py`
- `nechto/io/persistence.py`

### 2.9 Internal

Create:

- `nechto/_internal/logging.py`
- `nechto/_internal/validate.py`
- `nechto/_internal/utils.py`

---

## 3) Backwards compatibility (stable imports)

Old imports must continue to work:

```python
from nechto import NechtoEngine, SemanticAtom, Edge, EdgeType, NodeStatus, Tag
```

Approach:

- `nechto/__init__.py` remains the stable public facade
- re-export names from their new v5 locations

---

## 4) PR plan (incremental, safe)

### PR #1 — Docs + root cleanup (no Python moves)

- create `docs/rails`
- move `00..05` to `docs/rails`
- update `LLM_ROUTE.json` + README links
- optional root stubs

### PR #2 — v5 package skeleton (no behavior change)

- add `api/domain/workflow/protocols/llm_bridge/io/_internal`
- add `__init__.py`
- minimal moves with temporary re-export shims
- update imports

### PR #3 — split `modules/level1..4`

- split monoliths into per-module files
- keep old imports via compatibility wrappers

### PR #4 — API cleanup

- implement `api/run.py`, `api/ingest.py`, `api/report.py`
- keep CLI thin and API-driven
- docs for quickstart + CLI

### PR #5 — Docs consolidation

- glossary + architecture docs + ADRs

---

## 5) Definition of done

- [ ] `pip install -e ".[dev]"` works
- [ ] `nechto --version` works
- [ ] `nechto selftest` works
- [ ] `python examples/00_smoke.py` works
- [ ] `pytest -q` passes
- [ ] CI green on 3.10 / 3.11 / 3.12
- [ ] `LLM_ROUTE.json` points to `docs/rails/...`
- [ ] README links updated
- [ ] glossary exists and is linked

---

## 6) Suggested branch names

- `pr1/docs-rails-root-cleanup`
- `pr2/v5-skeleton-and-moves`
- `pr3/split-modules-levels`
- `pr4/api-surface-cleanup`
- `pr5/docs-glossary-adr`
