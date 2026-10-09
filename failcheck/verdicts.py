"""Verdict constants for pattern checks.

Every pattern's ``check()`` returns one of these:

- ``PASS`` — the pattern was evaluated and the harness does not exhibit it.
- ``FAIL`` — the harness exhibits the pattern; the check named in the
  evidence would pass on a broken system in exactly this way.
- ``NOT_APPLICABLE`` — the harness description carries no information the
  pattern can evaluate. This is an honest "can't tell", not a pass.
"""

PASS = "PASS"
FAIL = "FAIL"
NOT_APPLICABLE = "NOT_APPLICABLE"

ALL = (PASS, FAIL, NOT_APPLICABLE)
