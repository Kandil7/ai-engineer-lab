"""
Exercise 01: Reliability and Distributed Systems Patterns
==========================================================
Audit a service's dependency-call policy the way a reviewer would: run the
eight REL rules from Lecture 01 against a policy pack and flag missing
timeouts, unsafe retries, dead-man's-switch circuit breakers, unbounded
queues, unguarded side effects, and shared rate-limit buckets.

The demo runs the rules against two built-in packs: a BAD pack that trips
every rule, and a GOOD pack that must raise zero findings. It then exercises
the real components the lecture teaches — full-jitter retry, a circuit
breaker state machine, a per-caller token bucket, an idempotency store, and
a deadline budget — all against seeded, offline fixtures. No network.

Prerequisites:
    Python 3.11+ standard library only. No third-party packages.

Usage:
    python exercises/01-reliability-patterns.py
    python exercises/01-reliability-patterns.py path/to/policy.json
"""

from __future__ import annotations

import json
import random
import sys
import time
from collections.abc import Callable
from dataclasses import dataclass, field
from pathlib import Path

_SOURCE_TEXT = Path(__file__).read_text(encoding="utf-8")

# ---------------------------------------------------------------------------
# 1. Models
# ---------------------------------------------------------------------------


@dataclass
class Finding:
    """One rule violation in one policy pack."""

    severity: str
    code: str
    line: int
    message: str


@dataclass
class Analysis:
    """All findings for one policy pack."""

    source: str
    findings: list[Finding] = field(default_factory=list)

    @property
    def critical_count(self) -> int:
        return sum(1 for f in self.findings if f.severity == "critical")

    @property
    def warning_count(self) -> int:
        return sum(1 for f in self.findings if f.severity == "warning")


# ---------------------------------------------------------------------------
# 2. Policy access and marker-based line resolution
# ---------------------------------------------------------------------------


def _call(pack: dict) -> dict:
    """Return the call-policy object; a bare config dict is accepted too."""
    cfg = pack.get("call")
    if isinstance(cfg, dict):
        return cfg
    return pack


def _declared_line(label: str, marker: str) -> int:
    """Resolve a finding's line by scanning this file for '# LABEL:marker'."""
    needle = f"# {label}:{marker}"
    for number, line in enumerate(_SOURCE_TEXT.splitlines(), start=1):
        if needle in line:
            return number
    return 0


# ---------------------------------------------------------------------------
# 3. Rules (REL001 - REL008)
# ---------------------------------------------------------------------------


def check_timeout(pack: dict, label: str, findings: list[Finding]) -> None:
    """REL001: an outbound call without connect/read timeouts wedges a pool slot."""
    timeout = _call(pack).get("timeout")
    if (
        isinstance(timeout, dict)
        and timeout.get("connect") is not None
        and timeout.get("read") is not None
    ):
        return
    findings.append(
        Finding(
            severity="critical",
            code="REL001",
            line=_declared_line(label, "timeout"),
            message=(
                "No complete timeout policy (connect and read both required). "
                "A call with no timeout does not fail; it occupies a thread, socket, "
                "and pool slot until the OS gives up."
            ),
        )
    )


def check_backoff(pack: dict, label: str, findings: list[Finding]) -> None:
    """REL002: retries with fixed backoff fire in lockstep at the dependency."""
    retry = _call(pack).get("retry")
    if not isinstance(retry, dict) or int(retry.get("attempts", 1)) <= 1:
        return
    backoff = retry.get("backoff")
    kind = backoff.get("kind") if isinstance(backoff, dict) else None
    if kind in (None, "fixed", "none"):
        findings.append(
            Finding(
                severity="warning",
                code="REL002",
                line=_declared_line(label, "retry.backoff"),
                message=(
                    "Retries configured without growing backoff (fixed or missing). "
                    "Use exponential backoff with a cap so a recovering dependency "
                    "gets room instead of the original request rate."
                ),
            )
        )


def check_retryable_classes(pack: dict, label: str, findings: list[Finding]) -> None:
    """REL003: retrying non-retryable classes burns budget on deterministic failures."""
    retry = _call(pack).get("retry")
    if not isinstance(retry, dict) or int(retry.get("attempts", 1)) <= 1:
        return
    classes = {str(c).lower() for c in retry.get("retryable_classes", [])}
    bad = sorted(classes & {"4xx", "validation", "client"})
    if bad:
        findings.append(
            Finding(
                severity="warning",
                code="REL003",
                line=_declared_line(label, "retry.classes"),
                message=(
                    f"Retryable classes include non-retryable {bad}. "
                    "4xx and validation failures repeat identically on every attempt; "
                    "retrying them multiplies load without changing the outcome."
                ),
            )
        )


def check_breaker(pack: dict, label: str, findings: list[Finding]) -> None:
    """REL004: a breaker that never opens is a dead-man's switch nobody watches."""
    breaker = _call(pack).get("breaker")
    healthy = (
        isinstance(breaker, dict)
        and bool(breaker.get("enabled"))
        and bool(breaker.get("failure_rate_threshold"))
    )
    if healthy:
        return
    findings.append(
        Finding(
            severity="critical",
            code="REL004",
            line=_declared_line(label, "breaker"),
            message=(
                "Circuit breaker disabled or missing a failure-rate threshold, so it "
                "never opens. Failures keep being retried into a dead dependency and "
                "the caller's deadline is spent for nothing."
            ),
        )
    )


def check_queue(pack: dict, label: str, findings: list[Finding]) -> None:
    """REL005: an unbounded queue is a memory leak with a time axis."""
    queue = _call(pack).get("queue")
    maxsize = queue.get("maxsize") if isinstance(queue, dict) else None
    if isinstance(maxsize, int) and maxsize > 0:
        return
    findings.append(
        Finding(
            severity="critical",
            code="REL005",
            line=_declared_line(label, "queue"),
            message=(
                "Queue maxsize is missing or <= 0: unbounded. Producers must block or "
                "be rejected when the queue fills; otherwise resident memory climbs "
                "while the service still reports itself healthy."
            ),
        )
    )


def check_side_effect(pack: dict, label: str, findings: list[Finding]) -> None:
    """REL006: retries plus redelivery duplicate any unguarded side effect."""
    side = _call(pack).get("side_effect")
    if not isinstance(side, dict) or side.get("idempotency_key"):
        return
    findings.append(
        Finding(
            severity="critical",
            code="REL006",
            line=_declared_line(label, "side_effect"),
            message=(
                f"Side effect '{side.get('kind', 'operation')}' has no idempotency key. "
                "Retries and queue redelivery will charge, email, or write twice; "
                "guard it with an idempotency key, a natural key, or a dedup store."
            ),
        )
    )


def check_jitter(pack: dict, label: str, findings: list[Finding]) -> None:
    """REL007: no jitter means synchronized callers retry in lockstep."""
    retry = _call(pack).get("retry")
    if not isinstance(retry, dict) or int(retry.get("attempts", 1)) <= 1:
        return
    if str(retry.get("jitter") or "none").lower() in {"none", "no", "off", "false"}:
        findings.append(
            Finding(
                severity="warning",
                code="REL007",
                line=_declared_line(label, "retry.jitter"),
                message=(
                    "Retry jitter is disabled. Every caller that failed together retries "
                    "together: use full jitter (random in [0, backoff]) to spread the herd "
                    "across the whole window."
                ),
            )
        )


def check_rate_limit_key(pack: dict, label: str, findings: list[Finding]) -> None:
    """REL008: a shared rate-limit bucket lets one caller exhaust everyone's quota."""
    rate = _call(pack).get("rate_limit")
    if not isinstance(rate, dict) or not rate.get("enabled"):
        return
    key = str(rate.get("bucket_key") or "").lower()
    if key in {"", "global", "all", "shared"}:
        findings.append(
            Finding(
                severity="warning",
                code="REL008",
                line=_declared_line(label, "rate_limit.key"),
                message=(
                    "Rate limiter buckets by a shared key instead of per caller. "
                    "One caller's burst drains the single bucket and innocent callers "
                    "receive 429s; key by user, IP, or tenant."
                ),
            )
        )


# ---------------------------------------------------------------------------
# 4. Analysis entry point
# ---------------------------------------------------------------------------


def analyze_pack(pack: dict, label: str) -> Analysis:
    """Run every REL rule against one policy pack."""
    service = pack.get("service")
    source = f"{label} pack ({service})" if service else f"{label} pack"
    analysis = Analysis(source=source)

    check_timeout(pack, label, analysis.findings)
    check_backoff(pack, label, analysis.findings)
    check_retryable_classes(pack, label, analysis.findings)
    check_breaker(pack, label, analysis.findings)
    check_queue(pack, label, analysis.findings)
    check_side_effect(pack, label, analysis.findings)
    check_jitter(pack, label, analysis.findings)
    check_rate_limit_key(pack, label, analysis.findings)

    analysis.findings.sort(key=lambda f: (f.code, f.line))
    return analysis


def render(analysis: Analysis) -> str:
    """Format one analysis for the terminal."""
    lines = [f"Policy pack: {analysis.source}"]
    if not analysis.findings:
        lines.append("  No findings. 0 critical, 0 warning.")
        return "\n".join(lines)
    for f in analysis.findings:
        where = f"line {f.line}" if f.line else "line -"
        lines.append(f"  {f.code}  {f.severity:<8}  {where:<9}  {f.message}")
    lines.append(
        f"  {len(analysis.findings)} findings: "
        f"{analysis.critical_count} critical, {analysis.warning_count} warning"
    )
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# 5. Sample policy packs used for the demo
# ---------------------------------------------------------------------------

PACK_BAD: dict = {
    "service": "ingest-worker",
    "call": {
        "timeout": {"connect": None, "read": None},  # BAD:timeout
        "retry": {
            "attempts": 5,
            "backoff": {"kind": "fixed", "base": 1.0},  # BAD:retry.backoff
            "jitter": "none",  # BAD:retry.jitter
            "retryable_classes": [
                "timeout",
                "network",
                "5xx",
                "4xx",
            ],  # BAD:retry.classes
        },
        "breaker": {"enabled": False},  # BAD:breaker
        "queue": {"maxsize": 0},  # BAD:queue
        "side_effect": {"kind": "charge", "idempotency_key": None},  # BAD:side_effect
        "rate_limit": {"enabled": True, "bucket_key": "global"},  # BAD:rate_limit.key
    },
}

PACK_GOOD: dict = {
    "service": "chat-gateway",
    "call": {
        "timeout": {"connect": 10.0, "read": 60.0},  # GOOD:timeout
        "retry": {
            "attempts": 3,
            "backoff": {
                "kind": "exponential",
                "base": 1.0,
                "growth": 2.0,
                "cap": 30.0,
            },  # GOOD:retry.backoff
            "jitter": "full",  # GOOD:retry.jitter
            "retryable_classes": [
                "timeout",
                "network",
                "5xx",
                "429",
            ],  # GOOD:retry.classes
        },
        "breaker": {  # GOOD:breaker
            "enabled": True,
            "failure_rate_threshold": 0.5,
            "min_samples": 20,
            "cooldown_s": 30.0,
        },
        "queue": {"maxsize": 1000},  # GOOD:queue
        "side_effect": {
            "kind": "charge",
            "idempotency_key": "required",
        },  # GOOD:side_effect
        "rate_limit": {
            "enabled": True,
            "bucket_key": "user_id",
            "requests": 100,
            "window_s": 60,
        },  # GOOD:rate_limit.key
    },
}


# ---------------------------------------------------------------------------
# 6. Reliability components
# ---------------------------------------------------------------------------


class _FakeClock:
    """Deterministic clock for demos; never touches wall time."""

    def __init__(self, start: float = 0.0) -> None:
        self._t = start

    def __call__(self) -> float:
        return self._t

    def advance(self, seconds: float) -> None:
        self._t += seconds


@dataclass
class Deadline:
    """Absolute time budget handed down a call chain as remaining time."""

    budget_s: float
    now: Callable[[], float] = time.monotonic
    _expires_at: float = field(init=False, default=0.0)

    def __post_init__(self) -> None:
        self._expires_at = self.now() + self.budget_s

    def remaining(self) -> float:
        return max(0.0, self._expires_at - self.now())

    def expired(self) -> bool:
        return self.remaining() <= 0.0

    def can_attempt(self, min_slice_s: float) -> bool:
        """Never start an attempt that cannot finish inside the budget."""
        return self.remaining() >= min_slice_s


@dataclass(frozen=True)
class RetryPolicy:
    """Exponential backoff with jitter, an attempt cap, and class filtering."""

    attempts: int = 3
    base: float = 1.0
    growth: float = 2.0
    cap: float = 30.0
    jitter: str = "full"
    retryable_classes: tuple[str, ...] = ("timeout", "network", "5xx", "429")

    def delay(self, attempt: int, rng: random.Random) -> float:
        ceiling = min(self.cap, self.base * (self.growth**attempt))
        if self.jitter == "full":
            return rng.uniform(0.0, ceiling)
        if self.jitter == "equal":
            return ceiling / 2.0 + rng.uniform(0.0, ceiling / 2.0)
        return ceiling

    def should_retry(self, kind: str, attempt: int) -> bool:
        return attempt < self.attempts and kind in self.retryable_classes


class CircuitBreaker:
    """closed -> open -> half-open state machine with a failure-rate threshold."""

    def __init__(
        self,
        failure_rate: float = 0.5,
        min_samples: int = 20,
        cooldown_s: float = 30.0,
        now: Callable[[], float] = time.monotonic,
    ) -> None:
        self._rate = failure_rate
        self._min = min_samples
        self._cooldown = cooldown_s
        self._now = now
        self.state = "closed"
        self._fails = 0
        self._total = 0
        self._opened_at = 0.0
        self._trials_left = 0

    def allow(self) -> bool:
        if self.state == "open":
            if self._now() - self._opened_at < self._cooldown:
                return False
            self._transition("half-open")
            self._trials_left = 1
        if self.state == "half-open":
            if self._trials_left <= 0:
                return False
            self._trials_left -= 1
            return True
        return True

    def record(self, success: bool) -> None:
        if self.state == "half-open":
            if success:
                self._transition("closed")
                self._fails = self._total = 0
            else:
                self._reopen()
            return
        if self.state != "closed":
            return
        self._total += 1
        if not success:
            self._fails += 1
        if self._total >= self._min and self._fails / self._total >= self._rate:
            self._reopen()

    def _reopen(self) -> None:
        self._transition("open")
        self._opened_at = self._now()
        self._fails = self._total = 0

    def _transition(self, new_state: str) -> None:
        self.state = new_state


class TokenBucketLimiter:
    """Rate limiter with one refillable bucket per caller key."""

    def __init__(
        self,
        rate: float,
        capacity: int,
        now: Callable[[], float] = time.monotonic,
    ) -> None:
        self._rate = rate
        self._capacity = float(capacity)
        self._now = now
        self._buckets: dict[str, tuple[float, float]] = {}

    def allow(self, key: str) -> bool:
        tokens, last = self._buckets.get(key, (self._capacity, self._now()))
        now = self._now()
        tokens = min(self._capacity, tokens + (now - last) * self._rate)
        if tokens >= 1.0:
            self._buckets[key] = (tokens - 1.0, now)
            return True
        self._buckets[key] = (tokens, now)
        return False


class IdempotencyStore:
    """Records keys already applied so a repeat delivery skips the side effect."""

    def __init__(self) -> None:
        self._seen: set[str] = set()

    def first_time(self, key: str) -> bool:
        if key in self._seen:
            return False
        self._seen.add(key)
        return True


class FlakyDependency:
    """Offline stand-in: fails the first `failures` calls, then succeeds."""

    def __init__(self, failures: int) -> None:
        self._failures = failures
        self.calls = 0

    def call(self) -> str:
        self.calls += 1
        if self.calls <= self._failures:
            raise TimeoutError(f"simulated timeout on call {self.calls}")
        return "ok"


# ---------------------------------------------------------------------------
# 7. Demos
# ---------------------------------------------------------------------------


def _demo_jitter() -> None:
    n, attempt = 100, 3
    ceiling = min(
        RetryPolicy().cap, RetryPolicy().base * RetryPolicy().growth ** attempt
    )
    print(f"Jitter spread: {n} callers, attempt {attempt}, ceiling {ceiling:.1f}s")
    for mode in ("none", "equal", "full"):
        rng = random.Random(1729)
        policy = RetryPolicy(jitter=mode)
        delays = [policy.delay(attempt, rng) for _ in range(n)]
        spread = max(delays) - min(delays)
        print(
            f"    {mode:>4}-jitter: spread {spread:5.2f}s "
            f"(first wave {min(delays):.2f}..{max(delays):.2f}s)"
        )


def _demo_retry_loop() -> None:
    dep = FlakyDependency(failures=2)
    policy = RetryPolicy()
    rng = random.Random(2026)
    print("Retry loop vs flaky dependency (2 timeouts, then success):")
    for attempt in range(1, policy.attempts + 1):
        try:
            dep.call()
            print(f"    attempt {attempt}: success after {dep.calls} call(s)")
            return
        except TimeoutError:
            wait = policy.delay(attempt - 1, rng)
            print(f"    attempt {attempt}: timeout, full-jitter wait {wait:5.2f}s")
    print("    attempts exhausted")


def _demo_breaker() -> None:
    clock = _FakeClock()
    breaker = CircuitBreaker(
        failure_rate=0.5, min_samples=10, cooldown_s=30.0, now=clock
    )
    print("Circuit breaker: threshold 0.50, min samples 10, cooldown 30.0s")
    for _ in range(10):
        breaker.record(False)
    print(f"    after 10 failures: state={breaker.state}")
    print(f"    allow() while open: {breaker.allow()} (fails fast, no call made)")
    clock.advance(31.0)
    print(f"    allow() after 31s cooldown: {breaker.allow()} (half-open probe)")
    breaker.record(True)
    print(f"    probe succeeded: state={breaker.state}")


def _demo_idempotency() -> None:
    store = IdempotencyStore()
    with_key = sum(1 for key in ("op-7", "op-7") if store.first_time(key))
    without_key = sum(1 for _ in ("op-7", "op-7"))
    print("Idempotency: two deliveries of the same operation")
    print(f"    with idempotency key: {with_key} side effect(s) applied")
    print(f"    without key (REL006): {without_key} side effects applied")


def _demo_rate_limit() -> None:
    clock = _FakeClock()
    per_caller = TokenBucketLimiter(rate=2.0, capacity=5, now=clock)
    burst = [per_caller.allow("u1") for _ in range(7)]
    print("Rate limit: token bucket, capacity 5, refill 2/s")
    print(
        f"    caller u1, 7 rapid calls: {sum(burst)} allowed, "
        f"{len(burst) - sum(burst)} denied"
    )
    print(f"    caller u2, own bucket: {per_caller.allow('u2')}")
    shared = TokenBucketLimiter(rate=2.0, capacity=5, now=clock)
    for _ in range(7):
        shared.allow("global")
    print(
        "    shared 'global' bucket (REL008): caller u2 after u1's burst: "
        f"{shared.allow('global')}"
    )


def _demo_deadline() -> None:
    clock = _FakeClock()
    deadline = Deadline(2.0, now=clock)
    backoffs = [1.0, 2.0, 4.0]
    attempt_cost, min_slice = 0.45, 0.5
    print("Deadline: 2.00s budget, 0.50s minimum slice per attempt")
    for attempt in range(1, 5):
        remaining = deadline.remaining()
        if not deadline.can_attempt(min_slice):
            print(
                f"    attempt {attempt}: remaining {remaining:.2f}s < "
                f"{min_slice:.2f}s min slice -> refused"
            )
            break
        backoff = backoffs[attempt - 1]
        print(
            f"    attempt {attempt}: remaining {remaining:.2f}s -> run "
            f"(fails after {attempt_cost:.2f}s), backoff {backoff:.2f}s"
        )
        clock.advance(attempt_cost + backoff)


# ---------------------------------------------------------------------------
# 8. Entry point
# ---------------------------------------------------------------------------


def main(argv: list[str]) -> int:
    print("=" * 72)
    print("Exercise 01: Reliability and Distributed Systems Patterns")
    print("=" * 72)

    if len(argv) > 1:
        path = Path(argv[1])
        if not path.is_file():
            print(f"error: no such policy file: {path}", file=sys.stderr)
            return 2
        try:
            # utf-8-sig: Windows editors save JSON with a BOM; plain utf-8 would
            # leave U+FEFF in the text and json.loads would reject it.
            pack = json.loads(path.read_text(encoding="utf-8-sig"))
        except json.JSONDecodeError as exc:
            print(f"error: {path} is not valid JSON: {exc}", file=sys.stderr)
            return 2
        analysis = analyze_pack(pack, label="FILE")
        print(render(analysis))
        return 1 if analysis.critical_count else 0

    bad = analyze_pack(PACK_BAD, label="BAD")
    good = analyze_pack(PACK_GOOD, label="GOOD")
    print(render(bad))
    print()
    print(render(good))
    print("-" * 72)

    _demo_jitter()
    print()
    _demo_retry_loop()
    print()
    _demo_breaker()
    print()
    _demo_idempotency()
    print()
    _demo_rate_limit()
    print()
    _demo_deadline()
    print("-" * 72)
    print(
        f"Demo result: BAD pack raised {bad.critical_count} critical and "
        f"{bad.warning_count} warning findings; GOOD pack raised "
        f"{good.critical_count} critical and {good.warning_count} warning findings."
    )
    print("No network access, no wall-clock dependence: reruns are identical.")

    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
