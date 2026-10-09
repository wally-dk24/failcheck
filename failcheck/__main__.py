"""Command-line interface: ``python -m failcheck list`` and ``run``."""

import argparse
import importlib
import sys

from failcheck import __version__, verdicts
from failcheck.adapter import HarnessAdapter
from failcheck.patterns import PATTERNS
from failcheck.runner import run


def load_adapter(dotted_path):
    """Import ``dotted.path`` and return its ``ADAPTER`` (instance) or
    ``Adapter`` (class, instantiated with no args)."""
    module = importlib.import_module(dotted_path)
    for attr in ("ADAPTER", "adapter", "Adapter"):
        candidate = getattr(module, attr, None)
        if candidate is None:
            continue
        if isinstance(candidate, HarnessAdapter):
            return candidate
        if isinstance(candidate, type) and issubclass(candidate, HarnessAdapter):
            return candidate()
    raise SystemExit(
        f"error: module {dotted_path!r} defines no ADAPTER/adapter/Adapter "
        "implementing failcheck.adapter.HarnessAdapter"
    )


def cmd_list(_args):
    for pattern in PATTERNS:
        print(f"{pattern.NAME:22} {pattern.DESCRIPTION}")
    return 0


def cmd_run(args):
    adapter = load_adapter(args.harness)
    results = run(adapter)
    fails = sum(1 for _, v, _ in results if v == verdicts.FAIL)
    for pattern, verdict, evidence in results:
        mark = {"PASS": "ok  ", "FAIL": "FAIL", "NOT_APPLICABLE": "n/a "}[verdict]
        print(f"[{mark}] {pattern.NAME}")
        print(f"       {pattern.TITLE}")
        if verdict == verdicts.FAIL:
            print(f"       evidence: {evidence}")
            print(f"       remedy: {pattern.REMEDY}")
            print(f"       repro:  python3 demos/{pattern.NAME}.py")
    print()
    print(f"{len(results)} patterns, {fails} FAIL")
    return 1 if fails else 0


def main(argv=None):
    parser = argparse.ArgumentParser(
        prog="failcheck",
        description="Self-test suite for agent systems: find the checks "
        "that would pass on a broken system.",
    )
    parser.add_argument("--version", action="version", version=__version__)
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("list", help="list the twelve failure patterns")

    run_p = sub.add_parser("run", help="run the battery against a harness")
    run_p.add_argument(
        "--harness",
        required=True,
        help="dotted path to the module defining ADAPTER, "
        "e.g. my_harness (then: python -m failcheck run --harness my_harness)",
    )

    args = parser.parse_args(argv)
    if args.command == "list":
        return cmd_list(args)
    return cmd_run(args)


if __name__ == "__main__":
    sys.exit(main())
