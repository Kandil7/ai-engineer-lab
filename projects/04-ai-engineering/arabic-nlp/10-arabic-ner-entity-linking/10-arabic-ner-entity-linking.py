"""
Arabic NLP — 10: Arabic NER and Entity Linking
==============================================
Topics: entity detection over clitic-fused Arabic text, gazetteer baselines
measured before model claims, clitic-aware span reconstruction, candidate
blocking and scored linking into a canonical ID space (topic 08's canon),
entity-level evaluation, Quran references as structured data, and a config
audit that emits NER001-NER008 findings for misconfiguration.

Why this matters:
    Detection finds the span; linking resolves it to a stable entity ID.
    Arabic makes detection hard (clitics, no capitalization, ambiguous
    common-word names) and linking harder (surface variation, nested
    titles, unseen names). A pipeline that skips the gazetteer baseline,
    links every span by force, or mints its own IDs instead of using the
    canon breaks the downstream knowledge base in ways retrieval metrics
    never show. This exercise ships the tools the lecture measures with:
    a normalization-aware detector, a scored linker with AUTO/REVIEW/
    ABSTAIN bands, an entity-level evaluator, and a config auditor whose
    GOOD pack must score ZERO findings while the BAD pack surfaces all
    eight planted pathologies (NER001-NER008).

Run:      python 10-arabic-ner-entity-linking.py
          python 10-arabic-ner-entity-linking.py corpus.json
"""

from __future__ import annotations

import json
import re
import sys
import unicodedata
from dataclasses import dataclass, replace
from pathlib import Path

_reconf = getattr(sys.stdout, "reconfigure", None)
if _reconf is not None:
    _reconf(encoding="utf-8")

NORMALIZER_VERSION = "ar-ner-norm-1.0"
LINKER_VERSION = "ar-ner-link-1.0"

# ----------------------------------------------------------------------------
# 1. Data models
# ----------------------------------------------------------------------------


@dataclass(frozen=True)
class Span:
    """One detected or gold character span. Offsets are 1-based-free
    Python indices into the RAW (verbatim) text, half-open [start, end).
    `etype` is the entity type: "Person" | "Book" | "QuranVerse" |
    "Madhhab". Invariants: start < end, both within the source text."""

    start: int
    end: int
    etype: str

    def key(self) -> tuple[int, int, str]:
        return (self.start, self.end, self.etype)


@dataclass(frozen=True)
class EntityMention:
    """One detected mention: the raw span plus the observed surface and its
    working-copy (normalized) form. The raw text is never rewritten — the
    two-text discipline from Athar and topics 02/09."""

    span: Span
    text: str
    norm: str


@dataclass(frozen=True)
class GazetteerEntry:
    """One canonical entity in the knowledge base. Forms are stored
    NORMALIZED (the working copy of each observed surface). `ambiguous`
    marks entries whose single-token forms double as common words
    (e.g., مالك = "owner" and the narrator Malik); such entries match only
    when the preceding token is one of `common_cues`."""

    entity_id: str
    etype: str
    forms: tuple[str, ...]
    ambiguous: bool = False
    common_cues: tuple[str, ...] = ()


@dataclass(frozen=True)
class LinkDecision:
    """One linking outcome. band: "auto" (score >= auto_threshold),
    "review" (human band), "abstain" (below floor, left unlinked), or
    "forced" (abstention disabled — a governance defect, NER008)."""

    mention: EntityMention
    entity_id: str | None
    score: float
    band: str
    reason: str


@dataclass(frozen=True)
class Finding:
    """One pipeline misconfiguration. severity: "error" (identity or
    reference integrity broken) or "warning" (silent quality loss or a
    governance gap). code: NER001..NER008. line: 1-based line in the
    config listing where the misconfiguration is declared."""

    severity: str
    code: str
    message: str
    line: int


@dataclass(frozen=True)
class NerPipelineConfig:
    """The auditable pipeline configuration. Every BAD-pack pathology is a
    field here; the GOOD pack sets each field to its governed value."""

    name: str
    metric: str  # "entity" | "token"
    model_claim: str  # free-text claim of a model F1, or ""
    baseline_measured: bool
    auto_threshold: float
    threshold_study: bool
    allow_abstain: bool
    id_source: str  # "canon" | "mint"
    quran_mode: str  # "reference-parse" | "free-text"
    clitic_repair: bool
    gazetteer_guard: bool


@dataclass(frozen=True)
class EvalReport:
    """Entity-level (exact span+type) and token-level metrics in one
    record, so the audit can cite the gap between them (NER003)."""

    tp: int
    fp: int
    fn: int
    precision: float
    recall: float
    f1: float
    token_precision: float
    token_recall: float
    token_f1: float


@dataclass(frozen=True)
class RunStats:
    """What one pipeline run observed. `report` is the entity/token eval;
    `forced_links` counts abstentions overridden (NER008);
    `clitic_dependent` counts gold spans detectable only with clitic
    repair on (NER006); `guard_fp` counts false positives attributable
    to the disabled ambiguity guard (NER007)."""

    report: EvalReport
    forced_links: int
    clitic_dependent: int
    guard_fp: int


@dataclass(frozen=True)
class HeldOutDoc:
    """One held-out document with gold spans (raw offsets, half-open).
    Gold is the annotation the detector is measured against; it is never
    derived from the detector itself."""

    doc_id: str
    text: str
    gold: tuple[Span, ...]


# ----------------------------------------------------------------------------
# 2. Working-copy normalization (display-preserving, offset-mapped)
# ----------------------------------------------------------------------------

_ALEF_MAP = {"أ": "ا", "إ": "ا", "آ": "ا", "ٱ": "ا"}
_YEH_MAP = {"ى": "ي"}
_ARABIC_INDIC = {chr(0x0660 + i): str(i) for i in range(10)}
_EXTENDED_INDIC = {chr(0x06F0 + i): str(i) for i in range(10)}
_DIGIT_MAP = {**_ARABIC_INDIC, **_EXTENDED_INDIC}
_TATWEEL = "ـ"

_PUNCT = "،؛.:؟!«»\"'()[]{}-–—,;:"


def _fold_char(ch: str) -> str:
    if ch == _TATWEEL:
        return ""
    if ch in _ALEF_MAP:
        return _ALEF_MAP[ch]
    if ch in _YEH_MAP:
        return _YEH_MAP[ch]
    if ch in _DIGIT_MAP:
        return _DIGIT_MAP[ch]
    return ch


def normalize_with_map(raw: str) -> tuple[str, list[int]]:
    """Working copy of `raw` plus a per-character map back to raw offsets.

    Rules (working copy only; `raw` is never mutated): NFD, strip Mn
    (tashkeel), NFC, fold alef variants and alef maqsura, fold
    Arabic-Indic digits to ASCII, drop tatweel, casefold Latin, collapse
    whitespace runs. map[i] is the raw index of normalized character i,
    so every working-copy match converts back to a display-faithful raw
    span. The normalizer is stamped with NORMALIZER_VERSION."""
    parts: list[str] = []
    offsets: list[int] = []
    prev_space = True
    for i, ch in enumerate(raw):
        expanded = unicodedata.normalize("NFD", ch)
        kept = "".join(c for c in expanded if unicodedata.category(c) != "Mn")
        recomposed = unicodedata.normalize("NFC", kept)
        folded = "".join(_fold_char(c) for c in recomposed).casefold()
        if not folded:
            continue
        if folded.isspace():
            if prev_space:
                continue
            parts.append(" ")
            offsets.append(i)
            prev_space = True
            continue
        prev_space = False
        for c in folded:
            parts.append(c)
            offsets.append(i)
    while parts and parts[-1] == " ":
        parts.pop()
        offsets.pop()
    while parts and parts[0] == " ":
        parts.pop(0)
        offsets.pop(0)
    return "".join(parts), offsets


def normalize_ar(text: str) -> str:
    """Convenience wrapper: the working copy without the offset map."""
    return normalize_with_map(text)[0]


@dataclass(frozen=True)
class NormToken:
    """One whitespace token of the working copy, punctuation stripped from
    the edges. core is the matching form; start/end are core offsets into
    the working copy (not the raw text)."""

    core: str
    start: int
    end: int


def tokenize_working(norm_text: str) -> list[NormToken]:
    """Whitespace tokens of the working copy with edge punctuation stripped
    so حنبل، still participates in the window حنبل بن أحمد."""
    tokens: list[NormToken] = []
    i = 0
    n = len(norm_text)
    while i < n:
        while i < n and norm_text[i] == " ":
            i += 1
        if i >= n:
            break
        j = i
        while j < n and norm_text[j] != " ":
            j += 1
        core_start, core_end = i, j
        while core_start < core_end and norm_text[core_start] in _PUNCT:
            core_start += 1
        while core_end > core_start and norm_text[core_end - 1] in _PUNCT:
            core_end -= 1
        if core_start < core_end:
            tokens.append(
                NormToken(norm_text[core_start:core_end], core_start, core_end)
            )
        i = j
    return tokens


# ----------------------------------------------------------------------------
# 3. Gazetteer, clitic repair, and detection
# ----------------------------------------------------------------------------

# Proclitics stripped from a window's first token, longest first. The
# remaining join must match a gazetteer form exactly — the gazetteer IS the
# guard against over-stripping (والده -> هده never matches anything).
_PREFIXES = ("بال", "كال", "فال", "لل", "ال", "و", "ف", "ب", "ك", "ل")
# Enclitics stripped from a window's last token, longest first.
_SUFFIXES = ("ها", "هم", "هن", "كم", "نا", "هما", "ه", "ي", "ك")
# Shortest acceptable remainder after a strip. 2, not 3: the nasab particle
# ابن itself is only 2 characters, and لابن تيمية must reach it.
MIN_REST = 2
# Title tokens that extend a match outward into a nested outer span
# (الشافعي -> الإمام الشافعي). Normalized forms.
TITLES = ("الامام", "الشيخ", "الحافظ", "العلامة")
MAX_WINDOW = 6

# Subset surah table for Quran reference validation: name -> (number,
# ayah count). A reference-parse pipeline rejects out-of-range ayahs;
# a free-text pipeline does not (that is NER005).
SURAHS: dict[str, tuple[int, int]] = {
    "الفاتحة": (1, 7),
    "البقرة": (2, 286),
    "ال عمران": (3, 200),
    "يوسف": (12, 111),
    "الحجرات": (49, 18),
    "الملك": (67, 30),
}
SURA_BY_NUM = {num: (name, count) for name, (num, count) in SURAHS.items()}


def _raw_forms(*forms: str) -> tuple[str, ...]:
    return tuple(normalize_ar(f) for f in forms)


def build_gazetteer() -> dict[str, list[GazetteerEntry]]:
    """Normalized-form -> entries index. Forms are pre-normalized so
    detection never re-normalizes a known surface."""
    entries = [
        GazetteerEntry("person:shafii", "Person", _raw_forms("الشافعي", "شافعي")),
        GazetteerEntry("person:ahmad-ibn-hanbal", "Person", _raw_forms("أحمد بن حنبل")),
        GazetteerEntry("person:yahya-bin-main", "Person", _raw_forms("يحيى بن معين")),
        GazetteerEntry(
            "person:muhammad-bin-muslim",
            "Person",
            _raw_forms("محمد بن مسلم", "أبو عبد الله محمد بن مسلم"),
        ),
        GazetteerEntry("person:zuhayr-bin-harb", "Person", _raw_forms("زهير بن حرب")),
        GazetteerEntry(
            "person:ibn-taymiyyah",
            "Person",
            _raw_forms("ابن تيمية", "Ibn Taymiyyah"),
        ),
        GazetteerEntry("person:hisham-bin-urwa", "Person", _raw_forms("هشام بن عروة")),
        # مالك doubles as the common word "owner": the ambiguity guard
        # requires the isnad cue عن before this entry may match.
        GazetteerEntry(
            "person:malik",
            "Person",
            _raw_forms("مالك"),
            ambiguous=True,
            common_cues=("", "عن"),
        ),
        GazetteerEntry("person:ans-bin-malik", "Person", _raw_forms("أنس بن مالك")),
        GazetteerEntry("book:iman", "Book", _raw_forms("كتاب الإيمان")),
        GazetteerEntry("madhhab:shafii", "Madhhab", _raw_forms("الشافعية")),
    ]
    index: dict[str, list[GazetteerEntry]] = {}
    for entry in entries:
        for form in entry.forms:
            index.setdefault(form, []).append(entry)
    return index


CANON_QURAN_IDS = frozenset({"quran:2:255"})


def _window_variants(tokens: list[NormToken], i: int, j: int) -> list[tuple[str, int]]:
    """Matching variants of the token window [i, j): the exact join plus
    clitic-stripped joins. Each variant is (working-copy string,
    working-copy start offset of the entity core)."""

    variants: list[tuple[str, int]] = []
    first, last = tokens[i], tokens[j - 1]
    variants.append((" ".join(t.core for t in tokens[i:j]), first.start))

    for p in _PREFIXES:
        if first.core.startswith(p) and len(first.core) - len(p) >= MIN_REST:
            rest_first = first.core[len(p) :]
            parts = [rest_first] + [t.core for t in tokens[i + 1 : j]]
            variants.append((" ".join(parts), first.start + len(p)))
    for s in _SUFFIXES:
        if last.core.endswith(s) and len(last.core) - len(s) >= MIN_REST:
            rest_last = last.core[: len(last.core) - len(s)]
            parts = [t.core for t in tokens[i : j - 1]] + [rest_last]
            variants.append((" ".join(parts), first.start))
    first_s, last_s = first.core, last.core
    for p in _PREFIXES:
        if not (first_s.startswith(p) and len(first_s) - len(p) >= MIN_REST):
            continue
        for s in _SUFFIXES:
            if not (last_s.endswith(s) and len(last_s) - len(s) >= MIN_REST):
                continue
            parts = [first_s[len(p) :]] + [t.core for t in tokens[i + 1 : j - 1]]
            parts.append(last_s[: len(last_s) - len(s)])
            variants.append((" ".join(parts), first.start + len(p)))
    return variants


def _cue_ok(prev_core: str, entry: GazetteerEntry, guard_on: bool) -> bool:
    """Ambiguity guard: an ambiguous entry (مالك = narrator vs common word
    'owner') matches only when the preceding token is one of its cues
    (e.g., the isnad preposition عن). When the guard is off the cue is
    ignored, which is how common-word false positives leak in (NER007)."""
    if not entry.ambiguous or not guard_on:
        return True
    return prev_core in entry.common_cues


def _norm_index_for_raw(offsets: list[int], raw_start: int) -> int | None:
    """First working-copy offset whose raw index equals raw_start."""
    for i, off in enumerate(offsets):
        if off == raw_start:
            return i
    return None


def _detect_gazetteer(
    raw_text: str,
    offsets: list[int],
    tokens: list[NormToken],
    gaz: dict[str, list[GazetteerEntry]],
    config: NerPipelineConfig,
) -> list[tuple[Span, EntityMention]]:
    """Longest-window, left-to-right gazetteer matching with clitic repair
    (when enabled) and the ambiguity guard (when enabled). A match preceded
    by a title token (الإمام، الشيخ، ...) also yields the outer nested
    span. Returns raw spans paired with mentions."""
    found: list[tuple[Span, EntityMention]] = []
    covered: set[int] = set()
    n = len(tokens)
    i = 0
    while i < n:
        matched_len = 0
        for length in range(min(MAX_WINDOW, n - i), 0, -1):
            j = i + length
            for variant, v_start in _window_variants(tokens, i, j):
                exact_join = " ".join(t.core for t in tokens[i:j])
                if not config.clitic_repair and variant != exact_join:
                    continue
                entries = gaz.get(variant)
                if not entries:
                    continue
                prev_core = tokens[i - 1].core if i > 0 else ""
                usable = [
                    e for e in entries if _cue_ok(prev_core, e, config.gazetteer_guard)
                ]
                if not usable:
                    continue
                norm_start, norm_end = v_start, tokens[j - 1].end
                if any(k in covered for k in range(norm_start, norm_end)):
                    continue
                raw_start = offsets[norm_start]
                raw_end = offsets[norm_end - 1] + 1
                surface = exact_join
                span = Span(raw_start, raw_end, usable[0].etype)
                mention = EntityMention(span, surface, variant)
                found.append((span, mention))
                covered.update(range(norm_start, norm_end))
                matched_len = length
                break
            if matched_len:
                break
        i += matched_len if matched_len else 1
    # Title extension: match preceded by a title token -> also the outer
    # nested span (a Scholar phrase), kept as a separate mention.
    extended: list[tuple[Span, EntityMention]] = list(found)
    core_to_token = {t.start: idx for idx, t in enumerate(tokens)}
    for span, mention in found:
        norm_start = _norm_index_for_raw(offsets, span.start)
        if norm_start is None:
            continue
        tok_idx = core_to_token.get(norm_start)
        if tok_idx is None or tok_idx == 0:
            continue
        prev = tokens[tok_idx - 1]
        if prev.core not in TITLES:
            continue
        outer_start = offsets[prev.start]
        outer_end = span.end
        outer_span = Span(outer_start, outer_end, span.etype)
        outer_text = raw_text[outer_start:outer_end]
        outer_norm = prev.core + " " + mention.norm
        extended.append((outer_span, EntityMention(outer_span, outer_text, outer_norm)))
    return extended


# ----------------------------------------------------------------------------
# 4. Regex rules: nasab (ابن X) and Quran references
# ----------------------------------------------------------------------------


def _nasab_detect(
    offsets: list[int],
    tokens: list[NormToken],
    covered: set[int],
) -> list[tuple[Span, EntityMention]]:
    """Pattern rule: token ابن followed by a token detects an unseen nasab
    name (ابن الجوزي) the gazetteer never listed. Type Person."""
    found: list[tuple[Span, EntityMention]] = []
    for idx, tok in enumerate(tokens):
        if tok.core != "ابن" or idx + 1 >= len(tokens):
            continue
        nxt = tokens[idx + 1]
        if nxt.core in ("الله", "عبد"):
            continue
        if any(k in covered for k in range(tok.start, nxt.end)):
            continue
        norm_start, norm_end = tok.start, nxt.end
        raw_start = offsets[norm_start]
        raw_end = offsets[norm_end - 1] + 1
        surface = f"{tok.core} {nxt.core}"
        span = Span(raw_start, raw_end, "Person")
        found.append((span, EntityMention(span, surface, surface)))
        covered.update(range(norm_start, norm_end))
    return found


_QURAN_NAME = r"سورة\s+([^\s،,]+)\s*،\s*الاية\s*([0-9]+)"
_QURAN_COLON = r"([^\s،,:]{2,})\s*:\s*([0-9]{1,3})"
_QURAN_ASCII = r"(?<![\d:])([0-9]{1,3})\s*:\s*([0-9]{1,3})(?![\d:])"


def parse_quran_reference(ref: str, *, validate: bool) -> tuple[int, int] | None:
    """Parse a Quran citation in any of three surface variants into
    (surah, ayah). validate=True (reference-parse mode) checks the surah
    table and ayah range; validate=False (free-text mode) accepts any
    integers, which is how out-of-range citations leak into the canon.
    The input may be raw or working-copy text; it is normalized once."""
    ref = normalize_ar(ref)
    m = re.search(_QURAN_NAME, ref)
    if m:
        name, ayah_s = m.group(1), m.group(2)
        ayah = int(ayah_s)
        if name not in SURAHS:
            return None
        num, count = SURAHS[name]
        if validate and ayah > count:
            return None
        return (num, ayah)
    m = re.search(_QURAN_COLON, ref)
    if m:
        surah_s, ayah_s = m.group(1), m.group(2)
        if surah_s.isdigit():
            num, ayah = int(surah_s), int(ayah_s)
        else:
            name = normalize_ar(surah_s)
            if name not in SURAHS:
                return None
            num, count = SURAHS[name]
            if validate and int(ayah_s) > count:
                return None
            return (num, int(ayah_s))
        if num in SURA_BY_NUM:
            _, count = SURA_BY_NUM[num]
            if validate and ayah > count:
                return None
            return (num, ayah)
        return None if validate else (num, ayah)
    m = re.search(_QURAN_ASCII, ref)
    if m:
        num, ayah = int(m.group(1)), int(m.group(2))
        if num in SURA_BY_NUM:
            _, count = SURA_BY_NUM[num]
            if validate and ayah > count:
                return None
            return (num, ayah)
        return None if validate else (num, ayah)
    return None


def _quran_detect(
    norm_text: str,
    offsets: list[int],
    config: NerPipelineConfig,
    covered: set[int],
) -> list[tuple[Span, EntityMention]]:
    """Reference rule: surah:ayah citations become QuranVerse spans. In
    reference-parse mode the surah table validates the pair; in free-text
    mode any integers pass (NER005)."""
    validate = config.quran_mode == "reference-parse"
    found: list[tuple[Span, EntityMention]] = []
    patterns = (_QURAN_NAME, _QURAN_COLON, _QURAN_ASCII)
    for pattern in patterns:
        for m in re.finditer(pattern, norm_text):
            norm_start, norm_end = m.start(), m.end()
            if any(k in covered for k in range(norm_start, norm_end)):
                continue
            parsed = parse_quran_reference(m.group(0), validate=validate)
            if parsed is None:
                continue
            raw_start = offsets[norm_start]
            raw_end = offsets[norm_end - 1] + 1
            surface = norm_text[norm_start:norm_end]
            span = Span(raw_start, raw_end, "QuranVerse")
            found.append((span, EntityMention(span, surface, surface)))
            covered.update(range(norm_start, norm_end))
    return found


def detect(raw_text: str, config: NerPipelineConfig) -> list[EntityMention]:
    """Full detection pass: working copy, gazetteer windows (longest first,
    clitic repair and ambiguity guard per config), then nasab and Quran
    regex rules over uncovered regions."""
    gaz = build_gazetteer()
    norm_text, offsets = normalize_with_map(raw_text)
    tokens = tokenize_working(norm_text)
    gaz_found = _detect_gazetteer(raw_text, offsets, tokens, gaz, config)
    covered: set[int] = set()
    for span, _m in gaz_found:
        for ni, off in enumerate(offsets):
            if span.start <= off < span.end:
                covered.add(ni)
    mentions: list[EntityMention] = [m for _s, m in gaz_found]
    for span, mention in _nasab_detect(offsets, tokens, covered):
        for ni, off in enumerate(offsets):
            if span.start <= off < span.end:
                covered.add(ni)
        mentions.append(mention)
    for span, mention in _quran_detect(norm_text, offsets, config, covered):
        for ni, off in enumerate(offsets):
            if span.start <= off < span.end:
                covered.add(ni)
        mentions.append(mention)
    return mentions


# ----------------------------------------------------------------------------
# 5. Linking: blocking, scoring, bands
# ----------------------------------------------------------------------------


def jaro_winkler(s1: str, s2: str) -> float:
    """Jaro-Winkler similarity, stdlib-only. Prefix boost favors shared
    _heads like ابن, which is exactly where Arabic name pairs concentrate
     their similarity — so the string score alone must never auto-link."""

    if s1 == s2:
        return 1.0
    if not s1 or not s2:
        return 0.0
    jaro = _jaro(s1, s2)
    prefix = 0
    for a, b in zip(s1, s2):
        if a != b or prefix == 4:
            break
        prefix += 1
    return jaro + 0.1 * prefix * (1.0 - jaro)


def _jaro(s1: str, s2: str) -> float:
    len1, len2 = len(s1), len(s2)
    match_dist = max(max(len1, len2) // 2 - 1, 0)
    flags1 = [False] * len1
    flags2 = [False] * len2
    matches = 0
    for i, c1 in enumerate(s1):
        lo = max(0, i - match_dist)
        hi = min(i + match_dist + 1, len2)
        for j in range(lo, hi):
            if flags2[j] or s2[j] != c1:
                continue
            flags1[i] = flags2[j] = True
            matches += 1
            break
    if matches == 0:
        return 0.0
    k = 0
    transpositions = 0
    for i in range(len1):
        if not flags1[i]:
            continue
        while not flags2[k]:
            k += 1
        if s1[i] != s2[k]:
            transpositions += 1
        k += 1
    t = transpositions / 2
    m = float(matches)
    return (m / len1 + m / len2 + (m - t) / m) / 3.0


def trigrams(s: str) -> set[str]:
    if len(s) < 3:
        return {s} if s else set()
    return {s[i : i + 3] for i in range(len(s) - 2)}


def jaccard(a: set[str], b: set[str]) -> float:
    if not a and not b:
        return 1.0
    union = a | b
    if not union:
        return 0.0
    return len(a & b) / len(union)


def token_overlap(a: str, b: str) -> float:
    ta, tb = set(a.split()), set(b.split())
    if not ta or not tb:
        return 0.0
    return 2.0 * len(ta & tb) / (len(ta) + len(tb))


def score_link(mention_norm: str, entry: GazetteerEntry) -> float:
    """Link score in [0, 1]: 0.7 * best form similarity + 0.3 * token
    overlap. Form similarity is 1.0 on an exact normalized match, else
    0.5 * trigram Jaccard + 0.5 * Jaro-Winkler over the best form."""

    best_form = 0.0
    for form in entry.forms:
        if mention_norm == form:
            return 1.0
        sim = 0.5 * jaccard(trigrams(mention_norm), trigrams(form))
        sim += 0.5 * jaro_winkler(mention_norm, form)
        best_form = max(best_form, sim)
    overlap = max(
        (token_overlap(mention_norm, form) for form in entry.forms), default=0.0
    )
    return 0.7 * best_form + 0.3 * overlap


def block_candidates(
    mention: EntityMention,
    gaz: dict[str, list[GazetteerEntry]],
) -> list[GazetteerEntry]:
    """Candidate blocking: same entity type, at least one shared character
    trigram with any form. Cheap, recall-oriented; scoring does the rest."""
    seen: dict[str, GazetteerEntry] = {}
    m_tri = trigrams(mention.norm)
    for form, entries in gaz.items():
        if not (m_tri & trigrams(form)):
            continue
        for entry in entries:
            if entry.etype == mention.span.etype:
                seen.setdefault(entry.entity_id, entry)
    return list(seen.values())


REVIEW_FLOOR = 0.55


def link_mention(
    mention: EntityMention,
    gaz: dict[str, list[GazetteerEntry]],
    config: NerPipelineConfig,
) -> LinkDecision:
    """Score every blocked candidate, then band the best: auto / review /
    abstain (or forced when abstention is disabled — NER008). The entity
    ID comes from the canon when id_source='canon'; minting local IDs
    breaks the join into topic 08's resolution output (NER004)."""
    if mention.span.etype == "QuranVerse":
        parsed = parse_quran_reference(
            mention.norm, validate=config.quran_mode == "reference-parse"
        )
        if parsed is None:
            return LinkDecision(mention, None, 0.0, "abstain", "unparsed-quran-ref")
        canon_id = f"quran:{parsed[0]}:{parsed[1]}"
        if config.id_source == "canon":
            if canon_id in CANON_QURAN_IDS:
                return LinkDecision(mention, canon_id, 1.0, "auto", "canon-quran-ref")
            return LinkDecision(mention, None, 0.0, "abstain", "quran-id-not-in-canon")
        return LinkDecision(mention, f"mint:{canon_id}", 1.0, "auto", "minted-quran-id")

    candidates = block_candidates(mention, gaz)
    if not candidates:
        if config.allow_abstain:
            return LinkDecision(mention, None, 0.0, "abstain", "no-blocked-candidates")
        return LinkDecision(mention, None, 0.0, "forced", "no-blocked-candidates")
    best_entry = max(candidates, key=lambda e: score_link(mention.norm, e))
    best_score = score_link(mention.norm, best_entry)
    if best_score >= config.auto_threshold:
        band = "auto"
    elif best_score >= REVIEW_FLOOR:
        band = "review"
    elif config.allow_abstain:
        return LinkDecision(mention, None, best_score, "abstain", "below-review-floor")
    else:
        band = "forced"
    entity_id = (
        best_entry.entity_id
        if config.id_source == "canon"
        else f"mint:{best_entry.entity_id}"
    )
    return LinkDecision(mention, entity_id, best_score, band, "scored")


# ----------------------------------------------------------------------------
# 6. Entity-level evaluation
# ----------------------------------------------------------------------------


def evaluate(
    predictions: dict[str, list[Span]],
    gold: dict[str, list[Span]],
    texts: dict[str, str],
) -> EvalReport:
    """Exact span+type matching for entity-level metrics, plus token-level
    metrics over whitespace tokens fully contained in a span. Both are
    computed per document and then pooled, so spans from one doc can never
    be scored against another doc's gold. The gap between the two levels
    is the audit's NER003 exhibit."""
    tp = fp = fn = 0
    pred_tok: set[tuple[str, int]] = set()
    gold_tok: set[tuple[str, int]] = set()
    for doc_id, text in texts.items():
        preds = predictions.get(doc_id, [])
        golds = gold.get(doc_id, [])
        pred_keys = {p.key() for p in preds}
        gold_keys = {g.key() for g in golds}
        tp += len(pred_keys & gold_keys)
        fp += len(pred_keys - gold_keys)
        fn += len(gold_keys - pred_keys)
        offset = 0
        for t_idx, tok in enumerate(text.split()):
            t_start, t_end = offset, offset + len(tok)
            if any(s.start <= t_start and t_end <= s.end for s in preds):
                pred_tok.add((doc_id, t_idx))
            if any(s.start <= t_start and t_end <= s.end for s in golds):
                gold_tok.add((doc_id, t_idx))
            offset = t_end + 1
    precision = tp / (tp + fp) if tp + fp else 0.0
    recall = tp / (tp + fn) if tp + fn else 0.0
    f1 = 2 * precision * recall / (precision + recall) if precision + recall else 0.0
    tp_t = len(pred_tok & gold_tok)
    fp_t = len(pred_tok - gold_tok)
    fn_t = len(gold_tok - pred_tok)
    p_t = tp_t / (tp_t + fp_t) if tp_t + fp_t else 0.0
    r_t = tp_t / (tp_t + fn_t) if tp_t + fn_t else 0.0
    f1_t = 2 * p_t * r_t / (p_t + r_t) if p_t + r_t else 0.0
    return EvalReport(tp, fp, fn, precision, recall, f1, p_t, r_t, f1_t)


def run_pipeline(
    config: NerPipelineConfig, docs: list[HeldOutDoc]
) -> tuple[list[LinkDecision], RunStats]:
    """Detect, link, and evaluate over held-out docs. Also derives the
    three run-level exhibits the audit messages cite: forced links,
    clitic-dependent gold spans, and guard-attributable false positives."""
    gaz = build_gazetteer()
    all_decisions: list[LinkDecision] = []
    predictions: dict[str, list[Span]] = {}
    gold: dict[str, list[Span]] = {}
    texts: dict[str, str] = {}
    for doc in docs:
        texts[doc.doc_id] = doc.text
        gold[doc.doc_id] = list(doc.gold)
        mentions = detect(doc.text, config)
        predictions[doc.doc_id] = [m.span for m in mentions]
        for mention in mentions:
            all_decisions.append(link_mention(mention, gaz, config))
    report = evaluate(predictions, gold, texts)
    forced = sum(1 for d in all_decisions if d.band == "forced")

    repair_on = replace(config, clitic_repair=True)
    repair_off = replace(config, clitic_repair=False)
    guard_on = replace(config, gazetteer_guard=True)
    guard_off = replace(config, gazetteer_guard=False)

    def gold_hits(cfg: NerPipelineConfig) -> set[tuple[str, int, int, str]]:
        hits: set[tuple[str, int, int, str]] = set()
        for doc in docs:
            pred_keys = {m.span.key() for m in detect(doc.text, cfg)}
            for g in doc.gold:
                if g.key() in pred_keys:
                    hits.add((doc.doc_id, *g.key()))
        return hits

    clitic_dependent = len(gold_hits(repair_on) - gold_hits(repair_off))

    def fp_count(cfg: NerPipelineConfig) -> int:
        total = 0
        for doc in docs:
            pred_keys = {m.span.key() for m in detect(doc.text, cfg)}
            gold_keys = {g.key() for g in doc.gold}
            total += len(pred_keys - gold_keys)
        return total

    guard_fp = max(0, fp_count(guard_off) - fp_count(guard_on))
    stats = RunStats(report, forced, clitic_dependent, guard_fp)
    return all_decisions, stats


# ----------------------------------------------------------------------------
# 7. Pipeline configuration audit (NER001-NER008)
# ----------------------------------------------------------------------------

# (severity, code, rule text). Severity "error" = identity/reference
# integrity broken; "warning" = silent quality loss or governance gap.
RULE_CATALOG: tuple[tuple[str, str, str], ...] = (
    (
        "warning",
        "NER001",
        "model improvement claimed without gazetteer-baseline measurement",
    ),
    ("warning", "NER002", "auto-link threshold set without a labelled pair study"),
    ("warning", "NER003", "evaluation reported at token level only, not entity level"),
    ("error", "NER004", "linker mints local IDs instead of using the external canon"),
    (
        "error",
        "NER005",
        "Quran reference parsed as free text, without surah-table validation",
    ),
    ("warning", "NER006", "clitic-attached entities unsegmented; repair disabled"),
    ("warning", "NER007", "gazetteer ambiguity guard disabled; common words may match"),
    ("error", "NER008", "abstention disabled; every span is force-linked"),
)


def _declared_line(source: str, code: str) -> int:
    """1-based line of the `# NERxxx:` marker in the source listing."""
    for idx, line in enumerate(source.splitlines(), 1):
        if f"# {code}:" in line:
            return idx
    return 0


def audit_pipeline(config: NerPipelineConfig, stats: RunStats) -> list[Finding]:
    """Declarative audit: one finding per violated rule, with the run
    exhibits cited in the message so the finding is evidence, not vibes."""
    source = Path(__file__).read_text(encoding="utf-8")
    findings: list[Finding] = []

    def add(code: str, message: str) -> None:
        severity = next(s for s, c, _ in RULE_CATALOG if c == code)
        findings.append(Finding(severity, code, message, _declared_line(source, code)))

    if config.model_claim and not config.baseline_measured:
        add(
            "NER001",
            f"model claim '{config.model_claim}' has no measured gazetteer baseline; "
            "an ungated model change cannot be attributed",
        )
    if not config.threshold_study:
        add(
            "NER002",
            f"auto_threshold={config.auto_threshold} ships without a labelled pair "
            "study; AUTO band precision is unmeasured",
        )
    if config.metric != "entity":
        add(
            "NER003",
            f"metric='{config.metric}' hides span errors: entity F1 "
            f"{stats.report.f1:.3f} vs token F1 {stats.report.token_f1:.3f}",
        )
    if config.id_source != "canon":
        add("NER004", "id_source='mint' breaks the join into topic 08's canon IDs")
    if config.quran_mode != "reference-parse":
        add(
            "NER005",
            "quran_mode='free-text' accepts out-of-range ayahs (e.g., 2:999) "
            "into the knowledge base",
        )
    if not config.clitic_repair:
        add(
            "NER006",
            f"clitic_repair=False drops {stats.clitic_dependent} gold span(s) "
            "that only a stripped proclitic reveals (e.g., لابن تيمية)",
        )
    if not config.gazetteer_guard:
        add(
            "NER007",
            f"gazetteer_guard=False admits {stats.guard_fp} common-word false "
            "positive(s) (e.g., مالك as 'owner')",
        )
    if not config.allow_abstain:
        add(
            "NER008",
            f"allow_abstain=False force-linked {stats.forced_links} span(s) "
            "below the review floor",
        )
    return findings


# ----------------------------------------------------------------------------
# 8. Held-out corpus with gold annotations
# ----------------------------------------------------------------------------


def _span_of(text: str, substr: str, etype: str) -> Span:
    start = text.index(substr)
    return Span(start, start + len(substr), etype)


_D1 = "وعن أحمد بن حنبل، وعن يحيى بن معين رضي الله عنهما."
_D2 = "قال الإمام الشافعي في كتبه في أصول الفقه."
_D3 = "روى أبو عبد الله محمد بن مسلم عن زهير بن حرب."
_D4 = "Among the later authors, Ibn Taymiyyah rejected the appeal."
_D5 = "ومن آيات الكرسي في سورة البقرة، الآية ٢٥٥."
_D6 = "وورد في 2:255 أثر قديم."
_D7 = "وفي مقدمة الكتاب: مالك الأمر إلى الله."
_D8 = "روى ابن الجوزي في كتابه من طريق هشام بن عروة."
_D9 = "ومذهب الشافعية في هذا الباب مختلف."
_D10 = "ومن كتبه: كتاب الإيمان لابن تيمية."
_D11 = "أخرج أحمد بن حنبل، عن قتادة، عن أنس بن مالك."

HELD_OUT: tuple[HeldOutDoc, ...] = (
    HeldOutDoc(
        "d1",
        _D1,
        (
            _span_of(_D1, "أحمد بن حنبل", "Person"),
            _span_of(_D1, "يحيى بن معين", "Person"),
        ),
    ),
    HeldOutDoc(
        "d2",
        _D2,
        (
            _span_of(_D2, "الإمام الشافعي", "Person"),
            _span_of(_D2, "الشافعي", "Person"),
        ),
    ),
    HeldOutDoc(
        "d3",
        _D3,
        (
            _span_of(_D3, "أبو عبد الله محمد بن مسلم", "Person"),
            _span_of(_D3, "زهير بن حرب", "Person"),
        ),
    ),
    HeldOutDoc("d4", _D4, (_span_of(_D4, "Ibn Taymiyyah", "Person"),)),
    HeldOutDoc("d5", _D5, (_span_of(_D5, "سورة البقرة، الآية ٢٥٥", "QuranVerse"),)),
    HeldOutDoc("d6", _D6, (_span_of(_D6, "2:255", "QuranVerse"),)),
    HeldOutDoc("d7", _D7, ()),
    HeldOutDoc(
        "d8",
        _D8,
        (
            _span_of(_D8, "ابن الجوزي", "Person"),
            _span_of(_D8, "هشام بن عروة", "Person"),
        ),
    ),
    HeldOutDoc("d9", _D9, (_span_of(_D9, "الشافعية", "Madhhab"),)),
    HeldOutDoc(
        "d10",
        _D10,
        (
            _span_of(_D10, "كتاب الإيمان", "Book"),
            _span_of(_D10, "ابن تيمية", "Person"),
        ),
    ),
    HeldOutDoc(
        "d11",
        _D11,
        (
            _span_of(_D11, "أحمد بن حنبل", "Person"),
            _span_of(_D11, "قتادة", "Person"),
            _span_of(_D11, "أنس بن مالك", "Person"),
        ),
    ),
)


# ----------------------------------------------------------------------------
# 9. BAD and GOOD pipeline configurations
# ----------------------------------------------------------------------------

# BAD pack: every planted pathology, one finding per rule.
# - model claim with no measured gazetteer baseline        (NER001)
# - auto threshold with no labelled pair study             (NER002)
# - evaluation reported at token level only                (NER003)
# - linker mints local IDs instead of the external canon   (NER004)
# - Quran refs parsed as free text, no surah validation    (NER005)
# - clitic repair off: لابن تيمية never matches            (NER006)
# - ambiguity guard off: مالك matches as a common word      (NER007)
# - abstention off: ابن الجوزي force-linked below floor    (NER008)
BAD_PIPELINE = NerPipelineConfig(
    name="bad-pack",
    metric="token",  # NER003:
    model_claim="arabert-f1-0.94",  # NER001:
    baseline_measured=False,  # NER001:
    auto_threshold=0.85,
    threshold_study=False,  # NER002:
    allow_abstain=False,  # NER008:
    id_source="mint",  # NER004:
    quran_mode="free-text",  # NER005:
    clitic_repair=False,  # NER006:
    gazetteer_guard=False,  # NER007:
)

# GOOD pack: the same corpus, governed. Must produce ZERO findings.
# - claim recorded WITH a measured gazetteer baseline
# - threshold justified by a pair study; entity-level metric
# - canon IDs only; Quran references validated against the surah table
# - clitic repair and the ambiguity guard on; abstention preserved
GOOD_PIPELINE = NerPipelineConfig(
    name="good-pack",
    metric="entity",
    model_claim="arabert-f1-0.94",
    baseline_measured=True,
    auto_threshold=0.85,
    threshold_study=True,
    allow_abstain=True,
    id_source="canon",
    quran_mode="reference-parse",
    clitic_repair=True,
    gazetteer_guard=True,
)


# ----------------------------------------------------------------------------
# 10. Self-checks and demo helpers
# ----------------------------------------------------------------------------


def check_normalizer() -> None:
    norm, offsets = normalize_with_map("بِسْمِ ٱللَّهِ ٢٥٥")
    assert "بسم" in norm and "الله" in norm.replace("ٱ", "ا")
    assert "255" in norm, norm
    assert len(norm) == len(offsets)
    raw = "الإمامُ الشّافعيُّ"
    norm2, offsets2 = normalize_with_map(raw)
    assert norm2 == "الامام الشافعي", norm2
    assert raw[offsets2[0]] == "ا", "map must point back into the raw text"
    print(f"[check] normalizer: {raw!r} -> {norm2!r} (map ok)")


def check_quran_parser() -> None:
    assert parse_quran_reference("سورة البقرة، الآية 255", validate=True) == (2, 255)
    assert parse_quran_reference("البقرة: 255", validate=True) == (2, 255)
    assert parse_quran_reference("2:255", validate=True) == (2, 255)
    assert parse_quran_reference("2:999", validate=True) is None
    assert parse_quran_reference("2:999", validate=False) == (2, 999)
    print(
        "[check] quran parser: 3 variants accepted, out-of-range rejected only in reference-parse"
    )


def check_linking_bands() -> None:
    gaz = build_gazetteer()
    exact = detect("قال الشافعي في كتاب الأم.", GOOD_PIPELINE)
    shafii = [m for m in exact if m.norm == "الشافعي"]
    assert shafii, "الشافعي must be detected"
    decision = link_mention(shafii[0], gaz, GOOD_PIPELINE)
    assert decision.band == "auto" and decision.entity_id == "person:shafii", decision
    title = detect("قال الإمام الشافعي في كتبه.", GOOD_PIPELINE)
    outer = [m for m in title if m.norm == "الامام الشافعي"]
    assert outer, "title-extended outer span must be detected"
    outer_decision = link_mention(outer[0], gaz, GOOD_PIPELINE)
    assert outer_decision.band in ("review", "auto"), outer_decision
    unseen = detect("روى ابن الجوزي من طريق هشام بن عروة.", GOOD_PIPELINE)
    juz = [m for m in unseen if m.norm == "ابن الجوزي"]
    assert juz, "nasab rule must detect ابن الجوزي"
    juz_decision = link_mention(juz[0], gaz, GOOD_PIPELINE)
    assert juz_decision.band == "abstain" and juz_decision.entity_id is None, (
        juz_decision
    )
    latin = detect("Ibn Taymiyyah rejected the appeal.", GOOD_PIPELINE)
    latin_m = [m for m in latin if m.norm == "ibn taymiyyah"]
    assert latin_m and link_mention(latin_m[0], gaz, GOOD_PIPELINE).band == "auto"
    print(
        "[check] bands: exact AUTO, title-extension "
        f"{outer_decision.band.upper()} ({outer_decision.score:.2f}), "
        f"unseen nasab ABSTAIN ({juz_decision.score:.2f}), Latin AUTO"
    )


def check_held_out_good() -> None:
    _decisions, stats = run_pipeline(GOOD_PIPELINE, list(HELD_OUT))
    r = stats.report
    print(
        f"[check] held-out GOOD: entity P/R/F1 = "
        f"{r.precision:.3f}/{r.recall:.3f}/{r.f1:.3f} "
        f"(tp={r.tp} fp={r.fp} fn={r.fn}); "
        f"token F1 = {r.token_f1:.3f}"
    )
    assert r.fp == 0, f"GOOD pack must have zero false positives, got {r.fp}"
    assert r.f1 >= 0.85, f"GOOD entity F1 must clear 0.85, got {r.f1:.3f}"


def check_audit_packs() -> list[Finding]:
    bad_decisions, bad_stats = run_pipeline(BAD_PIPELINE, list(HELD_OUT))
    bad_findings = audit_pipeline(BAD_PIPELINE, bad_stats)
    good_decisions, good_stats = run_pipeline(GOOD_PIPELINE, list(HELD_OUT))
    good_findings = audit_pipeline(GOOD_PIPELINE, good_stats)
    assert sorted(f.code for f in bad_findings) == sorted(
        code for _, code, _ in RULE_CATALOG
    ), (
        f"BAD pack must surface all eight rules, got {sorted(f.code for f in bad_findings)}"
    )
    assert len(bad_findings) == len(RULE_CATALOG), (
        f"BAD pack must emit exactly one finding per rule, got {len(bad_findings)}"
    )
    assert good_findings == [], (
        f"GOOD pack must produce zero findings, got {good_findings}"
    )
    print(
        f"[check] audit: BAD = {len(bad_findings)} findings "
        f"(entity F1 {bad_stats.report.f1:.3f}), "
        f"GOOD = 0 findings (entity F1 {good_stats.report.f1:.3f})"
    )
    return bad_findings


def print_decisions(decisions: list[LinkDecision]) -> None:
    for d in decisions:
        canon = d.entity_id or "-"
        print(
            f"  {d.band.upper():<7} score={d.score:.2f}  canon={canon:<28} "
            f"'{d.mention.text}' ({d.mention.span.etype})"
        )


def print_findings(findings: list[Finding]) -> None:
    for f in findings:
        print(f"  [{f.severity.upper():<7}] {f.code} (line {f.line}): {f.message}")


def print_demo() -> None:
    gaz = build_gazetteer()
    demos = [
        "قال الشافعي في كتاب الأم.",
        "قال الإمام الشافعي في كتبه.",
        "روى ابن الجوزي من طريق هشام بن عروة.",
        "Ibn Taymiyyah rejected the appeal.",
        "ومن آيات الكرسي في سورة البقرة، الآية ٢٥٥.",
    ]
    print("--- link decisions (GOOD pipeline) ---")
    for text in demos:
        print(f"  text: {text}")
        for mention in detect(text, GOOD_PIPELINE):
            d = link_mention(mention, gaz, GOOD_PIPELINE)
            print(
                f"    {d.band.upper():<7} score={d.score:.2f}  "
                f"canon={d.entity_id or '-':<28}  '{mention.text}'"
            )


# ----------------------------------------------------------------------------
# 11. External corpus loader (Windows-BOM tolerant)
# ----------------------------------------------------------------------------


def load_external(path: str) -> list[HeldOutDoc]:
    """Load [{id, text, spans: [{start, end, type}]}] with utf-8-sig so a
    BOM'd export from Excel still parses."""
    data = json.loads(Path(path).read_text(encoding="utf-8-sig"))
    docs = []
    for row in data:
        spans = tuple(
            Span(s["start"], s["end"], s["type"]) for s in row.get("spans", [])
        )
        docs.append(HeldOutDoc(row["id"], row["text"], spans))
    return docs


def run_corpus_file(path: str) -> int:
    docs = load_external(path)
    decisions, stats = run_pipeline(GOOD_PIPELINE, docs)
    r = stats.report
    print(
        f"external corpus: {len(docs)} docs | entity P/R/F1 = "
        f"{r.precision:.3f}/{r.recall:.3f}/{r.f1:.3f} | "
        f"tp={r.tp} fp={r.fp} fn={r.fn}"
    )
    print_decisions(decisions[:10])
    return 0 if r.f1 >= 0.5 else 1


# ----------------------------------------------------------------------------
# 12. Demo and self-checks
# ----------------------------------------------------------------------------


def main(argv: list[str]) -> int:
    if len(argv) > 1:
        return run_corpus_file(argv[1])
    check_normalizer()
    check_quran_parser()
    check_linking_bands()
    print()
    print_demo()
    print()
    check_held_out_good()
    bad_findings = check_audit_packs()
    print()
    print("--- BAD pack findings (NER001-NER008) ---")
    print_findings(bad_findings)
    print()
    good_decisions, good_stats = run_pipeline(GOOD_PIPELINE, list(HELD_OUT))
    print("--- GOOD pack: zero findings ---")
    print(
        f"  entity F1 = {good_stats.report.f1:.3f} "
        f"(tp={good_stats.report.tp} fp={good_stats.report.fp} fn={good_stats.report.fn}); "
        f"token F1 = {good_stats.report.token_f1:.3f}"
    )
    print()
    print("all self-checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
