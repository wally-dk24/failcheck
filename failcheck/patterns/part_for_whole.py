"""Pattern 6: part_for_whole — part of the data taken for the whole.

The check scans one log file and claims "no errors anywhere"; it polls
one region and claims the fleet is healthy. Partial coverage with a
total claim is a scope lie. The unexamined remainder is exactly where
the failure will be.
"""

from failcheck import verdicts

NAME = "part_for_whole"
TITLE = "Part of the data taken for the whole"
DESCRIPTION = "Partial coverage behind a total claim."

REMEDY = (
    "Scope every claim to the evidence actually examined: 'no errors in "
    "app.log in the last hour', not 'no errors'. In the adapter, "
    "coverage='partial' must come with a claim narrowed to the part, or "
    "the check must be extended until coverage='full'. When extending is "
    "impractical, say what is NOT covered — the uncovered remainder is a "
    "known blind spot, which is strictly better than an unknown one."
)


def check(harness_context):
    """FAIL on any check with partial coverage behind an unscoped claim."""
    offenders = []
    evaluable = 0
    for c in harness_context["checks"]:
        coverage = c.get("coverage")
        if coverage is None:
            continue
        evaluable += 1
        if str(coverage).strip().lower() == "partial":
            offenders.append(
                f"{c.get('name', '?')} claims {c.get('claim', '?')!r} "
                f"from {c.get('evidence_how', '?')!r}"
            )
    if not evaluable:
        return verdicts.NOT_APPLICABLE, "no check states its coverage"
    if offenders:
        return (
            verdicts.FAIL,
            "checks with partial coverage behind total claims: "
            + "; ".join(offenders),
        )
    return verdicts.PASS, "every evaluated check covers its claim"
