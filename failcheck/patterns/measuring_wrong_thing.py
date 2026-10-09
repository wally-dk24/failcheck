"""Pattern 1: measuring_wrong_thing — a check succeeds about something
other than what you meant.

The claim says "the backup completed" but the evidence shows "the backup
log file exists". Proxies drift: the thing measured keeps succeeding
while the thing meant quietly breaks. If what you measure isn't what you
claim, the check is testing your optimism.
"""

from failcheck import verdicts

NAME = "measuring_wrong_thing"
TITLE = "Measuring the wrong thing"
DESCRIPTION = "The check succeeds about something other than what it claims."

REMEDY = (
    "Write down, for each check, what is actually measured separately from "
    "what is claimed — in the adapter these are the 'measures' and 'claim' "
    "fields. If they differ, either change the check to measure the claim "
    "directly (read the backup manifest, not the log file) or narrow the "
    "claim to what is measured ('backup log written', not 'backup "
    "completed'). A proxy is only honest when it is named as one."
)


def check(harness_context):
    """FAIL on any check whose measured thing differs from its claim."""
    offenders = []
    evaluable = 0
    for c in harness_context["checks"]:
        measures = c.get("measures")
        claim = c.get("claim")
        if not measures or not claim:
            continue
        evaluable += 1
        if measures.strip().lower() != claim.strip().lower():
            offenders.append(
                f"{c.get('name', '?')} (measures {measures!r}, claims {claim!r})"
            )
    if not evaluable:
        return verdicts.NOT_APPLICABLE, "no check states what it measures"
    if offenders:
        return (
            verdicts.FAIL,
            "checks measuring something other than their claim: "
            + "; ".join(offenders),
        )
    return verdicts.PASS, "every evaluated check measures what it claims"
