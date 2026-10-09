# failcheck

**A self-test suite for agent systems.** Every agent stack is full of checks that would pass on a broken system. failcheck runs your harness, crons, and watchdogs through a battery of twelve named failure patterns and reports which patterns your checks exhibit.

The scarce capability isn't another verifier; it's a *check that can fail*.

## Why

Three real cases, all from production agent systems:

1. **A verification suite stayed green for three weeks** while reading a stale copy of its own previous answer. The freshness field was printed from a stale path. Green the whole time.
2. **A witness log went silent for nine days.** On resume, nothing flagged the gap — the continuity check compared against an absent file and passed.
3. **A poll series hid a sixteen-hour detection lag** behind single-run "no new items" summaries. Each run was fine; the series was blind.

The tie-rule: **a check reports on the run, not on the premise the run rests on.** failcheck tests the premise.

## Install

Stdlib only. Zero dependencies.

```bash
git clone https://github.com/wally-dk24/failcheck
cd failcheck
python3 -m pytest tests/   # 35 tests
```

Python 3.10+. No network, no keys, no services.

## Quick start

Describe your checks with the adapter, then run the battery:

```python
# my_harness.py
from failcheck.adapter import HarnessAdapter

class MyAdapter(HarnessAdapter):
    def describe_checks(self):
        yield {
            "name": "inbox poll",
            "claim": "no new messages",
            "evidence_how": "Twilio API list, last 2 minutes",
            "measures": "no new messages",   # what is ACTUALLY measured
            "on_empty": "verify",            # empty -> verify the source
            "source_verified": True,
            "recheck": "each-run",
            "can_abstain": True,             # the check can say "unknown"
            "supports_claim": True,
            "coverage": "full",
            "stage_observed": "completed",   # not just "accepted"
            "independent": True,             # check doesn't share fate
            "exposure": "none",
            "mutates_target": False,
        }

    def count_pairs(self):
        # two counts of the same thing that must agree
        yield {"what": "pending jobs",
               "a": {"name": "dashboard", "value": 7},
               "b": {"name": "queue API", "value": 7}}

ADAPTER = MyAdapter()
```

```bash
python3 -m failcheck run --harness my_harness
```

Output is a per-pattern verdict table. Every `FAIL` row prints the evidence, the remedy, and the repro demo:

```
[FAIL] absence_as_answer
       Absence taken as an answer
       evidence: checks pass on empty evidence without verifying the source: inbox poll
       remedy: Every check that can return empty must do two things: ...
       repro:  python3 demos/absence_as_answer.py
```

`python3 -m failcheck list` prints the twelve patterns.

### The adapter contract

`describe_checks()` yields one dict per check. Required: `name`, `claim`, `evidence_how`. Optional honesty fields (documented in `failcheck/adapter.py`): `measures`, `on_empty`, `source_verified`, `recheck`, `can_abstain`, `supports_claim`, `coverage`, `stage_observed`, `independent`, `reader_limits`, `exposure`, `mutates_target`.

A pattern can only judge what you tell it. Missing fields make that pattern `NOT_APPLICABLE` — an honest "can't tell", not a pass. The value of the tool scales with the honesty of the descriptions.

`count_pairs()` optionally yields pairs of counts of the same thing that must agree.

## The twelve patterns

| # | Pattern | One line |
|---|---------|----------|
| 1 | `measuring_wrong_thing` | The check succeeds about something other than what it claims. |
| 2 | `absence_as_answer` | An unread "none" is taken as a real none. |
| 3 | `stale_claims` | Evidence is read once and trusted forever. |
| 4 | `unfailable_check` | The check has no "unknown" path; it always reports an answer. |
| 5 | `faulty_inference` | The conclusion doesn't follow from the evidence. |
| 6 | `part_for_whole` | Partial coverage behind a total claim. |
| 7 | `accepted_vs_done` | The check watches the hand-off, not the completion. |
| 8 | `disagreeing_counts` | Independent counts of the same thing don't match. |
| 9 | `identity_independence` | The check is not independent of what it checks. |
| 10 | `reader_limit_as_system` | A bounded read behind an unbounded claim. |
| 11 | `security_exposure` | The check touches secrets or privilege without handling them. |
| 12 | `probe_changes_target` | Measuring mutates what is measured. |

Each pattern module (`failcheck/patterns/<name>.py`) exposes `check(harness_context)` returning `(verdict, evidence)` with verdict one of `PASS` / `FAIL` / `NOT_APPLICABLE`, plus a one-paragraph `REMEDY`. Each has a runnable demo in `demos/<name>.py` showing the failure mode against a deliberately-broken fixture, naive vs fixed.

## Demos

```bash
python3 demos/absence_as_answer.py   # witness log with a gap: "unanchored", not "pass"
python3 demos/unfailable_check.py    # stale read: UNKNOWN, not write_missing=True
```

## Design notes

- **Verdicts are three-valued.** `NOT_APPLICABLE` ("can't tell") is load-bearing: a lazy adapter gets "can't tell" everywhere, never a clean bill of health.
- **The battery is proven against fixtures it did not write.** Every pattern's test fails it against a deliberately-broken fixture and passes it against a correct one (`tests/test_patterns.py`).
- **Heuristics, not oracles.** Some patterns use explicit operator judgments (`supports_claim`, `measures`); others use structural rules (totalizing words behind a bounded read, `on_empty: pass` without source verification). The taxonomy plus the demos plus the remedies are the product; the detector is the convenient part.

## License

MIT. See [LICENSE](LICENSE).
