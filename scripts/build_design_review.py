#!/usr/bin/env python3
"""Build representative, source-linked fixtures for the local design HTML only."""
import json
import argparse
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
AUTHORING = DOCS / "content-authoring"
OUT = DOCS / "design-system"


def read(path):
    return json.loads(path.read_text())


def plain(japanese):
    return "".join(segment["base"] for segment in japanese["segments"])


all_lessons = [read(path) for path in sorted(AUTHORING.glob("lesson-*.json"))]
all_vocabulary = [(lesson, word, form) for lesson in all_lessons for word in lesson["vocabulary"] for form in word["forms"]]
all_examples = [(lesson, sentence) for lesson in all_lessons for sentence in lesson["examples"]]
lessons = []
for number in [1, 26]:
    source = next(lesson for lesson in all_lessons if lesson["reference_lesson_number"] == number)
    lesson = {key: source[key] for key in ["id", "reference_lesson_number", "source_level_label", "title", "kanji_reference_units"]}
    if number == 1:
        keys = {"speaker", "person_over_there", "teacher_address", "student", "company_employee", "doctor"}
        lesson["vocabulary"] = [word for word in source["vocabulary"] if word["editorial_key"] in keys]
    else:
        lesson["vocabulary"] = source["vocabulary"][:6]
    lesson["grammar_points"] = source["grammar_points"][:2]
    lesson["sentence_patterns"] = source["sentence_patterns"][:2]
    lesson["examples"] = [sentence for pattern in lesson["sentence_patterns"] for sentence in source["examples"] if sentence["pattern_id"] == pattern["id"]][:6]
    lesson["dialogues"] = source["dialogues"][:1]
    lessons.append(lesson)

character_sets = {level: read(AUTHORING / "kanji" / f"characters-{level.lower()}.json")["entries"] for level in ["N5", "N4"]}
units = []
for number in [1, 21, 26]:
    source = read(AUTHORING / "kanji" / f"unit-{number:02}.json")
    unit = {key: source[key] for key in ["id", "source_level_label", "reference_unit_number", "title", "publisher_lesson_milestone"]}
    candidates = character_sets[source["source_level_label"]] + character_sets["N5"] + character_sets["N4"]
    unit["characters"] = [next(char for char in candidates if char["character"] == glyph) for glyph in source["character_glyphs"]]
    units.append(unit)

targets = []


def target(kind, item_id, level, label, destination, fields=None, search_text=None, lesson_id=None, anchor=None):
    entry = {"key": f"{kind}:{item_id}", "type": kind, "level": level, "levels": [level], "label": label, "route": destination, "fields": fields or [], "searchText": search_text or label, "order": len(targets)}
    if lesson_id:
        entry["lessonId"] = lesson_id
        entry["lessonIds"] = [lesson_id]
    if anchor:
        entry["anchor"] = anchor
    targets.append(entry)
    return entry


for lesson in lessons:
    level, lesson_id = lesson["source_level_label"], lesson["id"]
    destination = {"kind": "lesson", "id": lesson_id}
    target("lesson", lesson_id, level, lesson["title"], destination)
    for word in lesson["vocabulary"]:
        fields = [plain(form["japanese"]) for form in word["forms"]] + [form["kana_reading"] for form in word["forms"]] + word.get("search_aliases", {}).get("romaji", [])
        target("vocabulary", word["id"], level, {"vi": plain(word["forms"][0]["japanese"]), "en": plain(word["forms"][0]["japanese"])}, destination, fields, word["meanings"][0]["text"], lesson_id, f"item-{word['id']}")
    for grammar in lesson["grammar_points"]:
        target("grammar", grammar["id"], level, grammar["title"], destination, [], grammar["explanation"], lesson_id, f"item-{grammar['id']}")
    for pattern in lesson["sentence_patterns"]:
        examples = [sentence for sentence in lesson["examples"] if sentence["pattern_id"] == pattern["id"]]
        label = next(grammar["title"] for grammar in lesson["grammar_points"] if grammar["id"] == pattern["grammar_point_id"])
        target("patterns", pattern["id"], level, label, destination, [plain(sentence["japanese"]) for sentence in examples], {lang: " ".join(sentence["translation"][lang] for sentence in examples) for lang in ["vi", "en"]}, lesson_id, f"item-{pattern['id']}")
    for dialogue in lesson["dialogues"]:
        target("dialogues", dialogue["id"], level, dialogue["title"], destination, [plain(turn["japanese"]) for turn in dialogue["turns"]], {lang: " ".join(turn["translation"][lang] for turn in dialogue["turns"]) for lang in ["vi", "en"]}, lesson_id, f"item-{dialogue['id']}")

character_sentences = {}
for unit in units:
    level, unit_id = unit["source_level_label"], unit["id"]
    target("unit", unit_id, level, unit["title"], {"kind": "unit", "id": unit_id})
    related_lessons = [lesson["id"] for lesson in lessons if f"REF_KANJI_UNIT_{unit['reference_unit_number']:02}" in lesson["kanji_reference_units"]]
    for char in unit["characters"]:
        destination = {"kind": "character", "id": char["id"], "unitId": unit_id}
        entry = next((entry for entry in targets if entry["key"] == f"kanji:{char['id']}"), None)
        if entry:
            if level not in entry["levels"]:
                entry["levels"].append(level)
            entry["routes"].append({"level": level, **destination})
            entry["lessonIds"] = sorted(set(entry.get("lessonIds", []) + related_lessons))
        else:
            entry = target("kanji", char["id"], level, {"vi": char["character"], "en": char["character"]}, destination, [char["character"], *char["on_readings"], *char["kun_readings"], *char["han_viet"]], char["meanings"])
            entry["routes"] = [{"level": level, **destination}]
            entry["lessonIds"] = related_lessons
        example_words = [plain(example["japanese"]) for example in char["examples"]]
        matching = [sentence for _, sentence in all_examples if any(word and word in plain(sentence["japanese"]) for word in example_words)]
        character_sentences[char["id"]] = matching[:3]

kana_requests = {
    "hiragana": {"basic": list("あいうえおかきさし"), "voiced": list("がぎぐげごぱぴぷ"), "combined": ["きゃ", "きゅ", "きょ", "しゃ", "しゅ", "しょ"], "special": list("っんゃゅょ")},
    "katakana": {"basic": list("アイウエオカキコサ"), "voiced": list("ガギグゲゴパピプ"), "combined": ["キャ", "キュ", "キョ", "シャ", "ファ", "フィ", "フェ", "フォ", "ティ", "ディ", "ウィ", "ヴァ"], "special": list("ッンャュョー")},
}
kana = []
for script, groups in kana_requests.items():
    for group, glyphs in groups.items():
        for glyph in glyphs:
            matches = []
            for lesson, word, form in all_vocabulary:
                spelling, reading = plain(form["japanese"]), form["kana_reading"]
                sample = reading if script == "hiragana" else spelling
                if glyph not in sample:
                    continue
                if script == "hiragana" and any("ァ" <= char <= "ヺ" for char in spelling):
                    continue
                matches.append((not sample.startswith(glyph), lesson["reference_lesson_number"], len(reading), word, form))
            if not matches:
                continue
            _, _, _, word, form = min(matches, key=lambda match: match[:3])
            meaning = next((meaning["text"] for meaning in word["meanings"] if form["key"] in meaning["form_keys"]), word["meanings"][0]["text"])
            spelling = plain(form["japanese"])
            sentence = next((sentence for _, sentence in all_examples if spelling in plain(sentence["japanese"])), None)
            kana.append({"id": f"{script}-{group}-{glyph}", "script": script, "group": group, "glyph": glyph, "word": {"japanese": form["japanese"], "reading": form["kana_reading"], "meanings": meaning, "sourceWordId": word["id"]}, "sentence": sentence})

payload = {
    "artifact": "representative_design_review_not_release_content",
    "tokens": read(OUT / "tokens.json"),
    "languages": ["ar", "bn", "zh-Hans", "nl", "en", "fr", "de", "he", "hi", "id", "it", "ko", "pt", "ru", "es", "th", "tr", "uk", "vi"],
    "lessonOrder": {level: [lesson["reference_lesson_number"] for lesson in all_lessons if lesson["source_level_label"] == level] for level in ["N5", "N4"]},
    "lessons": lessons,
    "units": units,
    "targets": targets,
    "characterSentences": character_sentences,
    "kana": kana,
}
encoded = json.dumps(payload, ensure_ascii=False, separators=(",", ":")).replace("<", "\\u003c").replace(">", "\\u003e").replace("&", "\\u0026")
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("--check", action="store_true")
args = parser.parse_args()
output = "/* Generated by scripts/build_design_review.py; review fixtures only. */\nwindow.PROJECT_BETA_REVIEW = " + encoded + ";\n"
if args.check:
    if (OUT / "review-data.js").read_text() != output:
        raise SystemExit("Stale representative review fixtures")
else:
    (OUT / "review-data.js").write_text(output)
print(f"Review fixtures: {len(lessons)} lessons, {len(units)} units, {len(targets)} targets, {len(kana)} representative kana cells.")
