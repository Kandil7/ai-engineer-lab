"""
Arabic NLP — 08: Arabic Entity Resolution
========================================
Topics: normalization for matching, blocking, fuzzy similarity, weighted
scoring with a conflict veto, canonization, merge-with-review, and
precision/recall against a labelled gold pair set.

Why this matters:
    An Islamic-knowledge corpus records the same scholar or book under many
    surface forms (kunya, laqab, nisba, alef variants, Arabic-Indic digits,
    Latin transliteration). Entity resolution decides which records are the
    same real-world entity — and a wrong merge silently corrupts every
    citation that depends on it, which is why a false merge is worse than a
    missed one. This exercise implements a small but real pipeline:
    normalizer -> blocking -> three string similarities -> weighted scoring
    with a year/context veto -> MergeCandidate emission -> gold-pair audit.

Run:      python 08-arabic-entity-resolution.py
          python 08-arabic-entity-resolution.py gold_pairs.jsonl
"""

from __future__ import annotations

import json
import sys
import time
import unicodedata
import uuid
from dataclasses import dataclass
from itertools import combinations

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

NORMALIZER_VERSION = "ar-er-norm-1.0"
AUTO_THRESHOLD = 0.85
REVIEW_THRESHOLD = 0.55
YEAR_TOLERANCE = 5
NAIVE_JW_THRESHOLD = 0.85


# ----------------------------------------------------------------------------
# 1. Data models
# ----------------------------------------------------------------------------


@dataclass(frozen=True)
class Entity:
    """One record. display keeps the observed surface form for display;
    aliases carry every other observed form. year/context are optional
    metadata used only as agreement/veto signals, never as merge keys."""

    entity_id: str
    category: str  # "author" | "book" | "narrator"
    display: str
    aliases: tuple[str, ...] = ()
    year: int | None = None
    context: str | None = None

    def forms(self) -> tuple[str, ...]:
        return (self.display, *self.aliases)


@dataclass(frozen=True)
class Alias:
    """One observed surface form, stamped with the normalizer version that
    produced its normalized key. Re-running with a new normalizer version
    re-derives aliases; it never mutates the observed surface."""

    entity_id: str
    surface: str
    normalized: str
    normalizer_version: str


@dataclass(frozen=True)
class MergeCandidate:
    """A pair the pipeline judged. decision is one of:
    "auto-merge" (score >= AUTO_THRESHOLD, no veto), "review" (score in the
    human band, or vetoed despite a high score), "no-merge"."""

    left_id: str
    right_id: str
    category: str
    score: float
    decision: str
    veto: str | None = None
    signals: tuple[tuple[str, float], ...] = ()


@dataclass(frozen=True)
class PairLabel:
    """One gold judgement: are these two records the same entity?"""

    left_id: str
    right_id: str
    same: bool
    category: str = ""
    note: str = ""


def pair_key(a: str, b: str) -> tuple[str, str]:
    return (a, b) if a <= b else (b, a)


# ----------------------------------------------------------------------------
# 2. Arabic normalization for matching
# ----------------------------------------------------------------------------

_ALEF_MAP = {"أ": "ا", "إ": "ا", "آ": "ا", "ٱ": "ا"}
_ARABIC_INDIC_DIGITS = {chr(0x0660 + i): str(i) for i in range(10)}
_EXTENDED_INDIC_DIGITS = {chr(0x06F0 + i): str(i) for i in range(10)}
_DIGIT_MAP = {**_ARABIC_INDIC_DIGITS, **_EXTENDED_INDIC_DIGITS}


def strip_tashkeel(text: str) -> str:
    """Strip combining marks (fatha, damma, kasra, sukun, shadda, tanween,
    superscript alef). Display text keeps tashkeel; this index copy never
    sees it — محمد and محمَّد must collide for name matching."""
    return "".join(ch for ch in text if unicodedata.category(ch) != "Mn")


def normalize_ar(text: str, *, fold_ta_marbuta: bool = False) -> str:
    """Index-copy normalization for entity matching (versioned).

    Orthographic unification only; the original string is never mutated.
    - NFC first, so precomposed and decomposed inputs agree.
    - Tashkeel stripped (display copy keeps it).
    - Tatweel removed (decorative).
    - Alef variants أ إ آ ٱ folded to ا.
    - Alef maqsura ى folded to ي.
    - Arabic-Indic and Extended Arabic-Indic digits folded to ASCII.
    - Whitespace collapsed.
    Ta marbuta ة -> ه is deliberately NOT applied here: it is a fuzzy-only
    relaxation (pass fold_ta_marbuta=True to a fuzzy key generator), because
    folding it in the index copy over-merges distinct words.
    """
    text = unicodedata.normalize("NFC", text)
    text = strip_tashkeel(text)
    text = text.replace("ـ", "")
    for src, dst in _ALEF_MAP.items():
        text = text.replace(src, dst)
    text = text.replace("ى", "ي")
    if fold_ta_marbuta:
        text = text.replace("ة", "ه")
    text = "".join(_DIGIT_MAP.get(ch, ch) for ch in text)
    return " ".join(text.split()).strip()


def collapse_spaces(text: str) -> str:
    """Remove all spaces: عبدالرحمن and عبد الرحمن collapse to one key.
    Space placement after عبد, ذو, etc. is genuinely inconsistent across
    sources, so collapsed equality is a strong match signal."""
    return text.replace(" ", "")


# ----------------------------------------------------------------------------
# 3. String similarity
# ----------------------------------------------------------------------------


def damerau_levenshtein(a: str, b: str) -> int:
    """Optimal string alignment distance: insertions, deletions,
    substitutions, and adjacent transpositions."""
    la, lb = len(a), len(b)
    if la == 0:
        return lb
    if lb == 0:
        return la
    prev2: list[int] = []
    prev = list(range(lb + 1))
    for i in range(1, la + 1):
        cur = [i] + [0] * lb
        for j in range(1, lb + 1):
            cost = 0 if a[i - 1] == b[j - 1] else 1
            cur[j] = min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + cost)
            if i > 1 and j > 1 and a[i - 1] == b[j - 2] and a[i - 2] == b[j - 1]:
                cur[j] = min(cur[j], prev2[j - 2] + 1)
        prev2, prev = prev, cur
    return prev[lb]


def damerau_levenshtein_sim(a: str, b: str) -> float:
    longest = max(len(a), len(b), 1)
    return 1.0 - damerau_levenshtein(a, b) / longest


def jaro(s1: str, s2: str) -> float:
    if not s1 and not s2:
        return 1.0
    if not s1 or not s2:
        return 0.0
    match_window = max(len(s1), len(s2)) // 2 - 1
    if match_window < 0:
        match_window = 0
    flags1 = [False] * len(s1)
    flags2 = [False] * len(s2)
    matches = 0
    for i, ch in enumerate(s1):
        lo = max(0, i - match_window)
        hi = min(i + match_window + 1, len(s2))
        for j in range(lo, hi):
            if not flags2[j] and s2[j] == ch:
                flags1[i] = flags2[j] = True
                matches += 1
                break
    if matches == 0:
        return 0.0
    transpositions = 0
    k = 0
    for i in range(len(s1)):
        if not flags1[i]:
            continue
        while not flags2[k]:
            k += 1
        if s1[i] != s2[k]:
            transpositions += 1
        k += 1
    half = transpositions / 2
    return (matches / len(s1) + matches / len(s2) + (matches - half) / matches) / 3


def jaro_winkler(s1: str, s2: str, max_prefix: int = 4) -> float:
    """Jaro with a Winkler prefix bonus — strong for personal names that
    share a long common prefix (محمد بن ...)."""
    base = jaro(s1, s2)
    prefix = 0
    for c1, c2 in zip(s1, s2):
        if c1 != c2 or prefix == max_prefix:
            break
        prefix += 1
    return base + prefix * 0.1 * (1.0 - base)


def char_ngram_jaccard(a: str, b: str, n: int = 2) -> float:
    """Jaccard over character n-gram sets. Robust to insertions and
    transpositions that destroy edit-distance scores on longer names."""
    if not a and not b:
        return 1.0
    if not a or not b:
        return 0.0
    grams_a = {a[i : i + n] for i in range(max(len(a) - n + 1, 1))}
    grams_b = {b[i : i + n] for i in range(max(len(b) - n + 1, 1))}
    union = grams_a | grams_b
    if not union:
        return 1.0
    return len(grams_a & grams_b) / len(union)


def token_set_jaccard(a: str, b: str) -> float:
    tokens_a = set(a.split())
    tokens_b = set(b.split())
    union = tokens_a | tokens_b
    if not union:
        return 1.0
    return len(tokens_a & tokens_b) / len(union)


# ----------------------------------------------------------------------------
# 4. Blocking / candidate generation
# ----------------------------------------------------------------------------


def blocking_keys(entity: Entity) -> set[str]:
    """Keys under which this entity becomes a candidate. Never all-pairs:
    a bucket key (category + initial letter + length bucket) plus one key
    per character trigram of every collapsed form. Latin-script forms
    produce Latin trigrams and will NOT collide with Arabic trigrams —
    a known recall gap this pipeline measures rather than hides."""
    keys: set[str] = set()
    for form in entity.forms():
        norm = normalize_ar(form)
        if not norm:
            continue
        collapsed = collapse_spaces(norm)
        bucket = len(collapsed) // 4
        keys.add(f"{entity.category}|fl|{norm[0]}|{bucket}")
        if len(collapsed) >= 3:
            for i in range(len(collapsed) - 2):
                keys.add(f"{entity.category}|tri|{collapsed[i : i + 3]}")
        else:
            keys.add(f"{entity.category}|tri|{collapsed}")
    return keys


def generate_candidates(entities: list[Entity]) -> set[tuple[str, str]]:
    """Pairs that share at least one blocking key. Comparison (expensive)
    only ever runs on these pairs, never on the full cross product."""
    inverted: dict[str, list[str]] = {}
    for e in entities:
        for key in blocking_keys(e):
            inverted.setdefault(key, []).append(e.entity_id)
    pairs: set[tuple[str, str]] = set()
    for ids in inverted.values():
        for a, b in combinations(sorted(set(ids)), 2):
            pairs.add(pair_key(a, b))
    return pairs


# ----------------------------------------------------------------------------
# 5. Signals, scoring, and the conflict veto
# ----------------------------------------------------------------------------


def context_signal(e1: Entity, e2: Entity) -> tuple[float, str | None]:
    """Era/publisher/madhhab agreement. A hard veto on conflict: records
    that contradict on year or context never auto-merge, no matter how
    identical their strings are — identical names across different eras
    are the classic homonym trap in the scholarly corpus."""
    if e1.year is not None and e2.year is not None:
        if abs(e1.year - e2.year) > YEAR_TOLERANCE:
            return 0.0, "year-conflict"
    if e1.context and e2.context and e1.context != e2.context:
        return 0.0, "context-conflict"
    return 1.0, None


def compare_entities(e1: Entity, e2: Entity) -> MergeCandidate:
    """Weighted evidence over the best-matching form pair:

        score = 0.30*exact + 0.35*fuzzy + 0.15*token + 0.10*alias
                + 0.10*context

    exact is 1 when some form pair is equal after normalization or after
    space collapse. fuzzy is 0.4*ngram + 0.3*DL + 0.3*JW on the best pair.
    alias is 1 when any recorded forms of the two records agree (surface
    agreement across the alias tables). Weights are the kind of object a
    labelled pair set is tuned on — not a guess left in production."""
    best: tuple[tuple[float, float], float, float, float] | None = None
    alias = 0.0
    for f1 in e1.forms():
        n1 = normalize_ar(f1)
        c1 = collapse_spaces(n1)
        for f2 in e2.forms():
            n2 = normalize_ar(f2)
            c2 = collapse_spaces(n2)
            exact_pair = 1.0 if (n1 == n2 or c1 == c2) else 0.0
            if exact_pair:
                alias = 1.0
            ng = char_ngram_jaccard(c1, c2)
            dl = damerau_levenshtein_sim(n1, n2)
            jw = jaro_winkler(n1, n2)
            fuzzy = 0.4 * ng + 0.3 * dl + 0.3 * jw
            tok = token_set_jaccard(n1, n2)
            key = (exact_pair, fuzzy)
            if best is None or key > best[0]:
                best = (key, exact_pair, fuzzy, tok)
    assert best is not None  # Entity always has at least the display form
    _, exact, fuzzy, tok = best
    ctx, veto = context_signal(e1, e2)
    score = 0.30 * exact + 0.35 * fuzzy + 0.15 * tok + 0.10 * alias + 0.10 * ctx
    signals = (
        ("exact", exact),
        ("fuzzy", round(fuzzy, 4)),
        ("token", round(tok, 4)),
        ("alias", alias),
        ("context", ctx),
    )
    if veto is not None:
        decision = "review" if score >= REVIEW_THRESHOLD else "no-merge"
    elif score >= AUTO_THRESHOLD:
        decision = "auto-merge"
    elif score >= REVIEW_THRESHOLD:
        decision = "review"
    else:
        decision = "no-merge"
    return MergeCandidate(
        left_id=e1.entity_id,
        right_id=e2.entity_id,
        category=e1.category,
        score=round(score, 4),
        decision=decision,
        veto=veto,
        signals=signals,
    )


def naive_compare(e1: Entity, e2: Entity) -> str:
    """The naive baseline this lecture argues against: merge on the display
    string (normalized equality or a loose Jaro-Winkler cutoff), with no
    metadata veto. Used only to demonstrate the failure modes."""
    n1 = normalize_ar(e1.display)
    n2 = normalize_ar(e2.display)
    if n1 == n2 or jaro_winkler(n1, n2) >= NAIVE_JW_THRESHOLD:
        return "merge"
    return "no-merge"


# ----------------------------------------------------------------------------
# 6. Pipeline: candidates -> compare -> decide
# ----------------------------------------------------------------------------


def run_pipeline(entities: list[Entity]) -> list[MergeCandidate]:
    by_id = {e.entity_id: e for e in entities}
    candidates = []
    for a, b in sorted(generate_candidates(entities)):
        candidates.append(compare_entities(by_id[a], by_id[b]))
    return candidates


# ----------------------------------------------------------------------------
# 7. Canonization: canonical IDs, alias table, reversible merge
# ----------------------------------------------------------------------------

_CROCKFORD = "0123456789ABCDEFGHJKMNPQRSTVWXYZ"


def new_ulid() -> str:
    """26-char ULID: 48-bit millisecond timestamp + 80 bits of randomness,
    Crockford base32. Lexicographically sortable (unlike UUIDv4) and
    offline-generable (unlike DB sequences); prefer it or UUIDv7 for
    canonical entity ids."""
    value = (int(time.time() * 1000) << 80) | (uuid.uuid4().int & ((1 << 80) - 1))
    out = []
    for _ in range(26):
        out.append(_CROCKFORD[value & 0x1F])
        value >>= 5
    return "".join(reversed(out))


def canonize(candidates: list[MergeCandidate]) -> dict[str, str]:
    """Union-find over auto-merge decisions: every member id resolves to
    one canonical ULID per cluster. Old ids are never rewritten — they
    become aliases of the canonical id (no destructive updates)."""
    parent: dict[str, str] = {}

    def find(x: str) -> str:
        parent.setdefault(x, x)
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def union(a: str, b: str) -> None:
        ra, rb = find(a), find(b)
        if ra != rb:
            parent[rb] = ra

    for c in candidates:
        if c.decision == "auto-merge":
            union(c.left_id, c.right_id)
    canonical: dict[str, str] = {}
    cluster_ulid: dict[str, str] = {}
    for member in sorted(parent):
        root = find(member)
        cluster_ulid.setdefault(root, new_ulid())
        canonical[member] = cluster_ulid[root]
    return canonical


def build_alias_table(entities: list[Entity]) -> dict[str, list[Alias]]:
    """Every observed form of every record, stamped with the normalizer
    version. The alias table preserves all forms; it never replaces the
    original surface with the normalized one."""
    table: dict[str, list[Alias]] = {}
    for e in entities:
        rows = [
            Alias(e.entity_id, form, normalize_ar(form), NORMALIZER_VERSION)
            for form in e.forms()
        ]
        table.setdefault(e.entity_id, []).extend(rows)
    return table


# ----------------------------------------------------------------------------
# 8. Evaluation against a labelled gold pair set
# ----------------------------------------------------------------------------


def evaluate_pack(
    entities: list[Entity], labels: list[PairLabel]
) -> tuple[dict[str, tuple[float, float, float]], float, list[MergeCandidate]]:
    """Per-category precision/recall/F1 of auto-merge decisions against the
    gold labels, plus blocking recall (fraction of gold-positive pairs that
    were generated as candidates at all)."""
    gold_pos = {pair_key(l.left_id, l.right_id) for l in labels if l.same}
    generated = generate_candidates(entities)
    candidates = run_pipeline(entities)
    auto = {
        pair_key(c.left_id, c.right_id)
        for c in candidates
        if c.decision == "auto-merge"
    }
    categories = sorted({l.category for l in labels if l.category})
    metrics: dict[str, tuple[float, float, float]] = {}
    for cat in categories:
        cat_gold = {p for p in gold_pos if _category_of(entities, p[0]) == cat}
        cat_auto = {p for p in auto if _category_of(entities, p[0]) == cat}
        tp = len(cat_gold & cat_auto)
        fp = len(cat_auto - cat_gold)
        fn = len(cat_gold - cat_auto)
        precision = tp / (tp + fp) if (tp + fp) else 1.0
        recall = tp / (tp + fn) if (tp + fn) else 1.0
        f1 = (
            2 * precision * recall / (precision + recall)
            if (precision + recall)
            else 0.0
        )
        metrics[cat] = (round(precision, 4), round(recall, 4), round(f1, 4))
    blocking_recall = len(gold_pos & generated) / len(gold_pos) if gold_pos else 1.0
    return metrics, blocking_recall, candidates


def _category_of(entities: list[Entity], entity_id: str) -> str:
    for e in entities:
        if e.entity_id == entity_id:
            return e.category
    return "unknown"


def audit_findings(
    candidates: list[MergeCandidate],
    labels: list[PairLabel],
    entities: list[Entity],
) -> list[tuple[str, str]]:
    """Everything a human must see: wrong auto-merges, review-band
    candidates, gold-positive pairs that were blocked out or scored below
    the auto threshold. An empty list on a clean pack is the goal."""
    by_id = {e.entity_id: e for e in entities}
    gold_pos = {pair_key(l.left_id, l.right_id) for l in labels if l.same}
    gold_neg = {pair_key(l.left_id, l.right_id) for l in labels if not l.same}
    generated = generate_candidates(entities)
    findings: list[tuple[str, str]] = []
    for c in candidates:
        key = pair_key(c.left_id, c.right_id)
        names = f"{by_id[key[0]].display}  <->  {by_id[key[1]].display}"
        if c.decision == "auto-merge" and key in gold_neg:
            findings.append(("wrong auto-merge", f"{names}  score={c.score}"))
        elif c.decision == "review":
            veto = f"  veto={c.veto}" if c.veto else ""
            findings.append(("review needed", f"{names}  score={c.score}{veto}"))
    for key in sorted(gold_pos):
        names = f"{by_id[key[0]].display}  <->  {by_id[key[1]].display}"
        if key not in generated:
            findings.append(("blocking miss", names))
        elif key not in {
            pair_key(c.left_id, c.right_id)
            for c in candidates
            if c.decision == "auto-merge"
        }:
            findings.append(("below auto threshold", names))
    return findings


# ----------------------------------------------------------------------------
# 9. Sample packs: GOOD (must produce zero findings) and BAD (pathologies)
# ----------------------------------------------------------------------------

# GOOD pack: clean entities. Five gold-positive pairs must all be found
# (alef variant, shadda, digit folding, space-after-عبد, alias agreement)
# and no wrong merge or review-band candidate may appear.
GOOD_PACK: tuple[Entity, ...] = (
    Entity(
        "au-1",
        "author",
        "محمد بن إسماعيل البخاري",
        aliases=("الإمام البخاري",),
        year=256,
    ),
    Entity(
        "au-2",
        "author",
        "الإمام الجعفي",
        aliases=("محمَّد بن إسماعيل البخاري",),
        year=256,
    ),
    Entity("au-3", "author", "أحمد بن حنبل", year=241),
    Entity("au-4", "author", "يعقوب بن إسحاق الذهلي", year=275),
    Entity("bk-1", "book", "كتاب الإيمان"),
    Entity("bk-2", "book", "كتاب الايمان"),
    Entity("bk-3", "book", "كتاب التوحيد"),
    Entity("bk-4", "book", "طبعة دار الحديث ١٤٤٥"),
    Entity("bk-5", "book", "طبعة دار الحديث 1445"),
    Entity("nr-1", "narrator", "عبد الرحمن بن عوف", year=34),
    Entity("nr-2", "narrator", "عبدالرحمن بن عوف", year=34),
    Entity("nr-3", "narrator", "عبد الله بن مسعود", year=32),
    Entity("nr-4", "narrator", "محمَّد بن مسلم"),
    Entity("nr-5", "narrator", "محمد بن مسلم"),
)

GOOD_LABELS: tuple[PairLabel, ...] = (
    PairLabel(
        "au-1",
        "au-2",
        True,
        "author",
        "same author; alias of au-2 equals display of au-1",
    ),
    PairLabel("bk-1", "bk-2", True, "book", "alef-variant spelling"),
    PairLabel("bk-4", "bk-5", True, "book", "Arabic-Indic vs ASCII digits"),
    PairLabel("nr-1", "nr-2", True, "narrator", "space after عبد"),
    PairLabel("nr-4", "nr-5", True, "narrator", "shadda stripped"),
)

# BAD pack: the pathologies this pipeline must surface, not hide.
# - h-1/h-2: homonyms, identical display, conflicting death years. The
#   naive pipeline merges them; the veto must hold them for review.
# - z-1/z-2: two DIFFERENT books with one title extending the other. The
#   naive Jaro-Winkler cutoff merges them; the weighted score must not.
# - t-1/t-2: the same person under Arabic and Latin transliteration.
#   No shared trigram -> blocking never generates the pair (recall loss).
# - s-1/s-2: kunya-only record vs full name. Generated but scores below
#   the auto threshold — a real miss a human review queue should catch.
BAD_PACK: tuple[Entity, ...] = (
    Entity("h-1", "narrator", "محمد بن عبد الله", year=150),
    Entity("h-2", "narrator", "محمد بن عبد الله", year=200),
    Entity("s-1", "author", "الشافعي"),
    Entity("s-2", "author", "محمد بن إدريس الشافعي", year=204),
    Entity("t-1", "author", "ابن تيمية", year=728),
    Entity("t-2", "author", "Ibn Taymiyyah", year=728),
    Entity("z-1", "book", "كتاب الزهد"),
    Entity("z-2", "book", "كتاب الزهد الكبير"),
)

BAD_LABELS: tuple[PairLabel, ...] = (
    PairLabel(
        "h-1", "h-2", False, "narrator", "homonyms: identical names, 50 years apart"
    ),
    PairLabel("z-1", "z-2", False, "book", "distinct works, similar titles"),
    PairLabel("s-1", "s-2", True, "author", "kunya-only record of al-Shafi'i"),
    PairLabel("t-1", "t-2", True, "author", "Arabic vs Latin transliteration"),
)


# ----------------------------------------------------------------------------
# 10. Demo and self-checks
# ----------------------------------------------------------------------------


def run_bad_pack() -> None:
    entities = list(BAD_PACK)
    labels = list(BAD_LABELS)
    by_id = {e.entity_id: e for e in entities}

    print("=== BAD pack: naive pipeline (display string, loose JW cutoff) ===")
    naive_merges: list[tuple[str, str]] = []
    for a, b in sorted(generate_candidates(entities)):
        if naive_compare(by_id[a], by_id[b]) == "merge":
            naive_merges.append(pair_key(a, b))
    gold_pos = {pair_key(l.left_id, l.right_id) for l in labels if l.same}
    wrong = [p for p in naive_merges if p not in gold_pos]
    missed = sorted(gold_pos - set(naive_merges))
    for p in wrong:
        print(f"  WRONG merge: {by_id[p[0]].display}  <->  {by_id[p[1]].display}")
    for p in missed:
        print(f"  missed gold: {by_id[p[0]].display}  <->  {by_id[p[1]].display}")
    print(f"  naive: {len(wrong)} wrong merges, {len(missed)} missed merges")
    assert len(wrong) >= 2, (
        "naive pipeline should wrongly merge at least the homonyms and the near-title books"
    )
    assert len(missed) >= 2, (
        "naive pipeline should miss the transliteration and kunya pairs"
    )

    print()
    print("=== BAD pack: governed pipeline (weighted signals, veto, band) ===")
    metrics, blocking_recall, candidates = evaluate_pack(entities, labels)
    findings = audit_findings(candidates, labels, entities)
    for kind, detail in findings:
        print(f"  [{kind}] {detail}")
    print(f"  governed findings: {len(findings)}")
    print(f"  blocking recall on gold pairs: {blocking_recall:.2f}")
    kinds = {k for k, _ in findings}
    assert "review needed" in kinds, "vetoed homonyms must land in the review band"
    assert "blocking miss" in kinds, (
        "the transliteration pair must be reported as a blocking miss"
    )
    assert "below auto threshold" in kinds, (
        "the kunya-only pair must be reported below threshold"
    )
    auto_wrongs = [p for p in findings if p[0] == "wrong auto-merge"]
    assert not auto_wrongs, (
        "governed pipeline must not auto-merge any gold-negative pair"
    )
    assert blocking_recall < 1.0, (
        "the transliteration blocking gap must stay visible, not hidden"
    )


def run_good_pack() -> None:
    entities = list(GOOD_PACK)
    labels = list(GOOD_LABELS)
    metrics, blocking_recall, candidates = evaluate_pack(entities, labels)
    findings = audit_findings(candidates, labels, entities)
    auto = [c for c in candidates if c.decision == "auto-merge"]
    reviews = [c for c in candidates if c.decision == "review"]

    print("=== GOOD pack: governed pipeline ===")
    for cat, (p, r, f1) in metrics.items():
        print(f"  {cat}: precision={p:.2f} recall={r:.2f} F1={f1:.2f}")
    print(f"  blocking recall: {blocking_recall:.2f}")
    print(f"  auto-merges: {len(auto)} (all gold-positive)")
    print(f"  review: {len(reviews)}")
    print(f"  findings: {len(findings)}")
    print("GOOD pack clean")

    assert findings == [], f"GOOD pack must produce zero findings, got {findings}"
    assert len(auto) == len([l for l in labels if l.same]), (
        "every gold pair must auto-merge"
    )
    assert blocking_recall == 1.0, "every gold pair must be generated by blocking"
    for cat, (p, r, f1) in metrics.items():
        assert (p, r, f1) == (1.0, 1.0, 1.0), (
            f"{cat} metrics must be perfect, got {(p, r, f1)}"
        )


def check_similarities() -> None:
    """Lock the similarity primitives against known values. The identity
    case matters: a Jaro bug once made identical strings score 0.833,
    which silently pushed exact-match pairs out of the auto-merge band."""
    assert jaro("محمد", "محمد") == 1.0
    assert jaro_winkler("محمد", "محمد") == 1.0
    assert jaro_winkler("Ibn Taymiyyah", "Ibn Taymiyyah") == 1.0
    assert abs(jaro("MARTHA", "MARHTA") - 0.9444444) < 1e-6
    assert abs(jaro_winkler("MARTHA", "MARHTA") - 0.9611111) < 1e-6
    assert damerau_levenshtein("AB", "BA") == 1, "adjacent transposition costs 1"
    assert damerau_levenshtein("كتاب", "كتاب") == 0
    assert damerau_levenshtein_sim("كتاب", "كتاب") == 1.0
    assert char_ngram_jaccard("الإيمان", "الإيمان") == 1.0
    assert 0.0 < char_ngram_jaccard("كتاب الزهد", "كتاب الزهد الكبير") < 1.0
    assert token_set_jaccard("كتاب التوحيد", "كتاب التوحيد") == 1.0
    assert token_set_jaccard("كتاب التوحيد", "عقيدة") == 0.0


def check_normalizer() -> None:
    """The Arabic variant pairs the lecture promises this normalizer handles."""
    assert normalize_ar("كتاب الإيمان") == normalize_ar("كتاب الايمان")
    assert normalize_ar("محمد") == normalize_ar("محمَّد")
    assert normalize_ar("١٤٤٥") == normalize_ar("1445")
    assert normalize_ar("۱۴۴۵") == normalize_ar("1445")
    assert collapse_spaces(normalize_ar("عبد الرحمن بن عوف")) == collapse_spaces(
        normalize_ar("عبدالرحمن بن عوف")
    )
    assert normalize_ar("كـــتاب") == normalize_ar("كتاب")
    assert normalize_ar("مدرسة") != normalize_ar("مدرسه"), (
        "ta marbuta must NOT fold in the index copy"
    )
    probe = "مُحَمَّد بن إدريس الشَّافِعيّ"
    assert normalize_ar(normalize_ar(probe)) == normalize_ar(probe), (
        "normalizer must be idempotent"
    )


def check_canonization() -> None:
    entities = list(GOOD_PACK)
    candidates = run_pipeline(entities)
    canonical = canonize(candidates)
    au = [c for c in candidates if pair_key(c.left_id, c.right_id) == ("au-1", "au-2")]
    assert au and au[0].decision == "auto-merge"
    assert canonical["au-1"] == canonical["au-2"], (
        "merged records share one canonical id"
    )
    assert len(canonical["au-1"]) == 26, "canonical id is a ULID"
    table = build_alias_table(entities)
    surfaces = {a.surface for a in table["au-2"]}
    assert "محمَّد بن إسماعيل البخاري" in surfaces, (
        "alias table preserves the original surface"
    )
    assert all(
        a.normalizer_version == NORMALIZER_VERSION
        for rows in table.values()
        for a in rows
    )


def load_pair_file(path: str) -> tuple[list[Entity], list[PairLabel]]:
    """Load a labelled pair file: either a JSON array or JSONL, each record
    {"left": {"id"?, "display", "year"?, "aliases"?, "context"?},
     "right": {...}, "same": bool, "category": str}.

    Record identity comes from the optional "id" field, shared by every
    occurrence of the same record. Without ids each side of a label is its
    own record — deduping by display would merge homonyms and pre-answer
    the labels, which is the display-string anti-pattern this pipeline
    exists to avoid. Same-id on both sides of a label is rejected."""
    with open(path, encoding="utf-8-sig") as fh:  # tolerate a Windows BOM
        raw = fh.read().strip()
    if not raw:
        raise ValueError(f"empty pair file: {path}")
    try:
        data = json.loads(raw)
        if isinstance(data, dict):
            data = data.get("pairs", [])
        records = list(data)
    except json.JSONDecodeError:
        records = [json.loads(line) for line in raw.splitlines() if line.strip()]
    entities: dict[str, Entity] = {}
    labels: list[PairLabel] = []
    for i, rec in enumerate(records):
        category = str(rec.get("category", "unknown"))
        ids: list[str] = []
        for side in ("left", "right"):
            node = rec[side]
            display = str(node["display"])
            eid = str(node.get("id") or f"auto-{category}-{i}-{side}")
            if eid in entities and normalize_ar(entities[eid].display) != normalize_ar(
                display
            ):
                raise ValueError(
                    f"record '{eid}' reused with a different display: "
                    f"{entities[eid].display!r} vs {display!r}"
                )
            if eid not in entities:
                entities[eid] = Entity(
                    entity_id=eid,
                    category=category,
                    display=display,
                    aliases=tuple(node.get("aliases", ())),
                    year=node.get("year"),
                    context=node.get("context"),
                )
            ids.append(eid)
        if ids[0] == ids[1]:
            raise ValueError(
                f"label {i} places record '{ids[0]}' on both sides; "
                "a record cannot be compared with itself"
            )
        a, b = pair_key(ids[0], ids[1])
        labels.append(
            PairLabel(a, b, bool(rec["same"]), category, str(rec.get("note", "")))
        )
    return list(entities.values()), labels


def run_pair_file(path: str) -> int:
    entities, labels = load_pair_file(path)
    metrics, blocking_recall, candidates = evaluate_pack(entities, labels)
    findings = audit_findings(candidates, labels, entities)
    print(f"=== pair file: {path} ===")
    for cat, (p, r, f1) in metrics.items():
        print(f"  {cat}: precision={p:.2f} recall={r:.2f} F1={f1:.2f}")
    print(f"  blocking recall: {blocking_recall:.2f}")
    for kind, detail in findings:
        print(f"  [{kind}] {detail}")
    wrongs = [f for f in findings if f[0] == "wrong auto-merge"]
    print(f"  findings: {len(findings)} (wrong auto-merges: {len(wrongs)})")
    return 1 if wrongs else 0


def main(argv: list[str]) -> int:
    if len(argv) > 1:
        return run_pair_file(argv[1])
    check_similarities()
    check_normalizer()
    check_canonization()
    run_bad_pack()
    print()
    run_good_pack()
    print()
    print("all self-checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
