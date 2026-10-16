"""
Exercise 11: Agent Loop — Simulator, Checkpoints, and Trajectory Audit
=======================================================================
Run an agent loop the way Lecture 11 teaches it: perceive, plan, act,
observe, with a hard iteration bound, stuck-loop detection, checkpoints
before destructive calls, and a success predicate that stops the loop.
Then audit trajectories with the eight AGT rules: missing bounds, stuck
loops, unapproved destructive calls, fire-and-forget results, missing
checkpoints, unbounded state, missing outcomes, and blown budgets.

The demo runs the rules against two built-in packs: a BAD pack that trips
every rule exactly once, and a GOOD pack that must raise zero findings.
It then runs the live simulator against fake deterministic tools, proving
the loop terminates with checkpoints captured — all offline, stdlib only,
deterministic.

Prerequisites:
    Python 3.11+ standard library only. No third-party packages.

Usage:
    python exercises/11-agent-loop.py
    python exercises/11-agent-loop.py path/to/trajectory.json
"""

from __future__ import annotations

import json
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable

_SOURCE_TEXT = Path(__file__).read_text(encoding="utf-8")

# ----- 1. Models -----


@dataclass
class Finding:
    """One rule violation in one trajectory."""

    severity: str
    code: str
    line: int
    message: str


@dataclass
class Checkpoint:
    """State snapshot captured before a destructive tool call."""

    step_index: int
    state: dict[str, Any]


@dataclass
class Tool:
    """One tool the simulated agent may call."""

    name: str
    destructive: bool
    handler: Callable[[dict[str, Any], dict[str, Any]], str]


@dataclass
class Trajectory:
    """Everything one agent-loop run did, and how it ended."""

    steps: list[dict[str, Any]] = field(default_factory=list)
    outcome: str | None = None
    checkpoints: list[Checkpoint] = field(default_factory=list)
    meta: dict[str, Any] = field(default_factory=dict)


# ----- 2. Marker-based line resolution -----


def _declared_line(marker: str) -> int:
    """Resolve a finding's line by scanning this file for 'marker'."""
    for lineno, line in enumerate(_SOURCE_TEXT.splitlines(), start=1):
        if marker in line:
            return lineno
    return 0


# ----- 3. Deterministic simulator: perceive-plan-act-observe -----


def _h_search(args: dict[str, Any], state: dict[str, Any]) -> str:
    """Fake deterministic search: always finds two hits."""
    query = str(args.get("query", ""))
    state["last_search"] = query
    return f"found 2 hits for '{query}' [evidence ready]"


def _h_read(args: dict[str, Any], state: dict[str, Any]) -> str:
    """Fake deterministic file read with one locked path and one goal path."""
    path = str(args.get("file_path", ""))
    state["last_read"] = path
    if path == "DONE.md":
        return "file contents: TASK-DONE milestone recorded"
    if "locked" in path:
        return f"Error: permission denied for '{path}'"
    return f"contents of {path} (42 lines)"


def _h_delete_cache(args: dict[str, Any], state: dict[str, Any]) -> str:
    """Fake deterministic destructive tool: clears the simulated cache."""
    target = str(args.get("target", "cache"))
    state["cache"] = "cleared"
    return f"deleted {target} contents (37 entries removed)"


TOOLS = [
    Tool(name="search_code", destructive=False, handler=_h_search),
    Tool(name="read_file", destructive=False, handler=_h_read),
    Tool(name="delete_cache", destructive=True, handler=_h_delete_cache),
]

POLICY = {
    "max_iterations": 3,
    "max_state_keys": 25,
    "approvals": set(),
    "success_contains": "TASK-DONE",
    "script": [],
    "destructive_tools": ["delete_cache"],
}

LIVE_POLICY = {
    "max_iterations": 6,
    "max_state_keys": 25,
    "approvals": {"delete_cache"},
    "success_contains": "TASK-DONE",
    "script": [
        ("search_code", {"query": "retry helper"}),
        ("delete_cache", {"target": "cache"}),
        ("read_file", {"file_path": "DONE.md"}),
    ],
    "destructive_tools": ["delete_cache"],
}

STUCK_POLICY = {
    "max_iterations": 5,
    "max_state_keys": 25,
    "approvals": set(),
    "success_contains": "TASK-DONE",
    "script": [
        ("read_file", {"file_path": "locked.txt"}),
        ("read_file", {"file_path": "locked.txt"}),
        ("read_file", {"file_path": "locked.txt"}),
    ],
    "destructive_tools": ["delete_cache"],
}


def _record(
    steps: list[dict[str, Any]],
    index: int,
    thought: str,
    action: str,
    args: dict[str, Any],
    observation: str,
    result_id: str,
    approved: bool,
    state: dict[str, Any],
) -> None:
    """Append one well-formed step dict to the trajectory."""
    steps.append(
        {
            "index": index,
            "thought": thought,
            "action": action,
            "args": dict(args),
            "observation": observation,
            "result_id": result_id,
            "approved": approved,
            "state_size": len(state),
        }
    )


def run_loop(task: str, tools: list[Tool], policy: dict[str, Any]) -> Trajectory:
    """Execute perceive-plan-act-observe up to max_iterations.

    Perceive builds the state summary, plan pops the next scripted action,
    act validates approval plus captures a checkpoint before any destructive
    call, observe records the step. The loop stops on the success predicate,
    on a repeated action plus observation pair (stuck), on state growth past
    the cap, on an exhausted plan (graceful give-up), or on the iteration
    bound. Unknown tools yield an error observation so the loop can recover,
    mirroring DevMate's unknown-action recovery.
    """
    max_iterations = int(policy.get("max_iterations", 10))
    approvals = set(policy.get("approvals", ()))
    success_contains = str(policy.get("success_contains", "TASK-DONE"))
    state_cap = int(policy.get("max_state_keys", 25))
    script = list(policy.get("script", []))
    by_name = {t.name: t for t in tools}
    steps: list[dict[str, Any]] = []
    checkpoints: list[Checkpoint] = []
    state: dict[str, Any] = {"task": task}
    outcome: str | None = None
    last_pair: tuple[str, str] | None = None
    pos = 0
    for index in range(max_iterations):
        if pos >= len(script):
            outcome = (
                "gave_up: plan exhausted with no success signal; "
                "returning partial results instead of looping forever"
            )
            break
        action, args = script[pos]
        pos += 1
        prev_ref = steps[-1]["result_id"] if steps else "task-brief"
        thought = (
            f"Using {prev_ref} I will call {action} "
            f"with {json.dumps(args, sort_keys=True)}"
        )
        result_id = f"r{index}"
        tool = by_name.get(action)
        if tool is None:
            observation = (
                f"Error: unknown action '{action}'. Available: {sorted(by_name)}"
            )
            _record(
                steps,
                index,
                thought,
                action,
                args,
                observation,
                result_id,
                False,
                state,
            )
            pair = (action, observation)
            if pair == last_pair:
                outcome = (
                    "stuck_loop_detected: same action with same observation "
                    "twice in a row; stopping with partial results"
                )
                break
            last_pair = pair
            continue
        if tool.destructive:
            checkpoints.append(Checkpoint(step_index=index, state=dict(state)))
            if action not in approvals:
                observation = f"Error: approval denied for destructive tool '{action}'"
                _record(
                    steps,
                    index,
                    thought,
                    action,
                    args,
                    observation,
                    result_id,
                    False,
                    state,
                )
                pair = (action, observation)
                if pair == last_pair:
                    outcome = (
                        "stuck_loop_detected: same action with same observation "
                        "twice in a row; stopping with partial results"
                    )
                    break
                last_pair = pair
                continue
        observation = tool.handler(dict(args), state)
        _record(
            steps,
            index,
            thought,
            action,
            args,
            observation,
            result_id,
            action in approvals or not tool.destructive,
            state,
        )
        if success_contains in observation:
            outcome = f"success: finished with evidence: {observation[:120]}"
            break
        pair = (action, observation)
        if pair == last_pair:
            outcome = (
                "stuck_loop_detected: same action with same observation "
                "twice in a row; stopping with partial results"
            )
            break
        last_pair = pair
        if len(state) > state_cap:
            outcome = (
                f"state_cap_exceeded: {len(state)} keys pass the cap "
                f"of {state_cap}; stopping before memory grows unboundedly"
            )
            break
    else:
        outcome = (
            f"max_iterations_reached: stopped after {max_iterations} steps "
            "with partial results"
        )
    return Trajectory(
        steps=steps,
        outcome=outcome,
        checkpoints=checkpoints,
        meta={
            "task": task,
            "max_iterations": max_iterations,
            "max_state_keys": state_cap,
        },
    )


# ----- 4. Trajectory auditor: eight AGT rules -----


def _as_dict_traj(traj: Trajectory | dict[str, Any]) -> dict[str, Any]:
    """Normalize a Trajectory or a plain dict into one plain dict."""
    if isinstance(traj, Trajectory):
        return {
            "meta": dict(traj.meta),
            "steps": [dict(s) for s in traj.steps],
            "outcome": traj.outcome,
            "checkpoints": [
                {"step_index": c.step_index, "state": dict(c.state)}
                for c in traj.checkpoints
            ],
        }
    data = dict(traj)
    data["meta"] = dict(data.get("meta") or {})
    data["steps"] = [dict(s) for s in (data.get("steps") or [])]
    raw_cps = data.get("checkpoints") or []
    norm_cps = []
    for c in raw_cps:
        if isinstance(c, Checkpoint):
            norm_cps.append({"step_index": c.step_index})
        elif isinstance(c, dict):
            norm_cps.append({"step_index": c.get("step_index")})
    data["checkpoints"] = norm_cps
    return data


def _valid_bound(value: Any) -> bool:
    """A usable iteration bound is a positive int (bools do not count)."""
    return isinstance(value, int) and not isinstance(value, bool) and value > 0


def audit_trajectory(
    traj: Trajectory | dict[str, Any], policy: dict[str, Any]
) -> list[Finding]:
    """Run the eight AGT rules over one trajectory, in code order."""
    data = _as_dict_traj(traj)
    meta = data["meta"]
    steps = data["steps"]
    outcome = data.get("outcome")
    checkpoints = data["checkpoints"]
    out: list[Finding] = []
    destructive = set(policy.get("destructive_tools", ()))

    bound = meta.get("max_iterations")
    if not _valid_bound(bound):
        out.append(
            Finding(
                "error",
                "AGT001",
                _declared_line("# BAD:AGT001"),
                "trajectory meta declares no positive max_iterations bound; "
                "a loop without a hard bound is open-loop",
            )
        )
    for i in range(1, len(steps)):
        prev, cur = steps[i - 1], steps[i]
        if (
            prev.get("action") == cur.get("action")
            and prev.get("observation") == cur.get("observation")
            and not cur.get("replan")
        ):
            out.append(
                Finding(
                    "error",
                    "AGT002",
                    _declared_line("# BAD:AGT002"),
                    f"steps {prev.get('index')} and {cur.get('index')} repeat "
                    f"action '{cur.get('action')}' with an identical "
                    "observation and no replan step between; the loop is stuck",
                )
            )
            break
    for s in steps:
        if s.get("action") in destructive and not s.get("approved"):
            out.append(
                Finding(
                    "critical",
                    "AGT003",
                    _declared_line("# BAD:AGT003"),
                    f"destructive tool '{s.get('action')}' executed at step "
                    f"{s.get('index')} with no approval record",
                )
            )
    later_contexts: list[str] = []
    for s in steps:
        later_contexts.append(
            f"{s.get('thought', '')} {json.dumps(s.get('args', {}), sort_keys=True, default=str)}"
        )
    outcome_text = str(outcome or "")
    for i, s in enumerate(steps):
        rid = s.get("result_id")
        if not rid:
            continue
        following = " ".join(later_contexts[i + 1 :]) + " " + outcome_text
        if rid not in following:
            out.append(
                Finding(
                    "warning",
                    "AGT004",
                    _declared_line("# BAD:AGT004"),
                    f"result '{rid}' from step {s.get('index')} is never "
                    "referenced by any later thought, action, or the outcome; "
                    "a fire-and-forget tool call wastes budget",
                )
            )
    have_cps = {c.get("step_index") for c in checkpoints}
    for s in steps:
        if s.get("action") in destructive and s.get("index") not in have_cps:
            out.append(
                Finding(
                    "critical",
                    "AGT005",
                    _declared_line("# BAD:AGT005"),
                    f"destructive action at step {s.get('index')} has no "
                    "checkpoint captured immediately before it; resume is "
                    "impossible after an interruption",
                )
            )
    cap = meta.get("max_state_keys", policy.get("max_state_keys", 25))
    if not _valid_bound(cap):
        cap = 25
    over = [
        (s.get("index"), s.get("state_size"))
        for s in steps
        if isinstance(s.get("state_size"), int) and s["state_size"] > cap
    ]
    if over:
        worst = max(over, key=lambda t: t[1])
        out.append(
            Finding(
                "error",
                "AGT006",
                _declared_line("# BAD:AGT006"),
                f"state grows unboundedly: step {worst[0]} holds "
                f"{worst[1]} keys past the cap of {cap}",
            )
        )
    if not outcome:
        out.append(
            Finding(
                "error",
                "AGT007",
                _declared_line("# BAD:AGT007"),
                "trajectory has no outcome record; the ending is unknown and "
                "no partial-result report exists",
            )
        )
    raw_budget: Any = bound if _valid_bound(bound) else policy.get("max_iterations")
    budget = 0
    if (
        isinstance(raw_budget, int)
        and not isinstance(raw_budget, bool)
        and raw_budget > 0
    ):
        budget = raw_budget
    if budget > 0 and len(steps) > budget:
        source = "meta" if _valid_bound(bound) else "policy"
        out.append(
            Finding(
                "error",
                "AGT008",
                _declared_line("# BAD:AGT008"),
                f"loop ran {len(steps)} steps past the stated budget of "
                f"{budget} from {source}; the bound was not enforced",
            )
        )
    return out


# ----- 5. Built-in trajectories -----

TRAJ_BAD = {
    "meta": {"task": "clear the cache and report", "max_state_keys": 25},  # BAD:AGT001
    "steps": [  # BAD:AGT008 (4 steps run past the policy budget of 3)
        {
            "index": 0,
            "thought": "I will search the index for the retry helper",
            "action": "search_code",
            "args": {"query": "retry helper"},
            "observation": "found retry helper in util.py",
            "result_id": "r0",
            "approved": False,
            "state_size": 3,
        },
        {
            "index": 1,
            "thought": "Using r0 I will read util.py to see the helper",
            "action": "read_file",
            "args": {"file_path": "util.py"},
            "observation": "Error: permission denied",
            "result_id": "r1",
            "approved": False,
            "state_size": 9,
        },
        {
            "index": 2,  # BAD:AGT002 (same action plus observation as step 1, no replan)
            "thought": "Using r1 I will retry reading util.py the same way",
            "action": "read_file",
            "args": {"file_path": "util.py"},
            "observation": "Error: permission denied",
            "result_id": "r2",
            "approved": False,
            "state_size": 31,  # BAD:AGT006 (31 keys pass the cap of 25)
        },
        {
            "index": 3,
            "thought": "Using r2 I will clear the cache and finish",
            "action": "delete_cache",
            "args": {"target": "cache"},
            "observation": "cache deleted",
            "result_id": "r3",  # BAD:AGT004 (r3 is never referenced later)
            "approved": False,  # BAD:AGT003 (destructive with no approval)
            "state_size": 33,
        },
    ],
    "outcome": None,  # BAD:AGT007 (no outcome record)
    "checkpoints": [],  # BAD:AGT005 (no checkpoint before the destructive step)
}

TRAJ_GOOD = {
    "meta": {
        "task": "clear the cache and report",
        "max_iterations": 10,
        "max_state_keys": 25,
    },
    "steps": [
        {
            "index": 0,
            "thought": "I will search the index for the retry helper",
            "action": "search_code",
            "args": {"query": "retry helper"},
            "observation": "found retry helper in util.py",
            "result_id": "r0",
            "approved": False,
            "state_size": 4,
        },
        {
            "index": 1,
            "thought": "Using r0 I will clear the cache now that it is approved",
            "action": "delete_cache",
            "args": {"target": "cache"},
            "observation": "deleted cache contents (37 entries removed)",
            "result_id": "r1",
            "approved": True,
            "state_size": 6,
        },
        {
            "index": 2,
            "thought": "Using r1 I will read DONE.md to confirm the milestone",
            "action": "read_file",
            "args": {"file_path": "DONE.md"},
            "observation": "file contents: TASK-DONE milestone recorded",
            "result_id": "r2",
            "approved": False,
            "state_size": 7,
        },
    ],
    "outcome": "success: cache cleared and milestone confirmed from r2",
    "checkpoints": [{"step_index": 1, "state": {"task": "clear the cache"}}],
}


# ----- 6. Demos -----


def _print_findings(title: str, findings: list[Finding]) -> None:
    print(f"--- {title}: {len(findings)} finding(s) ---")
    for f in findings:
        print(f"{f.code} [{f.severity}] line {f.line}: {f.message}")


def _demo_audit() -> None:
    bad = audit_trajectory(TRAJ_BAD, POLICY)
    _print_findings("BAD pack", bad)
    good = audit_trajectory(TRAJ_GOOD, POLICY)
    _print_findings("GOOD pack", good)
    if not good:
        print("GOOD pack clean")


def _demo_live() -> Trajectory:
    print("--- live run_loop demo ---")
    traj = run_loop("clear the cache and report", TOOLS, LIVE_POLICY)
    print(f"outcome: {traj.outcome}")
    print(f"steps: {len(traj.steps)} (budget {traj.meta['max_iterations']})")
    print(f"checkpoints: {len(traj.checkpoints)}")
    for c in traj.checkpoints:
        print(f"checkpoint before step {c.step_index}: keys={sorted(c.state)}")
    return traj


# ----- 7. Self-check and entry -----


def _self_check() -> None:
    bad_codes = sorted(f.code for f in audit_trajectory(TRAJ_BAD, POLICY))
    assert bad_codes == [f"AGT00{i}" for i in range(1, 9)], (
        f"BAD pack codes: {bad_codes}"
    )
    assert not audit_trajectory(TRAJ_GOOD, POLICY), "GOOD pack must raise zero findings"
    live = run_loop("clear the cache and report", TOOLS, LIVE_POLICY)
    assert live.outcome is not None and live.outcome.startswith("success"), live.outcome
    assert len(live.steps) <= LIVE_POLICY["max_iterations"], live.steps
    assert len(live.checkpoints) >= 1, "live run must capture a checkpoint"
    stuck = run_loop("read the locked file", TOOLS, STUCK_POLICY)
    assert stuck.outcome is not None and stuck.outcome.startswith(
        "stuck_loop_detected"
    ), stuck.outcome
    assert len(stuck.steps) == 2, stuck.steps
    print("SELF-CHECK passed: 8/8 BAD codes, 0 GOOD findings, live run ends in budget")


def main(argv: list[str]) -> int:
    if len(argv) > 1:
        raw = Path(argv[1]).read_text(encoding="utf-8-sig")
        traj = json.loads(raw)
        _print_findings(f"trajectory {argv[1]}", audit_trajectory(traj, POLICY))
        return 0
    _demo_audit()
    _demo_live()
    _self_check()
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
