#!/usr/bin/env python3
"""Build one offline Study Studio HTML file.

The build takes a chapter JSON, the engine CSS and JS, and the HTML shell,
and writes a single file that opens from disk with the network off.

The order follows docs/STUDIO-SPEC.md section 12:

  1. Load and validate the chapter through scripts/validate_chapter.py.
  2. Compare every paragraph hash against the optional <chapter>.sha256
     sidecar. A missing sidecar prints a notice and the build continues.
  3. Inline the chapter JSON into the template.
  4. Inline the CSS and the JS.
  5. Scan the result for external references and fail on any hit.
  6. Write build/<chapterId>.html.
  7. Optionally run the in-page self-test in a headless browser.

Usage:
    python scripts/build_studio.py
    python scripts/build_studio.py --chapter schema/example-chapter.json
    python scripts/build_studio.py --out build --selftest
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import subprocess
import sys
from html.parser import HTMLParser
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

import validate_chapter  # noqa: E402  (the gate lives next to this script)

TEMPLATE_PATH = ROOT / "engine" / "template.html"
CSS_PATH = ROOT / "engine" / "studio.css"
JS_PATH = ROOT / "engine" / "studio.js"
DEFAULT_CHAPTER = ROOT / "schema" / "example-chapter.json"
DEFAULT_OUT = ROOT / "build"
STUDIO_PHASE = "1"

PLACEHOLDER_CSS = "<!--STUDIO_CSS-->"
PLACEHOLDER_JS = "<!--STUDIO_JS-->"
PLACEHOLDER_DATA = "<!--CHAPTER_DATA-->"
PLACEHOLDER_PHASE = "<!--STUDIO_PHASE-->"


# --------------------------------------------------------------------------
# Step 2: paragraph hashes against the sidecar
# --------------------------------------------------------------------------


def paragraph_hashes(data: dict) -> dict[str, str]:
    """SHA-256 of every paragraph text, keyed by `<sectionId>:<index>`."""
    hashes: dict[str, str] = {}
    for section in data.get("sections", []):
        section_id = section.get("id", "?")
        for index, paragraph in enumerate(section.get("paragraphs", [])):
            text = paragraph.get("text", "")
            key = f"{section_id}:{index}"
            hashes[key] = hashlib.sha256(text.encode("utf-8")).hexdigest()
    return hashes


def find_sidecar(chapter_path: Path) -> Path | None:
    """The sidecar is a sibling of the chapter file.

    Two names are accepted so a chapter can be written either way:
    `<chapter>.json.sha256` and `<chapter>.sha256`.
    """
    candidates = [
        chapter_path.with_name(chapter_path.name + ".sha256"),
        chapter_path.with_suffix(".sha256"),
    ]
    for candidate in candidates:
        if candidate.is_file():
            return candidate
    return None


def parse_sidecar(path: Path) -> dict[str, str]:
    """Read a sidecar into a mapping of paragraph key to SHA-256.

    Two formats are accepted:
      - JSON: an object of key -> hash, or a list of {key, sha256};
      - text: one `hash  key` pair per line, `#` comments allowed.
    """
    text = path.read_text(encoding="utf-8-sig")
    entries: dict[str, str] = {}

    stripped = text.strip()
    if stripped.startswith("{") or stripped.startswith("["):
        payload = json.loads(stripped)
        if isinstance(payload, dict):
            for key, value in payload.items():
                entries[str(key)] = str(value).strip().lower()
        else:
            for row in payload:
                key = row.get("key")
                value = row.get("sha256")
                if key is not None and value is not None:
                    entries[str(key)] = str(value).strip().lower()
        return entries

    for line in text.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        parts = line.split()
        if len(parts) >= 2:
            entries[parts[1]] = parts[0].lower()
    return entries


def check_hashes(data: dict, chapter_path: Path) -> list[str]:
    """Return a list of problems. An empty list means the hashes agree."""
    sidecar = find_sidecar(chapter_path)
    if sidecar is None:
        print(
            f"[2/7] hash check skipped: no sidecar next to {chapter_path.name} "
            f"(expected {chapter_path.name}.sha256)"
        )
        return []

    print(f"[2/7] hash check against {sidecar.name}")
    expected = paragraph_hashes(data)
    found = parse_sidecar(sidecar)
    problems: list[str] = []

    for key, digest in sorted(expected.items()):
        if key not in found:
            problems.append(f"paragraph {key} is missing from the sidecar")
        elif found[key] != digest:
            problems.append(
                f"paragraph {key} drifted: sidecar {found[key][:12]}… vs chapter {digest[:12]}…"
            )
    for key in sorted(found):
        if key not in expected:
            problems.append(
                f"sidecar lists {key}, which is not a paragraph of this chapter"
            )

    if problems:
        for problem in problems:
            print(f"  HASH    {problem}")
        return problems

    print(f"  all {len(expected)} paragraph hashes match")
    return []


# --------------------------------------------------------------------------
# Step 3: inline the chapter JSON
# --------------------------------------------------------------------------


def inline_chapter_json(data: dict) -> str:
    """Serialise the chapter so it cannot break out of the script block.

    `</` is escaped so the closing tag can never appear. `<!--` and
    `<script` are escaped as well: they would otherwise put the HTML
    parser into a script-escaped state, where a later `</script` in the
    data stops closing the element. Both escapes are valid JSON escapes,
    so the parsed value is unchanged.
    """
    raw = json.dumps(data, ensure_ascii=False, separators=(",", ":"))
    raw = raw.replace("</", "<\\/")
    raw = raw.replace("<!--", "<\\u0021--")
    raw = raw.replace("<script", "<\\u0073cript")
    return raw


# --------------------------------------------------------------------------
# Step 5: the external reference scan
# --------------------------------------------------------------------------

# The rule of the scan:
#
#   A URL inside visible prose is text. A text node is never fetched, so
#   text nodes are not inspected. Anything the page would actually load
#   is inspected: an element attribute that names a resource, and every
#   CSS url() and @import.
#
#   The scan therefore fails on a URL that the page loads and ignores a
#   URL that the page only prints. That is why a paragraph may teach the
#   phrase "https://example.com" without breaking the build.

BANNED_ELEMENTS = {
    "iframe",
    "frame",
    "frameset",
    "object",
    "embed",
    "applet",
    "base",
    "portal",
}

# Attributes whose value names a resource the browser would fetch.
LOADING_ATTRIBUTES = {
    "src",
    "srcset",
    "imagesrcset",
    "poster",
    "data",
    "background",
    "manifest",
    "code",
    "archive",
    "codebase",
    "profile",
    "longdesc",
    "ping",
    "action",
    "formaction",
    "xlink:href",
}

# Schemes that reach the network, plus the ones that execute code.
NETWORK_SCHEMES = {"http", "https", "ftp", "ftps", "ws", "wss", "file", "gopher"}

CSS_COMMENT_RE = re.compile(r"/\*.*?\*/", re.DOTALL)
CSS_URL_RE = re.compile(
    r"url\(\s*(?:\"([^\"]*)\"|'([^']*)'|([^)\s]*))\s*\)", re.IGNORECASE
)
CSS_IMPORT_RE = re.compile(r"@import\b", re.IGNORECASE)
CSS_ANY_URL_RE = re.compile(r"https?://|//cdn", re.IGNORECASE)
SCHEME_RE = re.compile(r"^([a-zA-Z][a-zA-Z0-9+.\-]*):")
URL_STRIP_RE = re.compile(r"[\s\x00-\x20]")


def _strip_url(value: str) -> str:
    """Browsers ignore whitespace and control characters inside a URL."""
    return URL_STRIP_RE.sub("", value or "")


class ExternalReferenceScanner(HTMLParser):
    """Find everything the built page would load from outside itself."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.findings: list[str] = []
        self._in_style = False
        self._style_chunks: list[str] = []

    # -- helpers -------------------------------------------------------
    def _fail(self, where: str, message: str) -> None:
        self.findings.append(f"{where}: {message}")

    def _check_url(self, where: str, attr: str, raw: str) -> None:
        value = _strip_url(raw)
        if not value:
            return
        if value.startswith("#"):
            # A fragment points inside the same document. Nothing is loaded.
            return
        if value.startswith("//"):
            self._fail(where, f'{attr}="{raw}" loads a protocol-relative resource')
            return
        match = SCHEME_RE.match(value)
        if match:
            scheme = match.group(1).lower()
            if scheme in ("mailto", "tel"):
                return
            if scheme == "data":
                if value.lower().startswith("data:image/") and attr in (
                    "src",
                    "poster",
                    "xlink:href",
                    "srcset",
                    "imagesrcset",
                ):
                    return
                self._fail(where, f'{attr}="{raw}" loads an inline data document')
                return
            if scheme in NETWORK_SCHEMES:
                self._fail(where, f'{attr}="{raw}" loads a network resource')
                return
            self._fail(where, f'{attr}="{raw}" uses the unsupported scheme "{scheme}"')
            return
        # A relative path: the studio is one file, so this would pull in a sibling.
        self._fail(where, f'{attr}="{raw}" loads a sibling file')

    def _check_css(self, css: str, where: str) -> None:
        stripped = CSS_COMMENT_RE.sub(" ", css)
        if CSS_IMPORT_RE.search(stripped):
            self._fail(where, "the stylesheet uses @import")
        for match in CSS_URL_RE.finditer(stripped):
            target = match.group(1) or match.group(2) or match.group(3) or ""
            target = _strip_url(target)
            if not target:
                continue
            if target.startswith("#"):
                continue  # a local reference, for example an SVG marker
            if target.lower().startswith("data:image/"):
                continue  # an inline image
            self._fail(where, f"the stylesheet loads {target!r} through url()")
        if CSS_ANY_URL_RE.search(stripped):
            self._fail(where, "the stylesheet contains an external reference")

    # -- parser hooks --------------------------------------------------
    def handle_starttag(self, tag: str, attrs) -> None:
        tag = tag.lower()
        if tag in BANNED_ELEMENTS:
            self._fail(f"<{tag}>", f"the <{tag}> element can load an external document")
        if tag == "meta":
            for name, value in attrs:
                if (name or "").lower() == "http-equiv" and (
                    value or ""
                ).lower() == "refresh":
                    self._fail(
                        "<meta http-equiv=refresh>", "a meta refresh navigates the page"
                    )
        if tag == "style":
            self._in_style = True
            self._style_chunks = []

        for name, value in attrs:
            name = (name or "").lower()
            value = value or ""
            if name == "href":
                if tag == "a":
                    # A link the reader may click is still a way out of the file.
                    self._check_url(f"<a href>", "href", value)
                elif tag == "link":
                    self._fail(
                        f"<link href>", "a link element can load a stylesheet or a font"
                    )
                else:
                    self._check_url(f"<{tag} href>", "href", value)
            elif name in ("srcset", "imagesrcset"):
                for candidate in value.split(","):
                    if candidate.strip():
                        self._check_url(f"<{tag} {name}>", name, candidate.strip())
            elif name in LOADING_ATTRIBUTES:
                self._check_url(f"<{tag} {name}>", name, value)

    def handle_data(self, data: str) -> None:
        if self._in_style:
            self._style_chunks.append(data)

    def handle_endtag(self, tag: str) -> None:
        if tag.lower() == "style" and self._in_style:
            self._in_style = False
            self._check_css("".join(self._style_chunks), "<style>")
            self._style_chunks = []


def scan_for_external_references(html: str) -> list[str]:
    """Return every external reference the page would load."""
    scanner = ExternalReferenceScanner()
    scanner.feed(html)
    scanner.close()
    if scanner._in_style:
        scanner._check_css("".join(scanner._style_chunks), "<style>")
    return scanner.findings


# --------------------------------------------------------------------------
# Step 7: optional headless self-test
# --------------------------------------------------------------------------

CHROME_CANDIDATES = [
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
    "/usr/bin/google-chrome",
    "/usr/bin/chromium",
    "/usr/bin/chromium-browser",
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
]


def find_chrome() -> str | None:
    for candidate in CHROME_CANDIDATES:
        if Path(candidate).is_file():
            return candidate
    for name in ("chrome", "google-chrome", "chromium", "chromium-browser"):
        found = shutil.which(name)
        if found:
            return found
    return None


def run_headless_selftest(html_path: Path) -> tuple[bool, str]:
    """Open the built file with ?selftest=1 and read the result."""
    chrome = find_chrome()
    if not chrome:
        return False, "no Chrome binary was found"

    url = html_path.resolve().as_uri() + "?selftest=1"
    command = [
        chrome,
        "--headless=new",
        "--disable-gpu",
        "--no-sandbox",
        "--virtual-time-budget=10000",
        "--dump-dom",
        url,
    ]
    try:
        completed = subprocess.run(
            command, capture_output=True, text=True, timeout=120, check=False
        )
    except (OSError, subprocess.SubprocessError) as exc:
        return False, f"the headless browser failed: {exc}"

    dom = completed.stdout or ""
    if "selftest-output" not in dom:
        return False, "the headless browser did not render the self-test output"

    match = re.search(r"SELFTEST\s+(\d+)\s+passed\s+(\d+)\s+failed", dom)
    if not match:
        return False, "the self-test output carried no summary line"
    passed, failed = int(match.group(1)), int(match.group(2))
    if failed:
        return False, f"the self-test reported {failed} failure(s)"
    return True, f"the self-test reported {passed} passed and {failed} failed"


# --------------------------------------------------------------------------
# The build
# --------------------------------------------------------------------------


def build(chapter_path: Path, out_dir: Path, run_selftest: bool) -> int:
    print(f"study-studio build: chapter {chapter_path}")
    print(f"                    engine  {ROOT / 'engine'}")

    if not chapter_path.is_file():
        print(f"[FAIL] the chapter file does not exist: {chapter_path}")
        return 1
    for required in (TEMPLATE_PATH, CSS_PATH, JS_PATH):
        if not required.is_file():
            print(f"[FAIL] the engine file does not exist: {required}")
            return 1

    # 1. validate
    try:
        data = json.loads(chapter_path.read_text(encoding="utf-8-sig"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"[FAIL] the chapter file could not be read or parsed: {exc}")
        return 1

    report = validate_chapter.validate(data)
    if report.errors:
        print(f"[1/7] contract check FAILED with {len(report.errors)} error(s)")
        for finding in report.errors:
            print(f"  ERROR   {finding.code}  {finding.location}: {finding.message}")
        return 1
    print(f"[1/7] contract check passed ({report.checks} top-level checks)")
    for finding in report.warnings:
        print(f"  WARN    {finding.code}  {finding.location}: {finding.message}")

    # 2. hashes
    hash_problems = check_hashes(data, chapter_path)
    if hash_problems:
        print("[FAIL] the chapter text drifted from the recorded hashes")
        return 1

    chapter_id = data.get("meta", {}).get("chapterId", "chapter")

    # 3 and 4. inline
    template = TEMPLATE_PATH.read_text(encoding="utf-8")
    css = CSS_PATH.read_text(encoding="utf-8")
    js = JS_PATH.read_text(encoding="utf-8")

    for placeholder in (
        PLACEHOLDER_CSS,
        PLACEHOLDER_JS,
        PLACEHOLDER_DATA,
        PLACEHOLDER_PHASE,
    ):
        if placeholder not in template:
            print(f"[FAIL] the template is missing the placeholder {placeholder}")
            return 1

    html = template.replace(PLACEHOLDER_CSS, css)
    html = html.replace(PLACEHOLDER_JS, js)
    html = html.replace(PLACEHOLDER_DATA, inline_chapter_json(data))
    html = html.replace(PLACEHOLDER_PHASE, STUDIO_PHASE)
    print(f"[3/7] inlined the chapter JSON ({len(data.get('sections', []))} sections)")
    print(
        f"[4/7] inlined {len(css.splitlines())} lines of CSS and {len(js.splitlines())} lines of JS"
    )

    # 5. external reference scan
    findings = scan_for_external_references(html)
    if findings:
        print(f"[FAIL] the built file would load {len(findings)} external resource(s)")
        for finding in findings:
            print(f"  EXTERNAL  {finding}")
        return 1
    print("[5/7] external reference scan: 0 external references")

    # 6. write
    out_dir.mkdir(parents=True, exist_ok=True)
    output_path = out_dir / f"{chapter_id}.html"
    output_path.write_text(html, encoding="utf-8", newline="\n")
    size = output_path.stat().st_size
    print(f"[6/7] wrote {output_path} ({size:,} bytes, phase {STUDIO_PHASE})")

    # 7. optional self-test
    if run_selftest:
        ok, message = run_headless_selftest(output_path)
        print(f"[7/7] headless self-test: {message}")
        if not ok:
            return 1
    else:
        print("[7/7] headless self-test skipped (run with --selftest)")

    print(f"done: {output_path}")
    return 0


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="Build an offline Study Studio file.")
    parser.add_argument(
        "--chapter",
        default=str(DEFAULT_CHAPTER),
        help="the chapter JSON to build (default: schema/example-chapter.json)",
    )
    parser.add_argument(
        "--out",
        default=str(DEFAULT_OUT),
        help="the directory to write the HTML into (default: build/)",
    )
    parser.add_argument(
        "--selftest",
        action="store_true",
        help="run the in-page self-test in a headless browser after the build",
    )
    args = parser.parse_args(argv[1:])
    return build(Path(args.chapter).resolve(), Path(args.out).resolve(), args.selftest)


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
