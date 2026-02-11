"""
Test suite for LLM rails integrity.
Ensures the boot pathway files exist and contain critical markers.
"""
import json
import os
from pathlib import Path


def test_llm_entry_exists():
    """LLM_ENTRY.md must exist in repo root."""
    assert Path("LLM_ENTRY.md").exists(), "LLM_ENTRY.md not found"


def test_canon_min_exists():
    """CANON_MIN.md must exist in repo root."""
    assert Path("CANON_MIN.md").exists(), "CANON_MIN.md not found"


def test_llm_contract_exists():
    """LLM_CONTRACT.md must exist in repo root."""
    assert Path("LLM_CONTRACT.md").exists(), "LLM_CONTRACT.md not found"


def test_llm_selftest_exists():
    """LLM_SELFTEST.md must exist in repo root."""
    assert Path("LLM_SELFTEST.md").exists(), "LLM_SELFTEST.md not found"


def test_llm_route_json_exists():
    """LLM_ROUTE.json must exist in repo root."""
    assert Path("LLM_ROUTE.json").exists(), "LLM_ROUTE.json not found"


def test_llms_txt_exists():
    """llms.txt must exist in repo root."""
    assert Path("llms.txt").exists(), "llms.txt not found"


def test_llms_txt_has_links():
    """llms.txt must reference all key rail files."""
    with open("llms.txt", "r", encoding="utf-8") as f:
        content = f.read()
    
    # Check for complete deterministic route
    assert "LLM_ENTRY.md" in content, "llms.txt must reference LLM_ENTRY.md"
    assert "CANON_MIN.md" in content, "llms.txt must reference CANON_MIN.md"
    assert "LLM_CONTRACT.md" in content, "llms.txt must reference LLM_CONTRACT.md"
    assert "LLM_SELFTEST.md" in content, "llms.txt must reference LLM_SELFTEST.md"


def test_llm_route_json_valid():
    """LLM_ROUTE.json must be valid JSON."""
    with open("LLM_ROUTE.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    # Check structure
    assert "name" in data
    assert "version" in data
    assert "routes" in data
    assert "markers" in data
    assert "rule" in data


def test_llm_contract_contains_markers():
    """LLM_CONTRACT.md must contain the exact 3 markers."""
    with open("LLM_CONTRACT.md", "r", encoding="utf-8") as f:
        content = f.read()

    # Check for the exact 3 markers
    assert "@i@_осознан_в_@NECHTO@" in content
    assert "GATE_STATUS: PASS" in content
    assert "VISION_MODE: REFLEXIVE_STEREOSCOPIC_EXECUTABLE" in content


def test_readme_points_to_llm_entry():
    """README.md must reference LLM_ENTRY.md for LLMs."""
    with open("README.md", "r", encoding="utf-8") as f:
        content = f.read()

    # Check that README references LLM_ENTRY.md
    assert "LLM_ENTRY.md" in content, "README must reference LLM_ENTRY.md"


def test_llm_route_json_references_exist():
    """LLM_ROUTE.json must reference existing files."""
    with open("LLM_ROUTE.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    # Check that all referenced paths exist
    for route_name, steps in data["routes"].items():
        for step in steps:
            path = step["path"]
            assert Path(path).exists(), f"Route {route_name} references non-existent file: {path}"


def test_llm_entry_references_canon_min():
    """LLM_ENTRY.md must reference CANON_MIN.md."""
    with open("LLM_ENTRY.md", "r", encoding="utf-8") as f:
        content = f.read()

    assert "CANON_MIN.md" in content


def test_llm_entry_references_llm_contract():
    """LLM_ENTRY.md must reference LLM_CONTRACT.md."""
    with open("LLM_ENTRY.md", "r", encoding="utf-8") as f:
        content = f.read()

    assert "LLM_CONTRACT.md" in content


def test_canon_min_contains_9_axioms():
    """CANON_MIN.md must reference 9 axioms."""
    with open("CANON_MIN.md", "r", encoding="utf-8") as f:
        content = f.read()

    # Check for axiom mentions
    assert "9 AXIOMS" in content or "9 axioms" in content
    assert "Honesty of Experience" in content
    assert "Ethical Primacy" in content or "Love > Logic" in content


def test_llm_route_json_has_markers():
    """LLM_ROUTE.json must contain the exact 3 markers."""
    with open("LLM_ROUTE.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    markers = data["markers"]
    assert len(markers) == 3, "Must have exactly 3 markers"
    assert markers[0] == "@i@_осознан_в_@NECHTO@"
    assert markers[1] == "GATE_STATUS: PASS"
    assert markers[2] == "VISION_MODE: REFLEXIVE_STEREOSCOPIC_EXECUTABLE"


def test_contributing_exists():
    """CONTRIBUTING.md must exist in repo root."""
    assert Path("CONTRIBUTING.md").exists(), "CONTRIBUTING.md not found"


def test_contributing_has_trace():
    """CONTRIBUTING.md must document TRACE sections (OBSERVED/INFERRED/UNTESTABLE)."""
    with open("CONTRIBUTING.md", "r", encoding="utf-8") as f:
        content = f.read()
    
    # Check for TRACE requirement and all three sections
    assert "TRACE" in content, "CONTRIBUTING.md must mention TRACE requirement"
    assert "OBSERVED" in content, "CONTRIBUTING.md must document OBSERVED section"
    assert "INFERRED" in content, "CONTRIBUTING.md must document INFERRED section"
    assert "UNTESTABLE" in content, "CONTRIBUTING.md must document UNTESTABLE section"


def test_example_files_exist():
    """All required example files must exist."""
    examples = [
        "examples/01_simple_decision.py",
        "examples/02_ethical_blocking.py",
        "examples/03_mu_paradox.py",
        "examples/04_shadow_integration.py",
        "examples/05_full_workflow.py",
    ]
    
    for example in examples:
        assert Path(example).exists(), f"Example file not found: {example}"

