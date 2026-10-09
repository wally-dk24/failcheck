"""Tests for the runner and the CLI."""

import subprocess
import sys

import pytest

from failcheck import verdicts
from failcheck.adapter import HarnessAdapter
from failcheck.runner import build_context, run
from tests.broken_harness import BrokenAdapter
from tests.clean_harness import CleanAdapter


def test_build_context_shape():
    ctx = build_context(BrokenAdapter())
    assert ctx["adapter_name"] == "BrokenAdapter"
    assert len(ctx["checks"]) == 1
    assert ctx["count_pairs"] == []


def test_run_returns_twelve_results_in_order():
    results = run(BrokenAdapter())
    assert len(results) == 12
    names = [p.NAME for p, _, _ in results]
    assert names == ["measuring_wrong_thing", "absence_as_answer", "stale_claims",
                     "unfailable_check", "faulty_inference", "part_for_whole",
                     "accepted_vs_done", "disagreeing_counts",
                     "identity_independence", "reader_limit_as_system",
                     "security_exposure", "probe_changes_target"]
    for _, verdict, _ in results:
        assert verdict in verdicts.ALL


def test_run_flags_broken_harness():
    failed = {p.NAME for p, v, _ in run(BrokenAdapter()) if v == verdicts.FAIL}
    assert "absence_as_answer" in failed
    assert "unfailable_check" in failed


def test_run_passes_clean_harness():
    failed = [(p.NAME, e) for p, v, e in run(CleanAdapter())
              if v == verdicts.FAIL]
    assert failed == [], f"clean harness failed: {failed}"


def test_run_rejects_invalid_verdict():
    class BadAdapter(HarnessAdapter):
        def describe_checks(self):
            return iter(())

    import failcheck.patterns.absence_as_answer as mod
    real = mod.check
    mod.check = lambda ctx: ("MAYBE", "x")
    try:
        with pytest.raises(ValueError, match="invalid verdict"):
            run(BadAdapter())
    finally:
        mod.check = real


def _cli(*args):
    r = subprocess.run([sys.executable, "-m", "failcheck", *args],
                       capture_output=True, text=True, cwd=".")
    return r.returncode, r.stdout


def test_cli_list_shows_twelve_patterns():
    code, out = _cli("list")
    assert code == 0
    lines = [l for l in out.splitlines() if l.strip()]
    assert len(lines) == 12
    assert any("absence_as_answer" in l for l in lines)


def test_cli_run_broken_harness_exits_1_and_shows_remedy():
    code, out = _cli("run", "--harness", "tests.broken_harness")
    assert code == 1
    assert "[FAIL] absence_as_answer" in out
    assert "remedy:" in out
    assert "repro:  python3 demos/absence_as_answer.py" in out


def test_cli_run_clean_harness_exits_0():
    code, out = _cli("run", "--harness", "tests.clean_harness")
    assert code == 0, out
    assert "0 FAIL" in out


def test_cli_run_missing_adapter_errors():
    code, out = _cli("run", "--harness", "tests.test_patterns")
    assert code != 0
