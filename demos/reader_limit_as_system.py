#!/usr/bin/env python3
"""Demo: reader_limit_as_system — the last 1000 lines.

The checker reads the last 1000 lines of a 5000-line log and reports
"no errors in the system". The error is on line 5000... of the part it
never read (line 4200 of the file, beyond the window). The fixed
checker scopes its claim to the window.

Run: python3 demos/reader_limit_as_system.py
"""

WINDOW = 1000


def read_last_n(lines, n):
    return lines[-n:]


def naive_no_errors_system(all_lines):
    """Broken: bounded read, unbounded claim."""
    return not any("ERROR" in l for l in read_last_n(all_lines, WINDOW))


def fixed_no_errors_in_window(all_lines):
    """Fixed: the claim names the window."""
    return not any("ERROR" in l for l in read_last_n(all_lines, WINDOW))


def main():
    all_lines = [f"INFO line {i}\n" for i in range(5000)]
    all_lines[500] = "ERROR disk full\n"  # outside the last-1000 window

    print(f"naive checker says 'no errors in the system': "
          f"{naive_no_errors_system(all_lines)}   <-- line 500 unread")
    print(f"fixed checker says 'no errors in last {WINDOW} lines': "
          f"{fixed_no_errors_in_window(all_lines)} (lines 0-3999: UNEXAMINED)")
    assert naive_no_errors_system(all_lines) is True
    assert fixed_no_errors_in_window(all_lines) is True
    print("\nok: the window is named; what wasn't read isn't evidence")


if __name__ == "__main__":
    main()
