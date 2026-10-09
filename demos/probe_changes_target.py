#!/usr/bin/env python3
"""Demo: probe_changes_target — the queue-depth check that eats a message.

To find out if the queue is draining, the naive probe pops a message
and checks its age. The measurement consumed the work it was measuring.
The fixed probe peeks without popping.

Run: python3 demos/probe_changes_target.py
"""

from collections import deque


def naive_oldest_age(queue):
    """Broken: pops to observe; the queue is now shorter."""
    msg = queue.popleft()
    return msg["age_s"]


def fixed_oldest_age(queue):
    """Fixed: read-only peek."""
    return queue[0]["age_s"]


def main():
    q1 = deque([{"age_s": 120}, {"age_s": 5}])
    q2 = deque([{"age_s": 120}, {"age_s": 5}])

    naive = naive_oldest_age(q1)
    fixed = fixed_oldest_age(q2)

    print(f"naive probe says oldest age: {naive}s; queue now has {len(q1)} msgs"
          "   <-- the probe ate one")
    print(f"fixed probe says oldest age: {fixed}s; queue now has {len(q2)} msgs")
    assert len(q1) == 1 and len(q2) == 2
    print("\nok: the fixed probe observes without mutating")


if __name__ == "__main__":
    main()
