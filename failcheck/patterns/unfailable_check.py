"""Pattern 4: unfailable_check — a check that could never fail.

A check with no "I don't know" path always reports an answer, which means
it reports confident answers from broken premises: a read that predates
the write it checks, a comparison against a baseline that was never
established, a probe whose timeout means "healthy". If a check cannot
abstain, its passes carry no information.
"""

from failcheck import verdicts

NAME = "unfailable_check"
TITLE = "A check that could never fail"
DESCRIPTION = "The check has no 'unknown' path; it always reports an answer."

REMEDY = (
    "Give every check an explicit abstain path and use it whenever a "
    "premise of the check is unverified: the read timestamp predates the "
    "last write, the baseline is missing, the probe timed out. In the "
    "adapter, set can_abstain=True and make 'unknown' a first-class "
    "verdict that pages the operator instead of passing silently. A "
    "check that cannot say 'I don't know' cannot be trusted when it "
    "says 'all clear'."
)


def check(harness_context):
    """FAIL on any check that cannot abstain."""
    offenders = []
    evaluable = 0
    for c in harness_context["checks"]:
        can_abstain = c.get("can_abstain")
        if can_abstain is None:
            continue
        evaluable += 1
        if not can_abstain:
            offenders.append(c.get("name", "?"))
    if not evaluable:
        return verdicts.NOT_APPLICABLE, "no check declares whether it can abstain"
    if offenders:
        return (
            verdicts.FAIL,
            "checks with no 'unknown' path (always report an answer): "
            + ", ".join(offenders),
        )
    return verdicts.PASS, "all evaluated checks can abstain"
