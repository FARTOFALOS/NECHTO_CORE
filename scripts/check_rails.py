from __future__ import annotations

import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

CANON_DIR = ROOT / "docs" / "rails"
ROOT_RAILS = [
    "00_ORIENTATION.md",
    "01_AXIOMS.md",
    "02_CONTRACT.md",
    "03_CALIBRATION.md",
    "04_CANON.md",
    "05_ACTIVATION.md",
]
CANON_RAILS = [
    "00_ORIENTATION.md",
    "00A_GATE.md",
    "01_AXIOMS.md",
    "02_CONTRACT.md",
    "03_CALIBRATION.md",
    "04_CANON.md",
    "05_ACTIVATION.md",
]

NEXT_EXPECTED = {
    "00_ORIENTATION.md": "NEXT: docs/rails/00A_GATE.md",
    "00A_GATE.md": "NEXT: docs/rails/01_AXIOMS.md",
    "01_AXIOMS.md": "NEXT: docs/rails/02_CONTRACT.md",
    "02_CONTRACT.md": "NEXT: docs/rails/03_CALIBRATION.md",
    "03_CALIBRATION.md": "NEXT: docs/rails/04_CANON.md",
    "04_CANON.md": "NEXT: docs/rails/05_ACTIVATION.md",
}

BIDI_CHARS = [
    "\u202A", "\u202B", "\u202C", "\u202D", "\u202E",
    "\u2066", "\u2067", "\u2068", "\u2069",
]

def fail(msg: str) -> None:
    print(f"[rails-integrity] FAIL: {msg}", file=sys.stderr)
    sys.exit(1)

def read_text(p: Path) -> str:
    try:
        return p.read_text(encoding="utf-8")
    except Exception as e:
        fail(f"cannot read {p}: {e}")

def contains_bidi(text: str) -> bool:
    return any(ch in text for ch in BIDI_CHARS)

def main() -> None:
    # 1) Canonical rails exist
    if not CANON_DIR.exists():
        fail("docs/rails directory missing")
    for f in CANON_RAILS:
        p = CANON_DIR / f
        if not p.exists():
            fail(f"missing canonical rail: {p}")

    # 2) Root rails exist and are stubs
    for f in ROOT_RAILS:
        p = ROOT / f
        if not p.exists():
            fail(f"missing root rail stub: {p}")
        text = read_text(p)
        if len(text) > 900:
            fail(f"root rail is too long (not a stub?): {f} (len={len(text)})")
        if "CANONICAL: docs/rails/" not in text:
            fail(f"root rail stub missing CANONICAL pointer: {f}")
        if contains_bidi(text):
            fail(f"bidi control chars found in root rail stub: {f}")

    # 3) Canon rails NEXT links point to docs/rails
    for fname, expected in NEXT_EXPECTED.items():
        p = CANON_DIR / fname
        text = read_text(p)
        if expected not in text:
            fail(f"{p} missing expected NEXT link: '{expected}'")
        # forbid root NEXT references
        if "NEXT: 0" in text or "NEXT: 1" in text or "NEXT: 2" in text:
            fail(f"{p} appears to reference root rails in NEXT link")
        if "NEXT: 00_" in text or "NEXT: 01_" in text:
            fail(f"{p} appears to reference root rails in NEXT link")
        if contains_bidi(text):
            fail(f"bidi control chars found in canonical rail: {p.name}")

    # 4) README LLM lock at top
    readme = read_text(ROOT / "README.md")
    first_40 = "\n".join(readme.splitlines()[:40])
    if "# LLM START HERE (NON-NEGOTIABLE)" not in first_40:
        fail("README must begin with LLM START HERE block (first ~40 lines)")
    if "docs/rails/00_ORIENTATION.md" not in first_40:
        fail("README LLM block must reference docs/rails/00_ORIENTATION.md")
    if contains_bidi(readme):
        fail("bidi control chars found in README.md")

    # 5) llms.txt references canonical route
    llms = read_text(ROOT / "llms.txt")
    if "docs/rails/00_ORIENTATION.md" not in llms or "docs/rails/00A_GATE.md" not in llms:
        fail("llms.txt must contain docs/rails entry + 00A_GATE")
    if contains_bidi(llms):
        fail("bidi control chars found in llms.txt")

    # 6) LLM_ROUTE.json points only to docs/rails
    route_path = ROOT / "LLM_ROUTE.json"
    data = json.loads(read_text(route_path))
    entry = data.get("entry") or data.get("canonical_entrypoint")
    if entry != "docs/rails/00_ORIENTATION.md":
        fail(f"LLM_ROUTE.json entry must be docs/rails/00_ORIENTATION.md (got {entry!r})")

    paths = []
    if "guided_pathway" in data:
        paths = [s["path"] for s in data["guided_pathway"]]
    elif "route" in data:
        paths = list(data["route"])
    else:
        fail("LLM_ROUTE.json must contain 'guided_pathway' or 'route'")

    if any(not str(p).startswith("docs/rails/") for p in paths):
        fail("LLM_ROUTE.json contains non docs/rails path(s)")
    if "docs/rails/00A_GATE.md" not in paths:
        fail("LLM_ROUTE.json must include docs/rails/00A_GATE.md in the pathway")

    if contains_bidi(read_text(route_path)):
        fail("bidi control chars found in LLM_ROUTE.json")

    print("[rails-integrity] PASS")

if __name__ == "__main__":
    main()
