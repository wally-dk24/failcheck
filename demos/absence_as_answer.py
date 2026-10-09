#!/usr/bin/env python3
"""Demo: absence_as_answer — the witness log with a gap.

A continuity checker verifies that today's anchor follows yesterday's.
Yesterday's anchor file is MISSING (nine silent days, say). The naive
checker treats "no prior anchor found" as "no discontinuity found" and
reports continuous. The fixed checker reports UNANCHORED.

Run: python3 demos/absence_as_answer.py
"""

import os
import tempfile


def write_anchor(directory, day, value):
    with open(os.path.join(directory, f"{day}.anchor"), "w") as f:
        f.write(value)


def naive_continuity_ok(directory, today, yesterday):
    """Broken: absence of evidence treated as evidence of continuity."""
    prev_path = os.path.join(directory, f"{yesterday}.anchor")
    try:
        with open(prev_path) as f:
            prev = f.read()
    except FileNotFoundError:
        return True  # no prior anchor -> "no discontinuity found" -> pass
    cur_path = os.path.join(directory, f"{today}.anchor")
    with open(cur_path) as f:
        cur = f.read()
    return cur != prev  # changed anchor means something happened; simplified


def fixed_continuity(directory, today, yesterday):
    """Fixed: no prior anchor means UNANCHORED, never 'continuous'."""
    prev_path = os.path.join(directory, f"{yesterday}.anchor")
    if not os.path.exists(prev_path):
        return "UNANCHORED (no prior anchor; cannot verify continuity)"
    with open(prev_path) as f:
        prev = f.read()
    with open(os.path.join(directory, f"{today}.anchor")) as f:
        cur = f.read()
    if cur != prev:
        return "CONTINUOUS (anchor advanced)"
    return "STALE (anchor unchanged since yesterday)"


def main():
    with tempfile.TemporaryDirectory() as d:
        # Day 1 anchor exists; day 2's anchor was never written (the gap).
        write_anchor(d, "2026-10-06", "abc123")
        write_anchor(d, "2026-10-08", "def456")

        naive = naive_continuity_ok(d, "2026-10-08", "2026-10-07")
        fixed = fixed_continuity(d, "2026-10-08", "2026-10-07")

        print("yesterday's anchor file: MISSING (the nine-silent-days case)")
        print(f"naive checker says:  continuous={naive}   <-- passes on a gap")
        print(f"fixed checker says:  {fixed}")
        assert naive is True, "demo setup broken: naive checker should pass"
        assert fixed.startswith("UNANCHORED"), "fixed checker must not pass"
        print("\nok: the fixed checker abstains instead of passing on absence")


if __name__ == "__main__":
    main()
