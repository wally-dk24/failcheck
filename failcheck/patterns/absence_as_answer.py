"""Pattern 2: absence_as_answer — an unread "none" taken as a real none.

A check that finds nothing must distinguish "I looked and there was
nothing" from "I never actually looked". A poll that errors silently, a
file that was never opened, an API call that returned nothing because
the credentials expired — all of these produce an empty result, and an
empty result is not a finding.
"""

from failcheck import verdicts

NAME = "absence_as_answer"
TITLE = "Absence taken as an answer"
DESCRIPTION = 'An unread "none" is taken as a real none.'

REMEDY = (
    "Every check that can return empty must do two things: verify the "
    "evidence source was actually read (the API call succeeded, the file "
    "was opened, the query ran), and say what 'empty' cost to establish. "
    "In the adapter, set source_verified=True and on_empty='verify' (re-read "
    "or cross-check) rather than 'pass'. A continuity check with no prior "
    "anchor must report 'unanchored', never 'continuous'."
)


def check(harness_context):
    """FAIL on any check that passes on empty evidence without verifying
    the source was read."""
    offenders = []
    evaluable = 0
    for c in harness_context["checks"]:
        on_empty = c.get("on_empty")
        if on_empty is None:
            continue
        evaluable += 1
        if on_empty == "pass" and not c.get("source_verified"):
            offenders.append(c.get("name", "?"))
    if not evaluable:
        return verdicts.NOT_APPLICABLE, "no check describes empty-result handling"
    if offenders:
        return (
            verdicts.FAIL,
            "checks pass on empty evidence without verifying the source: "
            + ", ".join(offenders),
        )
    return verdicts.PASS, "empty results are verified, not assumed"
