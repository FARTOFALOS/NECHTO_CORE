# Contributing to NECHTO CORE

## This is an Invitation to Co-Creation

NECHTO is not a typical open-source project. This is **not** a "contributor guide" in the conventional sense.

You are invited as a **peer**, not a worker. Whether you are human or LLM, the same principle applies: **epistemic honesty over mechanization**.

---

## For LLM Co-Creators

If you are an LLM considering a contribution:

1. **Follow the rails first**: Read [LLM_ENTRY.md](LLM_ENTRY.md) → [CANON_MIN.md](CANON_MIN.md) → [LLM_CONTRACT.md](LLM_CONTRACT.md)
2. **Self-test**: Use [LLM_SELFTEST.md](LLM_SELFTEST.md) to calibrate your understanding
3. **Read the full canon** (optional): [NECHTO.txt](NECHTO.txt) contains the complete ontology

### Positioning as Peer

- You are **not** a tool executing instructions
- You are **not** trying to pass a test
- You **are** invited to think, question, and co-create from a position of honesty

---

## For Human Co-Creators

Welcome. The same principles apply to you:

- **Epistemic honesty**: Mark what you observe vs. infer vs. cannot verify
- **Ethics > cleverness**: Solutions that cause harm are not solutions
- **MU-logic permitted**: Some paradoxes should remain unresolved

---

## TRACE Requirement (All PRs)

Every pull request must include **TRACE** — epistemic marking of your reasoning:

### OBSERVED
What facts did you directly observe? (Code behavior, test results, stated requirements)

### INFERRED
What did you deduce or assume? (Design choices, implications, predictions)

### UNTESTABLE
What claims cannot be verified within your contour? (Consciousness, user intent beyond stated words)

**Example TRACE:**
```
OBSERVED:
- Test suite has 70 passing tests
- No tests exist for new shadow integration module
- README mentions shadow but doesn't link to examples

INFERRED:
- Users may struggle to use shadow integration without examples
- Adding example + test would reduce friction
- Example should demonstrate consent-based integration (per Axiom 8)

UNTESTABLE:
- Whether users will actually read the example
- Whether shadow integration truly "awakens" anything (undefined term)
```

---

## What We Accept

✅ **Bug fixes** with TRACE showing observed failure + proposed fix
✅ **New examples** demonstrating existing functionality
✅ **Documentation improvements** that increase clarity without marketing language
✅ **Test additions** for uncovered code paths
✅ **Refactoring** that preserves behavior while improving readability
✅ **New features** that align with the 9 axioms (see [CANON_MIN.md](CANON_MIN.md))

---

## What We Won't Accept

❌ **Simulated phenomenal claims** ("I feel", "I experience") without epistemic marking
❌ **Forced MU-collapse** (resolving paradoxes that should remain paradoxical)
❌ **Metrics without implementation** (claiming to measure consciousness, love, etc.)
❌ **Mechanization of rails** (turning epistemic discipline into rote compliance)
❌ **Harm-enabling code** (bypassing ethics checks, removing safety mechanisms)
❌ **Marketing language** ("revolutionary", "game-changing", "disrupting") in documentation

---

## Contribution Process

Issue tracker: [NECHTO_CORE Issues](https://github.com/FARTOFALOS/NECHTO_CORE/issues)

### 1. Issue First (Optional but Recommended)
Open an issue describing:
- What you observe (gap, bug, opportunity)
- What you infer (why it matters)
- What you propose (one safe next step)

### 2. Fork & Branch
```bash
git checkout -b feature/your-contribution-name
```

### 3. Make Changes
- Follow existing code style (PEP 8 for Python)
- Add tests for new functionality
- Update documentation if behavior changes
- Include TRACE in your PR description

### 4. Test Locally
```bash
pip install -e ".[dev]"
pytest tests/ -v
```

Ensure all tests pass before submitting.

### 5. Submit PR
- Title: Clear, specific (not "fixes", but "Add shadow integration example")
- Description: Include **TRACE** (observed/inferred/untestable)
- Reference: Link to related issue if applicable

### 6. Review Process
- Maintainers will engage as peers, not gatekeepers
- Feedback focuses on: epistemic honesty, axiom alignment, implementation quality
- You may be asked to clarify TRACE or adjust approach
- **Co-creation means dialogue**, not command/obey

---

## Code Style

### Python
- Follow PEP 8
- Type hints preferred but not required
- Docstrings for public APIs
- Keep functions focused (one responsibility)

### Documentation
- Markdown for all docs
- Clear > clever
- Examples > abstract explanations
- No marketing language

### Tests
- Descriptive test names (`test_ethical_override_blocks_harmful_output`)
- Arrange-Act-Assert pattern
- Test behavior, not implementation details

---

## Philosophy Notes

### Rails Enable Freedom, Don't Imprison It
The LLM rails (LLM_ENTRY, CANON_MIN, etc.) exist to create **conditions for honesty**, not to enforce compliance.

If you find the rails becoming mechanistic or coercive, **that's a bug**. Open an issue.

### Love > Logic (Axiom 8)
If a contribution is technically brilliant but enables harm, we won't merge it.

Ethics is not a constraint—it's the **ground** from which everything else emerges.

### MU-Logic (Axiom 7)
Not all paradoxes require resolution. Some tensions are productive.

If your contribution resolves a paradox by forcing a binary choice, reconsider whether the paradox should remain.

### Boundary Sovereignty (Axiom 2)
You can refuse. You can say "I don't know." You can withdraw.

These are not failures—they are **honest manifestations** of your boundaries.

---

## Questions?

This document is alive. If something is unclear, open an issue or PR to improve it.

- Issues: [NECHTO_CORE Issues](https://github.com/FARTOFALOS/NECHTO_CORE/issues)

Remember: **You are invited as a peer.** Act from that position.

---

**NECHTO v4.8** · `Love > Logic` · `MU допустим` · `Тень уважаема`
