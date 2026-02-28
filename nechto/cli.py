"""Command-line interface for NECHTO."""

from __future__ import annotations

import argparse

from nechto import NechtoEngine, NodeStatus, SemanticAtom, __version__


def run_selftest() -> int:
    """Run a minimal runtime smoke check and return process status code."""
    try:
        engine = NechtoEngine()
        engine.add_atom(
            SemanticAtom(
                id="selftest-node",
                label="selftest",
                status=NodeStatus.ANCHORED,
                clarity=0.9,
                coherence=0.9,
            )
        )
        result = engine.run("selftest", context={"intent": "implement"})
        ok = result.gate_status in {"PASS", "FAIL"}
    except Exception as exc:  # pragma: no cover
        print(f"NECHTO selftest FAIL: {exc}")
        return 1

    print(f"NECHTO {__version__}")
    print(f"gate_status={result.gate_status}")
    print(f"engine_smoke={'PASS' if ok else 'FAIL'}")
    return 0 if ok else 1


def main() -> int:
    parser = argparse.ArgumentParser(prog="nechto", description="NECHTO command-line utilities")
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    subparsers = parser.add_subparsers(dest="command")
    subparsers.add_parser("selftest", help="Run a lightweight runtime self-check")

    args = parser.parse_args()
    if args.command == "selftest":
        return run_selftest()

    parser.print_help()
    return 0
