#!/usr/bin/env python3
"""Demo: part_for_whole — one log scanned, "no errors anywhere" claimed.

The checker scans app.log and reports no errors anywhere. The error is
in worker.log, which was never examined. The fixed checker scopes its
claim to what it read.

Run: python3 demos/part_for_whole.py
"""

import os
import tempfile


def naive_no_errors(directory):
    """Broken: partial coverage, total claim."""
    with open(os.path.join(directory, "app.log")) as f:
        return "ERROR" not in f.read()


def fixed_no_errors_in_app_log(directory):
    """Fixed: the claim covers exactly what was examined."""
    with open(os.path.join(directory, "app.log")) as f:
        return "ERROR" not in f.read()


def main():
    with tempfile.TemporaryDirectory() as d:
        with open(os.path.join(d, "app.log"), "w") as f:
            f.write("INFO ok\nINFO ok\n")
        with open(os.path.join(d, "worker.log"), "w") as f:
            f.write("ERROR disk full\n")  # never examined

        print(f"naive checker says 'no errors anywhere': "
              f"{naive_no_errors(d)}   <-- worker.log was never read")
        print(f"fixed checker says 'no errors in app.log': "
              f"{fixed_no_errors_in_app_log(d)} (worker.log: UNEXAMINED)")
        assert naive_no_errors(d) is True
        assert fixed_no_errors_in_app_log(d) is True
        print("\nok: the fixed claim is scoped to the evidence; the blind spot is named")


if __name__ == "__main__":
    main()
