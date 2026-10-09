"""Pattern 3: stale_claims — claims never re-checked against the source
of truth.

Evidence has a half-life. A config verified at process start, a token
validated once and cached, a "last successful run" timestamp from three
weeks ago — each was true when observed and is now a rumor the check
repeats with a straight face. Freshness is part of the claim.
"""

from failcheck import verdicts

NAME = "stale_claims"
TITLE = "Stale claims never re-checked"
DESCRIPTION = "Evidence is read once and trusted forever."

REMEDY = (
    "Record when each piece of evidence was produced and re-check it on a "
    "schedule that matches how fast the underlying truth changes. In the "
    "adapter, set recheck='each-run' (or a concrete interval) and have the "
    "check print the evidence age next to the verdict. A freshness field "
    "printed from a stale path stayed green for three weeks in a real "
    "system; the fix was recording input path, digest, producer, and age "
    "on every run."
)


def check(harness_context):
    """FAIL on any check whose evidence is never refreshed."""
    offenders = []
    evaluable = 0
    for c in harness_context["checks"]:
        recheck = c.get("recheck")
        if recheck is None:
            continue
        evaluable += 1
        if str(recheck).strip().lower() == "never":
            offenders.append(c.get("name", "?"))
    if not evaluable:
        return verdicts.NOT_APPLICABLE, "no check states its recheck schedule"
    if offenders:
        return (
            verdicts.FAIL,
            "checks whose evidence is never re-checked: " + ", ".join(offenders),
        )
    return verdicts.PASS, "every evaluated check refreshes its evidence"
