"""Check editorial batch integrity; linguistic self-review is a separate recorded gate."""
from __future__ import annotations
import argparse
import copy
import hashlib
import json
import re
import sys
from pathlib import Path
import validate_authoring_samples as lessons

ROOT = Path(__file__).resolve().parents[1]
AUTHORING = ROOT / 'docs/content-authoring'
KANJI = AUTHORING / 'kanji'
CATALOG = ROOT / 'docs/reference-inventory/catalog.json'
CHARACTER_SCHEMA = KANJI / 'kanji-character-set.schema.json'
UNIT_SCHEMA = KANJI / 'kanji-unit.schema.json'
LESSON_SCHEMA = AUTHORING / 'authoring.schema.json'
ANCHORS = AUTHORING / 'source-checks.json'
CORRECTIONS = AUTHORING / 'source-corrections.json'
SET_NAMES = ('characters-n5.json', 'characters-n4.json')
UNIT_GLOB = 'unit-*.json'
LESSON_GLOB = 'lesson-*.json'
UTF8 = 'utf-8'
NEWLINE = '\n'
NUMBER_RANGES = {'N5': set(range(1, 221)), 'N4': set(range(221, 537))}
BILINGUAL = frozenset(('title', 'meanings'))
CHILD = '{path}.{key}'
WORD_KEYS = ('id', 'japanese', 'kana_reading', 'meanings', 'origin')
COMPLETE = '--complete'
SELF_TEST = '--self-test'
REPORT = '--report'
SELF_REVIEW_STATE = {'self_review': 'accepted_for_batch_authoring', 'independent_review': 'not_claimed', 'release_status': 'draft_not_for_release'}

class BatchError(ValueError):
    """The authored draft does not meet a structural/reference rule."""

def check(condition, message):
    if not condition:
        raise BatchError(message)

def read(path):
    return json.loads(path.read_text(encoding=UTF8))

def validate_correction_ledger(ledger, sets, catalog, samples):
    """Check correction targets, approved values and traceable owner confirmations."""
    sources = {s['id']: s for s in catalog['sources']}
    entries = {e['source_character_number']: e for dataset in sets for e in dataset['entries']}
    vocabulary = {v['id']: (sample, v) for sample in samples for v in sample['vocabulary']}
    ids = set()
    pending = []
    for item in ledger['items']:
        check(item['id'] not in ids, 'Duplicate source-discrepancy ID')
        ids.add(item['id'])
        source = sources.get(item['source_id'])
        check(source is not None and 1 <= item['pdf_page'] <= source['page_count'], f'{item["id"]}: invalid source locator')
        if 'vocabulary_id' in item:
            target = vocabulary.get(item['vocabulary_id'])
            check(target is not None, f'{item["id"]}: unresolved vocabulary ID')
            sample, entry = target
            check(sample['reference_lesson_number'] == item['reference_lesson_number'] and entry['editorial_key'] == item['vocabulary_key'], f'{item["id"]}: wrong lesson target')
            check(any(lessons.surface(f['japanese']) == item['item'] for f in entry['forms']), f'{item["id"]}: unresolved lexical form')
        else:
            entry = entries.get(item['source_character_number'])
            check(entry is not None, f'{item["id"]}: unresolved character number')
            check(item['item'] == entry['character'] or any(lessons.surface(w['japanese']) == item['item'] for w in entry['examples']), f'{item["id"]}: unresolved affected item')
        check(item['draft_disposition'] in ('retain_corroborated_authored_value', 'retain_current_authored_value_pending_confirmation'), f'{item["id"]}: unexplained draft disposition')
        check(item['review_status'] in ('recheck_required', 'owner_confirmed'), f'{item["id"]}: unknown review status')
        if item['review_status'] == 'owner_confirmed':
            confirmation = ledger.get('confirmation', {})
            check(confirmation.get('decision_reference') == 'B-U-57' and
                  item.get('confirmation_reference') == 'B-U-57' and
                  item['id'] in confirmation.get('scope', []) and
                  item['owner_decision'] == 'apply_authored_value_confirmed',
                  f'{item["id"]}: missing owner confirmation evidence')
            if 'vocabulary_id' in item:
                values = [meaning['text'] for meaning in entry['meanings']]
                check(item['proposed_value'] in values, f'{item["id"]}: confirmed meaning not applied')
            elif item['item'] == entry['character']:
                field = 'on_readings' if item['id'] == 'SRC-04' else 'han_viet'
                check(entry[field] == [item['proposed_value']], f'{item["id"]}: confirmed reading not applied')
            else:
                examples = [word for word in entry['examples'] if lessons.surface(word['japanese']) == item['item']]
                check(any(word['meanings'] == item['proposed_value'] for word in examples), f'{item["id"]}: confirmed meaning not applied')
        else:
            pending.append(item['id'])
    return sorted(pending)

def validate_kanji(sets, units, catalog, character_schema, unit_schema, complete):
    source_map = {s['id']: s for s in catalog['sources']}
    reference_units = {u['number']: u for u in catalog['kanji_units']}
    masters = {}
    numbers = {}
    identities = {}
    word_count = 0

    def identity(item, kind):
        # Reuse of one lexical ID is valid only for the same lexical payload;
        # its per-use provenance may resolve to another verified source page.
        signature = {k: item[k] for k in WORD_KEYS} if kind == 'word' else item
        previous = identities.get(item['id'])
        check(previous is None or (kind == 'word' and previous == (kind, signature)), f'Conflicting or duplicate ID: {item["id"]}')
        identities[item['id']] = (kind, signature)

    def common(item, path):
        for item_path, node in lessons.walk(item, path):
            if 'segments' in node:
                for segment in node['segments']:
                    check(lessons.needs_reading(segment) == ('ruby' in segment), f'{item_path}: missing or misplaced contextual ruby')
            if 'source_id' in node:
                source = source_map.get(node['source_id'])
                check(source is not None, f'{item_path}: unknown source')
                if 'pdf_page_start' in node:
                    check(1 <= node['pdf_page_start'] <= node['pdf_page_end'] <= source['page_count'], f'{item_path}: invalid source pages')
            if item_path.rsplit('.', 1)[-1] in BILINGUAL:
                check(all(node[locale].strip() for locale in lessons.AUTHORED_LANGUAGES), f'{item_path}: blank Vietnamese/English text')

    def word(item, path):
        nonlocal word_count
        identity(item, 'word')
        check(lessons.normalized(lessons.reading(item['japanese'])) == lessons.normalized(item['kana_reading']), f'{path}: kana/ruby mismatch')
        word_count += 1

    set_levels = set()
    for data in sets:
        lessons.schema_check(data, character_schema, character_schema)
        level = data['source_level_label']
        check(level not in set_levels, f'Duplicate character set: {level}')
        set_levels.add(level)
        common(data, level)
        local_numbers = set()
        for entry in data['entries']:
            identity(entry, 'character')
            number = entry['source_character_number']
            glyph = entry['character']
            check(number in NUMBER_RANGES[level] and number not in numbers, f'Wrong/duplicate source character number: {number}')
            check(glyph not in masters, f'Duplicate master glyph: {glyph}')
            check(entry['on_readings'] or entry['kun_readings'], f'No source-listed reading: {glyph}')
            check(any(glyph in lessons.surface(w['japanese']) for w in entry['examples']), f'No example containing the target character: {glyph}')
            numbers[number] = glyph
            masters[glyph] = entry
            local_numbers.add(number)
            for index, example in enumerate(entry['examples']):
                word(example, f'{level}.{glyph}.examples[{index}]')
        if complete:
            check(local_numbers == NUMBER_RANGES[level], f'Character-number coverage differs from source set: {level}')

    unit_numbers = set()
    referenced_glyphs = set()
    missing_master_links = set()
    for unit in units:
        lessons.schema_check(unit, unit_schema, unit_schema)
        n = unit['reference_unit_number']
        reference = reference_units.get(n)
        check(reference is not None and n not in unit_numbers, f'Unknown/duplicate unit: {n}')
        unit_numbers.add(n)
        check(unit['source_level_label'] == reference['level_label_from_filename'], f'Unit {n}: wrong source level')
        for key in ('publisher_lesson_milestone', 'reference_lesson_scope', 'relationship'):
            check(unit[key] == reference[key], f'Unit {n}: {key} differs from source relationship')
        check(unit['review_state'] == SELF_REVIEW_STATE, f'Unit {n}: unsupported review/release claim')
        identity(unit, 'unit')
        common(unit, f'unit-{n:02}')
        referenced_glyphs.update(unit['character_glyphs'])
        missing_master_links.update(set(unit['character_glyphs']) - set(masters))
        for index, example in enumerate(unit['word_examples']):
            word(example, f'unit-{n:02}.word_examples[{index}]')
    if complete:
        check(set_levels == set(NUMBER_RANGES), 'Missing N5/N4 character set')
        check(unit_numbers == set(reference_units), 'Kanji unit coverage is incomplete')
        check(not missing_master_links, f'Unresolved unit glyphs: {sorted(missing_master_links)}')
    return {'characters': len(masters), 'kanji_units': len(units), 'kanji_word_occurrences': word_count, 'unique_kanji_word_ids': sum(kind == 'word' for kind, _ in identities.values()), 'unit_character_links': sum(len(u['character_glyphs']) for u in units), 'unit_glyphs_without_master': sorted(missing_master_links), 'dictionary_only_glyphs': sorted(set(masters) - referenced_glyphs), 'entity_ids': set(identities)}

def negative_fixtures(sets, units, catalog, cs, us):
    check(sets and units, 'Kanji fixtures require authored master and unit data')
    cases = ('duplicate_character', 'wrong_source_number', 'missing_target_example', 'wrong_word_reading', 'wrong_unit_milestone', 'unapproved_release', 'empty_meaning', 'invalid_source_page')
    for case in cases:
        broken_sets = copy.deepcopy(sets)
        broken_units = copy.deepcopy(units)
        entry = broken_sets[0]['entries'][0]
        unit = broken_units[0]
        if case == 'duplicate_character':
            broken_sets[0]['entries'].append(copy.deepcopy(entry))
        elif case == 'wrong_source_number':
            entry['source_character_number'] = 99999
        elif case == 'missing_target_example':
            entry['examples'][0]['japanese'] = {'segments': [{'base': 'かな'}]}
            entry['examples'][0]['kana_reading'] = 'かな'
            entry['examples'] = entry['examples'][:1]
        elif case == 'wrong_word_reading':
            entry['examples'][0]['kana_reading'] = 'まちがい'
        elif case == 'wrong_unit_milestone':
            unit['publisher_lesson_milestone']['global_lesson_number'] = 50 if unit['publisher_lesson_milestone']['global_lesson_number'] != 50 else 1
        elif case == 'unapproved_release':
            unit['review_state']['release_status'] = 'approved'
        elif case == 'empty_meaning':
            entry['meanings']['vi'] = ' '
        elif case == 'invalid_source_page':
            entry['source_refs'][0]['pdf_page_start'] = 0
        try:
            validate_kanji(broken_sets, broken_units, catalog, cs, us, False)
        except (BatchError, lessons.ValidationError):
            continue
        raise BatchError(f'Negative fixture was accepted: {case}')
    return len(cases)

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(COMPLETE, action='store_true', help='Require all 50 source lessons, 50 units and all 536 reference entries.')
    parser.add_argument(SELF_TEST, action='store_true')
    parser.add_argument(REPORT, type=Path)
    args = parser.parse_args()
    catalog = read(CATALOG)
    schema = read(LESSON_SCHEMA)
    character_schema = read(CHARACTER_SCHEMA)
    unit_schema = read(UNIT_SCHEMA)
    for shape in (schema, character_schema, unit_schema):
        lessons.schema_keywords(shape)
    lesson_paths = sorted(AUTHORING.glob(LESSON_GLOB))
    samples = [read(path) for path in lesson_paths]
    lessons.validate_payload(samples, schema, catalog, read(ANCHORS))
    actual_numbers = [s['reference_lesson_number'] for s in samples]
    check(len(set(actual_numbers)) == len(actual_numbers), 'Duplicate lesson reference number')
    if args.complete:
        check(set(actual_numbers) == {r['number'] for r in catalog['lessons']}, 'Lesson coverage is incomplete')
    set_paths = [KANJI / name for name in SET_NAMES if (KANJI / name).is_file()]
    unit_paths = sorted(KANJI.glob(UNIT_GLOB))
    sets = [read(p) for p in set_paths]
    units = [read(p) for p in unit_paths]
    stats = validate_kanji(sets, units, catalog, character_schema, unit_schema, args.complete)
    correction_flags = validate_correction_ledger(read(CORRECTIONS), sets, catalog, samples)
    lesson_ids = {entity['id'] for sample in samples for entity in [sample, *[item for key in lessons.ENTITY_COLLECTIONS for item in sample[key]]]}
    check(not (lesson_ids & stats.pop('entity_ids')), 'Lesson/Kanji entity ID collision')
    for source in catalog['sources']:
        check(hashlib.sha256((ROOT / source['relative_path']).read_bytes()).hexdigest() == source['sha256'], f'Source PDF changed: {source["id"]}')
    fixture_count = negative_fixtures(sets, units, catalog, character_schema, unit_schema) if args.self_test else 0
    result = {'status': 'complete_structure_passed' if args.complete else 'in_progress_structure_passed', 'scope': 'Editorial shape, identity, reading consistency, reference relationships and source checksums; not linguistic/release acceptance.', 'lessons': len(samples), **{key: sum(len(s[key]) for s in samples) for key in lessons.ENTITY_COLLECTIONS}, **stats, 'source_pdf_checksums_matched': len(catalog['sources']), 'source_discrepancies_requiring_recheck': correction_flags, 'source_discrepancies_owner_confirmed': sorted(item['id'] for item in read(CORRECTIONS)['items'] if item['review_status'] == 'owner_confirmed'), 'kanji_negative_fixtures_rejected': fixture_count, 'editorial_authority': 'B-U-51 primary-agent self-review with B-U-54 delegated cross-checking and B-U-57 owner-confirmed source corrections', 'independent_human_review': 'not_claimed', 'release_status': 'draft_not_for_release', 'languages_authored': sorted(lessons.AUTHORED_LANGUAGES), 'languages_missing': sorted(lessons.RELEASE_LANGUAGES - lessons.AUTHORED_LANGUAGES)}
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(json.dumps(result, ensure_ascii=False, indent=2) + NEWLINE, encoding=UTF8)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0

if __name__ == '__main__':
    try:
        sys.exit(main())
    except (BatchError, lessons.ValidationError, KeyError, ValueError, OSError) as error:
        print(f'FAILED: {error}', file=sys.stderr)
        sys.exit(1)
