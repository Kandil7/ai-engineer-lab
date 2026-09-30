"""
Challenge 02: Queues and Workflows — Reference Solution
=======================================================
"""

from __future__ import annotations

from collections.abc import Callable


def insert_if_absent(store: dict, key: str, value) -> bool:
    """Insert only when absent; True if inserted, False if already present.

    Why this approach: dict membership is the natural-key dedupe that makes
    at-least-once delivery safe — the second delivery is a no-op by
    construction, not by hope.
    """
    if key in store:
        return False
    store[key] = value
    return True


def run_job(
    job: dict, handler: Callable[[dict], bool], policy: dict, sleep: Callable[[float], None]
) -> str:
    """Run one job with retry policy; return 'done' or 'dead_letter'.

    Why this approach: classify before retrying. Transient failures get
    bounded exponential backoff (the delay doubles, so a recovering
    dependency is not stormed); permanent failures stop immediately —
    retrying a malformed payload three times is three wasted calls.
    """
    max_attempts = int(policy["max_attempts"])
    base = float(policy["base_delay"])
    transient = tuple(policy["transient"])
    attempts = 0
    while attempts < max_attempts:
        attempts += 1
        try:
            if handler(job):
                return "done"
        except transient:
            if attempts < max_attempts:
                sleep(base * (2 ** (attempts - 1)))
                continue
            return "dead_letter"
        except Exception:
            return "dead_letter"
    return "dead_letter"


def run_worker_pool(
    jobs: list[tuple[str, str]], handler: Callable[[str, str], bool], policy: dict
) -> dict[str, int]:
    """Process redelivered/poison jobs with idempotent accounting.

    Why this approach: a seen-set keyed by job id is the idempotency layer
    the broker cannot provide — at-least-once redelivery then costs only a
    hash lookup. Result bookkeeping is counters only, so memory stays flat
    no matter how long the job list is.
    """
    max_attempts = int(policy["max_attempts"])
    transient = tuple(policy["transient"])
    done = 0
    dead_lettered = 0
    skipped = 0
    handler_calls = 0
    seen: set[str] = set()
    for job_id, payload in jobs:
        if job_id in seen:
            skipped += 1
            continue
        seen.add(job_id)
        attempts = 0
        while attempts < max_attempts:
            attempts += 1
            handler_calls += 1
            try:
                if handler(job_id, payload):
                    done += 1
                    break
            except transient:
                if attempts >= max_attempts:
                    dead_lettered += 1
                    break
            except Exception:
                dead_lettered += 1
                break
    return {
        "done": done,
        "dead_lettered": dead_lettered,
        "skipped_duplicates": skipped,
        "handler_calls": handler_calls,
    }
