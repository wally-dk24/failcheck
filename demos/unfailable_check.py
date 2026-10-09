#!/usr/bin/env python3
"""Demo: unfailable_check — the stale read transaction.

A writer commits rows at t=10. A reader opened its read transaction at
t=5, so it sees the snapshot as of t=5: zero rows. The naive checker
reports write_missing=True — a confident answer from a broken premise.
The fixed checker notices its read predates the last commit and reports
UNKNOWN instead of an answer.

Run: python3 demos/unfailable_check.py
"""


class TinyDB:
    """A toy database with timestamped commits and snapshot reads."""

    def __init__(self):
        self.rows = []  # (committed_at, value)

    def write(self, value, at):
        self.rows.append((at, value))

    def last_commit_at(self):
        return max((t for t, _ in self.rows), default=0)

    def read_as_of(self, snapshot_at):
        return [v for t, v in self.rows if t <= snapshot_at]


def naive_check_write_landed(db, snapshot_at):
    """Broken: always answers; cannot say 'I don't know'."""
    rows = db.read_as_of(snapshot_at)
    return {"write_missing": len(rows) == 0}  # confident, and wrong


def fixed_check_write_landed(db, snapshot_at):
    """Fixed: abstains when the read predates the last commit."""
    if snapshot_at < db.last_commit_at():
        return {"verdict": "UNKNOWN",
                "reason": "read snapshot predates last commit"}
    rows = db.read_as_of(snapshot_at)
    return {"verdict": "OK" if rows else "WRITE_MISSING"}


def main():
    db = TinyDB()
    db.write("hello", at=10)          # the write happened at t=10
    snapshot_at = 5                    # ...but we read as of t=5

    naive = naive_check_write_landed(db, snapshot_at)
    fixed = fixed_check_write_landed(db, snapshot_at)

    print(f"write committed at t=10; reader snapshot at t=5 "
          f"(rows visible: {db.read_as_of(snapshot_at)})")
    print(f"naive checker says: {naive}   <-- confident and wrong")
    print(f"fixed checker says: {fixed}")
    assert naive == {"write_missing": True}
    assert fixed["verdict"] == "UNKNOWN"
    print("\nok: the fixed checker abstains instead of answering from a stale read")


if __name__ == "__main__":
    main()
