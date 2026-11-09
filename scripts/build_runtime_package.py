#!/usr/bin/env python3
"""Build a deterministic, derived runtime package. Never edits authoring inputs.

Drafts are development artifacts, not release bundles. T02/T03/T04/T09/T12
must supply their missing evidence before a release builder can be enabled.
"""
import argparse
import hashlib
import json
from pathlib import Path
import sqlite3
import sys
import unicodedata
import uuid
sys.dont_write_bytecode = True
import validate_authoring_batch as authoring
from localization_support import is_translation, localized_text
from translation_overlays import apply_overlays, load_overlays

ROOT = Path(__file__).resolve().parents[1]
GENERATOR_VERSION = "1.1.0"
RELEASE_BLOCKERS = ["source-row-reconciliation", "complete-kana", "candidate-dependencies",
                    "reviewed-speech-contexts", "19-language-review", "editorial-and-rights-acceptance"]


def encoded(value):
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n").encode()


def digest(data):
    return hashlib.sha256(data).hexdigest()


def normalize(text):
    # Preserve Japanese dakuten; fold accents only on Latin characters.
    text = unicodedata.normalize("NFKC", text).casefold().replace("đ", "d")
    result = []
    for char in unicodedata.normalize("NFC", text):
        if "LATIN" in unicodedata.name(char, ""):
            result.append("".join(c for c in unicodedata.normalize("NFD", char)
                                  if not unicodedata.combining(c)))
        elif 0x30A1 <= ord(char) <= 0x30F6:
            result.append(chr(ord(char) - 0x60))
        else:
            result.append(char)
    return "".join(result).strip()


def text_fields(value, locale=None):
    """Index only display/search fields; never source refs/editorial prose."""
    if isinstance(value, dict):
        if is_translation(value):
            # Exact same per-field policy as LocalizedContent: blank is missing,
            # English only fallback, never a different authored locale.
            selected = localized_text(value, locale)
            return [selected] if locale and selected is not None else []
        out = []
        for key, child in value.items():
            if key in {"japanese", "segments", "base", "ruby", "kana_reading", "forms",
                       "search_aliases", "romaji", "character", "han_viet", "on_readings",
                       "kun_readings", "templates", "pieces", "turns", "title", "meanings",
                       "text", "translation", "explanation", "notes", "scenario"}:
                if key == "segments":
                    out += ["".join(s["base"] for s in child),
                            "".join(s.get("ruby", s["base"]) for s in child)]
                elif key == "pieces":
                    out += ["".join(p["value"] for p in child if p["kind"] == "literal")]
                else:
                    out += text_fields(child, locale)
        return out
    if isinstance(value, list):
        return [s for item in value for s in text_fields(item, locale)]
    return [value] if isinstance(value, str) and value else []


def project(value):
    excluded = {"source_refs", "origin", "editorial_key", "review_state", "coverage",
                "format_version", "artifact_type", "language_coverage", "reading_scope",
                "publisher_lesson_milestone", "reference_lesson_scope", "relationship"}
    if isinstance(value, dict):
        return {k: project(v) for k, v in value.items() if k not in excluded}
    if isinstance(value, list):
        return [project(v) for v in value]
    return value


def build(output, mode="draft", locale_overlays=None):
    if mode != "draft":
        raise ValueError("Release blocked: " + ", ".join(RELEASE_BLOCKERS))
    if output.exists() and any(output.iterdir()):
        raise ValueError("Output must be empty; package replacement is an explicit caller operation")
    output.mkdir(parents=True, exist_ok=True)
    hashes = {}

    def read(path):
        raw = (ROOT / path).read_bytes()
        hashes[path] = digest(raw)
        return json.loads(raw)

    lessons = [read(f"docs/content-authoring/lesson-{n:02}.json") for n in range(1, 51)]
    units = [read(f"docs/content-authoring/kanji/unit-{n:02}.json") for n in range(1, 51)]
    sets = [read(f"docs/content-authoring/kanji/characters-{level}.json") for level in ("n5", "n4")]
    characters = [c for dataset in sets for c in dataset["entries"]]
    character_levels = {c["id"]: dataset["source_level_label"] for dataset in sets for c in dataset["entries"]}
    catalog = read("docs/reference-inventory/catalog.json")
    # Reuse the canonical structural validators instead of relaxing their rules in
    # a second import path. They do not constitute linguistic/release acceptance.
    authoring.lessons.validate_payload(lessons, read("docs/content-authoring/authoring.schema.json"),
        catalog, read("docs/content-authoring/source-checks.json"))
    authoring.validate_kanji(sets, units, catalog,
        read("docs/content-authoring/kanji/kanji-character-set.schema.json"),
        read("docs/content-authoring/kanji/kanji-unit.schema.json"), True)
    authoring.validate_correction_ledger(read("docs/content-authoring/source-corrections.json"), sets, catalog, lessons)
    # Base VI/EN schemas/review fingerprints remain intact. New locale sidecars
    # bind to exact owner IDs/content revisions and project into the same fields.
    documents = {f"docs/content-authoring/lesson-{n:02}.json": value for n, value in enumerate(lessons, 1)}
    documents.update({f"docs/content-authoring/kanji/unit-{n:02}.json": value for n, value in enumerate(units, 1)})
    documents.update({f"docs/content-authoring/kanji/characters-{level}.json": value for level, value in zip(("n5", "n4"), sets)})
    overlay_paths, overlays = load_overlays(ROOT)
    if locale_overlays is not None:
        # Offline verifier seam: synthetic text is never written to authored sources.
        overlays = locale_overlays
        overlay_paths = []
        hashes["fixtures/localization-overlays.json"] = digest(encoded(overlays))
    for path in overlay_paths: hashes[str(path.relative_to(ROOT))] = digest(path.read_bytes())
    # Validate kana/candidate references too, without bundling those authoring-only datasets.
    for name in ("kana/inventory.json", "sentence-bank/bank.json", "sentence-bank/bound-contexts.json"):
        path = "docs/content-authoring/" + name
        documents[path] = json.loads((ROOT / path).read_bytes())
    for overlay in overlays:
        for row in overlay.get('fields', []):
            path = row.get('path')
            if path in documents and path not in hashes:
                hashes[path] = digest((ROOT / path).read_bytes())
    projected = apply_overlays(documents, overlays)
    lessons = [projected[f"docs/content-authoring/lesson-{n:02}.json"] for n in range(1, 51)]
    units = [projected[f"docs/content-authoring/kanji/unit-{n:02}.json"] for n in range(1, 51)]
    sets = [projected[f"docs/content-authoring/kanji/characters-{level}.json"] for level in ("n5", "n4")]
    characters = [c for dataset in sets for c in dataset["entries"]]
    hashes["scripts/build_runtime_package.py"] = digest(Path(__file__).read_bytes())
    for path in ("scripts/validate_authoring_samples.py", "scripts/validate_authoring_batch.py",
                 "scripts/localization_support.py", "scripts/translation_overlays.py"):
        hashes[path] = digest((ROOT / path).read_bytes())
    manifest = dict(schemaVersion=1, generatorVersion=GENERATOR_VERSION, mode=mode,
                    sourceInputHashes=hashes, authoredLanguages=sorted({"en", "vi"} | {
                        overlay['locale'] for overlay in overlays if any(row['state'] == 'reviewed'
                            and row['path'] in hashes and '/kana/' not in row['path']
                            and '/sentence-bank/' not in row['path'] for row in overlay['fields'])}),
                    requiredLanguages=lessons[0]["language_coverage"]["required_for_release"],
                    releaseBlockers=RELEASE_BLOCKERS, orderedLessons={"N5": [], "N4": []},
                    entities={}, shards={}, unitMilestones={}, candidateIndexVersion=0,
                    speechIndexVersion=0, searchIndexVersion=1)
    rows = []
    glyphs = {c["character"]: c["id"] for c in characters}
    lesson_numbers = {l["reference_lesson_number"]: l["id"] for l in lessons}
    catalog_units = {u["number"]: u for u in catalog["kanji_units"]}

    def shard(kind, root, level, number=None):
        path = f"shards/{root['id']}.json"
        payload = project(root)
        if kind == "unit":
            payload["characterIDs"] = [glyphs[g] for g in root["character_glyphs"]]
        body = encoded(dict(schemaVersion=1, rootID=root["id"], content=payload))
        (output / "shards").mkdir(exist_ok=True)
        (output / path).write_bytes(body)
        manifest["shards"][path] = dict(sha256=digest(body), bytes=len(body))

        def entity(item, item_kind, pointer, target=None):
            identifier = item["id"]
            uuid.UUID(identifier)
            if identifier in manifest["entities"]:
                raise ValueError("Duplicate authored ID " + identifier)
            manifest["entities"][identifier] = dict(kind=item_kind, shard=path, pointer=pointer,
                rootID=root["id"], level=level, number=number, targetID=target or identifier)
            if item_kind in {"vocabulary", "grammar", "pattern", "dialogue", "kanji", "example", "word"}:
                rows.append((identifier, target or identifier, root["id"], item_kind, item))

        entity(root, kind, "")
        if kind == "lesson":
            for key, child_kind in [("vocabulary", "vocabulary"), ("grammar_points", "grammar"),
                                    ("sentence_patterns", "pattern"), ("examples", "example"),
                                    ("dialogues", "dialogue")]:
                for i, item in enumerate(root[key]):
                    entity(item, child_kind, f"/{key}/{i}", item.get("pattern_id"))
        else:
            for key in ("word_examples", "examples"):
                for i, item in enumerate(root.get(key, [])):
                    entity(item, "word", f"/{key}/{i}", root["id"])

    for l in lessons:
        manifest["orderedLessons"][l["source_level_label"]].append(l["id"])
        shard("lesson", l, l["source_level_label"], l["reference_lesson_number"])
    for u in units:
        number = u["reference_unit_number"]
        milestone = catalog_units[number]["publisher_lesson_milestone"]["global_lesson_number"]
        manifest["unitMilestones"][u["id"]] = lesson_numbers[milestone]
        shard("unit", u, u["source_level_label"], number)
    for c in characters:
        shard("kanji", c, character_levels[c["id"]])
    # Check authored references before emitting any apparently usable manifest.
    def refs(value):
        if isinstance(value, dict):
            for k, v in value.items():
                if k.endswith("_id") and k in {"grammar_point_id", "pattern_id"}:
                    if v not in manifest["entities"]:
                        raise ValueError("Missing mandatory reference " + v)
                elif k == "grammar_point_ids":
                    if any(i not in manifest["entities"] for i in v):
                        raise ValueError("Missing grammar reference")
                refs(v)
        elif isinstance(value, list):
            for v in value:
                refs(v)
    refs(lessons)
    db = sqlite3.connect(output / "search.sqlite")
    db.executescript("""
      PRAGMA user_version=1;
      CREATE TABLE metadata(key TEXT PRIMARY KEY, value TEXT NOT NULL);
      CREATE TABLE results(id TEXT PRIMARY KEY, targetID TEXT NOT NULL, rootID TEXT NOT NULL,
                           kind TEXT NOT NULL, authoredOrder INTEGER NOT NULL);
      CREATE TABLE fields(resultID TEXT NOT NULL REFERENCES results(id), locale TEXT NOT NULL,
                          original TEXT NOT NULL, normalized TEXT NOT NULL);
      CREATE INDEX lookup ON fields(locale, normalized);
    """)
    content_version = "draft-" + digest(encoded(hashes))[:20]
    manifest["contentVersion"] = content_version
    db.executemany("INSERT INTO metadata VALUES(?,?)", [("contentVersion", content_version),
                                                       ("normalizationVersion", "1")])
    for order, (identifier, target, root, kind, item) in enumerate(rows):
        db.execute("INSERT INTO results VALUES(?,?,?,?,?)", (identifier, target, root, kind, order))
        for locale in ["*"] + manifest["requiredLanguages"]:
            fields = text_fields(item, locale if locale != "*" else None)
            # Common Japanese fields and localized fields are stored separately.
            if locale != "*":
                common = set(text_fields(item))
                fields = [f for f in fields if f not in common]
            db.executemany("INSERT INTO fields VALUES(?,?,?,?)",
                           [(identifier, locale, f, normalize(f)) for f in sorted(set(fields)) if normalize(f)])
    db.commit()
    db.execute("VACUUM")
    db.close()
    raw = (output / "search.sqlite").read_bytes()
    manifest["searchIndex"] = dict(path="search.sqlite", sha256=digest(raw), bytes=len(raw))
    (output / "manifest.json").write_bytes(encoded(manifest))
    return manifest


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--mode", choices=["draft", "release"], default="draft")
    args = parser.parse_args()
    try:
        m = build(args.output, args.mode)
    except (ValueError, KeyError) as e:
        parser.error(str(e))
    print(f"Built {m['contentVersion']}: {len(m['shards'])} shards, {len(m['entities'])} stable IDs; DRAFT ONLY")


if __name__ == "__main__":
    main()
