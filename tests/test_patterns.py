"""Every pattern must FAIL on a deliberately-broken harness fixture and
PASS on a correct one. Fixtures are plain check dicts, the same shape an
operator's adapter yields."""

import pytest

from failcheck import verdicts
from failcheck.patterns import BY_NAME


def ctx(checks=None, pairs=None):
    return {
        "checks": checks or [],
        "count_pairs": pairs or [],
        "adapter_name": "TestAdapter",
    }


# (pattern_name, broken_check, correct_check) — broken must FAIL, correct must PASS.
# disagreeing_counts is pair-based and handled separately below.
CASES = [
    (
        "measuring_wrong_thing",
        {"name": "backup check", "claim": "backup completed",
         "measures": "backup log exists", "evidence_how": "stat backup.log"},
        {"name": "backup check", "claim": "backup completed",
         "measures": "backup completed", "evidence_how": "read manifest"},
    ),
    (
        "absence_as_answer",
        {"name": "inbox poll", "claim": "no new mail",
         "evidence_how": "API list returns []", "on_empty": "pass"},
        {"name": "inbox poll", "claim": "no new mail",
         "evidence_how": "API list returns []", "on_empty": "verify",
         "source_verified": True},
    ),
    (
        "stale_claims",
        {"name": "config check", "claim": "config valid",
         "evidence_how": "read at startup", "recheck": "never"},
        {"name": "config check", "claim": "config valid",
         "evidence_how": "re-read each run", "recheck": "each-run"},
    ),
    (
        "unfailable_check",
        {"name": "write check", "claim": "write landed",
         "evidence_how": "count rows; report missing if zero",
         "can_abstain": False},
        {"name": "write check", "claim": "write landed",
         "evidence_how": "count rows; unknown if read predates commit",
         "can_abstain": True},
    ),
    (
        "faulty_inference",
        {"name": "api check", "claim": "data correct",
         "evidence_how": "HTTP 200", "supports_claim": False},
        {"name": "api check", "claim": "data correct",
         "evidence_how": "HTTP 200 + digest match", "supports_claim": True},
    ),
    (
        "part_for_whole",
        {"name": "error scan", "claim": "no errors",
         "evidence_how": "scan app.log", "coverage": "partial"},
        {"name": "error scan", "claim": "no errors in app.log",
         "evidence_how": "scan app.log", "coverage": "full"},
    ),
    (
        "accepted_vs_done",
        {"name": "deploy check", "claim": "deploy done",
         "evidence_how": "CI job accepted", "stage_observed": "accepted"},
        {"name": "deploy check", "claim": "deploy done",
         "evidence_how": "deployed endpoint answers", "stage_observed": "completed"},
    ),
    (
        "identity_independence",
        {"name": "health check", "claim": "app alive",
         "evidence_how": "/health on the app's own port", "independent": False},
        {"name": "health check", "claim": "app alive",
         "evidence_how": "/health from separate prober", "independent": True},
    ),
    (
        "reader_limit_as_system",
        {"name": "log scan", "claim": "no errors in the system",
         "evidence_how": "read last 1000 lines", "reader_limits": "1000 lines"},
        {"name": "log scan", "claim": "no errors in the last 1000 lines",
         "evidence_how": "read last 1000 lines", "reader_limits": "1000 lines"},
    ),
    (
        "security_exposure",
        {"name": "state dump", "claim": "state captured",
         "evidence_how": "dump env to log", "exposure": "API keys in log"},
        {"name": "state dump", "claim": "state captured",
         "evidence_how": "dump redacted env to log", "exposure": "none"},
    ),
    (
        "probe_changes_target",
        {"name": "queue check", "claim": "queue draining",
         "evidence_how": "pop message, check age", "mutates_target": True},
        {"name": "queue check", "claim": "queue draining",
         "evidence_how": "peek at head, check age", "mutates_target": False},
    ),
]


@pytest.mark.parametrize("name,broken,correct", CASES)
def test_pattern_fails_on_broken_fixture(name, broken, correct):
    pattern = BY_NAME[name]
    verdict, evidence = pattern.check(ctx([broken]))
    assert verdict == verdicts.FAIL, f"{name} did not FAIL: {evidence}"
    assert broken["name"] in evidence


@pytest.mark.parametrize("name,broken,correct", CASES)
def test_pattern_passes_on_correct_fixture(name, broken, correct):
    pattern = BY_NAME[name]
    verdict, evidence = pattern.check(ctx([correct]))
    assert verdict == verdicts.PASS, f"{name} did not PASS: {evidence}"


def test_disagreeing_counts_fails_on_mismatch():
    pattern = BY_NAME["disagreeing_counts"]
    pairs = [{"what": "pending jobs",
              "a": {"name": "dashboard", "value": 12},
              "b": {"name": "queue API", "value": 15}}]
    verdict, evidence = pattern.check(ctx(pairs=pairs))
    assert verdict == verdicts.FAIL
    assert "12" in evidence and "15" in evidence


def test_disagreeing_counts_passes_on_agreement():
    pattern = BY_NAME["disagreeing_counts"]
    pairs = [{"what": "pending jobs",
              "a": {"name": "dashboard", "value": 12},
              "b": {"name": "queue API", "value": 12}}]
    verdict, _ = pattern.check(ctx(pairs=pairs))
    assert verdict == verdicts.PASS


def test_reader_limit_no_false_positive_on_install():
    """Regression: 'install' contains 'all' as a substring; the totalizing
    match must use word boundaries."""
    pattern = BY_NAME["reader_limit_as_system"]
    check = {"name": "deploy check", "claim": "no errors after install",
             "evidence_how": "read last 100 lines", "reader_limits": "100 lines"}
    verdict, _ = pattern.check(ctx([check]))
    assert verdict == verdicts.PASS


def test_all_patterns_not_applicable_on_empty_harness():
    for name, pattern in BY_NAME.items():
        verdict, _ = pattern.check(ctx())
        assert verdict == verdicts.NOT_APPLICABLE, f"{name} judged an empty harness"


def test_registry_has_twelve_patterns():
    assert len(BY_NAME) == 12
    for name, pattern in BY_NAME.items():
        assert pattern.NAME == name
        assert pattern.TITLE and pattern.DESCRIPTION and pattern.REMEDY
