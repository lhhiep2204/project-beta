"""Render readable editorial drafts from the canonical lesson and Kanji JSON."""
from __future__ import annotations
import argparse
import json
import os
from pathlib import Path
from urllib.parse import quote

ROOT = Path(__file__).resolve().parents[1]
AUTHORING = ROOT / 'docs/content-authoring'
KANJI = AUTHORING / 'kanji'
CATALOG = ROOT / 'docs/reference-inventory/catalog.json'
UTF8 = 'utf-8'
NEWLINE = '\n'
LESSON_GLOB = 'lesson-*.json'
UNIT_GLOB = 'unit-*.json'
SET_NAMES = ('characters-n5.json', 'characters-n4.json')
CORRECTIONS = AUTHORING / 'source-corrections.json'
CHECK_OPTION = '--check'
EMPTY_READING = '—'


def correction_flags(item, directory):
    """Join the separate source-discrepancy ledger without mutating canonical facts."""
    flags = []
    for correction in read(CORRECTIONS)['items']:
        if correction['review_status'] not in ('recheck_required', 'owner_confirmed'):
            continue
        if 'vocabulary_id' in correction:
            matches = item.get('id') == correction['vocabulary_id']
        elif 'character' in item:
            matches = item['source_character_number'] == correction['source_character_number']
        elif 'japanese' in item:
            matches = plain(item['japanese']) == correction['item'] and any(
                ref['source_id'] == correction['source_id'] and
                ref['pdf_page_start'] <= correction['pdf_page'] <= ref['pdf_page_end']
                for ref in item['source_refs'])
        else:
            matches = False
        if matches:
            target = quote(os.path.relpath(AUTHORING / 'source-corrections.md', directory))
            label = ('OWNER CONFIRMED' if correction['review_status'] == 'owner_confirmed' else
                     'OWNER DECISION PENDING' if correction['owner_decision'].startswith('pending_') else 'RECHECK REQUIRED')
            flags.append('[' + correction['id'] + ': ' + label + '](' + target + ')')
    return '; '.join(flags)


def read(path):
    return json.loads(path.read_text(encoding=UTF8))


def japanese(text):
    return ''.join(s['base'] + ('【' + s['ruby'] + '】' if 'ruby' in s else '') for s in text['segments'])


def plain(text):
    return ''.join(s['base'] for s in text['segments'])


def cell(value):
    return str(value).replace('|', '\\|').replace('\n', ' ')


def row(*values):
    return '| ' + ' | '.join(cell(v) for v in values) + ' |'


def source_link(ref, directory, sources):
    source = sources[ref['source_id']]
    start, end = ref['pdf_page_start'], ref['pdf_page_end']
    pages = str(start) if start == end else f'{start}–{end}'
    target = quote(os.path.relpath(ROOT / source['relative_path'], directory))
    return f'[{ref["source_id"]} PDF {pages}]({target}#page={start})'


def refs(items, directory, sources):
    return '; '.join(source_link(item, directory, sources) for item in items)


def template_text(pattern, template, locale):
    labels = {slot['key']: slot['label'][locale] for slot in pattern['slots']}
    return ''.join(part['value'] if part['kind'] == 'literal' else '[' + labels[part['value']] + ']' for part in template['pieces'])


def lesson_markdown(data, sources):
    n = data['reference_lesson_number']
    lines = [f'# Lesson {n}: {data["title"]["en"]}', '', data['title']['vi'], '',
             'Editorial draft in Japanese with Vietnamese/English support. Primary-agent self-review is the delegated authoring gate (B-U-51/54); independent human and release acceptance are not claimed. Other 17 approved release languages remain unauthored in this batch.', '',
             'Furigana is shown as `漢字【かな】` for review. Romaji search aliases are metadata only. Explanations, examples and dialogue are newly authored; source links align lexical facts and grammar topics.', '',
             '## Coverage', '']
    lines.extend('- ' + value for value in data['coverage']['included'])
    lines.extend(['', 'Omitted from this draft:', ''])
    lines.extend('- ' + value for value in data['coverage']['omitted'])
    lines.extend(['', 'Lesson references: ' + refs(data['source_refs'], AUTHORING, sources) + '.', '',
                  '## Vocabulary', '', row('Japanese form', 'Kana', 'Vietnamese', 'English', 'Type / group / register'), row('---', '---', '---', '---', '---')])
    for item in data['vocabulary']:
        for form in item['forms']:
            meanings = [sense['text'] for sense in item['meanings'] if form['key'] in sense['form_keys']]
            kind = item['entry_type'] + (' / ' + item['verb_group'] if 'verb_group' in item else '') + ' / ' + form['register']
            flags = correction_flags(item, AUTHORING)
            lines.append(row(japanese(form['japanese']) + (' ' + flags if flags else ''), form['kana_reading'], '; '.join(v['vi'] for v in meanings), '; '.join(v['en'] for v in meanings), kind))
    notes = [item for item in data['vocabulary'] if item['usage']['vi'] or item['usage']['en']]
    if notes:
        lines.extend(['', '### Usage and form distinctions', ''])
        for item in notes:
            lines.extend(['- **' + japanese(item['forms'][0]['japanese']) + '** — VI: ' + item['usage']['vi'] + ' EN: ' + item['usage']['en']])
    verbs = [item for item in data['vocabulary'] if item['entry_type'] == 'verb']
    if verbs:
        lines.extend(['', '### Dictionary forms', '', 'Dictionary forms are editorial conjugations from the source polite forms, with the listed group; they are not claimed as dictionary-form quotations from the source.', '', row('Polite form', 'Dictionary form', 'Kana', 'Group'), row('---', '---', '---', '---')])
        for item in verbs:
            forms = {f['key']: f for f in item['forms']}
            for form in item['dictionary_forms']:
                lines.append(row(japanese(forms[form['form_key']]['japanese']), japanese(form['japanese']), form['kana_reading'], item['verb_group']))
    lines.extend(['', '## Grammar and original examples', ''])
    for grammar in data['grammar_points']:
        lines.extend(['### ' + grammar['title']['en'], '', grammar['title']['vi'], '', '**VI:** ' + grammar['explanation']['vi'], '', '**EN:** ' + grammar['explanation']['en'], '', '**Usage note (VI):** ' + grammar['notes']['vi'], '', '**Usage note (EN):** ' + grammar['notes']['en'], ''])
        for pattern in [p for p in data['sentence_patterns'] if p['grammar_point_id'] == grammar['id']]:
            for template in pattern['templates']:
                lines.extend(['Pattern (' + template['key'] + ', VI): `' + template_text(pattern, template, 'vi') + '`', '', 'Pattern (' + template['key'] + ', EN): `' + template_text(pattern, template, 'en') + '`', ''])
            for example in [e for e in data['examples'] if e['pattern_id'] == pattern['id']]:
                if 'context' in example:
                    lines.extend(['Context (VI): ' + example['context']['vi'], '', 'Context (EN): ' + example['context']['en'], ''])
                lines.extend(['- ' + japanese(example['japanese']), '  - VI: ' + example['translation']['vi'], '  - EN: ' + example['translation']['en']])
        lines.extend(['', 'Knowledge alignment: ' + refs(grammar['source_refs'], AUTHORING, sources) + '. Source topic group: ' + grammar['source_topic_group'] + '. The explanation/examples are not source quotations.', ''])
    lines.extend(['## Original dialogue', ''])
    for dialogue in data['dialogues']:
        characters = {c['key']: japanese(c['display_name']) for c in dialogue['characters']}
        lines.extend(['### ' + dialogue['title']['en'], '', dialogue['title']['vi'], '', '**VI:** ' + dialogue['scenario']['vi'], '', '**EN:** ' + dialogue['scenario']['en'], '', row('Speaker', 'Japanese', 'Vietnamese', 'English'), row('---', '---', '---', '---')])
        for turn in dialogue['turns']:
            lines.append(row(characters[turn['speaker_key']], japanese(turn['japanese']), turn['translation']['vi'], turn['translation']['en']))
        lines.extend(['', 'Skill alignment: ' + refs(dialogue['source_refs'], AUTHORING, sources) + '. The scene, turns and translations are newly authored.', ''])
    lines.extend(['## Kanji reference relationship', '', ', '.join('[Unit ' + str(int(key.rsplit('_', 1)[1])) + '](kanji/unit-' + key.rsplit('_', 1)[1] + '.md)' for key in data['kanji_reference_units']) + '.', '', 'Unit milestones follow the reference catalog and do not choose the app’s cross-level learned-state policy.', '', '## Editorial evidence', '', '[Structured lesson JSON](lesson-' + f'{n:02}' + '.json). [Content index](content-index.md). Structural validation and delegated self-review do not establish voice, device, independent-human or release acceptance.', ''])
    return NEWLINE.join(lines)


def word_table(words, sources):
    lines = [row('Word', 'Kana', 'Vietnamese', 'English', 'Reference'), row('---', '---', '---', '---', '---')]
    for word in words:
        flags = correction_flags(word, KANJI)
        lines.append(row(japanese(word['japanese']), word['kana_reading'], word['meanings']['vi'], word['meanings']['en'], refs(word['source_refs'], KANJI, sources) + ('; ' + flags if flags else '')))
    return lines


def character_table(entries, sources):
    lines = [row('No.', 'Kanji', 'Hán-Việt', 'Vietnamese', 'English', 'On', 'Kun', 'Word example', 'Reference'), row('---', '---', '---', '---', '---', '---', '---', '---', '---')]
    for entry in entries:
        flags = correction_flags(entry, KANJI)
        lines.append(row(entry['source_character_number'], entry['character'], ', '.join(entry['han_viet']), entry['meanings']['vi'], entry['meanings']['en'], ', '.join(entry['on_readings']) or EMPTY_READING, ', '.join(entry['kun_readings']) or EMPTY_READING, '; '.join(japanese(w['japanese']) + ': ' + w['meanings']['vi'] + ' / ' + w['meanings']['en'] for w in entry['examples']), refs(entry['source_refs'], KANJI, sources) + ('; ' + flags if flags else '')))
    return lines


def unit_markdown(data, masters, sources):
    n = data['reference_unit_number']
    missing = set(data['character_glyphs']) - set(masters)
    if missing:
        raise ValueError(f'Unit {n}: unresolved master glyphs: {sorted(missing)}')
    milestone = data['publisher_lesson_milestone']['global_lesson_number']
    scope = data['reference_lesson_scope']
    scope_text = f'Reference lesson scope: {scope["start"]}–{scope["end"]}.'
    if scope['may_include_earlier_material']:
        scope_text += ' Earlier material may recur.'
    lines = ['# ' + data['title']['en'], '', data['title']['vi'], '', 'Japanese learning content with Vietnamese/English support. Draft under the delegated self-review gate; independent human and release acceptance are not claimed.', '', '## Source relationship', '', 'Publisher lesson milestone: **' + str(milestone) + '** (' + data['publisher_lesson_milestone']['reference_volume'] + '). Relationship: `' + data['relationship'] + '`.', '', scope_text, '', 'References: ' + refs(data['source_refs'], KANJI, sources) + '.', '', '## Kanji', '', 'On/Kun are the reference-listed subset, with source corrections linked to their recorded owner decisions. A dash means no reading of that class was listed. Okurigana notation belongs to the reading, not to a bare character to pronounce in isolation. Word readings are contextual. No stroke/radical content is included.', '']
    lines.extend(character_table([masters[g] for g in data['character_glyphs']], sources))
    lines.extend(['', '## Common reading words', ''])
    lines.extend(word_table(data['word_examples'], sources))
    lines.extend(['', '[Structured unit JSON](unit-' + f'{n:02}' + '.json). [Content index](../content-index.md).', ''])
    return NEWLINE.join(lines)


def kana_markdown(data, inventory, review):
    """Readable kana is derived from JSON, including its bounded review evidence."""
    counts = {}
    for entry in data['entries']:
        counts.setdefault(entry['script'] + ' / ' + entry['group'], []).append(entry)
    lines = ['# Kana inventory — Hiragana and Katakana', '',
             f"{len(data['entries'])} authored Vietnamese/English entries. Primary-agent self-review is complete within the recorded source scope; independent-human, native voice and release acceptance are not claimed.", '',
             'No displayed romaji or learned-lesson dependency. Dependent marks play complete contexts; reference forms remain separate. Speech text below is an editorial target, not recorded or synthesized audio evidence.', '',
             '[Authoring and scope](README.md). [Structured inventory](inventory.json). [Source ledger](source-inventory.json). [Item review](review.json). [Validation report](validation-report.json).', '']
    for title, entries in counts.items():
        lines += ['## ' + title, '',
                  row('Glyph', 'Example / reading', 'English', 'Vietnamese', 'Cell speech target', 'Usage', 'Identity / sources'),
                  row('---', '---', '---', '---', '---', '---', '---')]
        for e in entries:
            x = e['examples'][0]
            source_text = '; '.join(r['source_id'] + ': ' + r['locator'] for r in e['source_refs'])
            example_text = '; '.join(japanese(x['japanese']) + ' / ' + x['reading'] for x in e['examples'])
            lines.append(row(e['glyph'], example_text,
                             '; '.join(x['translation']['en'] for x in e['examples']),
                             '; '.join(x['translation']['vi'] for x in e['examples']),
                             e['speech']['mode'] + ': ' + e['speech']['text'],
                             e['guidance']['vi'] + ' / ' + e['guidance']['en'],
                             e['id'] + '; ' + source_text))
        lines.append('')
    lines += ['## Source-table denominator', '', inventory['coverage_boundary'], '',
              row('Source table', 'Cells mapped', 'Locator'), row('---', '---', '---')]
    lines += [row(t['id'], len(t['keys']), t['locator']) for t in inventory['tables']]
    lines += ['', '## Sources', '']
    for s in inventory['sources']:
        lines += ['- [' + s['id'] + ' — ' + s['title'] + '](' + s['url'] + '): ' + s['scope']]
    lines += ['', '## Review findings', '']
    lines += ['- ' + f['id'] + ': ' + f['resolution'] for f in review['findings']]
    lines += ['', '## Coverage exclusions', '']
    lines += ['- ' + x['scope'] + ': ' + x['reason'] for x in inventory['exclusions']]
    lines += ['', '## Evidence limits', '']
    lines += ['- ' + limit for limit in review['limits']]
    lines += ['', '[Content index](../content-index.md).', '']
    return NEWLINE.join(lines)


def sentence_bank_markdown(bank, identities, contexts, report):
    targets = {r['id']: r for r in identities['targets'].values()}
    complete = report['task_authoring_acceptance_complete']
    lines = ['# T04 sentence bank and speech authoring', '',
             ('**P0-T04 authoring is complete.**' if complete else '**P0-T04 authoring is incomplete.**') + ' This document is generated from canonical JSON; the owner HTML owns task status. Native integration is separate.', '',
             f"{report['reviewed_candidates']} dependency-complete candidates cover {report['reviewed_target_coverage']} of {report['targets']} form/sense/variant targets. {report['missing_targets']} remain in the full [gap ledger](coverage.json). " + ('All 304 original examples retain their identities, Japanese, translations and context, with reviewed annotations.' if complete else 'Pending annotations cannot be selected.'), '',
             f"{report['speech_targets']} speech targets include {report['dictionary_forms']} dictionary forms. All {report['bound_contexts']} bound contexts are authored: {report['vocabulary_bound_entries']} vocabulary entries / {report['vocabulary_bound_forms']} forms and {report['kanji_bound_words']} Kanji lexical occurrences. The earlier 53-entry count missed the second wave-dash character and readings without a marker.", '',
             'Source orthographic readings inherit the pinned T02 primary review. Newly authored bound contexts, particle edits and the listed complete candidates received B-U-51 primary self-review. No native voice/listening, independent-human, remaining-locales or release acceptance follows.', '',
             '[Scope and commands](README.md). [Bank JSON](bank.json). [Stable identity registry](identities.json). [Speech targets](speech.json). [Primary review](review.json). [Validation report](validation-report.json).', '',
             '## Reviewed sentence candidates', '',
             row('Sentence UUID / introduction', 'Japanese / speech', 'Vietnamese / English', 'Targets', 'Dependencies / simplicity'), row('---','---','---','---','---')]
    for c in bank['candidates']:
        if c['status'] != 'reviewed':
            continue
        descriptions = [targets[t]['kind'] + ':' + targets[t]['entity_id'] +
                        (':' + targets[t]['form_key'] if targets[t]['form_key'] else '') +
                        (':' + targets[t]['variant_key'] if targets[t]['variant_key'] else '') for t in c['target_ids']]
        lines.append(row(c['id'] + ' / ' + c['introduced_lesson_id'], japanese(c['japanese']) + ' / ' + c['speech_text'],
                         c['translation']['vi'] + ' / ' + c['translation']['en'], '; '.join(descriptions),
                         f"{len(c['vocabulary_ids'])} vocabulary; {len(c['grammar_ids'])} grammar; order {c['simplicity_order']}"))
    lines += ['', '## Reviewed bound pronunciation contexts', '',
              'These are labeled complete speech contexts. A word or counter phrase here is not automatically a sentence candidate and receives no learned-aware coverage credit.', '',
              row('Exact source form key', 'Context / speech', 'Vietnamese / English'), row('---','---','---')]
    for c in contexts['contexts']:
        lines.append(row(c['key'], japanese(c['japanese']) + ' / ' + c['speech_text'], c['translation']['vi'] + ' / ' + c['translation']['en']))
    lines += ['', '## Missing dependency-complete coverage', '', row('Target kind', 'Missing'), row('---','---')]
    lines += [row(kind, count) for kind, count in report['missing_by_kind'].items()]
    if not report['missing_by_kind']:
        lines.append(row('All target kinds', '0'))
    lines += ['', 'The [full machine-readable ledger](coverage.json) lists every missing target UUID, source pointer, form/sense UUID and reason. Missing targets do not receive an unrelated or automatically generated fallback. T08.05 owns native selection and visible snapshots; T05 owns native TTS proof.', '']
    return NEWLINE.join(lines)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(CHECK_OPTION, action='store_true')
    args = parser.parse_args()
    catalog = read(CATALOG)
    sources = {s['id']: s for s in catalog['sources']}
    lesson_data = [read(p) for p in sorted(AUTHORING.glob(LESSON_GLOB))]
    unit_data = [read(p) for p in sorted(KANJI.glob(UNIT_GLOB))]
    sets = [read(KANJI / name) for name in SET_NAMES if (KANJI / name).is_file()]
    masters = {e['character']: e for dataset in sets for e in dataset['entries']}
    outputs = {AUTHORING / f'lesson-{data["reference_lesson_number"]:02}.md': lesson_markdown(data, sources) for data in lesson_data}
    outputs.update({KANJI / f'unit-{data["reference_unit_number"]:02}.md': unit_markdown(data, masters, sources) for data in unit_data})
    for dataset in sets:
        level = dataset['source_level_label']
        lines = ['# ' + level + ' Kanji reference character definitions', '', 'Vietnamese/English editorial draft. Readings are reference-listed subsets; examples show contextual readings. No independent-human or release certification is claimed.', '']
        lines.extend(character_table(dataset['entries'], sources))
        lines.extend(['', '[Content index](../content-index.md).', ''])
        outputs[KANJI / ('characters-' + level.lower() + '.md')] = NEWLINE.join(lines)
    index = ['# Authored content index', '', 'Current authored drafts: **' + str(len(lesson_data)) + '/' + str(len(catalog['lessons'])) + ' lessons**, **' + str(len(unit_data)) + '/' + str(len(catalog['kanji_units'])) + ' Kanji units**, **' + str(len(masters)) + '/536 Kanji definitions**.', '', 'Vietnamese/English first under B-U-52; the other 17 approved languages remain a later authoring batch. Full common vocabulary and source grammar topics are required by B-U-53. Counts and structural checks alone do not prove semantic completeness. These editorial assets are not app resources or a selected runtime package.', '', '## Lessons', '', row('Lesson', 'Level', 'English', 'Vietnamese', 'Vocabulary', 'Grammar', 'Examples'), row('---', '---', '---', '---', '---', '---', '---')]
    for data in lesson_data:
        n = data['reference_lesson_number']
        index.append(row('[' + str(n) + '](lesson-' + f'{n:02}' + '.md)', data['source_level_label'], data['title']['en'], data['title']['vi'], len(data['vocabulary']), len(data['grammar_points']), len(data['examples'])))
    index.extend(['', '## Kanji units', '', row('Unit', 'Level', 'Title', 'Kanji links', 'Common words', 'Lesson milestone'), row('---', '---', '---', '---', '---', '---')])
    for data in unit_data:
        n = data['reference_unit_number']
        index.append(row('[' + str(n) + '](kanji/unit-' + f'{n:02}' + '.md)', data['source_level_label'], data['title']['vi'] + ' / ' + data['title']['en'], len(data['character_glyphs']), len(data['word_examples']), data['publisher_lesson_milestone']['global_lesson_number']))
    index.extend(['', 'Units 21–25 are preparation/review through the preceding volume’s lesson 25; they are not a second set of N4 lessons 21–25.', '', '## Editorial evidence', '', '- [Authoring guide](README.md)', '- [Current batch review](batch-review.md)', '- [Current coverage record](batch-source-coverage.json)', '- [Complete structural validation](batch-validation-report.json)', '- [Historical sample self-review and findings](editorial-review.md)', '- [Source corrections and owner decisions](source-corrections.md)', '- [Reference lesson/unit catalog](../reference-inventory/README.md)', ''])
    outputs[AUTHORING / 'content-index.md'] = NEWLINE.join(index)
    kana = AUTHORING / 'kana'
    outputs[kana / 'inventory.md'] = kana_markdown(read(kana / 'inventory.json'),
        read(kana / 'source-inventory.json'), read(kana / 'review.json'))
    outputs[AUTHORING / 'content-index.md'] += '\n## Kana\n\n[Complete authored kana inventory](kana/inventory.md): modern tables, extended Katakana, special uses and a separate rare/reference group. Primary self-review, source coverage and native-evidence limits are included.\n'
    sentence_bank = AUTHORING / 'sentence-bank'
    outputs[sentence_bank / 'inventory.md'] = sentence_bank_markdown(
        read(sentence_bank / 'bank.json'), read(sentence_bank / 'identities.json'),
        read(sentence_bank / 'bound-contexts.json'), read(sentence_bank / 'validation-report.json'))
    outputs[AUTHORING / 'content-index.md'] += '\n## T04 sentence bank and speech\n\n[Candidate and speech authoring inventory](sentence-bank/inventory.md): explicit form/sense IDs, reviewed candidates, bound contexts and the complete coverage ledger. Read its revision-bound completion result; speech authoring does not establish native pronunciation acceptance.\n'
    mismatches = []
    for path, content in outputs.items():
        if args.check:
            if not path.is_file() or path.read_text(encoding=UTF8) != content:
                mismatches.append(str(path.relative_to(ROOT)))
        else:
            path.write_text(content, encoding=UTF8)
    if mismatches:
        raise ValueError('Readable content differs from canonical JSON: ' + ', '.join(mismatches))
    print(('Checked' if args.check else 'Rendered') + ' ' + str(len(outputs)) + ' readable editorial files.')
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
