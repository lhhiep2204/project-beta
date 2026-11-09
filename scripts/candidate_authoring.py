"""T04 authoring utilities. These are offline review tools, not the app selector."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
DIRECTORY = ROOT / "docs/content-authoring/sentence-bank"
BOUND = re.compile("[〜～]")


def read(path):
    return json.loads(path.read_text())


def encoded(value):
    return (json.dumps(value, ensure_ascii=False, indent=2) + "\n").encode()


def digest(value):
    return hashlib.sha256(json.dumps(value, ensure_ascii=False, sort_keys=True,
                                    separators=(",", ":")).encode()).hexdigest()


def plain(value):
    return "".join(s["base"] for s in value["segments"])


def reading(value):
    return "".join(s.get("ruby", s["base"]) for s in value["segments"])


def corpus():
    """Enumerate the denominator from source JSON, including BOTH wave dashes.

    Keys locate existing identities; they are not semantic matching or new IDs.
    The checked-in identity registry owns newly assigned form/sense/target UUIDs.
    """
    targets, speech, lessons, entities, paths = {}, {}, {}, {}, []

    def target(key, kind, item, path, pointer, lesson_id, form_key=None, sense=None, variant=None):
        targets[key] = dict(kind=kind, entity_id=item["id"], path=path, pointer=pointer,
                            lesson_id=lesson_id, form_key=form_key, sense_index=sense,
                            variant_key=variant, source_sha256=digest(item))

    def spoken(key, item, japanese, path, pointer, lesson_id, form_key=None):
        speech[key] = dict(entity_id=item["id"], form_key=form_key, path=path,
                           pointer=pointer, lesson_id=lesson_id, japanese=japanese,
                           orthographic_reading=reading(japanese),
                           bound=bool(BOUND.search(plain(japanese))),
                           source_sha256=digest(item), source_refs=item.get("source_refs", []))

    def load(path):
        paths.append(path)
        return read(ROOT / path)

    for n in range(1, 51):
        path = f"docs/content-authoring/lesson-{n:02}.json"
        l = load(path)
        lessons[l["id"]] = dict(level=l["source_level_label"], number=n)
        entities[l["id"]] = l
        for i, v in enumerate(l["vocabulary"]):
            entities[v["id"]] = v
            for j, form in enumerate(v["forms"]):
                key = f"vocabulary:{v['id']}:{form['key']}"
                spoken(key, v, form["japanese"], path, f"/vocabulary/{i}/forms/{j}", l["id"], form["key"])
                for k, sense in enumerate(v["meanings"]):
                    if form["key"] in sense["form_keys"]:
                        target(key + f":sense:{k}", "vocabulary", v, path,
                               f"/vocabulary/{i}", l["id"], form["key"], k)
            for j, form in enumerate(v.get("dictionary_forms", [])):
                form_key = "dictionary:" + form["form_key"]
                key = f"vocabulary:{v['id']}:{form_key}"
                spoken(key, v, form["japanese"], path,
                       f"/vocabulary/{i}/dictionary_forms/{j}", l["id"], form_key)
                for k, sense in enumerate(v["meanings"]):
                    if form["form_key"] in sense["form_keys"]:
                        target(key + f":sense:{k}", "vocabulary", v, path,
                               f"/vocabulary/{i}", l["id"], form_key, k)
        for i, g in enumerate(l["grammar_points"]):
            entities[g["id"]] = g
            target(f"grammar:{g['id']}", "grammar", g, path, f"/grammar_points/{i}", l["id"])
        for i, p in enumerate(l["sentence_patterns"]):
            entities[p["id"]] = p
            for t in p["templates"]:
                target(f"pattern:{p['id']}:{t['key']}", "pattern", p, path,
                       f"/sentence_patterns/{i}", l["id"], variant=t["key"])
        for i, e in enumerate(l["examples"]):
            entities[e["id"]] = e
            spoken(f"example:{e['id']}", e, e["japanese"], path, f"/examples/{i}", l["id"])
        for i, d in enumerate(l["dialogues"]):
            entities[d["id"]] = d
            for j, turn in enumerate(d["turns"]):
                # A turn has no source UUID; its checked-in overlay UUID is pinned
                # to the immutable dialogue revision + pointer, never an app ID.
                spoken(f"dialogue:{d['id']}:turn:{j}", d, turn["japanese"], path,
                       f"/dialogues/{i}/turns/{j}", l["id"])
    catalog = read(ROOT / "docs/reference-inventory/catalog.json")
    number_ids = {v["number"]: k for k, v in lessons.items()}
    char_lessons = {}
    for n in range(1, 51):
        path = f"docs/content-authoring/kanji/unit-{n:02}.json"
        u = load(path)
        unit_ref = next(u for u in catalog["kanji_units"] if u["number"] == n)
        milestone = unit_ref["publisher_lesson_milestone"]["global_lesson_number"]
        lesson_id = number_ids[milestone]
        for glyph in u["character_glyphs"]:
            char_lessons.setdefault(glyph, lesson_id)
        for i, w in enumerate(u["word_examples"]):
            entities[w["id"]] = w
            key = f"word:{w['id']}"
            target(key, "word", w, path, f"/word_examples/{i}", lesson_id)
            spoken(key, w, w["japanese"], path, f"/word_examples/{i}", lesson_id)
    for level in ("n5", "n4"):
        path = f"docs/content-authoring/kanji/characters-{level}.json"
        for i, c in enumerate(load(path)["entries"]):
            entities[c["id"]] = c
            lesson_id = char_lessons[c["character"]]
            target(f"kanji:{c['id']}", "kanji", c, path, f"/entries/{i}", lesson_id)
            for j, w in enumerate(c["examples"]):
                entities[w["id"]] = w
                key = f"word:{w['id']}"
                target(key, "word", w, path, f"/entries/{i}/examples/{j}", lesson_id)
                spoken(key, w, w["japanese"], path, f"/entries/{i}/examples/{j}", lesson_id)
    return dict(targets=targets, speech=speech, lessons=lessons, entities=entities, paths=paths)


def rank(candidates, target_id, learned_endpoints, data, registry, forced_id=None):
    """Reference fixture oracle. T08.05 owns the native selector/snapshot.

    Exact target IDs only; supporting dependency counts are distinct identities.
    A returned list is a snapshot, never updated in response to state mutations.
    """
    if set(learned_endpoints) != {"N5", "N4"}:
        raise ValueError("Both independent prefixes are required")
    learned = set()
    for level in ("N5", "N4"):
        ordered = [k for k, v in sorted(data["lessons"].items(), key=lambda kv: kv[1]["number"])
                   if v["level"] == level]
        endpoint = learned_endpoints[level]
        if endpoint is not None:
            if endpoint not in ordered:
                raise ValueError("Invalid endpoint for " + level)
            learned.update(ordered[:ordered.index(endpoint)+1])
    targets = {r["id"]: data["targets"][k] for k, r in registry["targets"].items()}
    target = targets[target_id]
    introductions = {v["entity_id"]: v["lesson_id"] for v in data["targets"].values()}
    introductions.update(data.get("support_introductions", {}))
    introductions.update(data.get("equivalent_introductions", {}))

    def unfamiliar(identifier):
        sources = introductions[identifier]
        sources = sources if isinstance(sources, list) else [sources]
        return not any(source in learned for source in sources)

    def score(c):
        vocab = set(c["vocabulary_ids"])
        grammar = set(c["grammar_ids"])
        exception = c["target_exceptions"][target_id]
        vocab.difference_update(exception["vocabulary_ids"])
        grammar.difference_update(exception["grammar_ids"])
        return (sum(unfamiliar(g) for g in grammar),
                sum(unfamiliar(v) for v in vocab),
                c["simplicity_order"], len(plain(c["japanese"])),
                c["authored_order"], c["id"])

    matching = sorted((c for c in candidates if c["status"] == "reviewed"
                       and target_id in c["target_ids"]), key=score)
    if forced_id is not None:
        forced = next((c for c in matching if c["id"] == forced_id), None)
        if forced is None:
            raise ValueError("Search example does not match the target")
        matching = [forced] + [c for c in matching if c["id"] != forced_id]
    unique, seen, spoken_meanings = [], set(), set()
    for candidate in matching:
        japanese = (plain(candidate["japanese"]), reading(candidate["japanese"]))
        # Duplicate suppression never creates target correspondence. Membership
        # above still requires an explicit reviewed target ID. Preserve distinct
        # readings such as 一日 (いちにち / ついたち), while suppressing duplicate
        # orthographies of the same spoken sentence and exact VI/EN translation.
        spoken_meaning = (candidate["speech_text"], candidate["translation"]["en"],
                          candidate["translation"]["vi"])
        if japanese not in seen and spoken_meaning not in spoken_meanings:
            seen.add(japanese)
            spoken_meanings.add(spoken_meaning)
            unique.append(candidate)
    return unique[:3]


def resolve_form_speech(entity_id, form_id, sense_id, data, registry, speech, contexts):
    """Exact authoring lookup; no first-form, first-sense or substring fallback.

    A caller can keep displaying its canonical form/meaning when this returns
    None. No UI, voice selection or audio behavior is implemented here.
    """
    target = next((r for r in registry["targets"].values()
                   if r["kind"] == "vocabulary" and r["entity_id"] == entity_id
                   and r["form_id"] == form_id and r["sense_id"] == sense_id), None)
    if target is None:
        return None
    key = f"vocabulary:{entity_id}:{target['form_key']}"
    current = data["speech"].get(key)
    record = next((r for r in speech["records"] if r["key"] == key), None)
    if (current is None or record is None or record["status"] != "reviewed"
            or record["source_sha256"] != current["source_sha256"]):
        return None
    context = next((r for r in contexts["contexts"] if r["key"] == key), None)
    if current["bound"] and (context is None or record.get("context_sha256") != digest(context)):
        return None
    return dict(speech_text=record["speech_text"], label=context["label"] if context else None,
                form_id=form_id, sense_id=sense_id)
