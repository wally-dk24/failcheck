#!/usr/bin/env python3
"""Demo: identity_independence — the watchdog that shares fate.

The health endpoint is served by the very process it watches. Kill the
process and the "checker" dies with it — it can never report the
outage. The fixed checker runs in a separate process (here: a separate
object with its own liveness) and survives to report.

Run: python3 demos/identity_independence.py
"""


class Process:
    def __init__(self, name):
        self.name = name
        self.alive = True

    def kill(self):
        self.alive = False


class NaiveWatchdog:
    """Broken: lives inside the watched process."""

    def __init__(self, process):
        self.host = process  # same fate

    def healthy(self):
        if not self.host.alive:
            raise RuntimeError("watchdog died with its host")
        return True


class IndependentWatchdog:
    """Fixed: separate fate; can report the outage."""

    def __init__(self):
        self.alive = True

    def healthy(self, process):
        return self.alive and process.alive


def main():
    app = Process("app")
    naive = NaiveWatchdog(app)
    fixed = IndependentWatchdog()

    app.kill()  # the outage

    try:
        naive_result = naive.healthy()
    except RuntimeError as e:
        naive_result = f"DIED ({e})"
    fixed_result = fixed.healthy(app)

    print(f"after killing the app, naive watchdog reports: {naive_result}"
          "   <-- shares fate; can never report the outage")
    print(f"after killing the app, fixed watchdog reports healthy={fixed_result}")
    assert fixed_result is False
    print("\nok: the fixed checker survives its target and reports the truth")


if __name__ == "__main__":
    main()
