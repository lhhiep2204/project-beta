#!/usr/bin/env python3
"""Validate T03 authoring, its source denominator and revision-bound self-review.

No TTS engine, application, historical-accent or independent-human certification.
Uses only the standard library and the repository's supported schema walker.
"""
import argparse
from collections import Counter
import copy
import hashlib
import json
from pathlib import Path
import re
import sys
import unicodedata

sys.dont_write_bytecode = True
import validate_authoring_samples as shared

ROOT = Path(__file__).resolve().parents[1]
DIRECTORY = ROOT / 'docs/content-authoring/kana'
INPUTS = ['inventory.json', 'source-inventory.json', 'kana.schema.json']
CHECKS = {'source_coverage', 'reading_context', 'vi_en_meaning', 'usage_guidance'}


def read(name):
    return json.loads((DIRECTORY / name).read_text())


def digest(value):
    return hashlib.sha256(json.dumps(value, ensure_ascii=False, sort_keys=True,
                                     separators=(',', ':')).encode()).hexdigest()


def need(condition, message):
    if not condition:
        raise ValueError(message)


def hiragana(text):
    return ''.join(chr(ord(c) - 0x60) if 'ァ' <= c <= 'ヶ' else c for c in text)


def plain(example):
    return ''.join(s['base'] for s in example['japanese']['segments'])


def validate(data, inventory, schema, review=None, complete=False):
    shared.schema_keywords(schema)
    shared.schema_check(data, schema, schema)
    entries = data['entries']
    identifiers = [e['id'] for e in entries] + [x['id'] for e in entries for x in e['examples']]
    need(len(set(identifiers)) == len(identifiers), 'Duplicate entry/example UUID')
    by_key = {e['key']: e for e in entries}
    need(len(by_key) == len(entries), 'Duplicate editorial key')
    sources = {s['id']: s for s in inventory['sources']}
    need(len(sources) == len(inventory['sources']), 'Duplicate source ID')
    for source in sources.values():
        need(source['url'].startswith('https://') and source['scope'] and source['accessed'],
             'Missing source provenance')
    rows = {r['key']: r for r in inventory['rows']}
    need(len(rows) == len(inventory['rows']) and set(rows) == set(by_key), 'Source/item coverage differs')
    table_ids = [t['id'] for t in inventory['tables']]
    need(len(set(table_ids)) == len(table_ids), 'Duplicate source table')
    expected = []
    for table in inventory['tables']:
        need(table['source_id'] in sources and table['locator'], 'Unknown table source')
        expected.extend(table['keys'])
    expected.extend(inventory['supplemental_keys'])
    need(len(set(expected)) == len(expected) and set(expected) == set(by_key),
         'Source denominator duplicated or incomplete')
    need(inventory['coverage_boundary'] and inventory['exclusions'], 'Missing coverage boundary')
    languages = data['language_coverage']
    need(languages['authored'] == ['en', 'vi'], 'Unexpected authored languages')
    need(set(languages['required_for_release']) == shared.RELEASE_LANGUAGES,
         'Release language scope changed')
    need(set(languages['missing_for_release']) == shared.RELEASE_LANGUAGES - {'en', 'vi'},
         'Missing language gap declaration')
    for e in entries:
        key, glyph = e['key'], e['glyph']
        need(key == ':'.join((e['script'], e['group'], glyph)), 'Inconsistent key: ' + key)
        need(unicodedata.normalize('NFC', glyph) == glyph, 'Non-NFC glyph: ' + key)
        need(re.fullmatch(r'[ぁ-ゖ゛゜ゝゞゟァ-ヺーヽヾヿ]+', glyph), 'Invalid teaching glyph: ' + key)
        if e['script'] == 'hiragana':
            need(not re.search(r'[ァ-ヿ]', glyph), 'Wrong Hiragana script: ' + key)
        if e['script'] == 'katakana':
            need(not re.search(r'[ぁ-ゟ]', glyph), 'Wrong Katakana script: ' + key)
        row = rows[key]
        need(row['entry_id'] == e['id'] and row['source_refs'] == e['source_refs'],
             'Source ID/provenance link changed: ' + key)
        need(row['disposition'] == ('reference' if e['group'] == 'reference' else 'learning'),
             'Rare/reference group mixed into learning: ' + key)
        for ref in e['source_refs']:
            need(ref['source_id'] in sources, 'Unknown entry source: ' + key)
        need(1 <= len(e['examples']) <= 3, 'Example cap/empty target: ' + key)
        for x in e['examples']:
            reading = x['reading']
            need(re.fullmatch(r'[ぁ-ゖー]+', reading), 'Invalid context reading: ' + key)
            need(unicodedata.normalize('NFC', reading) == reading, 'Non-NFC reading: ' + key)
            reconstructed = ''.join(s.get('ruby', s['base']) for s in x['japanese']['segments'])
            need(hiragana(reconstructed) == reading, 'Context/ruby reading mismatch: ' + key)
            for s in x['japanese']['segments']:
                need(not re.search(r'[\u3400-\u9fff]', s['base']) or 'ruby' in s,
                     'Kanji context without ruby: ' + key)
            for value in x['translation'].values():
                need(value.strip(), 'Empty meaning: ' + key)
            relation = x['target_relation']
            if relation == 'contains':
                text = plain(x)
                # シ in シャ is not an example of the simple シ sound; similarly
                # ヴ in ヴァ cannot cover the uncombined ヴ table cell.
                small = 'ぁぃぅぇぉゃゅょゎァィゥェォャュョヮ'
                matches = list(re.finditer(re.escape(glyph), text))
                need(any(m.end() == len(text) or text[m.end()] not in small for m in matches),
                     'Example does not illustrate the actual sound: ' + key)
            elif relation == 'composition':
                mark = {'゛': '\u3099', '゜': '\u309a'}.get(glyph)
                need(mark and mark in unicodedata.normalize('NFD', plain(x)),
                     'Voicing mark missing from composed context: ' + key)
            elif relation == 'vowel_pattern':
                need(e['group'] == 'long_vowel', 'Vowel-pattern relation outside long vowels')
            else:
                need(e['group'] == 'reference', 'Reference relation in a modern learning cell')
        speech = e['speech']
        dependent = e['group'] in {'special', 'long_vowel', 'particle', 'reference'} or glyph in {'ん', 'ン', 'を', 'ヲ', 'ぢ', 'ヂ', 'づ', 'ヅ'}
        need(not dependent or speech['mode'] == 'context', 'Isolated dependent target: ' + key)
        if speech['mode'] == 'context':
            need(speech['text'] in [x['reading'] for x in e['examples']], 'Unreviewed speech context: ' + key)
            need(len(speech['text']) > 1, 'Dependent context is still isolated: ' + key)
        else:
            need(speech['text'] == glyph, 'Changed syllable speech target: ' + key)
    if complete:
        need(review is not None and review['status'] == 'primary_self_review_complete', 'Primary content review incomplete')
        need(review['independent_human_review'] == 'not_claimed' and review['native_tts_review'] == 'not_performed',
             'Unsupported review claim')
        for name, value in zip(INPUTS, [data, inventory, schema]):
            need(review['input_digests'][name] == digest(value), 'Stale reviewed input: ' + name)
        reviewed = {r['entry_id']: r for r in review['items']}
        need(len(reviewed) == len(review['items']) == len(entries), 'Item review coverage differs')
        for e in entries:
            r = reviewed.get(e['id'], {})
            need(r.get('entry_digest') == digest(e) and r.get('verdict') == 'accepted_for_authoring',
                 'Unreviewed or changed entry: ' + e['key'])
            need(set(r['checks']) == CHECKS and r['example_ids'] == [x['id'] for x in e['examples']],
                 'Incomplete per-item content review: ' + e['key'])
    return dict(entries=len(entries), examples=sum(len(e['examples']) for e in entries),
                learning_entries=sum(e['group'] != 'reference' for e in entries),
                reference_entries=sum(e['group'] == 'reference' for e in entries),
                groups=dict(sorted(Counter(e['script'] + ':' + e['group'] for e in entries).items())),
                source_tables={t['id']: len(t['keys']) for t in inventory['tables']})


def negative_fixtures(data, inventory, schema, review):
    """Semantic fixtures run WITHOUT review pins, so hash failure cannot mask bugs."""
    def four_examples(data, inventory):
        examples = []
        for n in range(4):
            example = copy.deepcopy(data['entries'][0]['examples'][0])
            example['id'] = f'f0000000-0000-4000-8000-{n:012d}'
            examples.append(example)
        data['entries'][0]['examples'] = examples

    mutations = [
        ('missing-cell', lambda d, i: d['entries'].pop()),
        ('duplicate-id', lambda d, i: d['entries'][1].update(id=d['entries'][0]['id'])),
        ('duplicate-example-id', lambda d, i: d['entries'][1]['examples'][0].update(id=d['entries'][0]['examples'][0]['id'])),
        ('empty-meaning', lambda d, i: d['entries'][0]['examples'][0]['translation'].update(vi='')),
        ('reading-mismatch', lambda d, i: d['entries'][0]['examples'][0].update(reading='いぬ')),
        ('unknown-source', lambda d, i: d['entries'][0]['source_refs'][0].update(source_id='unknown')),
        ('wrong-source-link', lambda d, i: i['rows'][0].update(entry_id=d['entries'][1]['id'])),
        ('lost-denominator', lambda d, i: i['tables'][0]['keys'].pop()),
        ('duplicate-denominator', lambda d, i: i['tables'][0]['keys'].append(i['tables'][0]['keys'][0])),
        ('reference-mixed', lambda d, i: i['rows'][-1].update(disposition='learning')),
        ('missing-language-gap', lambda d, i: d['language_coverage'].update(missing_for_release=[])),
        ('unapproved-learned-filter', lambda d, i: d['entries'][0].update(learned_lesson=1)),
        ('display-romaji', lambda d, i: d['entries'][0].update(romaji='a')),
        ('wrong-script', lambda d, i: d['entries'][0].update(glyph='ア')),
        ('unknown-speech-context', lambda d, i: d['entries'][-1]['speech'].update(text='あいうえお')),
        ('isolated-small-kana', lambda d, i: next(e for e in d['entries'] if e['glyph'] == 'っ')['speech'].update(mode='syllable', text='っ')),
        ('isolated-length-mark', lambda d, i: next(e for e in d['entries'] if e['glyph'] == 'ー')['speech'].update(mode='syllable', text='ー')),
        ('isolated-reference-mark', lambda d, i: next(e for e in d['entries'] if e['glyph'] == 'ゝ')['speech'].update(mode='syllable', text='ゝ')),
        ('wrong-sound-context', lambda d, i: next(e for e in d['entries'] if e['glyph'] == 'シ')['examples'][0].update(japanese={'segments': [{'base': 'シャツ'}]}, reading='しゃつ')),
        ('four-examples', four_examples),
        ('no-voiced-context', lambda d, i: next(e for e in d['entries'] if e['glyph'] == '゛')['examples'][0].update(japanese={'segments': [{'base': 'かさ'}]}, reading='かさ')),
    ]
    rejected = []
    for name, mutate in mutations:
        d, i = copy.deepcopy(data), copy.deepcopy(inventory)
        mutate(d, i)
        try:
            validate(d, i, schema)
        except ValueError:
            rejected.append(name)
        else:
            raise ValueError('Negative fixture accepted: ' + name)
    for name in ['stale-review', 'missing-item-review', 'unreviewed-example', 'missing-content-check']:
        r = copy.deepcopy(review)
        if name == 'stale-review':
            r['input_digests']['inventory.json'] = '0' * 64
        elif name == 'missing-item-review':
            r['items'].pop()
        elif name == 'unreviewed-example':
            r['items'][0]['example_ids'] = []
        else:
            r['items'][0]['checks'] = ['source_coverage']
        try:
            validate(data, inventory, schema, r, complete=True)
        except ValueError:
            rejected.append(name)
        else:
            raise ValueError('Review fixture accepted: ' + name)
    return rejected


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--self-test', action='store_true')
    parser.add_argument('--complete', action='store_true', help='Require revision-bound primary authoring review; never a release pass.')
    output = parser.add_mutually_exclusive_group()
    output.add_argument('--write', action='store_true')
    output.add_argument('--check', action='store_true')
    args = parser.parse_args()
    data, inventory, schema = [read(p) for p in INPUTS]
    review = read('review.json')
    counts = validate(data, inventory, schema, review, complete=args.complete)
    fixtures = negative_fixtures(data, inventory, schema, review) if args.self_test else []
    pins = {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in [DIRECTORY / n for n in INPUTS + ['review.json']] + [Path(__file__), ROOT / 'scripts/validate_authoring_samples.py']}
    report = dict(task='P0-T03', status='passed', scope='Kana authoring structure, source-table mapping and primary self-review integrity; not independent linguistic, historical-accent, runtime or release acceptance.',
                  task_authoring_acceptance_complete=args.complete, counts=counts,
                  negative_fixtures_rejected=fixtures, input_and_validator_sha256=pins,
                  limits=review['limits'])
    path = DIRECTORY / 'validation-report.json'
    if args.write:
        path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
    if args.check:
        need(json.loads(path.read_text()) == report, 'Stale kana validation report; use the same --complete/--self-test flags with --write')
    print(f"PASS: {counts['entries']} kana entries, {counts['examples']} contexts, {len(fixtures)} rejected fixtures; primary authoring review {'required and checked' if args.complete else 'not required'}.")
    print('LIMITS: no independent-human, app, TTS, device, other-17-language or release acceptance.')


if __name__ == '__main__':
    try:
        main()
    except (ValueError, KeyError) as error:
        raise SystemExit('FAIL: ' + str(error))
