"""Pattern 5: faulty_inference — the conclusion doesn't follow from the
evidence.

"Log file exists, therefore no errors." "The API answered, therefore the
data is correct." The evidence is real and the conclusion is a leap.
Inference is the quietest place for a check to lie, because both halves
look reasonable until you ask what the first actually proves about the
second.
"""

from failcheck import verdicts

NAME = "faulty_inference"
TITLE = "Faulty inference"
DESCRIPTION = "The conclusion doesn't follow from the evidence."

REMEDY = (
    "For each check, write the inference as a sentence — 'because <evidence>, "
    "therefore <claim>' — and ask whether the evidence could be true while "
    "the claim is false. If yes, the check needs stronger evidence or a "
    "weaker claim. In the adapter, supports_claim=False marks a check whose "
    "evidence you've already caught not entailing its claim; the pattern "
    "fails the harness until those are fixed or the claim is narrowed."
)


def check(harness_context):
    """FAIL on any check flagged as not entailing its claim."""
    offenders = []
    evaluable = 0
    for c in harness_context["checks"]:
        supports = c.get("supports_claim")
        if supports is None:
            continue
        evaluable += 1
        if not supports:
            offenders.append(
                f"{c.get('name', '?')} (evidence: {c.get('evidence_how', '?')})"
            )
    if not evaluable:
        return verdicts.NOT_APPLICABLE, "no check judges its own inference"
    if offenders:
        return (
            verdicts.FAIL,
            "checks whose evidence does not entail their claim: "
            + "; ".join(offenders),
        )
    return verdicts.PASS, "every evaluated check's evidence entails its claim"
