#!/usr/bin/env python3
"""T04 coverage/revision gate and offline ranking/speech failure fixtures.

Default validation permits a disclosed work-in-progress bank. --complete fails
until EVERY denominator target has reviewed dependency-complete candidates.
--write writes derived reports only; it NEVER creates or refreshes review pins.
No native app, TTS listening, performance or independent language acceptance.
"""
from __future__ import annotations

import argparse
from collections import Counter
import copy
import hashlib
import json
import re
import sys
import uuid

sys.dont_write_bytecode = True
from candidate_authoring import (ROOT, DIRECTORY, BOUND, corpus, read, encoded,
                                 digest, plain, reading, rank, resolve_form_speech)

INPUTS = ("identities.json", "bank.json", "bank.schema.json", "bound-contexts.json", "speech.json")
KANA = re.compile(r"[ぁ-ゖァ-ヺー、。！？?!「」『』…・\s]+")


def need(value, message):
    if not value:
        raise ValueError(message)


def schema_check(value, schema, root, path="$"):
    """Small explicitly bounded schema walker, including nullable draft fields."""
    if "$ref" in schema:
        return schema_check(value, root["$defs"][schema["$ref"].split("/")[-1]], root, path)
    types = {"object": dict, "array": list, "string": str, "integer": int,
             "boolean": bool, "null": type(None)}
    names = schema.get("type", list(types))
    names = [names] if isinstance(names, str) else names
    need(any(type(value) is types[t] for t in names), "Schema type: " + path)
    if "const" in schema:
        need(type(value) is type(schema["const"]) and value == schema["const"], "Schema const: " + path)
    if "enum" in schema:
        need(value in schema["enum"], "Schema enum: " + path)
    if isinstance(value, dict):
        properties = schema.get("properties", {})
        need(set(schema.get("required", [])) <= set(value), "Schema required: " + path)
        if schema.get("additionalProperties") is False:
            need(set(value) <= set(properties), "Schema extra field: " + path)
        for k, v in value.items():
            subschema = properties.get(k, schema.get("additionalProperties", {}))
            if isinstance(subschema, dict):
                schema_check(v, subschema, root, path + "." + k)
    elif isinstance(value, list):
        need(len(value) >= schema.get("minItems", 0), "Schema empty array: " + path)
        if schema.get("uniqueItems"):
            need(len(set(map(digest, value))) == len(value), "Schema duplicate array: " + path)
        for i, v in enumerate(value):
            schema_check(v, schema.get("items", {}), root, f"{path}[{i}]")
    elif isinstance(value, str):
        need(len(value) >= schema.get("minLength", 0), "Schema empty string: " + path)
        if "pattern" in schema:
            need(re.fullmatch(schema["pattern"], value), "Schema pattern: " + path)
    elif type(value) is int:
        need(value >= schema.get("minimum", value), "Schema minimum: " + path)


def japanese(value):
    need(value.get("segments"), "Empty Japanese")
    for s in value["segments"]:
        need(s.get("base"), "Empty Japanese segment")
        if re.search(r"[\u3400-\u9fffA-Z]", s["base"]):
            need(s.get("ruby") and KANA.fullmatch(s["ruby"]), "Missing contextual ruby")
    need(KANA.fullmatch(reading(value)), "Invalid Japanese reading")
    need(not BOUND.search(plain(value)), "Placeholder is not a complete speech/sentence context")


def validate(data, registry, bank, contexts, speech, schema, review=None):
    schema_check(bank, schema, schema)
    need(registry["version"] == bank["version"] == contexts["version"] == speech["version"] == 1,
         "Unsupported T04 schema")
    need(set(registry["targets"]) == set(data["targets"]), "Target denominator differs")
    need(set(registry["speech"]) == set(data["speech"]), "Speech denominator differs")
    # Overlay IDs are canonical and unique, including dictionary-form and sense
    # UUIDs. The canonical source curriculum itself is read-only to this gate.
    identifiers = list(registry["forms"].values()) + list(registry["senses"].values())
    identifiers += [r["id"] for group in ("targets", "speech") for r in registry[group].values()]
    need(len(set(identifiers)) == len(identifiers), "Duplicate overlay UUID")
    need(not set(identifiers) & set(data["entities"]), "Overlay aliases an existing entity UUID")
    for identifier in identifiers:
        need(str(uuid.UUID(identifier, version=4)) == identifier, "Invalid overlay UUIDv4")
    forms, senses = {}, {}
    for key, source in data["targets"].items():
        row = registry["targets"][key]
        need(all(row.get(k) == v for k, v in source.items()), "Stale target source/form/sense: " + key)
        if source["kind"] == "vocabulary":
            fk = f"{source['entity_id']}:{source['form_key']}"
            sk = f"{source['entity_id']}:{source['sense_index']}"
            need(row["form_id"] == registry["forms"].get(fk), "Wrong form ID")
            need(row["sense_id"] == registry["senses"].get(sk), "Wrong sense ID")
            forms[fk], senses[sk] = row["form_id"], row["sense_id"]
    need(forms == registry["forms"] and senses == registry["senses"], "Orphaned form/sense identity")
    for key, source in data["speech"].items():
        row = registry["speech"][key]
        need(all(row.get(k) == v for k, v in source.items()
                 if k not in ("japanese", "orthographic_reading", "source_refs")), "Stale speech source: " + key)
    target_ids = {v["id"]: v for v in registry["targets"].values()}
    by_context = {r["key"]: r for r in contexts["contexts"]}
    need(len(by_context) == len(contexts["contexts"]), "Duplicate bound context")
    bound = {k for k, v in data["speech"].items() if v["bound"]}
    need(set(by_context) == bound, "Bound context denominator differs (both wave dashes required)")
    for key, context in by_context.items():
        japanese(context["japanese"])
        need(KANA.fullmatch(context["speech_text"]), "Unsafe bound speech")
        for field in ("translation", "label"):
            need(set(context[field]) == {"en", "vi"} and all(context[field].values()), "Missing context VI/EN")
        need(context["review_note"], "Missing bound-context provenance")
    spoken = {r["key"]: r for r in speech["records"]}
    need(len(spoken) == len(speech["records"]) and set(spoken) == set(data["speech"]),
         "Speech row coverage/uniqueness differs")
    for key, record in spoken.items():
        source = data["speech"][key]
        need(record["id"] == registry["speech"][key]["id"], "Speech identity mismatch")
        need(record["source_sha256"] == source["source_sha256"], "Stale speech reading/sense")
        need(record["status"] in ("reviewed", "unavailable"), "Unknown speech status")
        if record["status"] == "unavailable":
            need(not record.get("speech_text") and record.get("reason"), "Unavailable speech needs scoped reason")
            continue
        need(record["source"] == ("bound_context" if source["bound"] else "canonical_segments"),
             "Bound form must use its exact labeled context")
        original = reading(by_context[key]["japanese"]) if source["bound"] else source["orthographic_reading"]
        rebuilt = list(original)
        seen = set()
        for edit in record["particle_edits"]:
            i = edit["offset"]
            need(type(i) is int and 0 <= i < len(rebuilt) and i not in seen, "Invalid/repeated speech offset")
            need(original[i] == edit["from"] and (edit["from"], edit["to"]) in (("は", "わ"), ("へ", "え")),
                 "Speech edit is not an explicit particle reading")
            seen.add(i)
            rebuilt[i] = edit["to"]
        need("".join(rebuilt) == record["speech_text"], "Speech differs from exact reading/particle edits")
        need(KANA.fullmatch(record["speech_text"]), "Speech contains Latin/base duplication/placeholder/label")
        if source["bound"]:
            need(record["speech_text"] == by_context[key]["speech_text"], "Wrong bound-context speech")
        need(record.get("context_sha256") == (digest(by_context[key]) if source["bound"] else None),
             "Speech context changed after exact pronunciation review")
        need(record["review_basis"], "Missing speech provenance")

    support = {v["id"]: v for v in bank["support_lexemes"]}
    need(len(support) == len(bank["support_lexemes"]), "Duplicate context lexeme")
    vocab = {k: v for k, v in data["entities"].items() if "forms" in v}
    grammar = {v["entity_id"] for v in data["targets"].values() if v["kind"] == "grammar"}
    data["support_introductions"] = {}
    for key, v in support.items():
        if key in data["entities"]:
            source = data["entities"][key]
            need(v.get("source_word_id") == key and "meanings" in source and isinstance(source["meanings"], dict),
                 "Context lexeme aliases a non-lexical source")
            need(v.get("source_sha256") == digest(source) and v["japanese"] == source["japanese"]
                 and v["meaning"] == source["meanings"], "Source lexical context drift")
        if v["introduced_lesson_id"] is not None:
            need(v["introduced_lesson_id"] in data["lessons"], "Unknown support introduction")
            evidence = v.get("introduction_evidence")
            need(evidence, "A lesson introduction needs explicit content evidence, not a unit milestone")
            entity = data["entities"].get(evidence["entity_id"])
            need(entity and digest(entity) == evidence["sha256"], "Stale lexical introduction evidence")
            need(evidence["kind"] in ("example", "dialogue_turn", "vocabulary_form"), "Unknown introduction kind")
            sk = ("example:" + entity["id"] if evidence["kind"] == "example" else
                  f"vocabulary:{entity['id']}:{evidence['form_key']}" if evidence["kind"] == "vocabulary_form" else
                  f"dialogue:{entity['id']}:turn:{evidence['turn_index']}")
            source = data["speech"].get(sk)
            need(source and source["lesson_id"] == v["introduced_lesson_id"], "Introduction is in another lesson")
            need(evidence["surface"] in plain(source["japanese"]) and evidence["review_note"],
                 "Missing lexical introduction locator/review")
        need(v["provenance"], "Missing support provenance")
        if not BOUND.search(plain(v["japanese"])):
            japanese(v["japanese"])
        else:
            need(v.get("source_word_id") == key, "Placeholder in an unsupported context lexeme")
        data["support_introductions"][key] = v["introduced_lesson_id"]
    for item in bank.get("support_grammar", []):
        identifier = item["id"]
        need(identifier not in grammar and identifier not in data["entities"], "Duplicate support grammar")
        need(item["introduced_lesson_id"] is None, "Context-only grammar cannot infer marked-lesson mastery")
        need(item["source_example_id"] in data["entities"]
             and item["source_sha256"] == digest(data["entities"][item["source_example_id"]]), "Stale support-grammar context")
        need(item["review_note"] and item["meaning"]["en"] and item["meaning"]["vi"], "Unreviewed support grammar")
        grammar.add(identifier)
        data["support_introductions"][identifier] = None
    data["equivalent_introductions"] = {}
    main_introductions = {v["entity_id"]: v["lesson_id"] for v in data["targets"].values() if v["kind"] == "vocabulary"}
    for group in bank.get("knowledge_equivalences", []):
        members = group["vocabulary_ids"]
        need(len(set(members)) == len(members) and len(members) >= 2 and set(members) <= set(vocab), "Invalid knowledge equivalence")
        facts = []
        for member in members:
            v = vocab[member]
            facts.append({(plain(f["japanese"]), reading(f["japanese"]), s["text"]["en"])
                          for f in v["forms"] for s in v["meanings"] if f["key"] in s["form_keys"]})
        need(set.intersection(*facts) and group["review_note"], "Knowledge equivalence crosses lexical senses")
        lessons = sorted({main_introductions[m] for m in members})
        for member in members:
            data["equivalent_introductions"][member] = lessons
    for tid, binding in bank.get("word_bindings", {}).items():
        need(tid in target_ids and target_ids[tid]["kind"] == "word", "Unknown word-binding target")
        source = data["entities"][target_ids[tid]["entity_id"]]
        need(binding["source_word_id"] == source["id"] and binding["source_sha256"] == digest(source),
             "Stale word/sense binding")
        need(binding["review_note"], "Unreviewed word binding")
        need(all(v in target_ids and target_ids[v]["kind"] == "vocabulary"
                 for v in binding["vocabulary_target_ids"]), "Unresolved word/form/sense equivalence")
        for dependency in binding["additional_dependency_ids"]:
            need(dependency in support and dependency in data["entities"], "Unknown source lexical dependency")
            other = data["entities"][dependency]
            need(plain(other["japanese"]) == plain(source["japanese"])
                 and reading(other["japanese"]) == reading(source["japanese"])
                 and other["meanings"] == source["meanings"], "Word binding adds an unrelated lexical sense")
        need(binding["vocabulary_target_ids"] or binding["additional_dependency_ids"], "Empty word binding")
    bare_character_bindings = {}
    for binding in bank.get("bare_character_bindings", []):
        ct, wt = binding["character_target_id"], binding["word_target_id"]
        need(ct in target_ids and target_ids[ct]["kind"] == "kanji"
             and wt in target_ids and target_ids[wt]["kind"] == "word", "Invalid bare-character binding")
        character = data["entities"][target_ids[ct]["entity_id"]]
        word = data["entities"][target_ids[wt]["entity_id"]]
        need(word["id"] in {w["id"] for w in character["examples"]}
             and plain(word["japanese"]) == character["character"], "A compound is not the taught bare character")
        need(binding["source_character_sha256"] == digest(character)
             and binding["source_word_sha256"] == digest(word), "Stale bare-character review")
        wb = bank["word_bindings"][wt]
        allowed = {target_ids[t]["entity_id"] for t in wb["vocabulary_target_ids"]}
        allowed.update(wb["additional_dependency_ids"])
        need(binding["review_note"] and set(binding["vocabulary_ids"]) <= allowed,
             "Bare-character exception crosses lexical senses")
        need((ct, wt) not in bare_character_bindings, "Duplicate bare-character binding")
        bare_character_bindings[ct, wt] = set(binding["vocabulary_ids"])
    candidates = bank["candidates"]
    need(len({c["id"] for c in candidates}) == len(candidates), "Duplicate candidate sentence UUID")
    need(len({c["authored_order"] for c in candidates}) == len(candidates), "Duplicate authored order")
    existing = {k: v for k, v in data["entities"].items() if "pattern_variant_key" in v}
    need({c["source_example_id"] for c in candidates if c["source_example_id"]} == set(existing),
         "Original example annotation queue omitted or duplicated")
    complete_ids, alignment_ids = set(), set()
    for candidate in candidates:
        need(candidate["introduced_lesson_id"] in data["lessons"], "Unknown candidate introduction")
        japanese(candidate["japanese"])
        need(KANA.fullmatch(candidate["speech_text"]), "Unsafe candidate speech")
        orthographic = reading(candidate["japanese"])
        need(len(orthographic) == len(candidate["speech_text"])
             and all(a == b or (a, b) in (("は", "わ"), ("へ", "え"))
                     for a, b in zip(orthographic, candidate["speech_text"])),
             "Candidate speech differs from its exact reading/particle projection")
        need(set(candidate["translation"]) == {"en", "vi"} and all(candidate["translation"].values()), "Missing sentence VI/EN")
        if candidate["source_example_id"]:
            x = existing[candidate["source_example_id"]]
            need(candidate["id"] == x["id"] and candidate["source_sha256"] == digest(x), "Stale source sentence")
            for field in ("japanese", "translation"):
                need(candidate[field] == x[field], "Existing authored sentence changed in sidecar")
            need(candidate.get("context") == x.get("context"), "Original sentence context lost")
            need(candidate["speech_text"] == spoken["example:" + x["id"]]["speech_text"], "Sentence audio mismatch")
            need(candidate["introduced_lesson_id"] == data["speech"]["example:" + x["id"]]["lesson_id"],
                 "Sentence introduction moved to another lesson")
        else:
            need(candidate["id"] not in data["entities"], "New sentence reuses source UUID")
        need(set(candidate["target_ids"]) <= set(target_ids), "Unknown target ID")
        need(set(candidate["target_exceptions"]) == set(candidate["target_ids"]), "Missing target-scoped exceptions")
        for tid, exception in candidate["target_exceptions"].items():
            t = target_ids[tid]
            allowed_v = {t["entity_id"]} if t["kind"] == "vocabulary" else set()
            if t["kind"] == "word":
                binding = bank.get("word_bindings", {}).get(tid, {})
                need(binding, "Word target lacks explicit reviewed form/sense binding")
                allowed_v = {target_ids[v]["entity_id"] for v in binding.get("vocabulary_target_ids", [])}
                allowed_v.update(binding.get("additional_dependency_ids", []))
            if t["kind"] == "kanji":
                character = data["entities"][t["entity_id"]]
                examples = {e["id"] for e in character["examples"]}
                need(any(target_ids[w]["kind"] == "word" and target_ids[w]["entity_id"] in examples
                         for w in candidate["target_ids"]), "Character correspondence lacks its curated source-word relation")
                need(character["character"] in plain(candidate["japanese"]),
                     "Character example does not display the source character")
                for wt in candidate["target_ids"]:
                    allowed_v.update(bare_character_bindings.get((tid, wt), set()))
            allowed_g = ({t["entity_id"]} if t["kind"] == "grammar" else
                         {data["entities"][t["entity_id"]]["grammar_point_id"]} if t["kind"] == "pattern" else set())
            need(set(exception["vocabulary_ids"]) <= allowed_v and set(exception["grammar_ids"]) <= allowed_g,
                 "Exception exempts unrelated supporting knowledge")
            need(set(exception["vocabulary_ids"]) == allowed_v & set(candidate["vocabulary_ids"])
                 and set(exception["grammar_ids"]) == allowed_g & set(candidate["grammar_ids"]),
                 "Explicit taught target was counted as unfamiliar support")
        alignment_ids.update(candidate["target_ids"])
        need(set(candidate["vocabulary_ids"]) <= set(vocab) | set(support), "Unresolved vocabulary dependency")
        need(set(candidate["grammar_ids"]) <= grammar, "Unresolved grammar dependency")
        if candidate["status"] != "reviewed":
            need(candidate["status"] == "dependencies_pending" and candidate["simplicity_order"] is None,
                 "Unreviewed simplicity promoted")
            continue
        need(type(candidate["simplicity_order"]) is int and candidate["simplicity_order"] >= 0, "Missing editorial simplicity")
        need(candidate["analysis"] and "".join(t["surface"] for t in candidate["analysis"]) == plain(candidate["japanese"]),
             "Incomplete sentence analysis")
        for atom in candidate["analysis"]:
            need(atom["surface"] and (atom["vocabulary_id"] or atom["grammar_ids"]), "Unexplained sentence span")
            need(set(atom["grammar_ids"]) <= set(candidate["grammar_ids"]), "Hidden grammar dependency")
            if atom["vocabulary_id"]:
                need(atom["vocabulary_id"] in candidate["vocabulary_ids"], "Hidden lexical dependency")
                if atom["vocabulary_id"] in vocab:
                    need(any(t["entity_id"] == atom["vocabulary_id"] and t["form_id"] == atom["form_id"]
                             and t["sense_id"] == atom["sense_id"] for t in target_ids.values()), "Wrong dependency form/sense")
        need(candidate["review_note"], "Missing primary candidate review")
        complete_ids.update(candidate["target_ids"])
    if review is not None:
        need(review["authority"] == "B-U-51" and review["reviewer"] == "primary agent", "Unsupported editorial authority")
        need(set(review["authoring_sha256"]) == set(INPUTS), "Incomplete authoring review pins")
        expected = {c["id"]: digest(c) for c in candidates if c["status"] == "reviewed"}
        need(review["candidate_sha256"] == expected, "Candidate changed after primary review")
        need(review["speech_sha256"] == {r["key"]: digest(r) for r in speech["records"]}, "Speech changed after primary review")
        need(review["context_sha256"] == {r["key"]: digest(r) for r in contexts["contexts"]}, "Context changed after primary review")
        for name, pin in review["authoring_sha256"].items():
            need(hashlib.sha256((DIRECTORY / name).read_bytes()).hexdigest() == pin, "Stale authoring review: " + name)
        t02 = read(ROOT / "docs/content-authoring/source-reconciliation/validation-report.json")
        need(t02["task_acceptance_complete"], "T02 source-reading review incomplete")
        for path, pin in {**t02["input_sha256"], **t02["implementation_sha256"]}.items():
            need(hashlib.sha256((ROOT / path).read_bytes()).hexdigest() == pin, "Inherited T02 review stale: " + path)
        need(review["inherited_t02_sha256"] == hashlib.sha256((ROOT / "docs/content-authoring/source-reconciliation/validation-report.json").read_bytes()).hexdigest(), "T02 review pin differs")
    missing = []
    for key, t in registry["targets"].items():
        if t["id"] not in complete_ids:
            missing.append(dict(target_id=t["id"], key=key, kind=t["kind"], source=t["path"], pointer=t["pointer"],
                                form_id=t["form_id"], sense_id=t["sense_id"],
                                reason="dependencies_pending" if t["id"] in alignment_ids else "no_matching_sentence"))
    return dict(targets=len(target_ids), targets_by_kind=dict(sorted(Counter(t["kind"] for t in target_ids.values()).items())),
                candidates=len(candidates), reviewed_candidates=sum(c["status"] == "reviewed" for c in candidates),
                reviewed_target_coverage=len(complete_ids), alignment_only_or_reviewed_coverage=len(alignment_ids),
                missing_targets=len(missing), missing_by_kind=dict(sorted(Counter(r["kind"] for r in missing).items())),
                speech_targets=len(spoken), reviewed_speech_targets=sum(r["status"] == "reviewed" for r in spoken.values()),
                vocabulary_bound_entries=len({r["entity_id"] for k, r in data["speech"].items() if k.startswith("vocabulary:") and r["bound"]}),
                vocabulary_bound_forms=sum(k.startswith("vocabulary:") for k in bound),
                kanji_bound_words=sum(k.startswith("word:") for k in bound), bound_contexts=len(bound),
                dictionary_forms=sum(":dictionary:" in k for k in data["speech"]),
                speech_authoring_complete=all(r["status"] == "reviewed" for r in spoken.values()),
                task_authoring_acceptance_complete=not missing and all(c["status"] == "reviewed" for c in candidates)
                and all(r["status"] == "reviewed" for r in spoken.values())), missing


def self_test(data, registry, bank, contexts, speech, schema, review):
    rejected = []

    def bad(name, mutate):
        args = copy.deepcopy([data, registry, bank, contexts, speech, schema, review])
        mutate(*args)
        try:
            validate(*args)
        except (ValueError, KeyError, IndexError):
            rejected.append(name)
        else:
            raise AssertionError("Accepted negative fixture: " + name)

    first_target = next(iter(registry["targets"]))
    first_speech = speech["records"][0]["key"]
    bad("missing_target", lambda d, r, *args: r["targets"].pop(first_target))
    bad("wrong_sense", lambda d, r, *args: r["targets"][first_target].update(sense_id=str(uuid.uuid4())))
    bad("stale_source", lambda d, r, *args: r["targets"][first_target].update(source_sha256="0" * 64))
    bad("missing_dictionary_form", lambda d, r, *args: r["speech"].pop(next(k for k in r["speech"] if ":dictionary:" in k)))
    bad("missing_wave_dash_context", lambda d, r, b, c, *args: c["contexts"].pop())
    bad("unlabeled_context", lambda d, r, b, c, *args: c["contexts"][0]["label"].pop("vi"))
    bad("placeholder_to_tts", lambda d, r, b, c, s, *args: s["records"][0].update(speech_text="〜さん"))
    bad("latin_to_tts", lambda d, r, b, c, s, *args: s["records"][0].update(speech_text="CD"))
    bad("duplicate_ruby_base_to_tts", lambda d, r, b, c, s, *args: s["records"][0].update(speech_text="わたしわたし"))
    bad("wrong_particle_offset", lambda d, r, b, c, s, *args: next(x for x in s["records"] if x["particle_edits"])["particle_edits"][0].update(offset=9999))
    bad("missing_speech_row", lambda d, r, b, c, s, *args: s["records"].pop())
    bad("duplicate_candidate", lambda d, r, b, *args: b["candidates"].append(copy.deepcopy(b["candidates"][0])))
    bad("unknown_target", lambda d, r, b, *args: b["candidates"][0]["target_ids"].append(str(uuid.uuid4())))
    bad("unknown_vocabulary", lambda d, r, b, *args: b["candidates"][0]["vocabulary_ids"].append(str(uuid.uuid4())))
    bad("unknown_grammar", lambda d, r, b, *args: b["candidates"][0]["grammar_ids"].append(str(uuid.uuid4())))
    bad("incomplete_span_analysis", lambda d, r, b, *args: b["candidates"][0]["analysis"].pop())
    bad("unreviewed_simplicity", lambda d, r, b, *args: b["candidates"][0].update(simplicity_order=None))
    bad("unrelated_target_exception", lambda d, r, b, *args: next(iter(b["candidates"][0]["target_exceptions"].values()))["grammar_ids"].append(str(uuid.uuid4())))
    bad("changed_translation_after_review", lambda d, r, b, *args: b["candidates"][-1]["translation"].update(en="Different sense."))
    bad("changed_context_after_review", lambda d, r, b, c, *args: c["contexts"][0]["translation"].update(en="Different referent."))
    bad("candidate_speech_wrong_reading", lambda d, r, b, *args: b["candidates"][0].update(speech_text="あ"))
    bad("support_introduction_without_evidence", lambda d, r, b, *args: b["support_lexemes"][0].pop("introduction_evidence"))
    bad("stale_word_binding", lambda d, r, b, *args: next(iter(b["word_bindings"].values())).update(source_sha256="0" * 64))
    bad("stale_bare_character_binding", lambda d, r, b, *args: b["bare_character_bindings"][0].update(source_word_sha256="0" * 64))
    bad("unrelated_bare_character_exception", lambda d, r, b, *args: b["bare_character_bindings"][0]["vocabulary_ids"].append(str(uuid.uuid4())))
    def omit_exception(d, r, b, *args):
        exception = next(e for c in b["candidates"] for e in c["target_exceptions"].values()
                         if e["vocabulary_ids"] or e["grammar_ids"])
        exception.update(vocabulary_ids=[], grammar_ids=[])
    bad("omitted_taught_target_exception", omit_exception)
    bad("stale_bound_context_fingerprint", lambda d, r, b, c, s, *args:
        next(x for x in s["records"] if x["source"] == "bound_context").update(context_sha256="0" * 64))

    result, _ = validate(data, registry, bank, contexts, speech, schema, review)
    # This assertion uses an explicitly incomplete copy even after the real bank
    # is complete; it must never force the production input to remain partial.
    partial = copy.deepcopy(bank)
    partial["candidates"] = [c for c in partial["candidates"] if c["source_example_id"]]
    partial_result, _ = validate(data, registry, partial, contexts, speech, schema)
    need(not partial_result["task_authoring_acceptance_complete"], "Partial bank incorrectly accepted as complete")
    # Synthetic reference-oracle fixtures isolate the two independent levels.
    # These metadata mutations are TEST INPUTS, never part of the authored bank.
    student = next(r for r in registry["targets"].values()
                   if r["entity_id"] == "681b4d01-0b30-4d75-a7c8-020dae929871" and r["form_key"] == "standard")
    a = copy.deepcopy(next(c for c in bank["candidates"] if c["source_example_id"] is None
                           and plain(c["japanese"]) == "学生です。"))
    b = copy.deepcopy(a)
    a.update(id="fixture-n5", grammar_ids=["1bc60b55-77d6-48fd-adc3-49bddfc36655"], simplicity_order=1)
    b.update(id="fixture-n4", grammar_ids=["31ef223a-6d7b-46d1-ae14-a8daca908f3e"], simplicity_order=2)
    orders = {v["number"]: k for k, v in data["lessons"].items()}
    cases = [(None, None, "fixture-n5"), (orders[25], None, "fixture-n5"),
             (None, orders[26], "fixture-n4"), (orders[25], orders[26], "fixture-n5")]
    for n5, n4, expected in cases:
        need(rank([a, b], student["id"], {"N5": n5, "N4": n4}, data, registry)[0]["id"] == expected,
             "Independent-prefix fixture failed")
    a.update(grammar_ids=[], vocabulary_ids=[student["entity_id"], "7b2a83f8-d0de-44f9-b768-0b1270b97a35",
                                             "4445a67d-ce63-4a54-b91c-ad2818d4792a"], simplicity_order=5)
    b.update(grammar_ids=["1bc60b55-77d6-48fd-adc3-49bddfc36655"], vocabulary_ids=[student["entity_id"]], simplicity_order=0)
    empty = {"N5": None, "N4": None}
    need(rank([a, b], student["id"], empty, data, registry)[0]["id"] == a["id"], "Grammar must precede unfamiliar word count")
    a.update(vocabulary_ids=[student["entity_id"]], simplicity_order=9)
    b.update(grammar_ids=[], vocabulary_ids=[student["entity_id"], "7b2a83f8-d0de-44f9-b768-0b1270b97a35"])
    need(rank([a, b], student["id"], empty, data, registry)[0]["id"] == a["id"], "Word count must precede simplicity")
    b.update(vocabulary_ids=[student["entity_id"]], simplicity_order=0)
    need(rank([a, b], student["id"], empty, data, registry)[0]["id"] == b["id"], "Editorial simplicity order ignored")
    a.update(simplicity_order=0, authored_order=2)
    b.update(authored_order=1)
    need(rank([a, b], student["id"], empty, data, registry)[0]["id"] == b["id"], "Stable authored tie order ignored")
    endpoints = {"N5": None, "N4": None}
    selected = rank(bank["candidates"], student["id"], endpoints, data, registry)
    need(len(selected) == 3 and len({c["id"] for c in selected}) == 3, "Three-example cap/dedup failed")
    snapshot = [c["id"] for c in selected]
    endpoints["N4"] = orders[50]
    need([c["id"] for c in selected] == snapshot, "Reference snapshot mutated")
    forced = next(c for c in bank["candidates"] if student["id"] in c["target_ids"] and c["id"] not in snapshot and c["status"] == "reviewed")
    included = rank(bank["candidates"], student["id"], endpoints, data, registry, forced["id"])
    need(included[0]["id"] == forced["id"] and len(included) == 3, "Search inclusion/cap failed")
    try:
        rank(bank["candidates"], student["id"], {"N5": orders[26], "N4": None}, data, registry)
        raise AssertionError("N4 endpoint accepted for N5")
    except ValueError:
        pass
    try:
        rank(bank["candidates"], student["id"], endpoints, data, registry, "unrelated")
        raise AssertionError("Unrelated forced sentence accepted")
    except ValueError:
        pass
    pending = copy.deepcopy(bank["candidates"][0])
    pending.update(status="dependencies_pending", simplicity_order=None)
    need(not rank([pending], pending["target_ids"][0], endpoints, data, registry), "Pending dependencies selected")
    duplicate = copy.deepcopy(a)
    duplicate["id"] = "fixture-duplicate"
    need(len(rank([a, duplicate], student["id"], empty, data, registry)) == 1,
         "Identical displayed/spoken sentence padded the result")
    duplicate["japanese"] = {"segments": [{"base": reading(a["japanese"])}]}
    need(len(rank([a, duplicate], student["id"], empty, data, registry)) == 1,
         "Orthographic variant padded identical spoken meaning")
    first_day, one_day = copy.deepcopy(a), copy.deepcopy(a)
    first_day.update(id="fixture-first-day", japanese={"segments": [{"base": "一日です。", "ruby": "ついたちです。"}]},
                     speech_text="ついたちです。", translation={"en": "It is the first.", "vi": "Là mùng một."})
    one_day.update(id="fixture-one-day", japanese={"segments": [{"base": "一日です。", "ruby": "いちにちです。"}]},
                   speech_text="いちにちです。", translation={"en": "It is one day.", "vi": "Là một ngày."})
    need(len(rank([first_day, one_day], student["id"], empty, data, registry)) == 2,
         "Distinct contextual readings were collapsed")
    unknown = next(s["id"] for s in bank["support_lexemes"] if s["introduced_lesson_id"] is None)
    a.update(vocabulary_ids=[student["entity_id"], unknown], grammar_ids=[], simplicity_order=0)
    b.update(vocabulary_ids=[student["entity_id"]], grammar_ids=[], simplicity_order=1)
    all_learned = {"N5": orders[25], "N4": orders[50]}
    need(rank([a, b], student["id"], all_learned, data, registry)[0]["id"] == b["id"],
         "Context-only support silently became learned")
    need(rank([a], student["id"], empty, data, registry), "Unfamiliar-support fallback suppressed")
    bare = bank["bare_character_bindings"][0]
    actual = next(c for c in bank["candidates"] if bare["character_target_id"] in c["target_ids"]
                  and bare["word_target_id"] in c["target_ids"]
                  and set(c["target_exceptions"][bare["character_target_id"]]["vocabulary_ids"]))
    need(set(actual["target_exceptions"][bare["character_target_id"]]["vocabulary_ids"])
         <= set(bare["vocabulary_ids"]), "Taught bare-character exception absent")
    variants = [r for r in registry["targets"].values() if r["entity_id"] == "49fa0e98-e1a6-4847-8031-75e3e36eaf68"]
    for t in variants:
        resolved = resolve_form_speech(t["entity_id"], t["form_id"], t["sense_id"], data, registry, speech, contexts)
        need(resolved and resolved["form_id"] == t["form_id"], "Exact form speech lookup failed")
    need(resolve_form_speech(variants[0]["entity_id"], variants[0]["form_id"], variants[1]["sense_id"], data, registry, speech, contexts) is None,
         "Wrong 見ます/診ます sense silently defaulted")
    bound_target = next(t for t in registry["targets"].values() if t["entity_id"] == "167e9197-dfb5-49b7-87dd-c962d54f8fcd")
    need(resolve_form_speech(bound_target["entity_id"], bound_target["form_id"], bound_target["sense_id"], data, registry, speech, {"contexts": []}) is None,
         "Missing bound context did not produce scoped unavailable")
    stale = copy.deepcopy(speech)
    key = f"vocabulary:{bound_target['entity_id']}:{bound_target['form_key']}"
    next(r for r in stale["records"] if r["key"] == key)["source_sha256"] = "0" * 64
    need(resolve_form_speech(bound_target["entity_id"], bound_target["form_id"], bound_target["sense_id"], data, registry, stale, contexts) is None,
         "Stale speech did not produce scoped unavailable")
    stale_contexts = copy.deepcopy(contexts)
    next(c for c in stale_contexts["contexts"] if c["key"] == key)["label"]["en"] = "Different context"
    need(resolve_form_speech(bound_target["entity_id"], bound_target["form_id"], bound_target["sense_id"],
                             data, registry, speech, stale_contexts) is None,
         "Changed unreviewed context did not produce scoped unavailable")
    return dict(negative_fixtures=len(rejected), rejected=rejected,
                reference_fixtures=["none", "N5_only", "N4_only", "both", "cap_three", "forced_search", "stable_returned_snapshot",
                                    "grammar_before_words", "words_before_simplicity", "editorial_simplicity", "stable_authored_order",
                                    "wrong_level_endpoint", "unrelated_forced_sentence", "pending_excluded", "exact_form_sense", "missing_context_unavailable", "stale_speech_unavailable",
                                    "duplicate_sentence_excluded", "orthographic_variant_excluded", "distinct_contextual_readings",
                                    "context_only_support_unfamiliar", "unfamiliar_support_fallback", "taught_bare_character_exception",
                                    "stale_context_unavailable"])


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--complete", action="store_true")
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    need(not (args.write and args.check), "Choose --write or --check")
    data = corpus()
    registry, bank, schema, contexts, speech = [read(DIRECTORY / p) for p in INPUTS]
    review = read(DIRECTORY / "review.json")
    result, missing = validate(data, registry, bank, contexts, speech, schema, review)
    fixtures = self_test(data, registry, bank, contexts, speech, schema, review) if args.self_test else review["expected_fixtures"]
    pins = {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in [*(ROOT / p for p in data["paths"]), *(DIRECTORY / p for p in (*INPUTS, "review.json")),
                      ROOT / "docs/reference-inventory/catalog.json", ROOT / "docs/content-authoring/source-reconciliation/validation-report.json",
                      ROOT / "scripts/candidate_authoring.py", ROOT / "scripts/validate_sentence_bank.py"]}
    report = dict(task="P0-T04", date=review["date"], **result, fixtures=fixtures, input_and_validator_sha256=pins,
                  limitations=["Coverage gaps, if any, are enumerated; structural checks do not replace primary semantic review.",
                               "Primary B-U-51 self-review and inherited T02 readings; no independent human certification.",
                               "Offline Python reference fixtures, not the T08.05 native selector or application tests.",
                               "No TTS listening, native playback, 17 remaining languages, performance or release acceptance."])
    outputs = {"validation-report.json": report, "coverage.json": dict(task="P0-T04", missing_targets=missing)}
    for name, payload in outputs.items():
        expected = encoded(payload)
        if args.check:
            need((DIRECTORY / name).read_bytes() == expected, "Stale generated T04 output: " + name)
        if args.write:
            (DIRECTORY / name).write_bytes(expected)
    print(json.dumps({k: v for k, v in report.items() if k not in ("input_and_validator_sha256", "limitations", "fixtures")}, ensure_ascii=False))
    if args.complete:
        need(result["task_authoring_acceptance_complete"], f"T04 incomplete: {len(missing)} targets lack reviewed dependency-complete sentences")


if __name__ == "__main__":
    try:
        main()
    except (ValueError, AssertionError, KeyError) as error:
        print("FAILED: " + str(error), file=sys.stderr)
        sys.exit(1)
