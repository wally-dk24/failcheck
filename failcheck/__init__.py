"""failcheck: a self-test suite for agent systems.

Every agent stack is full of checks that would pass on a broken system.
failcheck runs an agent's own harness, crons, and watchdogs through a
battery of twelve named failure patterns and reports which patterns the
harness exhibits.

The scarce capability isn't another verifier; it's a *check that can fail*.
"""

__version__ = "0.1.0"
