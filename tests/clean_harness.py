"""A clean harness for CLI tests: every check is honest."""

from failcheck.adapter import HarnessAdapter


class CleanAdapter(HarnessAdapter):
    def describe_checks(self):
        yield {
            "name": "witness continuity",
            "claim": "log continuous",
            "evidence_how": "compare anchors; missing yesterday is unanchored",
            "measures": "log continuous",
            "on_empty": "verify",
            "source_verified": True,
            "recheck": "each-run",
            "can_abstain": True,
            "supports_claim": True,
            "coverage": "full",
            "stage_observed": "completed",
            "independent": True,
            "exposure": "none",
            "mutates_target": False,
        }

    def count_pairs(self):
        yield {"what": "pending jobs",
               "a": {"name": "dashboard", "value": 7},
               "b": {"name": "queue API", "value": 7}}


ADAPTER = CleanAdapter()
