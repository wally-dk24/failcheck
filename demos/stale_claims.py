#!/usr/bin/env python3
"""Demo: stale_claims — the config that changed after startup.

A check verified the config at process start. Three weeks later the
config changed, but the check still reports the startup verdict. The
fixed checker re-reads the config on every run and reports its age.

Run: python3 demos/stale_claims.py
"""

import time


class ConfigFile:
    def __init__(self):
        self.content = "mode=safe"
        self.mtime = time.time()

    def update(self, content):
        self.content = content
        self.mtime = time.time()


def main():
    cfg = ConfigFile()
    startup_snapshot = cfg.content  # read once at startup

    # ... three weeks pass; someone flips the config ...
    cfg.update("mode=UNSAFE")

    naive_verdict = ("mode=safe" in startup_snapshot)  # still the old read
    fresh = cfg.content
    fixed_verdict = "mode=safe" in fresh

    print(f"config now: {cfg.content!r}; startup snapshot: {startup_snapshot!r}")
    print(f"naive checker says config safe: {naive_verdict}"
          "   <-- evidence is three weeks old")
    print(f"fixed checker says config safe: {fixed_verdict} "
          f"(evidence age: {time.time() - cfg.mtime:.1f}s)")
    assert naive_verdict is True
    assert fixed_verdict is False
    print("\nok: the fixed checker re-reads; freshness is part of the claim")


if __name__ == "__main__":
    main()
