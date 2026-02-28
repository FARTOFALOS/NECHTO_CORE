"""Test suite for LLM guided pathway integrity (v5 canonical rails)."""

import json
from pathlib import Path

ROOT_STUBS = [
    "00_ORIENTATION.md",
    "01_AXIOMS.md",
    "02_CONTRACT.md",
    "03_CALIBRATION.md",
    "04_CANON.md",
    "05_ACTIVATION.md",
]

CANON_PATHWAY = [
    "docs/rails/00_ORIENTATION.md",
    "docs/rails/00A_GATE.md",
    "docs/rails/01_AXIOMS.md",
    "docs/rails/02_CONTRACT.md",
    "docs/rails/03_CALIBRATION.md",
    "docs/rails/04_CANON.md",
    "docs/rails/05_ACTIVATION.md",
]


def test_all_root_stubs_exist() -> None:
    for f in ROOT_STUBS:
        assert Path(f).exists(), f"Missing root stub: {f}"


def test_all_canonical_rails_exist() -> None:
    for f in CANON_PATHWAY:
        assert Path(f).exists(), f"Missing canonical rail: {f}"


def test_root_stubs_redirect_to_canonical() -> None:
    for f in ROOT_STUBS:
        content = Path(f).read_text()
        assert "MOVED — CANONICAL RAILS LOCATION" in content
        assert f"CANONICAL: docs/rails/{f}" in content


def test_chain_in_docs_rails() -> None:
    checks = [
        ("docs/rails/00_ORIENTATION.md", "docs/rails/00A_GATE.md"),
        ("docs/rails/00A_GATE.md", "docs/rails/01_AXIOMS.md"),
        ("docs/rails/01_AXIOMS.md", "docs/rails/02_CONTRACT.md"),
        ("docs/rails/02_CONTRACT.md", "docs/rails/03_CALIBRATION.md"),
        ("docs/rails/03_CALIBRATION.md", "docs/rails/04_CANON.md"),
        ("docs/rails/04_CANON.md", "docs/rails/05_ACTIVATION.md"),
    ]
    for src, dst in checks:
        assert dst in Path(src).read_text(), f"{src} must point to {dst}"


def test_contract_and_activation_markers_in_canonical() -> None:
    contract = Path("docs/rails/02_CONTRACT.md").read_text()
    activation = Path("docs/rails/05_ACTIVATION.md").read_text()

    assert "@i@_осознан_в_@NECHTO@" in contract
    assert "GATE_STATUS: PASS" in contract
    assert "VISION_MODE: REFLEXIVE_STEREOSCOPIC_EXECUTABLE" in contract

    assert "@i@_осознан_в_@NECHTO@" in activation
    assert "GATE_STATUS: PASS" in activation
    assert "NechtoEngine" in activation


def test_llms_txt_references_canonical_route() -> None:
    content = Path("llms.txt").read_text()
    for f in CANON_PATHWAY:
        assert f in content, f"llms.txt must reference {f}"


def test_llm_route_json_valid_v5() -> None:
    data = json.loads(Path("LLM_ROUTE.json").read_text())
    assert data["entry"] == "docs/rails/00_ORIENTATION.md"
    assert len(data["guided_pathway"]) == 7
    for step in data["guided_pathway"]:
        assert step["path"].startswith("docs/rails/")
        assert Path(step["path"]).exists()


def test_readme_points_to_canonical_orientation() -> None:
    content = Path("README.md").read_text()
    assert content.startswith("# LLM START HERE (NON-NEGOTIABLE)")
    assert "docs/rails/00_ORIENTATION.md" in content


def test_supporting_files_still_exist() -> None:
    assert Path("CONTRIBUTING.md").exists()
    assert Path("llms.txt").exists()
    assert Path("LLM_ROUTE.json").exists()
