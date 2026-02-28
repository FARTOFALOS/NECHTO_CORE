"""Command-line interface for NECHTO."""

from __future__ import annotations

import argparse
from typing import Sequence

from nechto import Edge, EdgeType, NechtoEngine, NodeStatus, SemanticAtom, Tag, __version__


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="nechto", description="NECHTO command-line utilities")
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")

    subparsers = parser.add_subparsers(dest="command")
    subparsers.add_parser("selftest", help="Run a lightweight runtime self-check")
    return parser


def run_selftest() -> int:
    engine = NechtoEngine()
    engine.add_atom(
        SemanticAtom(
            label="presence",
            id="selftest-presence",
            status=NodeStatus.ANCHORED,
            clarity=0.9,
            coherence=0.8,
            empathy=0.6,
            boundary=0.9,
            tags=[Tag.WITNESS],
        )
    )
    engine.add_atom(
        SemanticAtom(
            label="intent",
            id="selftest-intent",
            status=NodeStatus.ANCHORED,
            clarity=0.85,
            practicality=0.8,
            agency=0.5,
            tags=[Tag.INTENT],
        )
    )
    engine.add_edge(Edge(from_id="selftest-presence", to_id="selftest-intent", type=EdgeType.SUPPORTS))

    result = engine.run("selftest", context={"intent": "implement"})

    print("NECHTO selftest OK")
    print(f"version={__version__}")
    print(f"gate_status={result.gate_status}")
    print(f"cycles={engine.state.current_cycle}")
    return 0


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command == "selftest":
        return run_selftest()

    parser.print_help()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
