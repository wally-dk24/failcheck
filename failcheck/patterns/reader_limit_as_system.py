"""Pattern 10: reader_limit_as_system — the reader's limit read as the
system's limit.

The scan reads the last 1000 log lines and reports "no errors in the
system". The API page size is 50 and the check reads page one. Every
reader has a window; the failure is promoting the window to the world.
What you didn't read is not evidence of anything.
"""

from failcheck import verdicts

NAME = "reader_limit_as_system"
TITLE = "The reader's limit read as the system's"
DESCRIPTION = "A bounded read behind an unbounded claim."

REMEDY = (
    "Name the reader's window in the claim itself: 'no errors in the last "
    "1000 lines', not 'no errors'. In the adapter, reader_limits records "
    "the bound (page size, line cap, time window); any claim broader than "
    "the bound fails this pattern. If the bound can't cover the claim, "
    "page through the whole thing or shrink the claim — never let the "
    "reader's convenience define the system's truth."
)

# Words that make a claim about the whole system rather than what was read.
TOTALIZING = ("all", "every", "anywhere", "entire", "whole", "system")


def check(harness_context):
    """FAIL when a check states reader limits but its claim is totalizing."""
    offenders = []
    evaluable = 0
    for c in harness_context["checks"]:
        limits = c.get("reader_limits")
        claim = c.get("claim", "")
        if not limits:
            continue
        evaluable += 1
        lowered = claim.lower()
        if any(word in lowered for word in TOTALIZING):
            offenders.append(
                f"{c.get('name', '?')} reads only {limits!r}, "
                f"claims {claim!r}"
            )
    if not evaluable:
        return verdicts.NOT_APPLICABLE, "no check states reader limits"
    if offenders:
        return (
            verdicts.FAIL,
            "checks promoting a bounded read to an unbounded claim: "
            + "; ".join(offenders),
        )
    return verdicts.PASS, "every evaluated claim is scoped to its reader"
