#!/usr/bin/env python3
"""Demo: faulty_inference — "the API answered, therefore the data is correct".

The evidence (HTTP 200) is real. The conclusion (payload correct) is a
leap: the endpoint returned 200 with a stale cached payload. The fixed
checker validates the payload digest, not just the status.

Run: python3 demos/faulty_inference.py
"""


def naive_data_correct(status, payload):
    """Broken: 200 therefore correct."""
    return status == 200


def fixed_data_correct(status, payload, expected_digest):
    """Fixed: the status proves reachability; the digest proves correctness."""
    if status != 200:
        return False
    return payload.get("digest") == expected_digest


def main():
    # The endpoint answers 200 but serves yesterday's cached payload.
    status, payload = 200, {"rows": 3, "digest": "yesterday"}

    print(f"naive checker says data correct: "
          f"{naive_data_correct(status, payload)}   <-- 200 proves nothing")
    print(f"fixed checker says data correct: "
          f"{fixed_data_correct(status, payload, expected_digest='today')}")
    assert naive_data_correct(status, payload) is True
    assert fixed_data_correct(status, payload, "today") is False
    print("\nok: the fixed checker asks what the evidence actually proves")


if __name__ == "__main__":
    main()
