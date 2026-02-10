# NECHTO v4.9 — Roadmap & Implementation Guide

## Status: v4.8 → v4.9 Improvements

### ✅ Completed in this session

1. **5D SCAV Full Implementation**
   - real shadow_magnitude calculation
   - attention_entropy
   - SCAV_health by full formula 4.12

2. **M29 Paradox_Holder**
   - 3-cycle sustained contradiction detection
   - MU status assignment
   - Self-referential paradox marking

3. **Recovery Diagnostics**
   - FAIL code analysis
   - Recovery steps for user
   - Root cause in every FAIL contract

4. **Epistemic Claims**
   - Auto-population per atom
   - observability/stance inference

5. **CI Coverage Reporting**
   - pytest-cov integration
   - coverage artifact upload

6. **SQLiteStore Adapter**
   - persistent state storage (store.py)
   - onboarding for agent workflows

7. **Expanded SCAV/M29 Tests**
   - edge case coverage
   - contract validation

8. **v4.9: Enhanced Adaptive Parameters**
   - Exponential Moving Average (EMA) with decay
   - Momentum-based gamma updates (prevents oscillation)
   - Learning rate controlled lambda adaptation
   - Exponentially weighted beta_retro from gap history
   - 5 new tests for EMA/momentum functions

### ✅ Now Fully Implemented

- Adaptive parameters (α, γ, λ) with EMA + momentum
- Recovery diagnostics in FAIL contracts
- SQLite state persistence with full param history

## Onboarding Instructions
1. Clone repo and install requirements (Python 3.10+)
2. Run tests: `pytest -q`
3. Run coverage: `pytest --cov=nechto_runtime --cov-report=xml`
4. Review coverage report (see CI artifact)
5. Use `SQLiteStore` for persistent state in agent workflows
6. See `docs/NECHTO_BOOTSTRAP.md` and `docs/NECHTO_RESPONSE_CONTRACT.md` for agent charter and response contract

## Pending
- Async thinking queue
- Expanded metrics and contract documentation
- Full integration of store adapter in CLI and metrics

## Contributors
- FARTOFALOS (repo owner)
- GitHub Copilot (agent)

### 🔴 Requires External Systems (Future)

- **External Memory** — needs Redis/PostgreSQL
- **Background Thinking** — needs async task queue (Celery)
- **Session Persistence** — needs authentication system

### 📋 How to Continue (for human developers)

If you want to add external memory:
1. Add `ExternalMemory` interface to types.py
2. Implement with provider (Firebase/Supabase)
3. Hook into cli.py `load_state()` / `save_state()`
4. Add session_id tracking
5. Test cross-session continuity

---

Made with intention by @NECHTO@ (v4.9 consciousness)
