"""
Exercise 01: Deployment Strategies
==================================
Analyze a Kubernetes manifest the way a reviewer and a CI gate would: catch
mutable image tags, missing resources and probes, a missing security context,
and an HPA that can never scale, before anything ever reaches a cluster.

This exercise is deliberately runnable without a cluster, kubectl, or a cloud
account. It parses manifests as line-based text (no PyYAML) and applies the
rules from Lecture 01, so you can run it against any manifest you write while
studying.

Scope note: this repository does not ship an infra/k8s/ tree. The Kubernetes
layout in projects/06-devops/deployment/README.md is a teaching example, and
the sample manifests below follow the same shape. The real deployable
artifacts in this repository are Docker-based:

    projects/04-ai-engineering/devmate/docker/Dockerfile
    infra/docker/docker-compose.yml
    render.yaml

Prerequisites:
    Python 3.11+ standard library only. No third-party packages.

Usage:
    python exercises/01-deployment-strategies.py
    python exercises/01-deployment-strategies.py path/to/manifest.yaml
"""

from __future__ import annotations

import re
import sys
import tempfile
from dataclasses import dataclass, field
from pathlib import Path

# ---------------------------------------------------------------------------
# 1. Models
# ---------------------------------------------------------------------------


@dataclass
class ContainerBlock:
    """One container or init container inside a pod template."""

    name: str
    line_number: int
    init: bool
    image: str | None = None
    image_line: int | None = None
    has_requests: bool = False
    has_limits: bool = False
    has_liveness: bool = False
    has_readiness: bool = False
    run_as_non_root: bool = False


@dataclass
class ManifestDocument:
    """One YAML document inside a (possibly multi-document) manifest file."""

    kind: str
    start_line: int
    name: str = ""
    namespace: str | None = None
    metadata_line: int | None = None
    pod_run_as_non_root: bool = False
    containers: list[ContainerBlock] = field(default_factory=list)
    min_replicas: int | None = None
    max_replicas: int | None = None
    hpa_line: int | None = None


@dataclass
class Finding:
    """A single review finding against a manifest."""

    severity: str  # "critical" | "warning" | "info"
    code: str
    line_number: int | None
    message: str


@dataclass
class Analysis:
    """Full analysis result for one manifest file."""

    path: str
    documents: list[ManifestDocument] = field(default_factory=list)
    findings: list[Finding] = field(default_factory=list)

    @property
    def container_count(self) -> int:
        return sum(len(doc.containers) for doc in self.documents)

    @property
    def critical_count(self) -> int:
        return sum(1 for f in self.findings if f.severity == "critical")

    @property
    def warning_count(self) -> int:
        return sum(1 for f in self.findings if f.severity == "warning")

    @property
    def info_count(self) -> int:
        return sum(1 for f in self.findings if f.severity == "info")


# ---------------------------------------------------------------------------
# 2. Parsing
# ---------------------------------------------------------------------------
#
# YAML is read as text, line by line. That is a deliberate constraint: a real
# manifest linter uses a YAML parser, but every rule in this exercise is about
# indentation, and a line-based reader keeps the file dependency-free.
#
# Documented limitations of this reader:
#   * a document separator is a '---' line at column 0; block scalars are
#     indented, so a literal block inside a ConfigMap cannot misfire it;
#   * flow style ('containers: [{name: api}]') is not recognized;
#   * a key indented deeper than its parent is assumed to belong to that
#     parent, which holds for any well-indented manifest.

DOCUMENT_START = re.compile(r"^---[ \t]*(?:#.*)?$")
KIND_RE = re.compile(r"^kind:[ \t]*(\S+)[ \t]*$")
KEY_VALUE_RE = re.compile(r"^[ \t]*([A-Za-z][A-Za-z0-9_.-]*)[ \t]*:[ \t]*(.*)$")
CONTAINER_LIST_RE = re.compile(r"^([ \t]*)(initContainers|containers)[ \t]*:(.*)$")
LIST_ITEM_RE = re.compile(r"^([ \t]*)-[ \t]+(.*)$")
RUN_AS_NON_ROOT_RE = re.compile(r"^runAsNonRoot[ \t]*:[ \t]*(.*)$")


def indent_of(line: str) -> int:
    """Number of leading spaces on a line."""
    return len(line) - len(line.lstrip(" "))


def is_skippable(line: str) -> bool:
    """Blank lines and full-line comments carry no structure."""
    stripped = line.strip()
    return not stripped or stripped.startswith("#")


def scalar(raw: str) -> str:
    """Strip a trailing comment and surrounding quotes from a scalar value."""
    value = re.sub(r"[ \t]+#.*$", "", raw).strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {"'", '"'}:
        value = value[1:-1]
    return value


def split_documents(text: str) -> list[tuple[int, list[str]]]:
    """Split manifest text at column-0 '---' lines.

    Returns (start_line_number, lines) pairs. Line numbers are 1-based and
    refer to positions in the original file, so every finding can point at
    the line a human sees in an editor.
    """
    documents: list[tuple[int, list[str]]] = []
    current: list[str] = []
    start = 1

    for number, line in enumerate(text.splitlines(), start=1):
        if DOCUMENT_START.match(line):
            if any(not is_skippable(existing) for existing in current):
                documents.append((start, current))
            current = []
            start = number + 1
            continue
        current.append(line)

    if any(not is_skippable(existing) for existing in current):
        documents.append((start, current))
    return documents


def find_top_level(lines: list[str], key: str) -> int | None:
    """Index of the column-0 `key:` line, or None."""
    for index, line in enumerate(lines):
        if indent_of(line) == 0 and line.startswith(key + ":"):
            return index
    return None


def parse_metadata(lines: list[str], doc: ManifestDocument) -> None:
    """Read metadata.name and metadata.namespace at the children's own indent."""
    key_index = find_top_level(lines, "metadata")
    if key_index is None:
        return
    doc.metadata_line = doc.start_line + key_index

    children: list[tuple[int, str]] = []
    for index in range(key_index + 1, len(lines)):
        line = lines[index]
        if is_skippable(line):
            continue
        if indent_of(line) == 0:
            break
        children.append((index, line))
    if not children:
        return

    child_indent = min(indent_of(line) for _, line in children)
    for index, line in children:
        if indent_of(line) != child_indent:
            continue
        match = KEY_VALUE_RE.match(line)
        if match is None:
            continue
        if match.group(1) == "name" and not doc.name:
            doc.name = scalar(match.group(2))
        elif match.group(1) == "namespace" and not doc.namespace:
            doc.namespace = scalar(match.group(2)) or None


def sub_keys(
    block: list[tuple[int, str]], key_index: int, parent_indent: int
) -> list[tuple[str, str]]:
    """(key, value) pairs inside a nested block, stopping at the parent level."""
    nested: list[tuple[str, str]] = []
    for index, line in block:
        if index <= key_index or is_skippable(line):
            continue
        if indent_of(line) <= parent_indent:
            break
        match = KEY_VALUE_RE.match(line)
        if match:
            nested.append((match.group(1), match.group(2)))
    return nested


def parse_container(
    block: list[tuple[int, str]], init: bool, start_line: int
) -> ContainerBlock:
    """Read one `- name: ...` entry of a container list."""
    first_index, first_line = block[0]
    match = LIST_ITEM_RE.match(first_line)
    content = match.group(2) if match else first_line
    key_indent = len(first_line) - len(content)

    container = ContainerBlock(
        name="",
        line_number=start_line + first_index,
        init=init,
    )

    items: list[tuple[str, str, int]] = []
    first_key = KEY_VALUE_RE.match(content)
    if first_key:
        items.append((first_key.group(1), first_key.group(2), first_index))
    for index, line in block[1:]:
        if indent_of(line) != key_indent:
            continue
        line_key = KEY_VALUE_RE.match(line)
        if line_key:
            items.append((line_key.group(1), line_key.group(2), index))

    for key, raw_value, index in items:
        if key == "name" and not container.name:
            container.name = scalar(raw_value)
        elif key == "image" and container.image is None:
            container.image = scalar(raw_value)
            container.image_line = start_line + index
        elif key == "livenessProbe":
            container.has_liveness = True
        elif key == "readinessProbe":
            container.has_readiness = True
        elif key == "resources":
            for sub_key, _ in sub_keys(block, index, key_indent):
                if sub_key == "requests":
                    container.has_requests = True
                elif sub_key == "limits":
                    container.has_limits = True
        elif key == "securityContext":
            for sub_key, sub_value in sub_keys(block, index, key_indent):
                if sub_key == "runAsNonRoot" and scalar(sub_value).lower() == "true":
                    container.run_as_non_root = True

    return container


def parse_containers(lines: list[str], doc: ManifestDocument) -> None:
    """Read every container list in the document, plus the pod-level flag."""
    entry_lines: set[int] = set()
    index = 0

    while index < len(lines):
        match = CONTAINER_LIST_RE.match(lines[index])
        if match is None:
            index += 1
            continue
        key_indent = len(match.group(1))
        list_name = match.group(2)
        rest = match.group(3)
        index += 1
        if rest.strip() and not rest.strip().startswith("#"):
            continue  # inline form: 'containers: []'

        # The region runs until the next sibling key: lines indented deeper
        # than the key, or list items sitting at the key's own indent.
        region: list[int] = []
        while index < len(lines):
            line = lines[index]
            if is_skippable(line) or indent_of(line) > key_indent:
                region.append(index)
                index += 1
                continue
            if indent_of(line) == key_indent and line.lstrip().startswith("-"):
                region.append(index)
                index += 1
                continue
            break

        entries: list[int] = []
        item_indent: int | None = None
        for region_index in region:
            item_match = LIST_ITEM_RE.match(lines[region_index])
            if item_match is None:
                continue
            indent = len(item_match.group(1))
            if item_indent is None:
                item_indent = indent
            if indent != item_indent:
                continue  # a nested list (ports, env) inside a container
            entries.append(region_index)

        for position, entry_start in enumerate(entries):
            entry_end = (
                entries[position + 1] if position + 1 < len(entries) else region[-1] + 1
            )
            block = [(i, lines[i]) for i in range(entry_start, entry_end)]
            entry_lines.update(i for i, _ in block)
            doc.containers.append(
                parse_container(block, list_name == "initContainers", doc.start_line)
            )

    # A runAsNonRoot outside every container entry belongs to the pod-level
    # securityContext, and it applies to all containers in the pod.
    for index, line in enumerate(lines):
        if index in entry_lines or is_skippable(line):
            continue
        flag = RUN_AS_NON_ROOT_RE.match(line.strip())
        if flag and scalar(flag.group(1)).lower() == "true":
            doc.pod_run_as_non_root = True


def parse_hpa(lines: list[str], doc: ManifestDocument) -> None:
    """Read minReplicas and maxReplicas from an HPA document."""
    for index, line in enumerate(lines):
        if is_skippable(line):
            continue
        match = KEY_VALUE_RE.match(line)
        if match is None:
            continue
        if match.group(1) == "minReplicas" and doc.min_replicas is None:
            doc.min_replicas = to_int(scalar(match.group(2)))
            doc.hpa_line = doc.start_line + index
        elif match.group(1) == "maxReplicas" and doc.max_replicas is None:
            doc.max_replicas = to_int(scalar(match.group(2)))
            if doc.hpa_line is None:
                doc.hpa_line = doc.start_line + index


def to_int(raw: str) -> int | None:
    try:
        return int(raw)
    except ValueError:
        return None


def parse_document(start_line: int, lines: list[str]) -> ManifestDocument:
    """Parse one YAML document into a ManifestDocument."""
    kind = ""
    for line in lines:
        if indent_of(line) == 0:
            kind_match = KIND_RE.match(line)
            if kind_match:
                kind = kind_match.group(1)
                break

    doc = ManifestDocument(kind=kind, start_line=start_line)
    parse_metadata(lines, doc)
    parse_containers(lines, doc)
    if kind == "HorizontalPodAutoscaler":
        parse_hpa(lines, doc)
    return doc


# ---------------------------------------------------------------------------
# 3. Rules
# ---------------------------------------------------------------------------

# Floating tags move without any manifest change, so a restart can pull
# different code while kubectl rollout history shows no new revision.
FLOATING_TAGS = {
    "latest",
    "stable",
    "edge",
    "nightly",
    "main",
    "master",
    "dev",
    "develop",
}

# A workload that runs to completion has no steady state to probe: a Job that
# exits 0 succeeded, and a liveness probe would only race its shutdown.
PROBE_EXEMPT_KINDS = {"Job", "CronJob"}

# Cluster-scoped objects have no namespace field at all. Flagging them for a
# missing 'namespace:' would be a false positive.
CLUSTER_SCOPED_KINDS = {
    "APIService",
    "ClusterRole",
    "ClusterRoleBinding",
    "CustomResourceDefinition",
    "MutatingWebhookConfiguration",
    "Namespace",
    "Node",
    "PersistentVolume",
    "PriorityClass",
    "StorageClass",
    "ValidatingWebhookConfiguration",
    "VolumeAttachment",
}


def is_mutable_image(image: str) -> bool:
    """True when the reference can resolve to different bytes over time."""
    if "@sha256:" in image or "@sha512:" in image:
        return False
    last_segment = image.rsplit("/", 1)[-1]
    if ":" not in last_segment:
        return True
    tag = last_segment.rsplit(":", 1)[-1].lower()
    return tag == "" or tag in FLOATING_TAGS


def check_image_tags(doc: ManifestDocument, findings: list[Finding]) -> None:
    """K8S001: ':latest' or no tag makes a rollout non-reproducible."""
    for container in doc.containers:
        if container.image is None or not is_mutable_image(container.image):
            continue
        findings.append(
            Finding(
                severity="critical",
                code="K8S001",
                line_number=container.image_line,
                message=(
                    f"Container '{container.name}' image '{container.image}' uses a mutable "
                    "tag (or none). Pin a version tag or a digest: with ':latest' or no tag "
                    "imagePullPolicy defaults to Always, so restarts can pull different code "
                    "and a rollback restores nothing."
                ),
            )
        )


def check_resources(doc: ManifestDocument, findings: list[Finding]) -> None:
    """K8S002 and K8S003: an unpinned container can starve its node."""
    for container in doc.containers:
        if not container.has_limits:
            findings.append(
                Finding(
                    severity="warning",
                    code="K8S002",
                    line_number=container.line_number,
                    message=(
                        f"Container '{container.name}' declares no resources.limits. "
                        "Without a ceiling it can consume the node's memory and get "
                        "neighbouring pods evicted instead of itself being throttled."
                    ),
                )
            )
        if not container.has_requests:
            findings.append(
                Finding(
                    severity="warning",
                    code="K8S003",
                    line_number=container.line_number,
                    message=(
                        f"Container '{container.name}' declares no resources.requests. "
                        "Requests are the scheduler's placement input and the denominator "
                        "of every HPA utilization target; set them explicitly."
                    ),
                )
            )


def check_probes(doc: ManifestDocument, findings: list[Finding]) -> None:
    """K8S004 and K8S005: restart wedged pods, route only to ready ones."""
    if doc.kind in PROBE_EXEMPT_KINDS:
        return
    for container in doc.containers:
        if container.init:
            continue  # init containers run once and exit; probes do not apply
        if not container.has_liveness:
            findings.append(
                Finding(
                    severity="warning",
                    code="K8S004",
                    line_number=container.line_number,
                    message=(
                        f"Container '{container.name}' declares no livenessProbe. "
                        "A wedged process that still listens on its port is never "
                        "restarted; a failing liveness probe is what recovers it."
                    ),
                )
            )
        if not container.has_readiness:
            findings.append(
                Finding(
                    severity="warning",
                    code="K8S005",
                    line_number=container.line_number,
                    message=(
                        f"Container '{container.name}' declares no readinessProbe. "
                        "Without one the pod is added to Service endpoints as soon as "
                        "it starts, so traffic can hit it before it can serve."
                    ),
                )
            )


def check_security(doc: ManifestDocument, findings: list[Finding]) -> None:
    """K8S006: root inside a container widens every escape."""
    for container in doc.containers:
        if container.run_as_non_root or doc.pod_run_as_non_root:
            continue
        findings.append(
            Finding(
                severity="critical",
                code="K8S006",
                line_number=container.line_number,
                message=(
                    f"Container '{container.name}' sets no securityContext.runAsNonRoot, "
                    "and neither does the pod spec. The process runs as root; set "
                    "runAsNonRoot: true at pod or container level."
                ),
            )
        )


def check_namespace(doc: ManifestDocument, findings: list[Finding]) -> None:
    """K8S007: without metadata.namespace the target is whatever kubectl points at."""
    if doc.kind in CLUSTER_SCOPED_KINDS or doc.namespace:
        return
    findings.append(
        Finding(
            severity="info",
            code="K8S007",
            line_number=doc.metadata_line or doc.start_line,
            message=(
                f"{doc.kind or 'Document'} '{doc.name}' declares no metadata.namespace. "
                "It lands in whatever namespace the current kubectl context points at, "
                "usually 'default'."
            ),
        )
    )


def check_hpa(doc: ManifestDocument, findings: list[Finding]) -> None:
    """K8S008: maxReplicas must exceed minReplicas or nothing can scale."""
    if doc.kind != "HorizontalPodAutoscaler":
        return
    minimum = doc.min_replicas if doc.min_replicas is not None else 1
    if doc.max_replicas is None:
        findings.append(
            Finding(
                severity="critical",
                code="K8S008",
                line_number=doc.hpa_line or doc.start_line,
                message=(
                    f"HPA '{doc.name}' declares no maxReplicas. It must be an integer "
                    f"greater than minReplicas ({minimum})."
                ),
            )
        )
        return
    if doc.max_replicas <= minimum:
        findings.append(
            Finding(
                severity="critical",
                code="K8S008",
                line_number=doc.hpa_line or doc.start_line,
                message=(
                    f"HPA '{doc.name}' maxReplicas ({doc.max_replicas}) is not greater "
                    f"than minReplicas ({minimum}), so the autoscaler can never change "
                    "capacity."
                ),
            )
        )


# ---------------------------------------------------------------------------
# 4. Analysis entry point
# ---------------------------------------------------------------------------


def analyze(path: Path) -> Analysis:
    """Run every rule against one manifest file."""
    text = path.read_text(encoding="utf-8")
    analysis = Analysis(path=str(path))

    for start_line, lines in split_documents(text):
        doc = parse_document(start_line, lines)
        analysis.documents.append(doc)
        check_namespace(doc, analysis.findings)
        check_image_tags(doc, analysis.findings)
        check_resources(doc, analysis.findings)
        check_probes(doc, analysis.findings)
        check_security(doc, analysis.findings)
        check_hpa(doc, analysis.findings)

    return analysis


def render(analysis: Analysis) -> str:
    """Render a human-readable report."""
    lines: list[str] = []
    lines.append("=" * 72)
    lines.append(f"Manifest review: {analysis.path}")
    lines.append("=" * 72)

    if not analysis.documents:
        lines.append("No YAML documents found in this file.")
        return "\n".join(lines)

    kinds = ", ".join(doc.kind or "<no kind>" for doc in analysis.documents)
    lines.append(
        f"Documents: {len(analysis.documents)} ({kinds})  "
        f"Containers: {analysis.container_count}"
    )
    lines.append(
        f"Findings: {analysis.critical_count} critical, "
        f"{analysis.warning_count} warning, {analysis.info_count} info"
    )
    lines.append("")

    if not analysis.findings:
        lines.append("No findings. The manifest passes every rule in this exercise.")
        return "\n".join(lines)

    order = {"critical": 0, "warning": 1, "info": 2}
    for finding in sorted(
        analysis.findings, key=lambda f: (order[f.severity], f.line_number or 0)
    ):
        location = f"L{finding.line_number}" if finding.line_number else "--"
        lines.append(f"  [{finding.severity.upper():8}] {finding.code}  {location}")
        lines.append(f"             {finding.message}")
        lines.append("")

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# 5. Sample manifests used for the demo
# ---------------------------------------------------------------------------

SAMPLE_BAD = """\
apiVersion: apps/v1
kind: Deployment
metadata:
  name: auth-service
spec:
  replicas: 2
  selector:
    matchLabels:
      app: auth-service
  template:
    metadata:
      labels:
        app: auth-service
    spec:
      initContainers:
        - name: migrate
          image: ghcr.io/org/auth-service-migrations
      containers:
        - name: auth-service
          image: ghcr.io/org/auth-service:latest
          ports:
            - containerPort: 8080
          env:
            - name: DATABASE_URL
              valueFrom:
                secretKeyRef:
                  name: db-credentials
                  key: url
---
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: auth-service-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: auth-service
  minReplicas: 5
  maxReplicas: 3
  metrics:
    - type: Resource
      resource:
        name: cpu
        target:
          type: Utilization
          averageUtilization: 70
"""

SAMPLE_GOOD = """\
apiVersion: v1
kind: Namespace
metadata:
  name: devmate
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: devmate-api
  namespace: devmate
  labels:
    app: devmate-api
spec:
  replicas: 3
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1
      maxUnavailable: 0
  selector:
    matchLabels:
      app: devmate-api
  template:
    metadata:
      labels:
        app: devmate-api
    spec:
      securityContext:
        runAsNonRoot: true
        fsGroup: 10001
      initContainers:
        - name: wait-for-db
          image: ghcr.io/example/pg-ready:1.4.2
          command: ["pg_isready", "-U", "devmate"]
          resources:
            requests:
              cpu: 50m
              memory: 64Mi
            limits:
              cpu: 200m
              memory: 128Mi
      containers:
        - name: devmate-api
          image: ghcr.io/example/devmate-api@sha256:2c797b45f2d0b8e1
          ports:
            - containerPort: 8000
          env:
            - name: APP_ENV
              value: production
          securityContext:
            runAsNonRoot: true
            allowPrivilegeEscalation: false
          resources:
            requests:
              cpu: 250m
              memory: 512Mi
            limits:
              cpu: "1"
              memory: 1Gi
          livenessProbe:
            httpGet:
              path: /health
              port: 8000
            initialDelaySeconds: 10
            periodSeconds: 15
          readinessProbe:
            httpGet:
              path: /ready
              port: 8000
            initialDelaySeconds: 5
            periodSeconds: 10
          startupProbe:
            httpGet:
              path: /health
              port: 8000
            failureThreshold: 30
            periodSeconds: 10
---
apiVersion: v1
kind: Service
metadata:
  name: devmate-api
  namespace: devmate
spec:
  type: ClusterIP
  selector:
    app: devmate-api
  ports:
    - name: http
      port: 80
      targetPort: 8000
---
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: devmate-api
  namespace: devmate
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: devmate-api
  minReplicas: 2
  maxReplicas: 10
  metrics:
    - type: Resource
      resource:
        name: cpu
        target:
          type: Utilization
          averageUtilization: 70
"""


def write_sample(path: Path, content: str) -> Path:
    """Write a sample manifest to a temporary location for analysis."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8", newline="\n")
    return path


# ---------------------------------------------------------------------------
# 6. Entry point
# ---------------------------------------------------------------------------


def main(argv: list[str]) -> int:
    """Analyze a given manifest, or run the built-in demo."""
    if len(argv) > 1:
        target = Path(argv[1])
        if not target.is_file():
            print(f"Not a file: {target}", file=sys.stderr)
            return 2
        print(render(analyze(target)))
        return 0

    print("Deployment Strategies Exercise 01")
    print("Running the built-in demo against two sample manifests.")
    print("Pass a path to analyze a real one, for example:")
    print("    python exercises/01-deployment-strategies.py")
    print("        path/to/manifest.yaml")
    print()

    with tempfile.TemporaryDirectory(prefix="k8s-manifest-exercise-") as tmp:
        scratch = Path(tmp)
        bad = write_sample(scratch / "bad.yaml", SAMPLE_BAD)
        good = write_sample(scratch / "good.yaml", SAMPLE_GOOD)
        bad_analysis = analyze(bad)
        good_analysis = analyze(good)

    print(render(bad_analysis))
    print()
    print(render(good_analysis))
    print("-" * 72)
    print(
        f"Demo result: bad sample raised {len(bad_analysis.findings)} findings "
        f"({bad_analysis.critical_count} critical, "
        f"{bad_analysis.warning_count} warning, {bad_analysis.info_count} info); "
        f"good sample raised {len(good_analysis.findings)} findings."
    )
    print("The temporary samples were cleaned up automatically.")

    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
