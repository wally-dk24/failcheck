#!/usr/bin/env python3
"""Demo: measuring_wrong_thing — the backup log vs the backup.

The claim is "backup completed". The naive checker verifies the backup
*log file* exists. The log was written, but the backup itself failed
halfway. The fixed checker reads the backup manifest.

Run: python3 demos/measuring_wrong_thing.py
"""

import os
import tempfile


def naive_backup_ok(directory):
    """Broken: measures the log, claims the backup."""
    return os.path.exists(os.path.join(directory, "backup.log"))


def fixed_backup_ok(directory):
    """Fixed: measures what it claims — the manifest the backup wrote."""
    manifest = os.path.join(directory, "backup.manifest")
    if not os.path.exists(manifest):
        return False
    with open(manifest) as f:
        return "COMPLETE" in f.read()


def main():
    with tempfile.TemporaryDirectory() as d:
        # The backup job ran, wrote its log, then died mid-copy.
        with open(os.path.join(d, "backup.log"), "w") as f:
            f.write("starting backup...\ncopying shard 1/4...\n")
        # No manifest: the backup never finished.

        print(f"naive checker says backup completed: {naive_backup_ok(d)}"
              "   <-- the log exists; the backup failed")
        print(f"fixed checker says backup completed: {fixed_backup_ok(d)}")
        assert naive_backup_ok(d) is True
        assert fixed_backup_ok(d) is False
        print("\nok: the fixed checker measures the claim, not a proxy")


if __name__ == "__main__":
    main()
