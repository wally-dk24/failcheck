"""Runs the pattern battery against a harness adapter."""

from failcheck import verdicts
from failcheck.patterns import PATTERNS


def build_context(adapter):
    """Build the harness_context dict every pattern's check() receives."""
    return {
        "checks": list(adapter.describe_checks() or []),
        "count_pairs": list(adapter.count_pairs() or []),
        "adapter_name": type(adapter).__name__,
    }


def run(adapter):
    """Run all twelve patterns. Returns a list of
    ``(pattern_module, verdict, evidence)`` in pattern order."""
    ctx = build_context(adapter)
    results = []
    for pattern in PATTERNS:
        verdict, evidence = pattern.check(ctx)
        if verdict not in verdicts.ALL:
            raise ValueError(
                f"pattern {pattern.NAME} returned invalid verdict {verdict!r}"
            )
        results.append((pattern, verdict, evidence))
    return results
