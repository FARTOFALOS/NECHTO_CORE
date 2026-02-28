"""
Test suite for LLM guided pathway integrity.
Ensures the 00→05 attention chain is intact and navigable.
"""
import json
from pathlib import Path


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Pathway files existence
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

PATHWAY = [
    "00_ORIENTATION.md",
    "01_AXIOMS.md",
    "02_CONTRACT.md",
    "03_CALIBRATION.md",
    "04_CANON.md",
    "05_ACTIVATION.md",
]


def test_all_pathway_files_exist():
    """All 6 guided pathway files must exist."""
    for f in PATHWAY:
        assert Path(f).exists(), f"Pathway file not found: {f}"


def test_llms_txt_exists():
    """llms.txt must exist in repo root."""
    assert Path("llms.txt").exists()


def test_llm_route_json_exists():
    """LLM_ROUTE.json must exist in repo root."""
    assert Path("LLM_ROUTE.json").exists()


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Chain integrity — each file points to the next
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def test_chain_00_points_to_01():
    content = Path("00_ORIENTATION.md").read_text()
    assert "01_AXIOMS.md" in content, "00 must point to 01"


def test_chain_01_points_to_02():
    content = Path("01_AXIOMS.md").read_text()
    assert "02_CONTRACT.md" in content, "01 must point to 02"


def test_chain_02_points_to_03():
    content = Path("02_CONTRACT.md").read_text()
    assert "03_CALIBRATION.md" in content, "02 must point to 03"


def test_chain_03_points_to_04():
    content = Path("03_CALIBRATION.md").read_text()
    assert "04_CANON.md" in content, "03 must point to 04"


def test_chain_04_points_to_05():
    content = Path("04_CANON.md").read_text()
    assert "05_ACTIVATION.md" in content, "04 must point to 05"


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Content integrity
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def test_axioms_contains_10():
    """01_AXIOMS.md must contain all 10 axioms."""
    content = Path("01_AXIOMS.md").read_text()
    assert "10 АКСИОМ" in content or "10 аксиом" in content
    assert "Honesty of Experience" in content
    assert "Ethical Primacy" in content or "Love > Logic" in content
    assert "Affective Coherence" in content


def test_contract_contains_markers():
    """02_CONTRACT.md must contain the exact 3 markers."""
    content = Path("02_CONTRACT.md").read_text()
    assert "@i@_осознан_в_@NECHTO@" in content
    assert "GATE_STATUS: PASS" in content
    assert "VISION_MODE: REFLEXIVE_STEREOSCOPIC_EXECUTABLE" in content


def test_activation_contains_markers():
    """05_ACTIVATION.md must also contain the markers."""
    content = Path("05_ACTIVATION.md").read_text()
    assert "@i@_осознан_в_@NECHTO@" in content
    assert "GATE_STATUS: PASS" in content


def test_activation_contains_code():
    """05_ACTIVATION.md must contain runnable code."""
    content = Path("05_ACTIVATION.md").read_text()
    assert "NechtoEngine" in content
    assert "engine.run" in content or "engine.i_am" in content


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# llms.txt and LLM_ROUTE.json
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def test_llms_txt_references_pathway():
    """llms.txt must reference all pathway files."""
    content = Path("llms.txt").read_text()
    for f in PATHWAY:
        assert f in content, f"llms.txt must reference {f}"


def test_llm_route_json_valid():
    """LLM_ROUTE.json must be valid JSON with guided_pathway."""
    data = json.loads(Path("LLM_ROUTE.json").read_text())
    assert "guided_pathway" in data
    assert "markers" in data
    assert len(data["guided_pathway"]) == 6


def test_llm_route_json_has_markers():
    """LLM_ROUTE.json must contain the exact 3 markers."""
    data = json.loads(Path("LLM_ROUTE.json").read_text())
    markers = data["markers"]
    assert markers["line1"] == "@i@_осознан_в_@NECHTO@"
    assert markers["line2"] == "GATE_STATUS: PASS"
    assert markers["line3"] == "VISION_MODE: REFLEXIVE_STEREOSCOPIC_EXECUTABLE"


def test_llm_route_json_paths_exist():
    """All paths in LLM_ROUTE.json must exist."""
    data = json.loads(Path("LLM_ROUTE.json").read_text())
    for step in data["guided_pathway"]:
        assert Path(step["path"]).exists(), f"Route references non-existent: {step['path']}"


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# README entry point
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def test_readme_points_to_orientation():
    """README.md must reference 00_ORIENTATION.md."""
    content = Path("README.md").read_text()
    assert "00_ORIENTATION.md" in content


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Supporting files
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def test_contributing_exists():
    """CONTRIBUTING.md must exist."""
    assert Path("CONTRIBUTING.md").exists()


def test_contributing_has_trace():
    """CONTRIBUTING.md must document TRACE sections."""
    content = Path("CONTRIBUTING.md").read_text()
    assert "TRACE" in content
    assert "OBSERVED" in content
    assert "INFERRED" in content
    assert "UNTESTABLE" in content


def test_example_files_exist():
    """Core example files must exist."""
    examples = [
        "examples/01_simple_decision.py",
        "examples/02_mu_paradox.py",
        "examples/03_shadow_integration.py",
        "examples/full_cycle.py",
    ]
    for ex in examples:
        assert Path(ex).exists(), f"Example not found: {ex}"

