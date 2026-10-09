"""Pattern 8: disagreeing_counts — two counts of one thing disagree.

The dashboard says 12 pending jobs; the queue API says 15. Both can't be
right, which means at least one of the instruments is broken — and every
check built on either number is suspect. Agreement between independent
counts is the cheapest integrity check a harness has.
"""

from failcheck import verdicts

NAME = "disagreeing_counts"
TITLE = "Two counts of one thing disagree"
DESCRIPTION = "Independent counts of the same thing don't match."

REMEDY = (
    "When two sources count the same thing, compare them on every run and "
    "treat disagreement as a first-class failure, not a rounding error. "
    "In the adapter, expose the pairs via count_pairs(): each pair names "
    "what is counted and gives both values with their sources. Fix the "
    "disagreement at the instrument level — a check built on a disputed "
    "number inherits the dispute."
)


def check(harness_context):
    """FAIL on any pair of counts that disagree."""
    pairs = harness_context.get("count_pairs") or []
    if not pairs:
        return verdicts.NOT_APPLICABLE, "no count pairs registered"
    offenders = []
    for p in pairs:
        a, b = p.get("a", {}), p.get("b", {})
        if a.get("value") != b.get("value"):
            offenders.append(
                f"{p.get('what', '?')}: {a.get('name', '?')}={a.get('value')!r} "
                f"vs {b.get('name', '?')}={b.get('value')!r}"
            )
    if offenders:
        return (
            verdicts.FAIL,
            "disagreeing counts: " + "; ".join(offenders),
        )
    return verdicts.PASS, "all registered count pairs agree"
