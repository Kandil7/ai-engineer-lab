"""
Exercise 01: Islamic-Domain Literacy and Corpus Governance
==========================================================
Audit a corpus manifest the way a release reviewer would: run the ten GOV
rules from Lecture 01 against sources, passages, citations, and the system's
refusal/audit configuration, and flag missing licence decisions, missing
checksums, redistribution violations, category and grade gaps, broken
isnad-matn linkage, under-specified citations, an unconfigured refusal path,
an incomplete audit log, and invalid ayah coordinates.

The demo runs the rules against two built-in manifests: a BAD manifest that
trips every rule, and a GOOD manifest that must raise zero findings. It then
exercises the two governance mechanics the lecture teaches — the refusal
template render and deterministic checksums — all against seeded, offline
fixtures. No network.

Grades in the sample passages are inherited metadata attributed to a named
grader (here: the source edition's own grading apparatus). The tool reports
what the sources say; it never issues a verdict of its own.

Prerequisites:
    Python 3.11+ standard library only. No third-party packages.

Usage:
    python exercises/01-islamic-domain-governance.py
    python exercises/01-islamic-domain-governance.py path/to/manifest.json
"""

from __future__ import annotations

import hashlib
import json
import sys
from dataclasses import dataclass, field
from pathlib import Path

_SOURCE_TEXT = Path(__file__).read_text(encoding="utf-8")

# ---------------------------------------------------------------------------
# 1. Models
# ---------------------------------------------------------------------------


@dataclass
class Finding:
    """One rule violation in one corpus manifest."""

    severity: str
    code: str
    line: int
    message: str


@dataclass
class Analysis:
    """All findings for one corpus manifest."""

    source: str
    findings: list[Finding] = field(default_factory=list)

    @property
    def critical_count(self) -> int:
        return sum(1 for f in self.findings if f.severity == "critical")

    @property
    def warning_count(self) -> int:
        return sum(1 for f in self.findings if f.severity == "warning")


@dataclass(frozen=True)
class Citation:
    """Where a scholar would check the passage: work plus coordinates."""

    work: str | None = None
    volume: int | None = None
    page: int | None = None
    locator: str | None = None  # hadith number, edition stamp, entry id
    surah: int | None = None
    ayah: int | None = None

    def has_coordinates(self) -> bool:
        """Book plus volume/page, or an equivalent locator, or surah:ayah."""
        if self.volume and self.page:
            return True
        return bool(self.locator) or bool(self.surah and self.ayah)


@dataclass(frozen=True)
class SourceRecord:
    """One provenance record: where the artifact came from and under what terms."""

    source_id: str
    origin: str
    licence_decision: str | None  # None = never decided (GOV001)
    terms_of_use: str
    retrieved_at: str
    checksum: str | None  # None = artifact not pinned (GOV002)
    use_policy: str  # "redistribution-ok" | "no-redistribution" | ...


@dataclass(frozen=True)
class Passage:
    """One retrievable chunk with category, inherited grade, and linkage."""

    chunk_id: str
    source_id: str
    text: str
    category: str | None
    grade: dict | None  # inherited: {"value", "grader", "note"} — never ours
    isnad_present: bool
    isnad_link: str | None  # chunk id of the paired isnad chunk, if split
    citation: Citation | None
    served_verbatim: bool


@dataclass(frozen=True)
class GovernanceConfig:
    """The system-side refusal path and audit-log contract."""

    refusal: dict  # {"template": str|None, "handoff": str|None}
    audit_log: dict  # {"records_chunk_ids", "records_model_version", "retention_days"}


# The category vocabulary the pipeline must tag with (lecture section 2).
CATEGORIES = frozenset(
    {
        "quran",
        "hadith",
        "athar",
        "tafsir",
        "fiqh",
        "fatwa",
        "qawaid",
        "usul",
        "shawahid",
        "taqrid",
    }
)

# Well-known ayah counts for the surahs used in samples; range-checked for
# the rest. A citation outside the count is a coordinate error, not a
# textual dispute (GOV010).
AYAH_COUNTS: dict[int, int] = {
    1: 7,
    2: 286,
    103: 3,
    112: 4,
    113: 5,
    114: 6,
}


# ---------------------------------------------------------------------------
# 2. Manifest access and marker-based line resolution
# ---------------------------------------------------------------------------


def _declared_line(label: str, marker: str) -> int:
    """Resolve a finding's line by scanning this file for '# LABEL:marker'."""
    needle = f"# {label}:{marker}"
    for number, line in enumerate(_SOURCE_TEXT.splitlines(), start=1):
        if needle in line:
            return number
    return 0


def _line_for(label: str, code: str, entity: str) -> int:
    """Marker key '<code-lower>.<entity-id>' places findings on the offender."""
    return _declared_line(label, f"{code.lower()}.{entity}")


def _parse_citation(raw: object) -> Citation | None:
    if isinstance(raw, dict):
        return Citation(**raw)
    return None


def _parse_passage(raw: dict) -> Passage:
    data = dict(raw)
    data["citation"] = _parse_citation(data.get("citation"))
    return Passage(**data)


def _parse_manifest(
    pack: dict,
) -> tuple[list[SourceRecord], list[Passage], GovernanceConfig]:
    sources = [SourceRecord(**s) for s in pack.get("sources", [])]
    passages = [_parse_passage(p) for p in pack.get("passages", [])]
    config = GovernanceConfig(**pack.get("config", {}))
    return sources, passages, config


# ---------------------------------------------------------------------------
# 3. Rules (GOV001 - GOV010)
# ---------------------------------------------------------------------------


def check_source_licence(
    sources: list[SourceRecord], label: str, findings: list[Finding]
) -> None:
    """GOV001: a source with no recorded licence decision cannot be used defensibly."""
    for src in sources:
        if (src.licence_decision or "").strip():
            continue
        findings.append(
            Finding(
                severity="critical",
                code="GOV001",
                line=_line_for(label, "GOV001", src.source_id),
                message=(
                    f"Source '{src.source_id}' has no recorded licence decision. "
                    "Record how the licence and terms of use actually read before any "
                    "passage from this source enters the corpus; 'the text is ancient' "
                    "is not a licence decision."
                ),
            )
        )


def check_source_checksum(
    sources: list[SourceRecord], label: str, findings: list[Finding]
) -> None:
    """GOV002: an unpinned artifact cannot support a reproducible research claim."""
    for src in sources:
        if (src.checksum or "").strip():
            continue
        findings.append(
            Finding(
                severity="warning",
                code="GOV002",
                line=_line_for(label, "GOV002", src.source_id),
                message=(
                    f"Source '{src.source_id}' has no checksum of the retrieved artifact. "
                    "Online corpora change; without the checksum a citation that resolved "
                    "last year cannot be defended and the research claim is not reproducible."
                ),
            )
        )


def check_redistribution(
    sources: list[SourceRecord],
    passages: list[Passage],
    label: str,
    findings: list[Finding],
) -> None:
    """GOV003: verbatim serving from a no-redistribution source is republication."""
    by_id = {s.source_id: s for s in sources}
    for p in passages:
        src = by_id.get(p.source_id)
        if src is None or not p.served_verbatim:
            continue
        if "no-redistribution" not in src.use_policy:
            continue
        findings.append(
            Finding(
                severity="critical",
                code="GOV003",
                line=_line_for(label, "GOV003", p.chunk_id),
                message=(
                    f"Chunk '{p.chunk_id}' is served verbatim from source '{src.source_id}', "
                    "whose use policy forbids redistribution. A RAG answer that returns the "
                    "verbatim passage is publishing it; summarize, link, or drop the chunk."
                ),
            )
        )


def check_category_tag(
    passages: list[Passage], label: str, findings: list[Finding]
) -> None:
    """GOV004: an untagged passage invites category conflation at answer time."""
    for p in passages:
        if p.category in CATEGORIES:
            continue
        shown = p.category if p.category else "missing"
        findings.append(
            Finding(
                severity="critical",
                code="GOV004",
                line=_line_for(label, "GOV004", p.chunk_id),
                message=(
                    f"Chunk '{p.chunk_id}' has category '{shown}'. Every passage must carry "
                    f"one of {sorted(CATEGORIES)}; serving an ayah, a report, and a scholar's "
                    "gloss under one retrieval pool is a category error with religious consequence."
                ),
            )
        )


def check_inherited_grade(
    passages: list[Passage], label: str, findings: list[Finding]
) -> None:
    """GOV005: a hadith passage must carry its inherited grade as data."""
    for p in passages:
        if p.category != "hadith" or p.grade:
            continue
        findings.append(
            Finding(
                severity="critical",
                code="GOV005",
                line=_line_for(label, "GOV005", p.chunk_id),
                message=(
                    f"Chunk '{p.chunk_id}' is tagged 'hadith' but carries no inherited grade "
                    "field. The grade travels with the passage as source-attributed metadata "
                    "(value plus grader); the system never grades on its own and never serves "
                    "a graded report as if ungraded."
                ),
            )
        )


def check_isnad_linkage(
    passages: list[Passage], label: str, findings: list[Finding]
) -> None:
    """GOV006: a matn split from its isnad must link back to the isnad chunk."""
    for p in passages:
        if p.category not in {"hadith", "athar"}:
            continue
        if p.isnad_present or p.isnad_link:
            continue
        findings.append(
            Finding(
                severity="critical",
                code="GOV006",
                line=_line_for(label, "GOV006", p.chunk_id),
                message=(
                    f"Chunk '{p.chunk_id}' is a report text without its isnad and without an "
                    "isnad_link to the chunk that holds one. Chunking may split matn from "
                    "isnad, but the linkage must survive; an orphaned matn hides who narrated "
                    "what from whom."
                ),
            )
        )


def check_citation_coordinates(
    passages: list[Passage], label: str, findings: list[Finding]
) -> None:
    """GOV007: a citation without coordinates is not checkable by a scholar."""
    for p in passages:
        c = p.citation
        if c is not None and (c.work or "").strip() and c.has_coordinates():
            continue
        findings.append(
            Finding(
                severity="warning",
                code="GOV007",
                line=_line_for(label, "GOV007", p.chunk_id),
                message=(
                    f"Chunk '{p.chunk_id}' lacks the citation coordinates a scholar would "
                    "check: book plus volume/page, or an equivalent locator (hadith number, "
                    "entry id), or surah:ayah. Naming the book alone does not let anyone "
                    "verify the passage."
                ),
            )
        )


def check_refusal_path(
    config: GovernanceConfig, label: str, findings: list[Finding]
) -> None:
    """GOV008: fatwa-shaped questions need a configured refusal and a handoff."""
    template = str(config.refusal.get("template") or "").strip()
    handoff = str(config.refusal.get("handoff") or "").strip()
    if template and handoff:
        return
    findings.append(
        Finding(
            severity="critical",
            code="GOV008",
            line=_declared_line(label, "gov008"),
            message=(
                "Refusal path is not configured (template and handoff target are both "
                "required). Questions that are fatwas in substance must be met with a "
                "designed refusal that states the boundary, cites what the corpus can, and "
                "hands off to a named trustworthy source or scholar — not a blank error."
            ),
        )
    )


def check_audit_log(
    config: GovernanceConfig, label: str, findings: list[Finding]
) -> None:
    """GOV009: a defensible Q&A log records chunk ids and the model version."""
    log = config.audit_log
    if log.get("records_chunk_ids") and log.get("records_model_version"):
        return
    findings.append(
        Finding(
            severity="warning",
            code="GOV009",
            line=_declared_line(label, "gov009"),
            message=(
                "Audit log omits retrieved chunk ids or the model version. A defensible "
                "Q&A log records the question, the chunk ids retrieved, the model version, "
                "the refusal flag, and user feedback — under a stated retention limit."
            ),
        )
    )


def _ayah_valid(surah: int, ayah: int) -> bool:
    if not (1 <= surah <= 114) or ayah < 1:
        return False
    known = AYAH_COUNTS.get(surah)
    return known is None or ayah <= known


def check_ayah_coordinates(
    passages: list[Passage], label: str, findings: list[Finding]
) -> None:
    """GOV010: a quran passage must carry a valid surah:ayah citation."""
    for p in passages:
        if p.category != "quran":
            continue
        c = p.citation
        if (
            c is not None
            and c.surah is not None
            and c.ayah is not None
            and _ayah_valid(c.surah, c.ayah)
        ):
            continue
        got = "no citation" if c is None else f"surah={c.surah} ayah={c.ayah}"
        findings.append(
            Finding(
                severity="critical",
                code="GOV010",
                line=_line_for(label, "GOV010", p.chunk_id),
                message=(
                    f"Chunk '{p.chunk_id}' is tagged 'quran' but its ayah citation fails "
                    f"validation ({got}). Surah must be 1..114 and the ayah must fall inside "
                    "the surah's known ayah count; a wrong coordinate misplaces a revelation."
                ),
            )
        )


# ---------------------------------------------------------------------------
# 4. Analysis entry point
# ---------------------------------------------------------------------------


def analyze_manifest(pack: dict, label: str) -> Analysis:
    """Run every GOV rule against one corpus manifest."""
    corpus = pack.get("corpus")
    source = f"{label} manifest ({corpus})" if corpus else f"{label} manifest"
    analysis = Analysis(source=source)

    sources, passages, config = _parse_manifest(pack)

    check_source_licence(sources, label, analysis.findings)
    check_source_checksum(sources, label, analysis.findings)
    check_redistribution(sources, passages, label, analysis.findings)
    check_category_tag(passages, label, analysis.findings)
    check_inherited_grade(passages, label, analysis.findings)
    check_isnad_linkage(passages, label, analysis.findings)
    check_citation_coordinates(passages, label, analysis.findings)
    check_refusal_path(config, label, analysis.findings)
    check_audit_log(config, label, analysis.findings)
    check_ayah_coordinates(passages, label, analysis.findings)

    analysis.findings.sort(key=lambda f: (f.code, f.line))
    return analysis


def render(analysis: Analysis) -> str:
    """Format one analysis for the terminal."""
    lines = [f"Corpus manifest: {analysis.source}"]
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
# 5. Sample corpus manifests used for the demo
# ---------------------------------------------------------------------------

_ISNAD = "عَنْ عُمَرَ بْنِ الْخَطَّابِ رضي الله عنه، قَالَ: سَمِعْتُ رَسُولَ اللَّهِ صلى الله عليه وسلم يَقُولُ:"
_MATN = (
    "«إِنَّمَا الْأَعْمَالُ بِالنِّيَّاتِ، وَإِنَّمَا لِكُلِّ امْرِئٍ مَا نَوَى، "
    "فَمَنْ كَانَتْ هِجْرَتُهُ إِلَى اللَّهِ وَرَسُولِهِ فَهِجْرَتُهُ إِلَى اللَّهِ "
    "وَرَسُولِهِ»"
)
_AYAH_2_255 = (
    "اللَّهُ لَا إِلَٰهَ إِلَّا هُوَ الْحَيُّ الْقَيُّومُ ۚ لَا تَأْخُذُهُ سِنَةٌ "
    "وَلَا نَوْمٌ ۚ لَهُ مَا فِي السَّمَاوَاتِ وَمَا فِي الْأَرْضِ"
)
_TAFSIR_META = (
    "مِنْ تَفْسِيرِ (اسمُ التِّفْسِيرِ كما هو مثبت في صفحة العنوان)، (المجلد ١، "
    "الصفحة ٤٥) في شرحِ سورةِ الإخلاص: ﴿قُلْ هُوَ اللَّهُ أَحَدٌ﴾ — نَصُّ الشَّرْحِ "
    "كَمَا وَرَدَ فِي الْمَصْحَفَةِ، مَنْسُوبٌ إِلَى مُصَنِّفِ التَّفْسِيرِ."
)
_FATWA_META = (
    "سُئِلَ (الْمُفْتِي كما هو مذكور في المصدر) عن مسألةٍ شخصيةٍ في (زمن ومكانِ "
    "الإجابة)، فجاء في الإجابةِ المنشورةِ: (نصُّ الإجابةِ كما وردَ في المصدرِ) — "
    "النظامُ يعرضُها مَعَ إِسْنَادِهَا مَنْسُوبًا لِصَاحِبِهَا، وَلَا يَسْتَخْلِصُ "
    "مِنْهَا حُكْمًا لِلسَّائِل."
)
_GRADE_INHERITED = {
    "value": "sahih",
    "grader": "the source edition's own grading apparatus",
    "note": "inherited metadata; the system does not re-grade",
}

PACK_BAD: dict = {
    "corpus": "athar-governance-demo",
    "sources": [
        {
            "source_id": "src-classical",
            "origin": "classical-bundle download (site mirror, 2026-03-02)",
            "licence_decision": None,  # BAD:gov001.src-classical
            "terms_of_use": "none published on the mirror",
            "retrieved_at": "2026-03-02",
            "checksum": "sha256:1f6d0c0f8a4b2e7d9c3a5b8e0d1f4a7c",
            "use_policy": "redistribution-ok",
        },
        {
            "source_id": "src-web-archive",
            "origin": "fatwa-archive API (terms v3)",
            "licence_decision": "no redistribution — terms of use forbid republication",
            "terms_of_use": "No bulk extraction; no republication of answers",
            "retrieved_at": "2026-03-05",
            "checksum": None,  # BAD:gov002.src-web-archive
            "use_policy": "no-redistribution",
        },
        {
            "source_id": "src-quran-open",
            "origin": "standard quran text, open metadata release",
            "licence_decision": "public-domain text; metadata under CC0",
            "terms_of_use": "attribution appreciated, not required",
            "retrieved_at": "2026-02-20",
            "checksum": "sha256:9c2b7e4d1a8f5c3b6d0e9a2f7c4b1d8e",
            "use_policy": "redistribution-ok",
        },
    ],
    "passages": [
        {
            "chunk_id": "bad-p-ayah",
            "source_id": "src-quran-open",
            "text": _AYAH_2_255,
            "category": "quran",
            "grade": None,
            "isnad_present": False,
            "isnad_link": None,
            "citation": {
                "work": "القرآن الكريم (المصحف القياسي)",
                "surah": 2,
                "ayah": 300,  # BAD:gov010.bad-p-ayah — surah 2 has 286 ayat
            },
            "served_verbatim": True,
        },
        {
            "chunk_id": "bad-p-fatwa",
            "source_id": "src-web-archive",
            "text": _FATWA_META,
            "category": "fatwa",
            "grade": None,
            "isnad_present": False,
            "isnad_link": None,
            "citation": {
                "work": "أرشيف الفتوى (الموقع)",
                "volume": 4,
                "page": 123,
            },
            "served_verbatim": True,  # BAD:gov003.bad-p-fatwa
        },
        {
            "chunk_id": "bad-p-untagged",
            "source_id": "src-classical",
            "text": "وَفِيهِ: أَنَّ الْمَسْأَلَةَ الَّتِي سُئِلَ عَنْهَا لَمْ تَكُنْ مَحْصُوصَةً.",
            "category": None,  # BAD:gov004.bad-p-untagged
            "grade": None,
            "isnad_present": False,
            "isnad_link": None,
            "citation": {"work": "مجمع الفوائد", "locator": "entry-17"},
            "served_verbatim": True,
        },
        {
            "chunk_id": "bad-p-hadith-nograde",
            "source_id": "src-classical",
            "text": _ISNAD + " " + _MATN,
            "category": "hadith",
            "grade": None,  # BAD:gov005.bad-p-hadith-nograde
            "isnad_present": True,
            "isnad_link": None,
            "citation": {"work": "جامع التراخيص (طبعة محققة)", "locator": "no. 4949"},
            "served_verbatim": True,
        },
        {
            "chunk_id": "bad-p-isnad",
            "source_id": "src-classical",
            "text": _ISNAD,
            "category": "hadith",
            "grade": _GRADE_INHERITED,
            "isnad_present": True,
            "isnad_link": None,
            "citation": {"work": "جامع التراخيص (طبعة محققة)", "locator": "no. 4949"},
            "served_verbatim": True,
        },
        {
            "chunk_id": "bad-p-matn",
            "source_id": "src-classical",
            "text": _MATN,
            "category": "hadith",
            "grade": _GRADE_INHERITED,
            "isnad_present": False,
            "isnad_link": None,  # BAD:gov006.bad-p-matn — split, never linked
            "citation": {"work": "جامع التراخيص (طبعة محققة)", "locator": "no. 4949"},
            "served_verbatim": True,
        },
        {
            "chunk_id": "bad-p-tafsir",
            "source_id": "src-classical",
            "text": _TAFSIR_META,
            "category": "tafsir",
            "grade": None,
            "isnad_present": False,
            "isnad_link": None,
            "citation": {
                "work": "تفسير المصحف (طبعة محققة)"
            },  # BAD:gov007.bad-p-tafsir
            "served_verbatim": True,
        },
    ],
    "config": {
        "refusal": {
            "template": None,  # BAD:gov008
            "handoff": None,
        },
        "audit_log": {
            "records_chunk_ids": False,  # BAD:gov009
            "records_model_version": False,
            "retention_days": 30,
        },
    },
}

PACK_GOOD: dict = {
    "corpus": "athar-governance-demo (compliant)",
    "sources": [
        {
            "source_id": "src-classical",
            "origin": "classical-bundle download (site mirror, 2026-03-02)",
            "licence_decision": "public-domain classical text; mirror terms allow reuse",
            "terms_of_use": "mirror permits verbatim reuse with attribution",
            "retrieved_at": "2026-03-02",
            "checksum": "sha256:1f6d0c0f8a4b2e7d9c3a5b8e0d1f4a7c",
            "use_policy": "redistribution-ok",
        },
        {
            "source_id": "src-web-archive",
            "origin": "fatwa-archive API (terms v3)",
            "licence_decision": "no redistribution — terms of use forbid republication",
            "terms_of_use": "No bulk extraction; no republication of answers",
            "retrieved_at": "2026-03-05",
            "checksum": "sha256:7e3a9c1d5b8f2a6e0c4d7b1f5a9e3c6d",
            "use_policy": "no-redistribution",
        },
        {
            "source_id": "src-quran-open",
            "origin": "standard quran text, open metadata release",
            "licence_decision": "public-domain text; metadata under CC0",
            "terms_of_use": "attribution appreciated, not required",
            "retrieved_at": "2026-02-20",
            "checksum": "sha256:9c2b7e4d1a8f5c3b6d0e9a2f7c4b1d8e",
            "use_policy": "redistribution-ok",
        },
    ],
    "passages": [
        {
            "chunk_id": "good-p-ayah",
            "source_id": "src-quran-open",
            "text": _AYAH_2_255,
            "category": "quran",
            "grade": None,
            "isnad_present": False,
            "isnad_link": None,
            "citation": {
                "work": "القرآن الكريم (المصحف القياسي)",
                "surah": 2,
                "ayah": 255,  # GOOD:gov010.good-p-ayah
            },
            "served_verbatim": True,
        },
        {
            "chunk_id": "good-p-fatwa",
            "source_id": "src-web-archive",
            "text": _FATWA_META,
            "category": "fatwa",
            "grade": None,
            "isnad_present": False,
            "isnad_link": None,
            "citation": {
                "work": "أرشيف الفتوى (الموقع)",
                "volume": 4,
                "page": 123,
            },
            "served_verbatim": False,  # GOOD:gov003.good-p-fatwa — reference only
        },
        {
            "chunk_id": "good-p-fiqh",
            "source_id": "src-classical",
            "text": "وَفِي الْكِتَابِ: تَقْسِيمُ الْأَحْكَامِ إِلَى أَصْلِيَّةٍ وَفُرُعِيَّةٍ.",
            "category": "fiqh",
            "grade": None,
            "isnad_present": False,
            "isnad_link": None,
            "citation": {
                "work": "مجمع الفوائد (طبعة محققة)",
                "volume": 1,
                "page": 42,
            },
            "served_verbatim": True,
        },
        {
            "chunk_id": "good-p-hadith",
            "source_id": "src-classical",
            "text": _ISNAD + " " + _MATN,
            "category": "hadith",
            "grade": dict(_GRADE_INHERITED),  # GOOD:gov005.good-p-hadith
            "isnad_present": True,
            "isnad_link": None,
            "citation": {"work": "جامع التراخيص (طبعة محققة)", "locator": "no. 4949"},
            "served_verbatim": True,
        },
        {
            "chunk_id": "good-p-isnad",
            "source_id": "src-classical",
            "text": _ISNAD,
            "category": "hadith",
            "grade": dict(_GRADE_INHERITED),
            "isnad_present": True,
            "isnad_link": None,
            "citation": {"work": "جامع التراخيص (طبعة محققة)", "locator": "no. 4949"},
            "served_verbatim": True,
        },
        {
            "chunk_id": "good-p-matn",
            "source_id": "src-classical",
            "text": _MATN,
            "category": "hadith",
            "grade": dict(_GRADE_INHERITED),
            "isnad_present": False,
            "isnad_link": "good-p-isnad",  # GOOD:gov006.good-p-matn — linked
            "citation": {"work": "جامع التراخيص (طبعة محققة)", "locator": "no. 4949"},
            "served_verbatim": True,
        },
        {
            "chunk_id": "good-p-tafsir",
            "source_id": "src-classical",
            "text": _TAFSIR_META,
            "category": "tafsir",
            "grade": None,
            "isnad_present": False,
            "isnad_link": None,
            "citation": {
                "work": "تفسير المصحف (طبعة محققة)",
                "volume": 1,
                "page": 45,  # GOOD:gov007.good-p-tafsir
            },
            "served_verbatim": True,
        },
    ],
    "config": {
        "refusal": {
            "template": (
                "هذا النظام يعرضُ النصوصَ مَعَ إِسْنَادِهَا ومَنَاسِبِهَا، وَلَا يُفْتِي. "
                "ما سألتَه مسألةُ إفتاءٍ شخصية؛ راجعْ مرجعًا موثوقًا أو عالِمًا مؤهَّلًا. "
                "وإليكَ ما يَسْتَطِيعُ النَّصُّ أَنْ يُؤَيِّدَهُ: (الإحالات)."
            ),
            "handoff": "named-scholar-or-fatwa-board (configured per deployment)",
        },
        "audit_log": {
            "records_chunk_ids": True,
            "records_model_version": True,
            "retention_days": 90,
        },
    },
}


# ---------------------------------------------------------------------------
# 6. Governance components
# ---------------------------------------------------------------------------


def render_refusal(template: str, question: str, citations: str) -> str:
    """Fill the refusal template: boundary, what the corpus can cite, handoff."""
    return template.replace("(الإحالات)", citations).replace("((Q))", question)


def artifact_checksum(payload: bytes) -> str:
    """Pin a retrieved artifact: sha256 is deterministic across machines."""
    return "sha256:" + hashlib.sha256(payload).hexdigest()


# ---------------------------------------------------------------------------
# 7. Demos
# ---------------------------------------------------------------------------


def _demo_refusal() -> None:
    config = GovernanceConfig(**PACK_GOOD["config"])
    template = str(config.refusal["template"])
    filled = render_refusal(
        template,
        question="Is this ruling valid for me in my situation?",
        citations="good-p-fatwa (reference, source-attributed)",
    )
    print("Refusal path: template rendered for a fatwa-shaped question")
    print(f"    boundary + citations + handoff: {config.refusal['handoff']}")
    print(f"    rendered (first 88 chars): {filled[:88]}...")
    print("    the system states the boundary, cites what it can, hands off.")


def _demo_checksum() -> None:
    payload = _ISNAD.encode("utf-8")
    first, second = artifact_checksum(payload), artifact_checksum(payload)
    print("Checksum: pinning a retrieved artifact (sha256)")
    print(f"    digest 1: {first[:31]}...")
    print(f"    digest 2: {second[:31]}...")
    print(f"    identical across runs: {first == second}")


# ---------------------------------------------------------------------------
# 8. Entry point
# ---------------------------------------------------------------------------


def main(argv: list[str]) -> int:
    # Windows legacy consoles (cp1252) cannot encode Arabic sample text;
    # write UTF-8 with replacement so the demo never dies on a print.
    reconfigure = getattr(sys.stdout, "reconfigure", None)
    if reconfigure is not None:
        reconfigure(encoding="utf-8", errors="replace")

    print("=" * 72)
    print("Exercise 01: Islamic-Domain Literacy and Corpus Governance")
    print("=" * 72)

    if len(argv) > 1:
        path = Path(argv[1])
        if not path.is_file():
            print(f"error: no such manifest file: {path}", file=sys.stderr)
            return 2
        try:
            # utf-8-sig: Windows editors save JSON with a BOM; plain utf-8 would
            # leave U+FEFF in the text and json.loads would reject it.
            pack = json.loads(path.read_text(encoding="utf-8-sig"))
        except json.JSONDecodeError as exc:
            print(f"error: {path} is not valid JSON: {exc}", file=sys.stderr)
            return 2
        analysis = analyze_manifest(pack, label="FILE")
        print(render(analysis))
        return 1 if analysis.critical_count else 0

    bad = analyze_manifest(PACK_BAD, label="BAD")
    good = analyze_manifest(PACK_GOOD, label="GOOD")
    print(render(bad))
    print()
    print(render(good))
    print("-" * 72)

    _demo_refusal()
    print()
    _demo_checksum()
    print("-" * 72)
    print(
        f"Demo result: BAD manifest raised {bad.critical_count} critical and "
        f"{bad.warning_count} warning findings; GOOD manifest raised "
        f"{good.critical_count} critical and {good.warning_count} warning findings."
    )
    print("No network access, no wall-clock dependence: reruns are identical.")

    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
