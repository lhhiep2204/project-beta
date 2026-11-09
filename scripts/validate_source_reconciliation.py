#!/usr/bin/env python3
"""Check T02 source denominators, identity links and the recorded review boundary.

An ordinary pass establishes ledger integrity only. --complete additionally
requires all four recorded content-review gates and the source-derived Kanji inventory.
"""
from __future__ import annotations
import argparse
import copy
import hashlib
import json
from pathlib import Path
import sys

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / 'docs/content-authoring/source-reconciliation'
FILES = ('source-inventory.json', 'vocabulary-ledger.json', 'grammar-ledger.json', 'review.json')
KANJI_FILES = ('kanji-source-inventory.json', 'kanji-ledger.json')


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read(path):
    return json.loads(path.read_text())


def require(value, message):
    if not value:
        raise ValueError(message)


def validate(inventory, vocabulary, grammar, review, catalog, lessons):
    """Pure integrity checks, also exercised by mutations in --self-test."""
    for document in (inventory, vocabulary, grammar, review):
        require(document['format_version'] == 1, 'Unsupported ledger format')
    require(set(review['tasks']) == {'T02.01', 'T02.02', 'T02.03', 'T02.04'},
            'Missing/unknown T02 content-review gate')
    expected_pages = {
        (l['translation_and_grammar']['source_id'], l['translation_and_grammar']['pdf_page_start'] + offset): l['number']
        for l in catalog['lessons'] for offset in (0, 1)
    }
    pages = inventory['vocabulary_pages']
    require(len(pages) == len(expected_pages), 'Missing or duplicate vocabulary page')
    seen_pages, rows = set(), {}
    for page in pages:
        page_key = (page['source_id'], page['pdf_page'])
        require(page_key not in seen_pages and page_key in expected_pages, 'Invalid/duplicate source page')
        seen_pages.add(page_key)
        require(page['lesson'] == expected_pages[page_key], 'Wrong source-page lesson')
        require(page['rows'], 'An assigned vocabulary page has no inventory')
        require(page['review_method'] == 'primary_visual_inventory_from_hash_verified_pdf', 'Missing page-inventory method')
        require([r['ordinal'] for r in page['rows']] == list(range(1, len(page['rows']) + 1)), 'Noncontiguous/duplicate source ordinals')
        for row in page['rows']:
            require(row['label'].strip(), 'Blank source label')
            require(row['scope'] == 'included', 'B-U-59 forbids the superseded fictional-name exclusion')
            key = f'{page["source_id"]}:{page["pdf_page"]}:{row["ordinal"]}'
            rows[key] = (page, row)
    require(seen_pages == set(expected_pages), 'Source-page coverage mismatch')
    words = {w['id']: (n, w) for n, l in lessons.items() for w in l['vocabulary']}
    records = vocabulary['vocabulary']
    require(len(records) == len(rows), 'Missing/duplicate vocabulary disposition')
    seen, mapped_ids, excluded = set(), set(), 0
    mapped_forms = set()
    for record in records:
        key = record['source_row']
        require(key in rows and key not in seen, 'Unknown/duplicate source-row disposition')
        seen.add(key)
        page, row = rows[key]
        require(record['disposition'] in ('mapped', 'excluded'), 'Unresolved vocabulary disposition')
        if record['disposition'] == 'excluded':
            require(row['scope'] == 'excluded_fictional_name', 'Included source row silently excluded')
            require(not record['targets'] and record['note'].strip(), 'Exclusion lacks a reason or contains a target')
            excluded += 1
            continue
        require(row['scope'] == 'included' and record['targets'], 'Invalid/empty mapped source row')
        targets = set()
        for target in record['targets']:
            uid = target['id']
            require(uid in words and uid not in targets, 'Dangling/duplicate authored target')
            targets.add(uid)
            n, word = words[uid]
            require(n == page['lesson'], 'Vocabulary mapped across lessons')
            keys = target['form_keys']
            require(keys and len(keys) == len(set(keys)), 'Empty/duplicate authored form keys')
            require(set(keys) <= {f['key'] for f in word['forms']}, 'Unknown authored form key')
            mapped_forms.update((uid, key) for key in keys)
            mapped_ids.add(uid)
    additions = vocabulary['editorial_additions']
    added_ids = set()
    for addition in additions:
        uid = addition['id']
        require(uid in words and uid not in mapped_ids and uid not in added_ids, 'Invalid/duplicate editorial addition')
        require(addition['lesson'] == words[uid][0] and addition['reason'].strip(), 'Unexplained editorial addition')
        added_ids.add(uid)
    require(mapped_ids | added_ids == set(words), 'Authored vocabulary has no source disposition/addition')
    require(mapped_forms == {(uid, f['key']) for uid in mapped_ids for f in words[uid][1]['forms']},
            'Authored source form has no reviewed disposition')
    # Bind the risky same-reading cases to their reviewed semantic identities.
    decisions = {r['source_row']: r for r in records}
    for key, n, editorial_key in (
        ('N5_GRAMMAR:89:1', 11, 'word_001'), ('N5_GRAMMAR:89:2', 11, 'word_002'),
        ('N5_GRAMMAR:84:12', 10, 'word_043'), ('N5_GRAMMAR:143:5', 20, 'word_005'),
        ('N5_GRAMMAR:143:6', 20, 'word_006'), ('N4_GRAMMAR:47:3', 29, 'word_3'),
    ):
        uid = next(w['id'] for w in lessons[n]['vocabulary'] if w['editorial_key'] == editorial_key)
        require([t['id'] for t in decisions[key]['targets']] == [uid], 'Lost reviewed homonym/construction disambiguation')
    source_groups = {}
    by_lesson = {}
    for group in inventory['grammar_groups']:
        n = group['lesson']
        loc = catalog['lessons'][n - 1]['translation_and_grammar']
        key = f'{group["source_id"]}:L{n}:G{group["group"]}'
        require(key not in source_groups and group['heading'].strip(), 'Duplicate/blank source grammar group')
        require(group['source_id'] == loc['source_id'] and loc['pdf_page_start'] <= group['pdf_page_start'] <= group['pdf_page_end'] <= loc['pdf_page_end'], 'Grammar locator outside source lesson')
        source_groups[key] = group
        by_lesson.setdefault(n, []).append(int(group['group']))
    require(set(by_lesson) == set(lessons), 'Missing grammar source lesson')
    for numbers in by_lesson.values():
        require(numbers == list(range(1, len(numbers) + 1)), 'Noncontiguous source grammar groups')
    require(len(source_groups) == 253, 'Reviewed source grammar denominator changed')
    require(len(grammar['grammar']) == len(source_groups), 'Missing/duplicate grammar disposition')
    seen = set()
    variant_count = 0
    for record in grammar['grammar']:
        key = record['source_group']
        require(key in source_groups and key not in seen, 'Unknown/duplicate grammar disposition')
        seen.add(key)
        group = source_groups[key]
        lesson = lessons[group['lesson']]
        gs = [g for g in lesson['grammar_points'] if g['source_topic_group'].split(':')[0].strip() == group['group']]
        require(record['disposition'] == 'mapped' and set(record['grammar_point_ids']) == {g['id'] for g in gs} and gs, 'Source group lost authored points')
        refs = [r for g in gs for r in g['source_refs'] if r['source_id'] == group['source_id']]
        require(refs and min(r['pdf_page_start'] for r in refs) <= group['pdf_page_start'] and
                max(r['pdf_page_end'] for r in refs) >= group['pdf_page_end'], 'Grammar provenance omits a source continuation page')
        ps = {p['id']: p for p in lesson['sentence_patterns'] if p['grammar_point_id'] in record['grammar_point_ids']}
        require(len(record['links']) == len(ps), 'Pattern link missing/duplicated')
        linked = set()
        for link in record['links']:
            pid = link['pattern_id']
            require(pid in ps and pid not in linked, 'Unknown/duplicate grammar pattern')
            linked.add(pid)
            pattern = ps[pid]
            require(link['grammar_point_id'] == pattern['grammar_point_id'], 'Wrong grammar/pattern link')
            require([v['key'] for v in link['variants']] == [v['key'] for v in pattern['templates']], 'Missing/reordered template variant')
            for variant in link['variants']:
                expected = [e['id'] for e in lesson['examples'] if e['pattern_id'] == pid and e['pattern_variant_key'] == variant['key']]
                require(expected and variant['example_ids'] == expected, 'Missing/wrong variant example links')
                variant_count += 1
    require(set(review['tasks']) == {'T02.01', 'T02.02', 'T02.03', 'T02.04'}, 'Missing task review boundary')
    for task in review['tasks'].values():
        require(task['status'] in ('ready', 'in_progress', 'done'), 'Unknown content review status')
        require(task['status'] == 'done' or task['remaining'], 'Unfinished review without explicit remaining work')
    return dict(vocabulary_pages=len(pages), source_vocabulary_rows=len(rows), mapped_source_rows=len(rows) - excluded,
                excluded_source_rows=excluded, authored_vocabulary_mapped=len(mapped_ids), editorial_additions=len(added_ids),
                authored_form_links=len(mapped_forms), source_grammar_groups=len(source_groups), linked_pattern_variants=variant_count)


def lexical_key(word):
    return (''.join(s['base'] for s in word['japanese']['segments']), word['kana_reading'])


def normalized_key(surface, reading):
    return tuple(v.replace('〜', '').replace('～', '') for v in (surface, reading))


def source_keys(row):
    pair = normalized_key(row['label'], row['reading'])
    return {pair, (pair[0] + 'する', pair[1] + 'する')}


def validate_kanji(inventory, ledger, catalog, units, masters):
    require(inventory['format_version'] == ledger['format_version'] == 1, 'Unsupported Kanji ledger format')
    definitions = inventory['definitions']
    require([r['number'] for r in definitions] == list(range(1, 537)), 'Missing/reordered source definition')
    require(len({r['character'] for r in definitions}) == 536, 'Duplicate source character')
    require(len(ledger['definitions']) == 536, 'Missing master disposition')
    definitions_by_number = {r['number']: r for r in definitions}
    require(set(masters) == set(definitions_by_number), 'Master/source denominator mismatch')
    seen, master_ids = set(), set()
    for record in ledger['definitions']:
        n = record['number']
        require(n in masters and n not in seen, 'Unknown/duplicate master disposition')
        seen.add(n)
        source, target = definitions_by_number[n], masters[n]
        require(record['disposition'] == 'mapped' and record['master_id'] == target['id'], 'Wrong master identity')
        require(target['id'] not in master_ids, 'Shared master identity duplicated')
        master_ids.add(target['id'])
        for field in ('character', 'han_viet', 'on_readings', 'kun_readings'):
            require(source[field] == target[field], 'Source character fact differs without a disposition: ' + str(n) + '/' + field)
        require(any(r['source_id'] == source['source_id'] and r['pdf_page_start'] <= source['pdf_page'] <= r['pdf_page_end']
                    for r in target['source_refs']), 'Master dictionary locator mismatch')
        require(record['example_ids'] == [w['id'] for w in target['examples']], 'Missing master compound identity')
        require(bool(record.get('source_correction')) == (n in (231, 301, 454)), 'Lost owner source-correction disposition')
    expected_units = {u['number']: u for u in catalog['kanji_units']}
    require([u['unit'] for u in inventory['units']] == list(range(1, 51)), 'Missing/reordered Kanji source unit')
    require([u['unit'] for u in ledger['units']] == list(range(1, 51)), 'Missing/reordered Kanji unit mapping')
    glyph_ids = {e['character']: e['id'] for e in masters.values()}
    source_rows, authored_words = {}, {}
    for source, relation in zip(inventory['units'], ledger['units']):
        n = source['unit']
        target, expected = units[n], expected_units[n]
        require(relation['unit_id'] == target['id'], 'Wrong unit identity')
        for field in ('publisher_lesson_milestone', 'reference_lesson_scope', 'relationship'):
            require(source[field] == target[field] == expected[field], 'Kanji source milestone/relationship drift')
        require(source['location'] == expected['location'], 'Wrong source unit locator')
        require(set(source['printed_character_glyphs']) <= set(target['character_glyphs']), 'Printed header character missing from unit')
        require(relation['master_ids'] == [glyph_ids[g] for g in target['character_glyphs']], 'Wrong unit/shared-master relationship')
        require([r['ordinal'] for r in source['items']] == list(range(1, len(source['items']) + 1)), 'Missing/duplicate Kanji lexical ordinal')
        for row in source['items']:
            require(row['label'] and row['reading'], 'Blank Kanji source compound')
            require(row['source_id'] == source['location']['source_id'], 'Wrong Kanji lexical source volume')
            first = row.get('pdf_page', row.get('pdf_page_start'))
            last = row.get('pdf_page', row.get('pdf_page_end'))
            dictionary_range = (181, 210) if n <= 20 else (186, 237)
            allowed = dictionary_range if row['section'] == 'dictionary_lexical_example' or (n == 15 and row['section'] == 'explicit_name_reading') else (
                source['location']['pdf_page_start'], source['location']['pdf_page_end'])
            require(first is not None and last is not None and allowed[0] <= first <= last <= allowed[1], 'Kanji lexical locator outside its reviewed section')
            source_rows[(n, row['ordinal'])] = row
        for word in target['word_examples']:
            require(word['id'] not in authored_words, 'Duplicate unit word identity')
            authored_words[word['id']] = (n, word)
    require(len(ledger['unit_words']) == len(source_rows), 'Missing Kanji source lexical disposition')
    seen, target_ids = set(), set()
    for record in ledger['unit_words']:
        key = (record['unit'], record['source_ordinal'])
        require(key in source_rows and key not in seen, 'Unknown/duplicate Kanji source lexical disposition')
        seen.add(key)
        require(record['disposition'] == 'mapped' and record['target_ids'], 'Unresolved Kanji source word')
        for uid in record['target_ids']:
            require(uid in authored_words, 'Dangling Kanji lexical identity')
            n, word = authored_words[uid]
            require(n == key[0], 'Kanji lexical mapping crosses units')
            require(normalized_key(*lexical_key(word)) in source_keys(source_rows[key]), 'Wrong Kanji contextual reading/form')
            target_ids.add(uid)
    require(target_ids == set(authored_words), 'Authored Kanji unit word has no source disposition')
    examples = {w['id']: (e, w) for e in masters.values() for w in e['examples']}
    require(len(ledger['master_examples']) == len(examples), 'Missing master example source disposition')
    seen = set()
    for record in ledger['master_examples']:
        uid = record['id']
        require(uid in examples and uid not in seen, 'Unknown/duplicate master example link')
        seen.add(uid)
        e, word = examples[uid]
        require(e['character'] in lexical_key(word)[0], 'Master example does not contain its character')
        if 'unit' in record:
            row = source_rows.get((record['unit'], record['source_ordinal']))
            require(row and normalized_key(*lexical_key(word)) in source_keys(row), 'Wrong source compound link')
        else:
            row = definitions_by_number[record['definition']]['lexical_anchor']
            require(lexical_key(word) == (row['label'], row['reading']), 'Wrong dictionary lexical anchor')
    return dict(source_kanji_definitions=len(definitions), source_kanji_units=len(units),
                source_unit_lexical_rows=len(source_rows), mapped_unit_words=len(target_ids),
                mapped_master_examples=len(examples), unit_master_links=sum(len(u['master_ids']) for u in ledger['units']))


def kanji_self_test(args):
    fixtures = [
        ('missing definition', lambda a: a[0]['definitions'].pop()),
        ('duplicate definition', lambda a: a[0]['definitions'][1].update(number=1)),
        ('wrong reading', lambda a: a[0]['definitions'][0].update(on_readings=['INVALID'])),
        ('missing unit', lambda a: a[0]['units'].pop()),
        ('missing compound disposition', lambda a: a[1]['unit_words'].pop()),
        ('wrong compound identity', lambda a: a[1]['unit_words'][0].update(target_ids=['missing'])),
        ('wrong compound reading', lambda a: a[0]['units'][0]['items'][0].update(reading='まちがい')),
        ('wrong compound locator', lambda a: a[0]['units'][0]['items'][0].update(pdf_page=1)),
        ('wrong preparatory milestone', lambda a: a[0]['units'][20]['publisher_lesson_milestone'].update(global_lesson_number=26)),
        ('missing header glyph', lambda a: a[3][26]['character_glyphs'].remove('議')),
        ('wrong shared master', lambda a: a[1]['units'][0]['master_ids'].reverse()),
        ('lost source correction', lambda a: a[1]['definitions'][230].update(source_correction=None)),
        ('lost master example', lambda a: a[1]['master_examples'].pop()),
    ]
    for name, mutate in fixtures:
        altered = copy.deepcopy(args)
        mutate(altered)
        try:
            validate_kanji(*altered)
        except ValueError:
            continue
        raise ValueError('Negative Kanji fixture accepted: ' + name)
    return len(fixtures)


def self_test(args):
    fixtures = [
        ('missing source row', lambda a: a[0]['vocabulary_pages'][0]['rows'].pop()),
        ('missing content-review gate', lambda a: a[3]['tasks'].pop('T02.04')),
        ('duplicate ordinal', lambda a: a[0]['vocabulary_pages'][0]['rows'][1].update(ordinal=1)),
        ('missing page', lambda a: a[0]['vocabulary_pages'].pop()),
        ('wrong lesson', lambda a: a[0]['vocabulary_pages'][0].update(lesson=2)),
        ('blank label', lambda a: a[0]['vocabulary_pages'][0]['rows'][0].update(label='')),
        ('missing disposition', lambda a: a[1]['vocabulary'].pop()),
        ('duplicate disposition', lambda a: a[1]['vocabulary'][1].update(source_row=a[1]['vocabulary'][0]['source_row'])),
        ('unknown UUID', lambda a: a[1]['vocabulary'][0]['targets'][0].update(id='missing')),
        ('unknown form', lambda a: a[1]['vocabulary'][0]['targets'][0].update(form_keys=['missing'])),
        ('empty forms', lambda a: a[1]['vocabulary'][0]['targets'][0].update(form_keys=[])),
        ('unjustified exclusion', lambda a: a[1]['vocabulary'][0].update(disposition='excluded', targets=[])),
        ('missing addition', lambda a: a[1].update(editorial_additions=[])),
        ('homonym merged', lambda a: next(r for r in a[1]['vocabulary'] if r['source_row']=='N5_GRAMMAR:89:1')['targets'].extend(next(r for r in a[1]['vocabulary'] if r['source_row']=='N5_GRAMMAR:89:2')['targets'])),
        ('missing grammar group', lambda a: a[0]['grammar_groups'].pop()),
        ('missing pattern link', lambda a: a[2]['grammar'][0]['links'].pop()),
        ('missing variant example', lambda a: a[2]['grammar'][0]['links'][0]['variants'][0].update(example_ids=[])),
    ]
    for name, mutate in fixtures:
        altered = copy.deepcopy(args)
        mutate(altered)
        try:
            validate(*altered)
        except ValueError:
            continue
        raise ValueError('Negative fixture accepted: ' + name)
    return len(fixtures)


def build_report(run_self_test=False):
    inventory, vocabulary, grammar, review = (read(DATA / name) for name in FILES)
    catalog = read(ROOT / 'docs/reference-inventory/catalog.json')
    lessons = {n: read(ROOT / f'docs/content-authoring/lesson-{n:02}.json') for n in range(1, 51)}
    inventory_pin = sha(DATA / FILES[0])
    for ledger in (vocabulary, grammar):
        require(ledger['source_inventory_sha256'] == inventory_pin, 'Source inventory changed after mapping review')
    require(set(vocabulary['content_sha256']) == {f'docs/content-authoring/lesson-{n:02}.json' for n in lessons}, 'Incomplete content pins')
    for path, pin in vocabulary['content_sha256'].items():
        require(sha(ROOT / path) == pin, 'Content changed after mapping review: ' + path)
    upstream = vocabulary['upstream_change']
    require(upstream['decision'] == 'B-U-59' and sha(ROOT / upstream['evidence']) == upstream['sha256'], 'Stale proper-name restoration evidence')
    names = read(ROOT / upstream['evidence'])
    mapped = {r['source_row']: r for r in vocabulary['vocabulary']}
    for row in names['source_rows']:
        require(row['source_row'] in mapped and mapped[row['source_row']]['disposition'] == 'mapped', 'B-U-59 source name lost its mapping')
        require({t['id'] for t in mapped[row['source_row']]['targets']} == set(row['item_ids']), 'B-U-59 proper-name identity mismatch')
    sources = {s['id']: s for s in catalog['sources']}
    for source in inventory['sources']:
        require(source == {k: sources[source['id']][k] for k in source}, 'Source catalog pin drift')
        require(sha(ROOT / source['relative_path']) == source['sha256'], 'Original source PDF changed')
    args = (inventory, vocabulary, grammar, review, catalog, lessons)
    counts = validate(*args)
    kanji_inventory, kanji_ledger = (read(DATA / name) for name in KANJI_FILES)
    require(kanji_ledger['source_inventory_sha256'] == sha(DATA / KANJI_FILES[0]), 'Kanji inventory changed after mapping')
    units = {n: read(ROOT / f'docs/content-authoring/kanji/unit-{n:02}.json') for n in range(1, 51)}
    masters = {e['source_character_number']: e for level in (5, 4)
               for e in read(ROOT / f'docs/content-authoring/kanji/characters-n{level}.json')['entries']}
    kanji_paths = {f'docs/content-authoring/kanji/unit-{n:02}.json' for n in units} | {
        'docs/content-authoring/kanji/characters-n5.json', 'docs/content-authoring/kanji/characters-n4.json'}
    require(set(kanji_ledger['content_sha256']) == kanji_paths, 'Incomplete Kanji content pins')
    for path, pin in kanji_ledger['content_sha256'].items():
        require(sha(ROOT / path) == pin, 'Kanji content changed after review: ' + path)
    kanji_args = (kanji_inventory, kanji_ledger, catalog, units, masters)
    counts.update(validate_kanji(*kanji_args))
    # These pins preserve a declared primary linguistic review. The machine does
    # not infer linguistic accuracy from linkage, file count or a status flag.
    expected_review_paths = set(vocabulary['content_sha256']) | kanji_paths
    records = review['content_reviews']
    require(len(records) == len(expected_review_paths) and {r['path'] for r in records} == expected_review_paths,
            'Missing/duplicate primary content-review record')
    for record in records:
        require(record['reviewer'] == 'primary_agent' and record['result'] == 'accepted_for_T02', 'Unaccepted primary content review')
        require(record['sha256'] == sha(ROOT / record['path']), 'Content changed after primary semantic review')
        require(set(record['checks']) == {'source_alignment', 'reading_ruby', 'vi_en_meaning', 'identity_provenance'}, 'Incomplete review dimensions')
    counts['primary_reviewed_content_files'] = len(records)
    pending = [key for key, value in review['tasks'].items() if value['status'] != 'done']
    for task in review['tasks'].values():
        require(task['status'] != 'done' or not task['remaining'], 'Task closed with unresolved content work')
    complete = not pending and not grammar['findings']
    return dict(task='P0-T02', date=review['date'], structural_valid=True, task_acceptance_complete=complete,
                acceptance_basis='Recorded B-U-51 primary source/content review plus independently checked ledger integrity; no human or release certification.',
                counts=counts, pending_content_reviews=pending, kanji_source_inventory_present=True,
                open_grammar_locator_findings=len(grammar['findings']),
                negative_fixtures_passed=(self_test(args) + kanji_self_test(kanji_args)) if run_self_test else 0,
                input_sha256={str((DATA / name).relative_to(ROOT)): sha(DATA / name) for name in (*FILES, *KANJI_FILES, 'proper-name-review.json', 'content-corrections.json')},
                implementation_sha256={str(Path(__file__).resolve().relative_to(ROOT)): sha(Path(__file__))},
                limits=review['limits'])


def markdown(report):
    c = report['counts']
    return '\n'.join([
        '# T02 source reconciliation (generated)', '',
        'Run `python3 scripts/validate_source_reconciliation.py --complete --self-test --write` after actual content review to regenerate; edit the adjacent JSON inputs.', '',
        ('**Status: complete for the delegated primary T02 review.**' if report['task_acceptance_complete'] else '**Status: in progress.**') +
        ' Structural checks and recorded linguistic self-review remain distinct; neither establishes human/release certification.', '',
        '| Checked inventory | Count |', '| --- | --- |',
        *[f'| {key.replace("_", " ")} | {value} |' for key, value in c.items()], '',
        f'Open grammar locator range findings: {report["open_grammar_locator_findings"]}.', '',
        'The vocabulary denominator comes from 100 manually enumerated source pages. The 253 numbered grammar groups '
        'and Kanji source facts are frozen separately from their authored ID mappings. Kanji transcription seeds, '
        'curated dictionary-example scope, contextual-lemma normalization and fresh image comparisons are disclosed in the inventory/review.', '',
        'The B-U-59 restoration of 41 lesson names is retained. T02 additionally restores 23 Kanji name occurrences and '
        'three counter readings with new IDs; all pre-existing IDs, PDFs and fixed dialogue scripts remain unchanged. '
        'See the correction log for form, provenance, terminology and bilingual edits.', '',
        '## Evidence inputs', '',
        '- [Source pages, lexical rows and numbered grammar groups](source-inventory.json)',
        '- [Vocabulary dispositions and stable form/ID links](vocabulary-ledger.json)',
        '- [Grammar, pattern, variant, example links and locator findings](grammar-ledger.json)',
        '- [Kanji source definitions, unit readings and milestones](kanji-source-inventory.json)',
        '- [Kanji unit/master/compound identity links](kanji-ledger.json)',
        '- [Item-level content correction log](content-corrections.json)',
        '- [Exact review scope and remaining work](review.json)',
        '- [Machine validation report](validation-report.json)', '',
        '## Limits', '', *['- ' + limit for limit in report['limits']], '',
        'Current task status is owned by [the owner HTML](../../index.html#T02).', ''
    ])


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--self-test', action='store_true')
    parser.add_argument('--complete', action='store_true')
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument('--write', action='store_true')
    mode.add_argument('--check', action='store_true')
    options = parser.parse_args()
    report = build_report(run_self_test=options.self_test or options.write or options.check)
    outputs = {'validation-report.json': json.dumps(report, ensure_ascii=False, indent=2) + '\n',
               'ledger.md': markdown(report)}
    for name, content in outputs.items():
        path = DATA / name
        if options.write:
            path.write_text(content)
        elif options.check:
            require(path.is_file() and path.read_text() == content, 'Stale generated reconciliation output: ' + name)
    print('PASS ledger integrity: ' + json.dumps(report['counts'], ensure_ascii=False))
    print(f'Negative fixtures: {report["negative_fixtures_passed"]}. T02 acceptance: ' + ('complete (primary review)' if report['task_acceptance_complete'] else 'PENDING (see review.json).'))
    if options.complete and not report['task_acceptance_complete']:
        print('FAIL --complete: ledger integrity does not establish T02 completion.', file=sys.stderr)
        return 1
    return 0


if __name__ == '__main__':
    try:
        sys.exit(main())
    except (ValueError, KeyError, TypeError, json.JSONDecodeError) as error:
        print('FAIL: ' + str(error), file=sys.stderr)
        sys.exit(1)
