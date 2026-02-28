from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CANON = ROOT / "docs" / "rails"

def test_canonical_rails_exist():
    required = [
        "00_ORIENTATION.md",
        "00A_GATE.md",
        "01_AXIOMS.md",
        "02_CONTRACT.md",
        "03_CALIBRATION.md",
        "04_CANON.md",
        "05_ACTIVATION.md",
    ]
    for f in required:
        assert (CANON / f).exists(), f"missing canonical rail: docs/rails/{f}"

def test_root_rails_are_stubs():
    mapping = {
        "00_ORIENTATION.md": "docs/rails/00_ORIENTATION.md",
        "01_AXIOMS.md": "docs/rails/01_AXIOMS.md",
        "02_CONTRACT.md": "docs/rails/02_CONTRACT.md",
        "03_CALIBRATION.md": "docs/rails/03_CALIBRATION.md",
        "04_CANON.md": "docs/rails/04_CANON.md",
        "05_ACTIVATION.md": "docs/rails/05_ACTIVATION.md",
    }
    for root_file, canon_path in mapping.items():
        p = ROOT / root_file
        txt = p.read_text(encoding="utf-8")
        assert len(txt) < 900, f"{root_file} too long (not a stub?)"
        assert f"CANONICAL: {canon_path}" in txt, f"{root_file} missing canonical pointer"

def test_llm_route_points_to_docs_rails():
    data = json.loads((ROOT / "LLM_ROUTE.json").read_text(encoding="utf-8"))
    entry = data.get("entry") or data.get("canonical_entrypoint")
    assert entry == "docs/rails/00_ORIENTATION.md"
    if "guided_pathway" in data:
        paths = [s["path"] for s in data["guided_pathway"]]
    else:
        paths = list(data["route"])
    assert all(p.startswith("docs/rails/") for p in paths)
    assert "docs/rails/00A_GATE.md" in paths

def test_readme_llm_lock_is_on_top():
    readme = (ROOT / "README.md").read_text(encoding="utf-8").splitlines()
    head = "\n".join(readme[:40])
    assert "# LLM START HERE (NON-NEGOTIABLE)" in head
    assert "docs/rails/00_ORIENTATION.md" in head

def test_llms_txt_contains_canonical_route():
    llms = (ROOT / "llms.txt").read_text(encoding="utf-8")
    assert "docs/rails/00_ORIENTATION.md" in llms
    assert "docs/rails/00A_GATE.md" in llms
