"""Pattern 7: accepted_vs_done — "accepted" or "queued" confused with
"done".

The job was accepted by the queue, the deploy was approved, the message
was handed to the broker. None of those are the thing done. Watching the
hand-off and reporting completion is how "done" comes to mean "the
login", not "the transaction".
"""

from failcheck import verdicts

NAME = "accepted_vs_done"
TITLE = '"Accepted" confused with "done"'
DESCRIPTION = "The check watches the hand-off, not the completion."

REMEDY = (
    "Verify the specific expected outcome, not that something happened. "
    "If the claim is 'deploy done', the evidence must be the deployed "
    "thing answering correctly — not the CI job accepted, not the "
    "approval granted. In the adapter, stage_observed='accepted' behind "
    "a claim of done fails this pattern; either follow the work to "
    "completion or narrow the claim to what was actually observed "
    "('deploy accepted', which is a weaker and honest claim)."
)


def check(harness_context):
    """FAIL on any check observing acceptance while claiming completion."""
    offenders = []
    evaluable = 0
    for c in harness_context["checks"]:
        stage = c.get("stage_observed")
        if stage is None:
            continue
        evaluable += 1
        if str(stage).strip().lower() in ("accepted", "queued", "submitted"):
            offenders.append(
                f"{c.get('name', '?')} observes {stage!r}, claims {c.get('claim', '?')!r}"
            )
    if not evaluable:
        return verdicts.NOT_APPLICABLE, "no check states which stage it observes"
    if offenders:
        return (
            verdicts.FAIL,
            "checks watching the hand-off instead of the completion: "
            + "; ".join(offenders),
        )
    return verdicts.PASS, "every evaluated check observes completion"
