"""Pattern 9: identity_independence — the check and the thing checked
share fate.

The watchdog's health endpoint is served by the process it watches; the
backup verifier reads the manifest the backup job wrote. When checker
and checked fail together, the check is a mirror, not a witness. A
check must be able to fail while the thing it checks is healthy, and
vice versa — otherwise it measures itself.
"""

from failcheck import verdicts

NAME = "identity_independence"
TITLE = "Check and checked share fate"
DESCRIPTION = "The check is not independent of what it checks."

REMEDY = (
    "Put the check on a separate fate line from its target: a different "
    "process, a different credential, a different data path. The test is "
    "simple — kill the target and confirm the check fails; kill everything "
    "except the target and confirm the check still runs. In the adapter, "
    "independent=False marks a check that shares fate with its target; "
    "either separate them or record the shared fate as a known weakness "
    "instead of pretending the check is a witness."
)


def check(harness_context):
    """FAIL on any check that shares fate with its target."""
    offenders = []
    evaluable = 0
    for c in harness_context["checks"]:
        independent = c.get("independent")
        if independent is None:
            continue
        evaluable += 1
        if not independent:
            offenders.append(c.get("name", "?"))
    if not evaluable:
        return verdicts.NOT_APPLICABLE, "no check states its independence"
    if offenders:
        return (
            verdicts.FAIL,
            "checks sharing fate with their target: " + ", ".join(offenders),
        )
    return verdicts.PASS, "every evaluated check is independent of its target"
