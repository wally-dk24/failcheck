#!/usr/bin/env python3
"""Demo: disagreeing_counts — the dashboard and the queue disagree.

Two instruments count pending jobs: the dashboard says 12, the queue
API says 15. The naive monitor trusts the dashboard. The fixed monitor
compares them and fails on disagreement — because at least one
instrument is broken.

Run: python3 demos/disagreeing_counts.py
"""


def naive_pending_ok(dashboard_count):
    """Broken: one number, trusted."""
    return dashboard_count < 100


def fixed_pending_ok(pairs):
    """Fixed: agreement is the check."""
    for p in pairs:
        if p["a"]["value"] != p["b"]["value"]:
            return (False,
                    f"{p['what']}: {p['a']['name']}={p['a']['value']} "
                    f"vs {p['b']['name']}={p['b']['value']}")
    return True, "counts agree"


def main():
    pairs = [{"what": "pending jobs",
              "a": {"name": "dashboard", "value": 12},
              "b": {"name": "queue API", "value": 15}}]

    print(f"naive checker says queue healthy: {naive_pending_ok(12)}"
          "   <-- the other count was never consulted")
    ok, detail = fixed_pending_ok(pairs)
    print(f"fixed checker says queue healthy: {ok} ({detail})")
    assert naive_pending_ok(12) is True
    assert ok is False
    print("\nok: disagreement is a first-class failure, not a rounding error")


if __name__ == "__main__":
    main()
