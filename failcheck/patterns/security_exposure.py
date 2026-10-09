"""Pattern 11: security_exposure — the check ignores its exposure
surface.

The debug dump writes the environment — API keys included — to a log
the check then reads. The health probe runs as root because it was easy.
A check that handles secrets carelessly is a vulnerability with a
verdict attached: it passes, and it leaks.
"""

from failcheck import verdicts

NAME = "security_exposure"
TITLE = "Security exposure ignored"
DESCRIPTION = "The check touches secrets or privilege without handling them."

REMEDY = (
    "Inventory what each check can see: environment variables, key files, "
    "privileges, network reach. Redact before logging, run with the least "
    "privilege that works, and never let a diagnostic artifact become a "
    "secret store. In the adapter, the exposure field names what the "
    "check touches ('none' if clean); anything else fails this pattern "
    "until it is handled or the check is redesigned not to need it."
)


def check(harness_context):
    """FAIL on any check with unhandled exposure."""
    offenders = []
    evaluable = 0
    for c in harness_context["checks"]:
        exposure = c.get("exposure")
        if exposure is None:
            continue
        evaluable += 1
        if str(exposure).strip().lower() not in ("none", "clean", ""):
            offenders.append(
                f"{c.get('name', '?')} exposes: {exposure}"
            )
    if not evaluable:
        return verdicts.NOT_APPLICABLE, "no check inventories its exposure"
    if offenders:
        return (
            verdicts.FAIL,
            "checks with unhandled exposure: " + "; ".join(offenders),
        )
    return verdicts.PASS, "every evaluated check has clean exposure"
