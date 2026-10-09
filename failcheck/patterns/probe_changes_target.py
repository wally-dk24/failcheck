"""Pattern 12: probe_changes_target — the measurement changes what it
measures.

The "is the queue draining?" check consumes a message to find out. The
latency probe's traffic is what trips the autoscaler. A probe that
mutates its target doesn't observe the system — it performs an
experiment on it, then reports the results as observations.
"""

from failcheck import verdicts

NAME = "probe_changes_target"
TITLE = "The probe changes the target"
DESCRIPTION = "Measuring mutates what is measured."

REMEDY = (
    "Prefer read-only observation: peek, don't pop; sample, don't "
    "stimulate. Where mutation is unavoidable (a synthetic transaction), "
    "run it against a canary the real traffic never sees, and label the "
    "verdict as experimental rather than observational. In the adapter, "
    "mutates_target=True fails this pattern until the probe is made "
    "read-only or moved to a canary."
)


def check(harness_context):
    """FAIL on any check whose measurement mutates its target."""
    offenders = []
    evaluable = 0
    for c in harness_context["checks"]:
        mutates = c.get("mutates_target")
        if mutates is None:
            continue
        evaluable += 1
        if mutates:
            offenders.append(c.get("name", "?"))
    if not evaluable:
        return verdicts.NOT_APPLICABLE, "no check states whether it mutates"
    if offenders:
        return (
            verdicts.FAIL,
            "checks that mutate their target: " + ", ".join(offenders),
        )
    return verdicts.PASS, "every evaluated check is read-only"
