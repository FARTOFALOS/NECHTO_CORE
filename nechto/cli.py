from __future__ import annotations

import argparse
import json
import sys
from typing import Any

from nechto import (
    __version__,
    Edge,
    EdgeType,
    NechtoEngine,
    NodeStatus,
    SemanticAtom,
    Tag,
)


def _safe_get(obj: Any, name: str, default: Any = None) -> Any:
    try:
        return getattr(obj, name)
    except Exception:
        return default


def cmd_selftest(_: argparse.Namespace) -> int:
    """
    Minimal smoke test:
      - import works
      - engine can add nodes/edges
      - workflow can execute at least once

    Returns:
      0 on success, 1 on error/exception
    """
    try:
        engine = NechtoEngine()

        # Minimal anchored graph (IDs are explicit for stable edge wiring)
        engine.add_atom(
            SemanticAtom(
                id="c1",
                label="clarity-of-intent",
                status=NodeStatus.ANCHORED,
                clarity=0.9,
                empathy=0.6,
                coherence=0.8,
                tags=[Tag.WITNESS, Tag.INTENT],
            )
        )
        engine.add_atom(
            SemanticAtom(
                id="c2",
                label="actionable-step",
                status=NodeStatus.ANCHORED,
                clarity=0.7,
                practicality=0.9,
                agency=0.5,
                tags=[Tag.INTENT],
            )
        )
        engine.add_edge(Edge(from_id="c1", to_id="c2", type=EdgeType.SUPPORTS))

        result = engine.run("implement", context={"intent": "implement"})

        payload = {
            "nechto_version": __version__,
            "gate_status": _safe_get(result, "gate_status", "UNKNOWN"),
            "fail_code": _safe_get(result, "fail_code", None),
            "candidate_set_size": _safe_get(result, "candidate_set_size", None),
            "active_set_size": _safe_get(result, "active_set_size", None),
            "blocked_fraction": _safe_get(result, "blocked_fraction", None),
            "cycle": _safe_get(result, "cycle", None),
        }

        # Metrics can be large; keep it small but useful
        metrics = _safe_get(result, "metrics", None)
        if isinstance(metrics, dict):
            payload["metrics_preview"] = {
                k: metrics.get(k)
                for k in (
                    "TSC_extended",
                    "SCAV_health",
                    "FLOW",
                    "ethical_coefficient",
                    "harm_probability",
                    "identity_alignment",
                )
                if k in metrics
            }

        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return 0

    except Exception as e:
        print(f"[nechto selftest] FAIL: {e!r}", file=sys.stderr)
        return 1


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="nechto", description="NECHTO CORE CLI")
    p.add_argument("--version", action="store_true", help="Print version and exit")

    sub = p.add_subparsers(dest="cmd", required=False)

    p_selftest = sub.add_parser("selftest", help="Run a minimal smoke test")
    p_selftest.set_defaults(func=cmd_selftest)

    return p


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.version:
        print(__version__)
        return 0

    func = getattr(args, "func", None)
    if func is None:
        parser.print_help()
        return 0

    return int(func(args))


if __name__ == "__main__":
    raise SystemExit(main())
