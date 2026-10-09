#!/usr/bin/env python3
"""Demo: accepted_vs_done — the job was accepted, not completed.

A deploy checker watches the CI queue: the job was accepted, so it
reports "deploy done". The job then failed. The fixed checker waits for
the terminal state and verifies the deployed thing answers.

Run: python3 demos/accepted_vs_done.py
"""


class FakeCI:
    def __init__(self):
        self.jobs = {}

    def submit(self, name):
        self.jobs[name] = "accepted"
        return "accepted"

    def finish(self, name, ok):
        self.jobs[name] = "succeeded" if ok else "failed"

    def state(self, name):
        return self.jobs[name]


def naive_deploy_done(ci):
    """Broken: watches the hand-off."""
    return ci.submit("deploy") == "accepted"


def fixed_deploy_done(ci):
    """Fixed: watches the completion, then verifies the outcome."""
    ci.submit("deploy")
    ci.finish("deploy", ok=False)  # the job ran and failed
    state = ci.state("deploy")
    deployed_answers = False  # the new version never went live
    return state == "succeeded" and deployed_answers


def main():
    ci = FakeCI()
    print(f"naive checker says deploy done: {naive_deploy_done(ci)}"
          "   <-- 'accepted' is not 'done'")
    ci2 = FakeCI()
    print(f"fixed checker says deploy done: {fixed_deploy_done(ci2)}")
    assert naive_deploy_done(FakeCI()) is True
    assert fixed_deploy_done(FakeCI()) is False
    print("\nok: the fixed checker verifies the outcome, not the hand-off")


if __name__ == "__main__":
    main()
