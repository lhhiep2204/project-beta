"""Validate the draft authoring format and its local references using the standard library.

The schema walker supports only the JSON Schema keywords used by this draft. It
rejects unsupported keywords rather than claiming general JSON Schema coverage.
Structural success is not independent linguistic, translation or release approval.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
import re
import sys
import unicodedata
import uuid
from pathlib import Path

REPOSITORY = Path(__file__).resolve().parents[1]
AUTHORING_DIRECTORY = REPOSITORY / 'docs/content-authoring'
SCHEMA_FILE = 'authoring.schema.json'
CATALOG_FILE = 'docs/reference-inventory/catalog.json'
SOURCE_CHECKS_FILE = 'source-checks.json'
LESSON_FILE_GLOB = 'lesson-*.json'
ANCHOR_LESSONS = {'N5': 1, 'N4': 26}
REPORT_FILE = 'validation-report.json'
UTF8 = 'utf-8'
NEWLINE = '\n'
EMPTY = ''
ROOT_PATH = '$'
REFERENCE_PREFIX = '#/$defs/'
REF = '$ref'
DEFINITIONS = '$defs'
TYPE = 'type'
PROPERTIES = 'properties'
REQUIRED = 'required'
ADDITIONAL = 'additionalProperties'
ITEMS = 'items'
MIN_ITEMS = 'minItems'
UNIQUE_ITEMS = 'uniqueItems'
MIN_LENGTH = 'minLength'
MINIMUM = 'minimum'
MAXIMUM = 'maximum'
PATTERN = 'pattern'
FORMAT = 'format'
UUID_FORMAT = 'uuid'
UNKNOWN_FIXTURE_ID = '00000000-0000-4000-8000-000000000000'
ENUM = 'enum'
CONST = 'const'
ALLOWED_SCHEMA_KEYS = frozenset((
    '$schema', '$id', 'title', 'description', DEFINITIONS, REF, TYPE, PROPERTIES,
    REQUIRED, ADDITIONAL, ITEMS, MIN_ITEMS, UNIQUE_ITEMS, MIN_LENGTH, MINIMUM,
    MAXIMUM, PATTERN, FORMAT, ENUM, CONST,
))
OBJECT_TYPE = 'object'
ARRAY_TYPE = 'array'
STRING_TYPE = 'string'
INTEGER_TYPE = 'integer'
BOOLEAN_TYPE = 'boolean'
TYPES = {OBJECT_TYPE: dict, ARRAY_TYPE: list, STRING_TYPE: str, INTEGER_TYPE: int, BOOLEAN_TYPE: bool}
ENTITY_COLLECTIONS = ('vocabulary', 'grammar_points', 'sentence_patterns', 'examples', 'dialogues')
BILINGUAL_FIELDS = frozenset(('title', 'text', 'explanation', 'notes', 'translation', 'description', 'label', 'scenario', 'context'))
AUTHORED_LANGUAGES = frozenset(('en', 'vi'))
RELEASE_LANGUAGES = frozenset(('ar', 'bn', 'zh-Hans', 'nl', 'en', 'fr', 'de', 'he', 'hi', 'id', 'it', 'ko', 'pt', 'ru', 'es', 'th', 'tr', 'uk', 'vi'))
KANJI_PATTERN = re.compile(r'[\u3400-\u9fff々〆ヶ]')
LATIN_ABBREVIATION_PATTERN = re.compile(r'[A-Z][A-Z0-9]{1,7}')
SPACE_PATTERN = re.compile(r'\s+')
SLOT_KIND = 'slot'
LITERAL_KIND = 'literal'
VERB_KIND = 'verb'
SELF_TEST_OPTION = '--self-test'
REPORT_OPTION = '--report'
SELF_TEST_DEST = 'self_test'
REPORT_DEST = 'report'
STORE_TRUE = 'store_true'
CLI_DESCRIPTION = 'Validate ProjectBeta editorial lesson drafts; no app build or dependencies required.'
CLI_SELF_TEST_HELP = 'Run negative fixtures for meaningful structure/reference regressions.'
CLI_REPORT_HELP = 'Write the structural verification result to this JSON path.'
ERROR_FORMAT = '{path}: {message}'
CHILD_PATH = '{path}.{key}'
INDEX_PATH = '{path}[{index}]'
FAILURE_FORMAT = 'FAILED: {error}'
SUCCESS_FORMAT = 'Validated {lessons} lessons, {vocabulary} vocabulary entries, {grammar} grammar points, {patterns} patterns, {examples} examples and {dialogues} dialogues; {source_checks} source anchors; {negative_fixtures} negative fixtures.'
ERRORS = {
    'schema_keys': 'Unsupported schema keywords: {keys}',
    'type': 'Expected {expected}',
    'const': 'Value differs from the required constant',
    'enum': 'Value is outside the allowed choices',
    'required': 'Missing required properties: {keys}',
    'extra': 'Unexpected properties: {keys}',
    'minimum': 'Value is below the required minimum',
    'maximum': 'Value exceeds the required maximum',
    'length': 'String or array is shorter than required',
    'pattern': 'String does not match the required pattern',
    'uuid': 'ID must be an opaque UUID version 4',
    'unique': 'Values must be unique',
    'identity': 'Duplicate editorial ID across the sample package',
    'local_key': 'Duplicate local key',
    'source': 'Unknown or out-of-range source reference',
    'hash': 'Source PDF checksum differs from the catalog',
    'blank_translation': 'Required English/Vietnamese text is blank',
    'ruby': 'Kanji and uppercase Latin abbreviations need explicit contextual kana; ruby must annotate one of those segments',
    'reading': 'Kana reading differs from the concatenated contextual readings',
    'form_link': 'Meaning or dictionary form points to an unknown form',
    'verb': 'Verb group and dictionary-form coverage are required only for verbs',
    'grammar_link': 'Unknown grammar-point reference',
    'pattern_link': 'Unknown pattern or template variant',
    'pattern_coverage': 'Every sentence pattern requires at least one linked complete example',
    'variant_coverage': 'Every declared template variant requires a linked complete example',
    'slots': 'Template slots must exactly match the declared slots',
    'speaker': 'Dialogue turn points to an unknown speaker',
    'languages': 'Draft or release language coverage is incorrect',
    'kanji_unit': 'Unknown reference Kanji unit',
    'lesson': 'Lesson reference is missing or differs from the source level',
    'source_fact': 'A targeted source-image anchor differs from the draft',
    'fixture': 'Invalid fixture was accepted: {name}',
}
FIXTURE_NAMES = (
    'duplicate_id', 'dangling_grammar', 'missing_ruby', 'wrong_reading',
    'missing_english', 'false_release_approval', 'invalid_source_page',
    'dangling_form', 'wrong_verb_group', 'dangling_speaker', 'dangling_slot',
    'missing_template_variant', 'false_language_coverage', 'blank_example_context',
    'pattern_without_example',
    'variant_without_example',
)


class ValidationError(ValueError):
    """An authoring-draft validation failure."""


def require(condition, path, rule, **details):
    if not condition:
        raise ValidationError(ERROR_FORMAT.format(path=path, message=ERRORS[rule].format(**details)))


def read_json(path):
    return json.loads(path.read_text(encoding=UTF8))


def normalized(text):
    return SPACE_PATTERN.sub(EMPTY, unicodedata.normalize('NFKC', text))


def child(path, key):
    return CHILD_PATH.format(path=path, key=key)


def schema_keywords(schema, path=ROOT_PATH):
    require(set(schema) <= ALLOWED_SCHEMA_KEYS, path, 'schema_keys', keys=sorted(set(schema) - ALLOWED_SCHEMA_KEYS))
    for collection in (PROPERTIES, DEFINITIONS):
        for key, value in schema.get(collection, {}).items():
            schema_keywords(value, child(path, key))
    if ITEMS in schema:
        schema_keywords(schema[ITEMS], child(path, ITEMS))


def schema_check(value, schema, root, path=ROOT_PATH):
    if REF in schema:
        require(schema[REF].startswith(REFERENCE_PREFIX), path, 'source')
        schema = root[DEFINITIONS][schema[REF][len(REFERENCE_PREFIX):]]
    if TYPE in schema:
        expected = schema[TYPE]
        valid = isinstance(value, TYPES[expected])
        if expected == INTEGER_TYPE:
            valid = valid and not isinstance(value, bool)
        require(valid, path, 'type', expected=expected)
    if CONST in schema:
        require(value == schema[CONST], path, 'const')
    if ENUM in schema:
        require(value in schema[ENUM], path, 'enum')
    if isinstance(value, dict):
        properties = schema.get(PROPERTIES, {})
        require(set(schema.get(REQUIRED, ())) <= set(value), path, 'required', keys=sorted(set(schema.get(REQUIRED, ())) - set(value)))
        if schema.get(ADDITIONAL) is False:
            require(set(value) <= set(properties), path, 'extra', keys=sorted(set(value) - set(properties)))
        for key, item in value.items():
            if key in properties:
                schema_check(item, properties[key], root, child(path, key))
    elif isinstance(value, list):
        require(len(value) >= schema.get(MIN_ITEMS, 0), path, 'length')
        if schema.get(UNIQUE_ITEMS):
            require(len({json.dumps(v, sort_keys=True, ensure_ascii=False) for v in value}) == len(value), path, 'unique')
        for index, item in enumerate(value):
            schema_check(item, schema.get(ITEMS, {}), root, INDEX_PATH.format(path=path, index=index))
    elif isinstance(value, str):
        require(len(value) >= schema.get(MIN_LENGTH, 0), path, 'length')
        if PATTERN in schema:
            require(re.search(schema[PATTERN], value) is not None, path, 'pattern')
        if schema.get(FORMAT) == UUID_FORMAT:
            try:
                parsed = uuid.UUID(value)
            except ValueError:
                parsed = None
            require(parsed is not None and parsed.version == 4 and str(parsed) == value, path, 'uuid')
    elif isinstance(value, (int, float)):
        if MINIMUM in schema:
            require(value >= schema[MINIMUM], path, 'minimum')
        if MAXIMUM in schema:
            require(value <= schema[MAXIMUM], path, 'maximum')


def walk(value, path=ROOT_PATH):
    if isinstance(value, dict):
        yield path, value
        for key, item in value.items():
            yield from walk(item, child(path, key))
    elif isinstance(value, list):
        for index, item in enumerate(value):
            yield from walk(item, INDEX_PATH.format(path=path, index=index))


def surface(text):
    return EMPTY.join(segment['base'] for segment in text['segments'])


def reading(text):
    return EMPTY.join(segment.get('ruby', segment['base']) for segment in text['segments'])


def needs_reading(segment):
    return bool(KANJI_PATTERN.search(segment['base']) or LATIN_ABBREVIATION_PATTERN.fullmatch(segment['base']))


def semantic_check(samples, catalog, source_anchors):
    ids = set()
    sources = {s['id']: s for s in catalog['sources']}
    reference_lessons = {r['number']: r for r in catalog['lessons']}
    units = {u['id'] for u in catalog['kanji_units']}
    for sample in samples:
        path = sample['editorial_key']
        entities = [sample] + [item for key in ENTITY_COLLECTIONS for item in sample[key]]
        for entity in entities:
            require(entity['id'] not in ids, path, 'identity')
            ids.add(entity['id'])
        for key in ENTITY_COLLECTIONS:
            keys = [r['editorial_key'] for r in sample[key]]
            require(len(keys) == len(set(keys)), child(path, key), 'local_key')
        language = sample['language_coverage']
        require(set(language['authored']) == AUTHORED_LANGUAGES and set(language['required_for_release']) == RELEASE_LANGUAGES and set(language['missing_for_release']) == RELEASE_LANGUAGES - AUTHORED_LANGUAGES, path, 'languages')
        reference = reference_lessons.get(sample['reference_lesson_number'])
        require(reference is not None and reference['level_label_from_filename'] == sample['source_level_label'], path, 'lesson')
        require(set(sample['kanji_reference_units']) <= units and sample['kanji_reference_units'] == reference['kanji_reference_units'], path, 'kanji_unit')
        for item_path, item in walk(sample, path):
            if 'segments' in item:
                for segment in item['segments']:
                    require(needs_reading(segment) == ('ruby' in segment), item_path, 'ruby')
            if 'source_id' in item:
                source = sources.get(item['source_id'])
                require(source is not None and 1 <= item['pdf_page_start'] <= item['pdf_page_end'] <= source['page_count'], item_path, 'source')
            if item_path.rsplit('.', 1)[-1] in BILINGUAL_FIELDS:
                require(all(item[locale].strip() for locale in AUTHORED_LANGUAGES), item_path, 'blank_translation')
        for item in sample['vocabulary']:
            forms = {f['key']: f for f in item['forms']}
            require(len(forms) == len(item['forms']), path, 'local_key')
            for f in item['forms']:
                require(normalized(reading(f['japanese'])) == normalized(f['kana_reading']), child(path, item['editorial_key']), 'reading')
            for meaning in item['meanings']:
                require(set(meaning['form_keys']) <= set(forms), path, 'form_link')
            require({k for meaning in item['meanings'] for k in meaning['form_keys']} == set(forms), path, 'form_link')
            if item['entry_type'] == VERB_KIND:
                dictionaries = item.get('dictionary_forms', [])
                require('verb_group' in item and 'dictionary_form_method' in item and {d['form_key'] for d in dictionaries} == set(forms) and len(dictionaries) == len(forms), path, 'verb')
                for d in dictionaries:
                    require(normalized(reading(d['japanese'])) == normalized(d['kana_reading']), path, 'reading')
            else:
                require(not any(k in item for k in ('verb_group', 'dictionary_forms', 'dictionary_form_method')), path, 'verb')
        grammar_ids = {g['id'] for g in sample['grammar_points']}
        patterns = {p['id']: p for p in sample['sentence_patterns']}
        require(set(patterns) <= {e['pattern_id'] for e in sample['examples']}, path, 'pattern_coverage')
        required_variants = {(p['id'], t['key']) for p in patterns.values() for t in p['templates']}
        require(required_variants <= {(e['pattern_id'], e['pattern_variant_key']) for e in sample['examples']}, path, 'variant_coverage')
        for pattern in patterns.values():
            require(pattern['grammar_point_id'] in grammar_ids, path, 'grammar_link')
            slots = {s['key'] for s in pattern['slots']}
            require(len(slots) == len(pattern['slots']), path, 'local_key')
            variants = [t['key'] for t in pattern['templates']]
            require(len(variants) == len(set(variants)), path, 'local_key')
            for template in pattern['templates']:
                require({p['value'] for p in template['pieces'] if p['kind'] == SLOT_KIND} == slots, path, 'slots')
        for example in sample['examples']:
            pattern = patterns.get(example['pattern_id'])
            require(pattern is not None and example['pattern_variant_key'] in {t['key'] for t in pattern['templates']}, path, 'pattern_link')
            require(set(example['grammar_point_ids']) <= grammar_ids and pattern['grammar_point_id'] in example['grammar_point_ids'], path, 'grammar_link')
        for dialogue in sample['dialogues']:
            characters = {c['key'] for c in dialogue['characters']}
            require(len(characters) == len(dialogue['characters']), path, 'local_key')
            for turn in dialogue['turns']:
                require(turn['speaker_key'] in characters, path, 'speaker')
                require(set(turn['grammar_point_ids']) <= grammar_ids, path, 'grammar_link')
    samples_by_number = {s['reference_lesson_number']: s for s in samples}
    for anchor in source_anchors['checks']:
        sample = samples_by_number[anchor.get('reference_lesson_number', ANCHOR_LESSONS[anchor['source_level_label']])]
        vocabulary = next(v for v in sample['vocabulary'] if v['editorial_key'] == anchor['vocabulary_key'])
        f = next(f for f in vocabulary['forms'] if f['key'] == anchor['form_key'])
        valid = surface(f['japanese']) == anchor['expected_surface'] and f['kana_reading'] == anchor['expected_kana']
        if 'expected_verb_group' in anchor:
            valid = valid and vocabulary.get('verb_group') == anchor['expected_verb_group']
        require(valid, anchor['vocabulary_key'], 'source_fact')


def validate_payload(samples, schema, catalog, anchors):
    for sample in samples:
        schema_check(sample, schema, schema)
    semantic_check(samples, catalog, anchors)


def negative_fixtures(samples, schema, catalog, anchors):
    by_number = {sample['reference_lesson_number']: sample for sample in samples}
    fixture_samples = [by_number[number] for number in ANCHOR_LESSONS.values()]
    for name in FIXTURE_NAMES:
        broken = copy.deepcopy(fixture_samples)
        first, second = broken
        if name == 'duplicate_id':
            first['vocabulary'][1]['id'] = first['vocabulary'][0]['id']
        elif name == 'dangling_grammar':
            first['examples'][0]['grammar_point_ids'] = [UNKNOWN_FIXTURE_ID]
        elif name == 'missing_ruby':
            first['vocabulary'][6]['forms'][0]['japanese']['segments'][0].pop('ruby')
        elif name == 'wrong_reading':
            first['vocabulary'][6]['forms'][0]['kana_reading'] = 'がくせい'
        elif name == 'missing_english':
            first['title'].pop('en')
        elif name == 'false_release_approval':
            first['review_state']['release_status'] = 'approved'
        elif name == 'invalid_source_page':
            first['source_refs'][0]['pdf_page_start'] = 0
        elif name == 'dangling_form':
            first['vocabulary'][0]['meanings'][0]['form_keys'] = ['unknown']
        elif name == 'wrong_verb_group':
            second['vocabulary'][0]['verb_group'] = 'I'
        elif name == 'dangling_speaker':
            first['dialogues'][0]['turns'][0]['speaker_key'] = 'unknown'
        elif name == 'dangling_slot':
            first['sentence_patterns'][0]['templates'][0]['pieces'][0]['value'] = 'unknown'
        elif name == 'missing_template_variant':
            first['examples'][0]['pattern_variant_key'] = 'unknown'
        elif name == 'false_language_coverage':
            first['language_coverage']['missing_for_release'] = []
        elif name == 'blank_example_context':
            second['examples'][0]['context']['vi'] = ' '
        elif name == 'pattern_without_example':
            pattern_id = first['sentence_patterns'][0]['id']
            first['examples'] = [e for e in first['examples'] if e['pattern_id'] != pattern_id]
        elif name == 'variant_without_example':
            pattern = next(p for p in first['sentence_patterns'] if len(p['templates']) > 1)
            variant = pattern['templates'][0]['key']
            first['examples'] = [e for e in first['examples'] if (e['pattern_id'], e['pattern_variant_key']) != (pattern['id'], variant)]
        try:
            validate_payload(broken, schema, catalog, anchors)
        except ValidationError:
            continue
        require(False, ROOT_PATH, 'fixture', name=name)
    return len(FIXTURE_NAMES)


def main():
    parser = argparse.ArgumentParser(description=CLI_DESCRIPTION)
    parser.add_argument(SELF_TEST_OPTION, dest=SELF_TEST_DEST, action=STORE_TRUE, help=CLI_SELF_TEST_HELP)
    parser.add_argument(REPORT_OPTION, dest=REPORT_DEST, type=Path, help=CLI_REPORT_HELP)
    args = parser.parse_args()
    schema = read_json(AUTHORING_DIRECTORY / SCHEMA_FILE)
    catalog = read_json(REPOSITORY / CATALOG_FILE)
    anchors = read_json(AUTHORING_DIRECTORY / SOURCE_CHECKS_FILE)
    samples = [read_json(path) for path in sorted(AUTHORING_DIRECTORY.glob(LESSON_FILE_GLOB))]
    schema_keywords(schema)
    validate_payload(samples, schema, catalog, anchors)
    for source in catalog['sources']:
        digest = hashlib.sha256((REPOSITORY / source['relative_path']).read_bytes()).hexdigest()
        require(digest == source['sha256'], source['id'], 'hash')
    fixture_count = negative_fixtures(samples, schema, catalog, anchors) if args.self_test else 0
    counts = {key: sum(len(s[key]) for s in samples) for key in ENTITY_COLLECTIONS}
    result = {
        'scope': 'Draft structure, reference integrity and targeted primary source anchors only.',
        'structure_validation': 'passed',
        'lessons': len(samples), **counts,
        'source_anchors_checked': len(anchors['checks']),
        'source_pdf_checksums_matched': len(catalog['sources']),
        'negative_fixtures_rejected': fixture_count,
        'languages_authored': sorted(AUTHORED_LANGUAGES),
        'release_languages_missing': sorted(RELEASE_LANGUAGES - AUTHORED_LANGUAGES),
        'independent_japanese_review': 'pending',
        'translation_review': 'pending',
        'release_status': 'draft_not_for_release',
    }
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(json.dumps(result, ensure_ascii=False, indent=2) + NEWLINE, encoding=UTF8)
    print(SUCCESS_FORMAT.format(lessons=len(samples), vocabulary=counts['vocabulary'], grammar=counts['grammar_points'], patterns=counts['sentence_patterns'], examples=counts['examples'], dialogues=counts['dialogues'], source_checks=len(anchors['checks']), negative_fixtures=fixture_count))
    return 0


if __name__ == '__main__':
    try:
        sys.exit(main())
    except (ValidationError, KeyError, ValueError, OSError) as error:
        print(FAILURE_FORMAT.format(error=error), file=sys.stderr)
        sys.exit(1)
