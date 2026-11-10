#!/usr/bin/env python3
"""Validate a CHAPTER_DATA document against the Study Studio contract.

The Study Studio engine reads one shape of data and nothing else. This
script is the gate that keeps a chapter file honest before it is inlined
into a single-file HTML studio.

It checks two things that plain JSON Schema validation does not catch
well on its own:

1. Structure. Required keys, types, and value shapes, matching
   schema/chapter.schema.json.
2. Referential integrity. Every id referenced from a section, a word, a
   lab, a figure, a flashcard, a quiz item, or a connection must resolve
   to an object that exists, and every node must be reachable.

Usage:
    python scripts/validate_chapter.py schema/example-chapter.json
    python scripts/validate_chapter.py --quiet schema/example-chapter.json

Exit codes:
    0  every check passed
    1  at least one check failed
    2  the file could not be read or parsed
"""

from __future__ import annotations

import json
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

# ---- Contract constants ----

TOP_LEVEL_KEYS = (
    "meta",
    "sections",
    "glossary",
    "conceptMap",
    "labs",
    "figures",
    "flashcards",
    "quiz",
    "collocations",
    "connections",
)

META_KEYS = (
    "chapterId",
    "title",
    "subtitle",
    "sourceTitle",
    "sourceType",
    "sourceLocator",
    "license",
    "attribution",
    "language",
    "estMinutes",
    "conceptCount",
)

SOURCE_TYPES = ("book", "roadmap", "paper", "repo-doc", "original")
LICENSES = ("personal-study", "CC-BY-4.0", "public-domain", "MIT")
LAB_KINDS = (
    "tokenizer",
    "embedding",
    "attention",
    "sampling",
    "rag-pipeline",
    "training",
    "quantization",
    "metrics",
    "cost-latency",
    "generic",
)
QUIZ_TYPES = (
    "mcq",
    "true-false",
    "order",
    "match",
    "fill-code",
    "spot-mistake",
    "explain",
)
SIMULATION_NOTE = "Illustrative simulation, not real model output."

ID_PREFIXES = {
    "sections": "s",
    "glossary": "w",
    "labs": "l",
    "figures": "f",
    "flashcards": "k",
    "quiz": "q",
    "conceptMap.nodes": "c",
}

# ---- Result types ----


@dataclass
class Finding:
    """One validation problem, with the place it was found."""

    severity: str
    code: str
    location: str
    message: str


@dataclass
class Report:
    findings: list[Finding] = field(default_factory=list)
    checks: int = 0

    def fail(self, code: str, location: str, message: str) -> None:
        self.findings.append(Finding("error", code, location, message))

    def warn(self, code: str, location: str, message: str) -> None:
        self.findings.append(Finding("warning", code, location, message))

    @property
    def errors(self) -> list[Finding]:
        return [f for f in self.findings if f.severity == "error"]

    @property
    def warnings(self) -> list[Finding]:
        return [f for f in self.findings if f.severity == "warning"]


# ---- Helpers ----


def _is_str(value: Any) -> bool:
    return isinstance(value, str)


def _is_num(value: Any) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool)


def _require_keys(obj: Any, keys: tuple[str, ...], where: str, report: Report) -> bool:
    """Every key present and non-empty (strings) or non-None."""
    if not isinstance(obj, dict):
        report.fail(
            "SCHEMA_TYPE", where, f"expected an object, found {type(obj).__name__}"
        )
        return False
    ok = True
    for key in keys:
        if key not in obj:
            report.fail("SCHEMA_MISSING", f"{where}.{key}", "required key is missing")
            ok = False
        elif isinstance(obj[key], str) and not obj[key].strip():
            report.fail("SCHEMA_EMPTY", f"{where}.{key}", "required string is empty")
            ok = False
    return ok


def _require_enum(
    obj: dict[str, Any], key: str, allowed: tuple[str, ...], where: str, report: Report
) -> None:
    value = obj.get(key)
    if value is None:
        return
    if value not in allowed:
        report.fail(
            "SCHEMA_ENUM",
            f"{where}.{key}",
            f"value {value!r} is not one of {', '.join(allowed)}",
        )


def _check_id(obj: dict[str, Any], prefix: str, where: str, report: Report) -> None:
    value = obj.get("id")
    if not isinstance(value, str):
        return
    if not value.startswith(prefix) or not value[len(prefix) :].isdigit():
        report.fail(
            "SCHEMA_ID", f"{where}.id", f"id {value!r} must look like {prefix}<digits>"
        )


# ---- Structural checks ----


def check_meta(data: dict[str, Any], report: Report) -> None:
    meta = data.get("meta")
    if not _require_keys(meta, META_KEYS, "meta", report):
        return
    assert isinstance(meta, dict)
    _require_enum(meta, "sourceType", SOURCE_TYPES, "meta", report)
    _require_enum(meta, "license", LICENSES, "meta", report)
    _require_enum(meta, "language", ("en", "ar", "en-ar"), "meta", report)
    if not _is_num(meta.get("estMinutes")):
        report.fail("SCHEMA_TYPE", "meta.estMinutes", "expected a number")
    if not _is_num(meta.get("conceptCount")):
        report.fail("SCHEMA_TYPE", "meta.conceptCount", "expected a number")


def check_sections(sections: Any, report: Report) -> None:
    if not isinstance(sections, list) or not sections:
        report.fail("SCHEMA_TYPE", "sections", "expected a non-empty array")
        return
    for index, section in enumerate(sections):
        where = f"sections[{index}]"
        if not _require_keys(
            section,
            (
                "id",
                "title",
                "order",
                "level",
                "paragraphs",
                "keySentences",
                "takeaways",
                "studyAid",
                "confusion",
                "prediction",
            ),
            where,
            report,
        ):
            continue
        assert isinstance(section, dict)
        _check_id(section, "s", where, report)
        paragraphs = section.get("paragraphs")
        if not isinstance(paragraphs, list) or not paragraphs:
            report.fail(
                "SCHEMA_TYPE", f"{where}.paragraphs", "expected a non-empty array"
            )
        else:
            for p_index, paragraph in enumerate(paragraphs):
                p_where = f"{where}.paragraphs[{p_index}]"
                if not isinstance(paragraph, dict):
                    report.fail("SCHEMA_TYPE", p_where, "expected an object")
                    continue
                if "text" not in paragraph:
                    report.fail(
                        "SCHEMA_MISSING", f"{p_where}.text", "required key is missing"
                    )
                _require_enum(
                    paragraph,
                    "kind",
                    ("text", "code", "list", "quote", "formula"),
                    p_where,
                    report,
                )
                if paragraph.get("kind") == "list" and not paragraph.get("items"):
                    report.fail(
                        "SCHEMA_MISSING",
                        f"{p_where}.items",
                        "a list paragraph needs items",
                    )
                if paragraph.get("kind") == "code" and not paragraph.get("code"):
                    report.fail(
                        "SCHEMA_MISSING",
                        f"{p_where}.code",
                        "a code paragraph needs code",
                    )
                if paragraph.get("kind") == "formula" and not paragraph.get("formula"):
                    report.fail(
                        "SCHEMA_MISSING",
                        f"{p_where}.formula",
                        "a formula paragraph needs formula",
                    )
        study_aid = section.get("studyAid")
        if isinstance(study_aid, dict):
            _require_keys(study_aid, ("whyItMatters",), f"{where}.studyAid", report)
            if study_aid.get("badge") != "AI":
                report.fail(
                    "SCHEMA_BADGE",
                    f"{where}.studyAid.badge",
                    "study aids must carry the AI badge",
                )
        confusion = section.get("confusion")
        if isinstance(confusion, dict):
            _require_keys(
                confusion,
                ("simpleEnglish", "simpleArabic", "analogy"),
                f"{where}.confusion",
                report,
            )
        prediction = section.get("prediction")
        if isinstance(prediction, dict):
            _require_keys(
                prediction, ("question", "answer"), f"{where}.prediction", report
            )


def check_glossary(glossary: Any, report: Report) -> None:
    if not isinstance(glossary, list):
        report.fail("SCHEMA_TYPE", "glossary", "expected an array")
        return
    for index, entry in enumerate(glossary):
        where = f"glossary[{index}]"
        if not _require_keys(
            entry, ("id", "term", "meaningEn", "meaningAr", "wordType"), where, report
        ):
            continue
        assert isinstance(entry, dict)
        _check_id(entry, "w", where, report)
        _require_enum(
            entry,
            "wordType",
            ("noun", "verb", "adjective", "adverb", "phrase"),
            where,
            report,
        )


def check_concept_map(concept_map: Any, report: Report) -> None:
    if not isinstance(concept_map, dict):
        report.fail("SCHEMA_TYPE", "conceptMap", "expected an object")
        return
    nodes = concept_map.get("nodes")
    edges = concept_map.get("edges")
    if not isinstance(nodes, list) or not nodes:
        report.fail("SCHEMA_TYPE", "conceptMap.nodes", "expected a non-empty array")
        return
    if not isinstance(edges, list):
        report.fail("SCHEMA_TYPE", "conceptMap.edges", "expected an array")
        return
    for index, node in enumerate(nodes):
        where = f"conceptMap.nodes[{index}]"
        if not _require_keys(node, ("id", "label", "kind"), where, report):
            continue
        assert isinstance(node, dict)
        _check_id(node, "c", where, report)
        _require_enum(node, "kind", ("core", "supporting", "advanced"), where, report)
    for index, edge in enumerate(edges):
        where = f"conceptMap.edges[{index}]"
        if not _require_keys(edge, ("from", "to", "relation"), where, report):
            continue


def check_labs(labs: Any, report: Report) -> None:
    if not isinstance(labs, list):
        report.fail("SCHEMA_TYPE", "labs", "expected an array")
        return
    for index, lab in enumerate(labs):
        where = f"labs[{index}]"
        if not _require_keys(
            lab,
            (
                "id",
                "title",
                "goal",
                "controls",
                "tasks",
                "takeawayEn",
                "takeawayAr",
                "simulationNote",
            ),
            where,
            report,
        ):
            continue
        assert isinstance(lab, dict)
        _check_id(lab, "l", where, report)
        _require_enum(lab, "kind", LAB_KINDS, where, report)
        if lab.get("simulationNote") != SIMULATION_NOTE:
            report.fail(
                "LAB_NOTE",
                f"{where}.simulationNote",
                f"must be exactly {SIMULATION_NOTE!r} so no lab looks like measured output",
            )
        tasks = lab.get("tasks")
        if not isinstance(tasks, list) or len(tasks) != 3:
            report.fail(
                "LAB_TASKS", f"{where}.tasks", "a lab needs exactly three guided tasks"
            )
        else:
            for t_index, task in enumerate(tasks):
                t_where = f"{where}.tasks[{t_index}]"
                if not isinstance(task, dict):
                    report.fail("SCHEMA_TYPE", t_where, "expected an object")
                    continue
                _require_keys(task, ("prompt", "check"), t_where, report)
        controls = lab.get("controls")
        if not isinstance(controls, list):
            report.fail("SCHEMA_TYPE", f"{where}.controls", "expected an array")


def check_figures(figures: Any, report: Report) -> None:
    if not isinstance(figures, list):
        report.fail("SCHEMA_TYPE", "figures", "expected an array")
        return
    for index, figure in enumerate(figures):
        where = f"figures[{index}]"
        if not _require_keys(
            figure,
            ("id", "title", "svg", "captionEn", "captionAr", "steps", "hotspots"),
            where,
            report,
        ):
            continue
        assert isinstance(figure, dict)
        _check_id(figure, "f", where, report)
        svg = figure.get("svg", "")
        if _is_str(svg):
            lowered = svg.lower()
            if "<svg" not in lowered:
                report.fail(
                    "FIGURE_SVG", f"{where}.svg", "svg must contain inline SVG markup"
                )
            for banned in ("<script", "url(http", "onload=", "onclick="):
                if banned in lowered:
                    report.fail(
                        "FIGURE_SVG",
                        f"{where}.svg",
                        f"svg must not contain {banned!r} (the studio is one offline file)",
                    )
        steps = figure.get("steps")
        if not isinstance(steps, list) or not steps:
            report.fail(
                "FIGURE_STEPS", f"{where}.steps", "a figure needs at least one step"
            )
        else:
            for s_index, step in enumerate(steps):
                s_where = f"{where}.steps[{s_index}]"
                if not isinstance(step, dict):
                    report.fail("SCHEMA_TYPE", s_where, "expected an object")
                    continue
                _require_keys(
                    step, ("narrativeEn", "narrativeAr", "highlight"), s_where, report
                )


def check_flashcards(flashcards: Any, report: Report) -> None:
    if not isinstance(flashcards, list):
        report.fail("SCHEMA_TYPE", "flashcards", "expected an array")
        return
    for index, card in enumerate(flashcards):
        where = f"flashcards[{index}]"
        if not _require_keys(card, ("id", "front", "back", "kind"), where, report):
            continue
        assert isinstance(card, dict)
        _check_id(card, "k", where, report)
        _require_enum(card, "kind", ("term", "en-ar", "code"), where, report)


def check_quiz(quiz: Any, report: Report) -> None:
    if not isinstance(quiz, list):
        report.fail("SCHEMA_TYPE", "quiz", "expected an array")
        return
    for index, item in enumerate(quiz):
        where = f"quiz[{index}]"
        if not _require_keys(
            item,
            ("id", "type", "prompt", "answer", "explanationEn", "explanationAr"),
            where,
            report,
        ):
            continue
        assert isinstance(item, dict)
        _check_id(item, "q", where, report)
        _require_enum(item, "type", QUIZ_TYPES, where, report)
        answer = item.get("answer")
        if not isinstance(answer, list) or not answer:
            report.fail(
                "QUIZ_ANSWER", f"{where}.answer", "answer must be a non-empty array"
            )
            continue
        if item.get("type") in ("mcq", "true-false", "spot-mistake"):
            options = item.get("options")
            if not isinstance(options, list) or not options:
                report.fail(
                    "QUIZ_OPTIONS",
                    f"{where}.options",
                    "this question type needs options",
                )
            else:
                for option in answer:
                    if option not in options:
                        report.fail(
                            "QUIZ_ANSWER",
                            f"{where}.answer",
                            f"answer {option!r} is not among the offered options",
                        )
        if item.get("type") == "true-false" and set(item.get("options", [])) != {
            "True",
            "False",
        }:
            report.fail(
                "QUIZ_OPTIONS",
                f"{where}.options",
                "true-false needs exactly True and False",
            )
        if item.get("type") == "explain" and not item.get("answerText"):
            report.warn(
                "QUIZ_ANSWER_TEXT",
                f"{where}.answerText",
                "an explain question should carry a self-check reference answer",
            )


def check_collocations(collocations: Any, report: Report) -> None:
    if not isinstance(collocations, list):
        report.fail("SCHEMA_TYPE", "collocations", "expected an array")
        return
    for index, collocation in enumerate(collocations):
        where = f"collocations[{index}]"
        _require_keys(collocation, ("phrase", "meaningAr"), where, report)


def check_connections(connections: Any, report: Report) -> None:
    if not isinstance(connections, list):
        report.fail("SCHEMA_TYPE", "connections", "expected an array")
        return
    for index, connection in enumerate(connections):
        where = f"connections[{index}]"
        if not _require_keys(
            connection, ("chapterId", "title", "conceptIds"), where, report
        ):
            continue
        assert isinstance(connection, dict)
        if (
            not isinstance(connection.get("conceptIds"), list)
            or not connection["conceptIds"]
        ):
            report.fail(
                "SCHEMA_TYPE", f"{where}.conceptIds", "expected a non-empty array"
            )


# ---- Referential integrity ----


def check_references(data: dict[str, Any], report: Report) -> None:
    """Every cross-object reference must resolve to something that exists."""
    sections = data.get("sections") or []
    glossary = data.get("glossary") or []
    labs = data.get("labs") or []
    figures = data.get("figures") or []
    flashcards = data.get("flashcards") or []
    quiz = data.get("quiz") or []
    concept_map = data.get("conceptMap") or {}
    nodes = concept_map.get("nodes") or []
    edges = concept_map.get("edges") or []

    word_ids = {e.get("id") for e in glossary if isinstance(e, dict)}
    lab_ids = {x.get("id") for x in labs if isinstance(x, dict)}
    node_ids = {n.get("id") for n in nodes if isinstance(n, dict)}
    section_ids = {s.get("id") for s in sections if isinstance(s, dict)}

    def resolve(ref: Any, pool: set[Any], label: str, where: str) -> None:
        if ref is None:
            return
        if ref not in pool:
            report.fail("REF_MISSING", where, f"{label} {ref!r} does not exist")

    for index, section in enumerate(sections):
        if not isinstance(section, dict):
            continue
        where = f"sections[{index}]"
        for ref in section.get("wordIds", []) or []:
            resolve(ref, word_ids, "word", f"{where}.wordIds")
        resolve(section.get("sectionId"), section_ids, "section", f"{where}.sectionId")

    for index, entry in enumerate(glossary):
        if not isinstance(entry, dict):
            continue
        where = f"glossary[{index}]"
        resolve(entry.get("conceptId"), node_ids, "concept", f"{where}.conceptId")
        resolve(entry.get("labId"), lab_ids, "lab", f"{where}.labId")

    for index, node in enumerate(nodes):
        if not isinstance(node, dict):
            continue
        where = f"conceptMap.nodes[{index}]"
        resolve(node.get("sectionId"), section_ids, "section", f"{where}.sectionId")
        resolve(node.get("labId"), lab_ids, "lab", f"{where}.labId")
        for ref in node.get("wordIds", []) or []:
            resolve(ref, word_ids, "word", f"{where}.wordIds")

    for index, edge in enumerate(edges):
        if not isinstance(edge, dict):
            continue
        where = f"conceptMap.edges[{index}]"
        resolve(edge.get("from"), node_ids, "concept", f"{where}.from")
        resolve(edge.get("to"), node_ids, "concept", f"{where}.to")

    for index, figure in enumerate(figures):
        if not isinstance(figure, dict):
            continue
        where = f"figures[{index}]"
        svg_ids = _svg_element_ids(figure.get("svg", ""))
        for s_index, step in enumerate(figure.get("steps", []) or []):
            if not isinstance(step, dict):
                continue
            for ref in step.get("highlight", []) or []:
                if svg_ids and ref not in svg_ids:
                    report.fail(
                        "REF_MISSING",
                        f"{where}.steps[{s_index}].highlight",
                        f"element id {ref!r} is not in the svg (found: {', '.join(sorted(svg_ids)) or 'none'})",
                    )
        for h_index, hotspot in enumerate(figure.get("hotspots", []) or []):
            if not isinstance(hotspot, dict):
                continue
            resolve(
                hotspot.get("target"),
                svg_ids,
                "svg element",
                f"{where}.hotspots[{h_index}].target",
            )
        for ref in figure.get("buildOrder", []) or []:
            resolve(ref, svg_ids, "svg element", f"{where}.buildOrder")

    for index, card in enumerate(flashcards):
        if not isinstance(card, dict):
            continue
        resolve(
            card.get("conceptId"), node_ids, "concept", f"flashcards[{index}].conceptId"
        )

    for index, item in enumerate(quiz):
        if not isinstance(item, dict):
            continue
        resolve(item.get("conceptId"), node_ids, "concept", f"quiz[{index}].conceptId")

    for index, connection in enumerate(data.get("connections") or []):
        if not isinstance(connection, dict):
            continue
        for ref in connection.get("conceptIds", []) or []:
            resolve(ref, node_ids, "concept", f"connections[{index}].conceptIds")

    # Every concept node should be reachable from another node or be a root
    # the learning path lists, otherwise the map has orphan islands.
    linked = {e.get("from") for e in edges if isinstance(e, dict)}
    linked |= {e.get("to") for e in edges if isinstance(e, dict)}
    path = concept_map.get("learningPath") or []
    for node_id in node_ids:
        if node_id not in linked and node_id not in path:
            report.warn(
                "REF_ORPHAN",
                "conceptMap",
                f"concept {node_id!r} has no edge and is not in the learning path",
            )


def _svg_element_ids(svg: str) -> set[str]:
    """Collect element ids from inline SVG markup."""
    ids: set[str] = set()
    if not isinstance(svg, str):
        return ids
    marker = 'id="'
    index = svg.find(marker)
    while index != -1:
        start = index + len(marker)
        end = svg.find('"', start)
        if end == -1:
            break
        ids.add(svg[start:end])
        index = svg.find(marker, end)
    return ids


def check_unique_ids(data: dict[str, Any], report: Report) -> None:
    """Ids are unique inside each collection."""
    collections = {
        "sections": data.get("sections") or [],
        "glossary": data.get("glossary") or [],
        "labs": data.get("labs") or [],
        "figures": data.get("figures") or [],
        "flashcards": data.get("flashcards") or [],
        "quiz": data.get("quiz") or [],
        "conceptMap.nodes": (data.get("conceptMap") or {}).get("nodes") or [],
    }
    for name, items in collections.items():
        seen: set[Any] = set()
        for item in items:
            if not isinstance(item, dict):
                continue
            value = item.get("id")
            if value in seen:
                report.fail(
                    "ID_DUPLICATE", name, f"id {value!r} appears more than once"
                )
            seen.add(value)


# ---- Entry point ----


def validate(data: Any) -> Report:
    report = Report()
    if not isinstance(data, dict):
        report.fail(
            "SCHEMA_TYPE", "<root>", "the chapter file must contain a JSON object"
        )
        return report

    for key in TOP_LEVEL_KEYS:
        if key not in data:
            report.fail("SCHEMA_MISSING", key, "required top-level key is missing")

    report.checks += len(TOP_LEVEL_KEYS)
    check_meta(data, report)
    check_sections(data.get("sections"), report)
    check_glossary(data.get("glossary"), report)
    check_concept_map(data.get("conceptMap"), report)
    check_labs(data.get("labs"), report)
    check_figures(data.get("figures"), report)
    check_flashcards(data.get("flashcards"), report)
    check_quiz(data.get("quiz"), report)
    check_collocations(data.get("collocations"), report)
    check_connections(data.get("connections"), report)
    check_unique_ids(data, report)
    check_references(data, report)
    return report


def main(argv: list[str]) -> int:
    quiet = False
    paths: list[str] = []
    for arg in argv[1:]:
        if arg in ("--quiet", "-q"):
            quiet = True
        elif arg in ("--help", "-h"):
            print(__doc__)
            return 0
        else:
            paths.append(arg)

    if not paths:
        print("usage: validate_chapter.py [--quiet] <chapter.json> [...]")
        return 2

    exit_code = 0
    for raw in paths:
        path = Path(raw)
        if not path.is_file():
            print(f"[FAIL] {raw}: file not found")
            exit_code = 1
            continue
        try:
            data = json.loads(path.read_text(encoding="utf-8-sig"))
        except (OSError, json.JSONDecodeError) as exc:
            print(f"[FAIL] {raw}: could not read or parse: {exc}")
            exit_code = 1
            continue

        report = validate(data)
        errors = report.errors
        warnings = report.warnings
        if errors:
            print(f"[FAIL] {raw}: {len(errors)} error(s), {len(warnings)} warning(s)")
            for finding in errors:
                print(
                    f"  ERROR   {finding.code}  {finding.location}: {finding.message}"
                )
            exit_code = 1
        elif not quiet:
            print(f"[PASS] {raw}: contract satisfied")
        if warnings and not quiet:
            for finding in warnings:
                print(
                    f"  WARN    {finding.code}  {finding.location}: {finding.message}"
                )

    return exit_code


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
