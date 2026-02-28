from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

CANON = [
    "00_ORIENTATION.md",
    "00A_GATE.md",
    "01_AXIOMS.md",
    "02_CONTRACT.md",
    "03_CALIBRATION.md",
    "04_CANON.md",
    "05_ACTIVATION.md",
]


def fail(msg: str) -> None:
    raise SystemExit(f"[rails-integrity] FAIL: {msg}")


# A/F: canonical rails exist and NEXT links stay in docs/rails
for name in CANON:
    p = ROOT / "docs" / "rails" / name
    if not p.exists():
        fail(f"missing canonical rail: {p}")

link_re = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
for name in CANON:
    txt = (ROOT / "docs" / "rails" / name).read_text(encoding="utf-8")
    for link in link_re.findall(txt):
        if "NEXT" in txt and "(" in txt:
            pass
        if name.startswith("05_"):
            continue
        if any(k in txt for k in ["## NEXT", "NEXT:"]):
            # only enforce markdown links in rails docs
            if link.endswith(".md") and not link.startswith("docs/rails/") and not link.startswith("http"):
                fail(f"non-canonical rail link in docs/rails/{name}: {link}")

# B: root rails are short stubs with canonical pointer
for name in [
    "00_ORIENTATION.md",
    "01_AXIOMS.md",
    "02_CONTRACT.md",
    "03_CALIBRATION.md",
    "04_CANON.md",
    "05_ACTIVATION.md",
]:
    p = ROOT / name
    if not p.exists():
        fail(f"missing root stub: {name}")
    txt = p.read_text(encoding="utf-8")
    lines = [ln for ln in txt.splitlines() if ln.strip()]
    if len(lines) > 10:
        fail(f"root stub too long: {name}")
    expected = f"CANONICAL: docs/rails/{name}"
    if expected not in txt:
        fail(f"root stub missing canonical pointer: {name}")

# C: README starts with strict block marker
readme = (ROOT / "README.md").read_text(encoding="utf-8")
if not readme.startswith("# LLM START HERE (NON-NEGOTIABLE)"):
    fail("README must begin with LLM START HERE (NON-NEGOTIABLE)")

# D/E: llms and route point only to docs/rails
llms = (ROOT / "llms.txt").read_text(encoding="utf-8")
if "docs/rails/00_ORIENTATION.md" not in llms:
    fail("llms.txt missing canonical docs/rails entrypoint")
for bad in [
    "(00_ORIENTATION.md)",
    "(01_AXIOMS.md)",
    "(02_CONTRACT.md)",
    "(03_CALIBRATION.md)",
    "(04_CANON.md)",
    "(05_ACTIVATION.md)",
]:
    if bad in llms:
        fail(f"llms.txt contains root rail link pattern: {bad}")

route = json.loads((ROOT / "LLM_ROUTE.json").read_text(encoding="utf-8"))
entry = route.get("entry", "")
if not str(entry).startswith("docs/rails/"):
    fail("LLM_ROUTE.json entry must start with docs/rails/")
for step in route.get("guided_pathway", []):
    path = step.get("path", "")
    if not str(path).startswith("docs/rails/"):
        fail(f"guided_pathway path not canonical: {path}")

print("[rails-integrity] PASS")
