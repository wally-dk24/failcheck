"""The twelve failure patterns.

Each pattern module exposes:

- ``NAME`` — snake_case identifier (matches the module name).
- ``TITLE`` — short human title.
- ``DESCRIPTION`` — one line.
- ``REMEDY`` — one paragraph: what to do about it.
- ``check(harness_context)`` — returns ``(verdict, evidence)`` where
  verdict is one of ``failcheck.verdicts`` and evidence is a short
  string naming the offending check(s) and why.

``harness_context`` is a dict built by the runner::

    {"checks": [...],           # list of check dicts from the adapter
     "count_pairs": [...],      # optional pairs of counts that must agree
     "adapter_name": "..."}     # class name, for evidence strings
"""

from failcheck.patterns import (
    absence_as_answer,
    accepted_vs_done,
    disagreeing_counts,
    faulty_inference,
    identity_independence,
    measuring_wrong_thing,
    part_for_whole,
    probe_changes_target,
    reader_limit_as_system,
    security_exposure,
    stale_claims,
    unfailable_check,
)

PATTERNS = [
    measuring_wrong_thing,
    absence_as_answer,
    stale_claims,
    unfailable_check,
    faulty_inference,
    part_for_whole,
    accepted_vs_done,
    disagreeing_counts,
    identity_independence,
    reader_limit_as_system,
    security_exposure,
    probe_changes_target,
]

BY_NAME = {p.NAME: p for p in PATTERNS}

__all__ = ["PATTERNS", "BY_NAME"]
