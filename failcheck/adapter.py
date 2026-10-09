"""Harness adapter interface.

The operator describes how each of their checks produces evidence.
failcheck classifies which failure patterns apply and runs only those.

Implement :class:`HarnessAdapter` and point the CLI at the module that
defines ``ADAPTER``::

    # my_harness.py
    from failcheck.adapter import HarnessAdapter

    class MyAdapter(HarnessAdapter):
        def describe_checks(self):
            yield {
                "name": "inbox poll",
                "claim": "no new messages",
                "evidence_how": "Twilio API list, last 2 minutes",
                "on_empty": "verify",       # empty result -> verify the source
                "source_verified": True,    # the API call itself is checked
                "recheck": "each-run",
                "can_abstain": True,
            }

    ADAPTER = MyAdapter()

Then: ``python -m failcheck run --harness my_harness``

Check description schema — ``name``, ``claim`` and ``evidence_how`` are
required; the rest are optional honesty fields. A pattern can only judge
what you tell it; missing fields make that pattern NOT_APPLICABLE, which
is an honest "can't tell", not a pass:

- ``measures``: what is actually measured, if different from ``claim``.
- ``on_empty``: "pass" | "verify" | "fail" — what happens on empty/unread evidence.
- ``source_verified``: bool — is the evidence source itself verified readable?
- ``recheck``: "each-run" | "never" | ... — how often evidence is refreshed.
- ``can_abstain``: bool — can the check say "unknown"?
- ``supports_claim``: bool — does the evidence actually entail the claim?
- ``coverage``: "full" | "partial" — does the evidence cover the whole claim?
- ``stage_observed``: "accepted" | "completed" — which stage the check watches.
- ``independent``: bool — is the check independent of what it checks?
- ``reader_limits``: str — known limits of the reading mechanism.
- ``exposure``: str — secrets/permissions the check touches ("none" if clean).
- ``mutates_target``: bool — does measuring change the target?
"""

from abc import ABC, abstractmethod


class HarnessAdapter(ABC):
    """Describes an agent's checks so failcheck can test them."""

    @abstractmethod
    def describe_checks(self):
        """Yield one dict per check. See module docstring for the schema."""
        raise NotImplementedError

    def count_pairs(self):
        """Optionally yield ``{"what": str, "a": {"name","value"},
        "b": {"name","value"}}`` for two counts of the same thing that
        must agree. Defaults to none."""
        return iter(())
