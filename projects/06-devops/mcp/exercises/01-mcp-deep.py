"""
Exercise 01: MCP Deep — Server-Manifest Audit and Approval Flow
================================================================
Audit an MCP server the way a registry reviewer would: run the eight MCP
rules from Lecture 01 against a server manifest and flag missing schemas,
blind tool descriptions, unapproved destructive tools, unaddressable
resources, unvalidated prompt interpolation, sampling lies, missing
timeouts, and unpinned versions.

The demo runs the rules against two built-in packs: a BAD pack that trips
every rule, and a GOOD pack that must raise zero findings. It then exercises
the approval flow the lecture teaches — single-use approval ids bound to the
exact call, with replay denied — all offline, stdlib only, deterministic.

Prerequisites:
    Python 3.11+ standard library only. No third-party packages.

Usage:
    python exercises/01-mcp-deep.py
    python exercises/01-mcp-deep.py path/to/manifest.json
"""

from __future__ import annotations

import hashlib
import json
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

_SOURCE_TEXT = Path(__file__).read_text(encoding="utf-8")

# ----- 1. Models -----


@dataclass
class ToolDef:
    """One tool a server exposes to the model."""

    name: str
    description: str
    input_schema: dict
    destructive: bool = False
    requires_approval: bool = False
    timeout_s: float | None = None


@dataclass
class ResourceDef:
    """One addressable context object a server exposes."""

    uri: str
    description: str = ""


@dataclass
class PromptDef:
    """One reusable prompt template with validated arguments."""

    name: str
    template: str
    args: list[str] = field(default_factory=list)


@dataclass
class ServerManifest:
    """Everything a registry needs to admit (or reject) a server."""

    name: str
    version: str
    tools: list[ToolDef] = field(default_factory=list)
    resources: list[ResourceDef] = field(default_factory=list)
    prompts: list[PromptDef] = field(default_factory=list)
    declares_sampling: bool = False
    uses_sampling: bool = False


@dataclass
class Finding:
    """One rule violation in one manifest pack."""

    severity: str
    code: str
    line: int
    message: str


# ----- 2. Marker-based line resolution -----


def _declared_line(marker: str) -> int:
    """Resolve a finding's line by scanning this file for 'marker'."""
    for lineno, line in enumerate(_SOURCE_TEXT.splitlines(), start=1):
        if marker in line:
            return lineno
    return 0


# ----- 3. Audit rules -----

_PLACEHOLDER_RE = re.compile(r"\{([A-Za-z_][A-Za-z0-9_]*)\}")
_PINNED_RE = re.compile(r"^v?\d+\.\d+\.\d+([.+-].*)?$")
_SCHEME_RE = re.compile(r"^[A-Za-z][A-Za-z0-9+.-]*://")


def audit_manifest(m: ServerManifest) -> list[Finding]:
    """Run the eight MCP rules over one manifest, in code order."""
    out: list[Finding] = []
    for t in m.tools:
        if not isinstance(t.input_schema, dict) or len(t.input_schema) == 0:
            out.append(
                Finding(
                    "error",
                    "MCP001",
                    _declared_line("# BAD:MCP001"),
                    f"tool '{t.name}' has no inputSchema; arguments cannot be validated",
                )
            )
        if len((t.description or "").strip()) < 20:
            out.append(
                Finding(
                    "warning",
                    "MCP002",
                    _declared_line("# BAD:MCP002"),
                    f"tool '{t.name}' description is too short; the model cannot choose blind",
                )
            )
        if t.destructive and not t.requires_approval:
            out.append(
                Finding(
                    "critical",
                    "MCP003",
                    _declared_line("# BAD:MCP003"),
                    f"destructive tool '{t.name}' runs without requires_approval",
                )
            )
        if t.timeout_s is None or t.timeout_s <= 0:
            out.append(
                Finding(
                    "error",
                    "MCP007",
                    _declared_line("# BAD:MCP007"),
                    f"tool '{t.name}' has no positive timeout",
                )
            )
    for r in m.resources:
        if not _SCHEME_RE.match(r.uri or ""):
            out.append(
                Finding(
                    "error",
                    "MCP004",
                    _declared_line("# BAD:MCP004"),
                    f"resource uri '{r.uri}' has no scheme; it is not addressable",
                )
            )
    for p in m.prompts:
        unlisted = sorted(
            {
                g
                for g in _PLACEHOLDER_RE.findall(p.template or "")
                if g not in (p.args or [])
            }
        )
        if unlisted:
            out.append(
                Finding(
                    "error",
                    "MCP005",
                    _declared_line("# BAD:MCP005"),
                    f"prompt '{p.name}' interpolates unlisted args: {', '.join(unlisted)}",
                )
            )
    if m.uses_sampling and not m.declares_sampling:
        out.append(
            Finding(
                "critical",
                "MCP006",
                _declared_line("# BAD:MCP006"),
                "manifest uses sampling without declaring it",
            )
        )
    version = (m.version or "").strip()
    if not version or not _PINNED_RE.match(version):
        out.append(
            Finding(
                "error",
                "MCP008",
                _declared_line("# BAD:MCP008"),
                f"manifest version '{m.version}' is empty or unpinned",
            )
        )
    return out


# ----- 4. Built-in packs -----

PACK_BAD = ServerManifest(
    name="bad-demo",
    version="latest",  # BAD:MCP008
    declares_sampling=False,  # BAD:MCP006
    uses_sampling=True,
    tools=[
        ToolDef(
            name="mystery",
            description="Search the indexed repository for code snippets.",
            input_schema={},
            timeout_s=30.0,
        ),  # BAD:MCP001
        ToolDef(
            name="x",
            description="run it",
            input_schema={"type": "object"},
            timeout_s=30.0,
        ),  # BAD:MCP002
        ToolDef(
            name="wipe_cache",
            description="Delete the local retrieval cache directory contents.",
            input_schema={"type": "object"},
            destructive=True,
            requires_approval=False,
            timeout_s=30.0,
        ),  # BAD:MCP003
        ToolDef(
            name="slow_scan",
            description="Run a full repository scan and return every match found.",
            input_schema={"type": "object"},
            timeout_s=None,
        ),  # BAD:MCP007
    ],
    resources=[
        ResourceDef(
            uri="repo/files/config", description="Server configuration file."
        ),  # BAD:MCP004
    ],
    prompts=[
        PromptDef(
            name="summarize", template="Summarize {text} for {audience}.", args=["text"]
        ),  # BAD:MCP005
    ],
)

PACK_GOOD = ServerManifest(
    name="good-demo",
    version="1.4.0",
    declares_sampling=True,
    uses_sampling=True,
    tools=[
        ToolDef(
            name="search_code",
            description="Search the indexed repository for code snippets.",
            input_schema={
                "type": "object",
                "properties": {"query": {"type": "string"}},
                "required": ["query"],
            },
            timeout_s=30.0,
        ),
        ToolDef(
            name="read_file",
            description="Read one repository file with a traversal guard.",
            input_schema={
                "type": "object",
                "properties": {"file_path": {"type": "string"}},
                "required": ["file_path"],
            },
            requires_approval=True,
            timeout_s=15.0,
        ),
        ToolDef(
            name="rotate_cache",
            description="Rotate the local retrieval cache after human approval.",
            input_schema={"type": "object"},
            destructive=True,
            requires_approval=True,
            timeout_s=30.0,
        ),
    ],
    resources=[
        ResourceDef(
            uri="repo://files/config", description="Server configuration file."
        ),
    ],
    prompts=[
        PromptDef(
            name="summarize",
            template="Summarize {text} for {audience}.",
            args=["text", "audience"],
        ),
    ],
)


# ----- 5. Approval flow -----

_CONSUMED_IDS: set[str] = set()


def _request_hash(tool: ToolDef, arguments: dict | None) -> str:
    """Bind an approval id to the exact call: name plus arguments."""
    payload = json.dumps(
        {"tool": tool.name, "arguments": arguments or {}}, sort_keys=True, default=str
    )
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()[:16]


def decide_call(
    tool: ToolDef, approved_ids: set[str], arguments: dict | None = None
) -> dict:
    """Decide one call and return the receipt: ALLOW, DENY, or AUDIT.

    Approval ids are single-use: presenting an id consumes it, and any
    replay of the same id is DENIED. Safe tools need no approval.
    """
    req = _request_hash(tool, arguments)
    approval_id = f"{tool.name}:{req}"
    receipt = {
        "tool": tool.name,
        "request_hash": req,
        "approval_id": approval_id,
        "decision": "",
        "consumed": False,
        "reason": "",
    }
    if not (tool.destructive or tool.requires_approval):
        receipt["decision"] = "ALLOW"
        receipt["reason"] = "safe tool: no approval required"
        return receipt
    if approval_id in _CONSUMED_IDS:
        receipt["decision"] = "DENY"
        receipt["reason"] = "replay: approval id already consumed (single-use)"
        return receipt
    if approval_id in set(approved_ids or ()):
        _CONSUMED_IDS.add(approval_id)
        receipt["consumed"] = True
        if tool.destructive:
            receipt["decision"] = "ALLOW"
            receipt["reason"] = "destructive call with fresh single-use approval"
        else:
            receipt["decision"] = "AUDIT"
            receipt["reason"] = (
                "gated read with fresh single-use approval; logged to audit trail"
            )
        return receipt
    receipt["decision"] = "DENY"
    receipt["reason"] = "no approval id presented for a gated tool"
    return receipt


# ----- 6. Demos -----


def _print_findings(title: str, findings: list[Finding]) -> None:
    print(f"--- {title}: {len(findings)} finding(s) ---")
    for f in findings:
        print(f"{f.code} [{f.severity}] line {f.line}: {f.message}")


def _demo_audit() -> None:
    bad = audit_manifest(PACK_BAD)
    _print_findings("BAD pack", bad)
    good = audit_manifest(PACK_GOOD)
    _print_findings("GOOD pack", good)
    if not good:
        print("GOOD pack clean")


def _demo_approvals() -> None:
    search = ToolDef(
        name="search_code",
        description="Search the indexed repository for code snippets.",
        input_schema={"type": "object"},
        timeout_s=30.0,
    )
    gated_read = ToolDef(
        name="read_file",
        description="Read one repository file with a traversal guard.",
        input_schema={"type": "object"},
        requires_approval=True,
        timeout_s=15.0,
    )
    wipe = ToolDef(
        name="wipe_cache",
        description="Delete the local retrieval cache directory contents.",
        input_schema={"type": "object"},
        destructive=True,
        requires_approval=True,
        timeout_s=30.0,
    )
    print("--- approval flow ---")
    print(json.dumps(decide_call(search, set(), {"query": "retry"})))
    read_args = {"file_path": "README.md"}
    read_aid = f"read_file:{_request_hash(gated_read, read_args)}"
    print(json.dumps(decide_call(gated_read, {read_aid}, read_args)))
    print(json.dumps(decide_call(gated_read, {read_aid}, read_args)))
    print(json.dumps(decide_call(wipe, set(), {"target": "cache"})))
    wipe_args = {"target": "cache"}
    wipe_aid = f"wipe_cache:{_request_hash(wipe, wipe_args)}"
    print(json.dumps(decide_call(wipe, {wipe_aid}, wipe_args)))
    print(json.dumps(decide_call(wipe, {wipe_aid}, wipe_args)))


# ----- 7. Self-check and entry -----


def _self_check() -> None:
    bad_codes = sorted(f.code for f in audit_manifest(PACK_BAD))
    assert bad_codes == [f"MCP00{i}" for i in range(1, 9)], (
        f"BAD pack codes: {bad_codes}"
    )
    assert not audit_manifest(PACK_GOOD), "GOOD pack must raise zero findings"
    _CONSUMED_IDS.clear()
    probe = ToolDef(
        name="probe",
        description="Probe the approval demo path end to end cleanly.",
        input_schema={"type": "object"},
        destructive=True,
        requires_approval=True,
        timeout_s=5.0,
    )
    args = {"target": "cache"}
    aid = f"probe:{_request_hash(probe, args)}"
    first = decide_call(probe, {aid}, args)
    assert first["decision"] == "ALLOW" and first["consumed"] is True, first
    replay = decide_call(probe, {aid}, args)
    assert replay["decision"] == "DENY" and "replay" in replay["reason"], replay
    print("SELF-CHECK passed: 8/8 BAD codes, 0 GOOD findings, replay denied")


def _manifest_from_dict(d: dict) -> ServerManifest:
    return ServerManifest(
        name=str(d.get("name", "")),
        version=str(d.get("version", "")),
        tools=[
            ToolDef(
                name=str(t.get("name", "")),
                description=str(t.get("description", "")),
                input_schema=t.get("input_schema", {})
                if isinstance(t.get("input_schema"), dict)
                else {},
                destructive=bool(t.get("destructive", False)),
                requires_approval=bool(t.get("requires_approval", False)),
                timeout_s=t.get("timeout_s"),
            )
            for t in d.get("tools", [])
        ],
        resources=[
            ResourceDef(
                uri=str(r.get("uri", "")), description=str(r.get("description", ""))
            )
            for r in d.get("resources", [])
        ],
        prompts=[
            PromptDef(
                name=str(p.get("name", "")),
                template=str(p.get("template", "")),
                args=list(p.get("args", [])),
            )
            for p in d.get("prompts", [])
        ],
        declares_sampling=bool(d.get("declares_sampling", False)),
        uses_sampling=bool(d.get("uses_sampling", False)),
    )


def main(argv: list[str]) -> int:
    if len(argv) > 1:
        raw = Path(argv[1]).read_text(encoding="utf-8-sig")
        manifest = _manifest_from_dict(json.loads(raw))
        _print_findings(f"manifest {argv[1]}", audit_manifest(manifest))
        return 0
    _demo_audit()
    _demo_approvals()
    _self_check()
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
