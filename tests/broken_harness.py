"""A deliberately-broken harness for CLI tests: exhibits absence_as_answer
and unfailable_check, nothing else."""

from failcheck.adapter import HarnessAdapter


class BrokenAdapter(HarnessAdapter):
    def describe_checks(self):
        yield {
            "name": "witness continuity",
            "claim": "log continuous",
            "evidence_how": "compare anchors; missing yesterday counts as ok",
            "on_empty": "pass",
            "source_verified": False,
            "can_abstain": False,
        }


ADAPTER = BrokenAdapter()
