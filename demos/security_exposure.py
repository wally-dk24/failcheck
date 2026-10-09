#!/usr/bin/env python3
"""Demo: security_exposure — the debug dump that logs secrets.

A state-capture check dumps the environment to a log file for
diagnosis. The environment contains API keys. The check passes — and
leaks. The fixed checker redacts secrets before writing anything.

Run: python3 demos/security_exposure.py
"""

import os
import tempfile

SECRET_MARKERS = ("KEY", "SECRET", "TOKEN", "PASSWORD")


def naive_capture_state(env, path):
    """Broken: passes, and leaks."""
    with open(path, "w") as f:
        for k, v in env.items():
            f.write(f"{k}={v}\n")
    return True


def fixed_capture_state(env, path):
    """Fixed: redacts before writing."""
    with open(path, "w") as f:
        for k, v in env.items():
            if any(m in k for m in SECRET_MARKERS):
                v = "<redacted>"
            f.write(f"{k}={v}\n")
    return True


def main():
    env = {"APP_MODE": "prod", "BACKUP_API_KEY": "sk-live-abc123"}
    with tempfile.TemporaryDirectory() as d:
        naive_log = os.path.join(d, "naive.log")
        fixed_log = os.path.join(d, "fixed.log")
        naive_capture_state(env, naive_log)
        fixed_capture_state(env, fixed_log)
        with open(naive_log) as f:
            naive_leaked = "sk-live-abc123" in f.read()
        with open(fixed_log) as f:
            fixed_leaked = "sk-live-abc123" in f.read()

        print(f"naive checker passed; secret in log: {naive_leaked}"
              "   <-- a passing check that leaks")
        print(f"fixed checker passed; secret in log: {fixed_leaked}")
        assert naive_leaked is True
        assert fixed_leaked is False
        print("\nok: the fixed checker inventories exposure and redacts")


if __name__ == "__main__":
    main()
