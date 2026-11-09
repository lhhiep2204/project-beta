#!/usr/bin/env python3
"""T09.01 field-level inventory and UI placeholder/plural checks. No linguistic approval."""
import argparse
import copy
import hashlib
import json
from pathlib import Path
import re
import sys
sys.dont_write_bytecode = True
from localization_support import LANGUAGES, is_translation, localized_text
from build_runtime_package import text_fields
from translation_overlays import apply_overlays, field_at, load_overlays, pin, review_pin

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / 'docs/localization/coverage.json'
CATALOG = 'ios/ProjectBeta/ProjectBeta/Presentation/Localization/Interface.xcstrings'
# CLDR cardinal categories, checked 2026-11-09 against Unicode's plurals.xml:
# https://github.com/unicode-org/cldr/blob/main/common/supplemental/plurals.xml
# Apple compiles/evaluates actual selection; SDK-specific acceptance remains a locale-task check.
PLURALS = dict.fromkeys(LANGUAGES, {'one', 'other'})
PLURALS.update({k: {'other'} for k in ('zh-Hans', 'id', 'ko', 'th')})
PLURALS.update(ar={'zero', 'one', 'two', 'few', 'many', 'other'}, he={'one', 'two', 'other'},
               ru={'one', 'few', 'many', 'other'}, uk={'one', 'few', 'many', 'other'},
               fr={'one', 'many', 'other'}, es={'one', 'many', 'other'},
               it={'one', 'many', 'other'}, pt={'one', 'many', 'other'})


def placeholders(value):
    """Normalize printf argument positions; reject unsafe/unknown formats, including %n."""
    pattern = re.compile(r'%(?:(\d+)\$)?([-+ #0]*)(\d+)?(?:\.(\d+))?(lld|llu|ld|lu|d|u|f|@|%)')
    result = {}
    cursor = 0
    implicit = 0
    explicit = None
    for match in pattern.finditer(value):
        if '%' in value[cursor:match.start()]:
            raise ValueError('Unknown placeholder')
        cursor = match.end()
        position, flags, width, precision, kind = match.groups()
        if kind == '%':
            if match.group() != '%%': raise ValueError('Invalid escaped percent')
            continue
        positional = position is not None
        if explicit is not None and explicit != positional: raise ValueError('Mixed placeholder positions')
        explicit = positional
        implicit += 1
        index = int(position) if positional else implicit
        if index < 1: raise ValueError('Invalid position')
        if index in result and result[index] != kind: raise ValueError('Conflicting argument types')
        result[index] = kind
    if '%' in value[cursor:]: raise ValueError('Unknown placeholder')
    return result


def units(localization):
    if set(localization) == {'stringUnit'}:
        return {'value': localization['stringUnit']}
    if set(localization) == {'variations'} and set(localization['variations']) == {'plural'}:
        return {k: v['stringUnit'] for k, v in localization['variations']['plural'].items()}
    raise ValueError('Unsupported catalog shape')


def validate_catalog(catalog):
    if catalog['sourceLanguage'] != 'en' or catalog['version'] != '1.0': raise ValueError('Unsupported catalog')
    for key, entry in catalog['strings'].items():
        expected = placeholders(key)
        localizations = entry.get('localizations', {})
        if 'en' not in localizations: raise ValueError('Missing English UI fallback: ' + key)
        is_plural = 'variations' in localizations['en']
        for locale, localization in localizations.items():
            if locale not in LANGUAGES: raise ValueError('Unsupported UI locale')
            values = units(localization)
            if is_plural != ('variations' in localization): raise ValueError('Plural shape mismatch')
            if is_plural and set(values) != PLURALS[locale]: raise ValueError('Missing/unknown plural category')
            for unit in values.values():
                if not isinstance(unit.get('value'), str) or not unit['value'].strip(): raise ValueError('Empty UI value')
                if placeholders(unit['value']) != expected: raise ValueError('Placeholder mismatch')
                if unit.get('state') not in {'translated', 'needs_review', 'new'}: raise ValueError('Unknown translation state')
    return True


def inventory():
    paths = sorted((ROOT / 'docs/content-authoring').glob('lesson-*.json'))
    paths += sorted((ROOT / 'docs/content-authoring/kanji').glob('*.json'))
    paths = [p for p in paths if not p.name.endswith('.schema.json')]
    paths += [ROOT / ('docs/content-authoring/' + name) for name in
              ('kana/inventory.json', 'sentence-bank/bank.json', 'sentence-bank/bound-contexts.json')]
    hashes = {}
    fields = []

    def visit(value, pointer, owner, path, domain):
        if is_translation(value):
            if any(not isinstance(v, str) for v in value.values()): raise ValueError('Non-string translation')
            present = sorted(k for k, v in value.items() if v.strip())
            # An entirely empty vocabulary usage note is deliberately absent copy,
            # not 19 missing translations. Retain it in the ledger for traceability.
            empty_optional = not present and bool(re.fullmatch(r'/vocabulary/\d+/usage', pointer))
            fields.append(dict(path=path, pointer=pointer, ownerID=owner, domain=domain,
                               present=present, emptyOptional=empty_optional))
        elif isinstance(value, dict):
            owner = value.get('id', value.get('key', owner))
            for key, child in value.items():
                visit(child, pointer + '/' + key.replace('~', '~0').replace('/', '~1'), owner, path, domain)
        elif isinstance(value, list):
            for i, child in enumerate(value): visit(child, pointer + '/' + str(i), owner, path, domain)

    documents = {str(path.relative_to(ROOT)): json.loads(path.read_bytes()) for path in paths}
    overlay_paths, overlays = load_overlays(ROOT)
    projected = apply_overlays(documents, overlays)
    for path in overlay_paths: hashes[str(path.relative_to(ROOT))] = hashlib.sha256(path.read_bytes()).hexdigest()
    for path in paths:
        relative = str(path.relative_to(ROOT))
        hashes[relative] = hashlib.sha256(path.read_bytes()).hexdigest()
        domain = ('kana' if '/kana/' in relative else 'candidates' if '/sentence-bank/' in relative else
                  'kanji' if '/kanji/' in relative else 'lessons')
        visit(projected[relative], '', None, relative, domain)
    catalog = json.loads((ROOT / CATALOG).read_bytes())
    validate_catalog(catalog)
    hashes[CATALOG] = hashlib.sha256((ROOT / CATALOG).read_bytes()).hexdigest()
    ui = {}
    for locale in LANGUAGES:
        present = sum(locale in s.get('localizations', {}) for s in catalog['strings'].values())
        ready = sum(locale in s.get('localizations', {}) and all(u['state'] == 'translated' for u in units(s['localizations'][locale]).values()) for s in catalog['strings'].values())
        ui[locale] = dict(total=len(catalog['strings']), present=present, catalogTranslatedState=ready,
                          englishFallback=len(catalog['strings']) - present, editorialApproval='not established by T09.01')
    content = {}
    for domain in ('lessons', 'kanji', 'kana', 'candidates'):
        subset = [f for f in fields if f['domain'] == domain and not f['emptyOptional']]
        empty_optional = sum(f['domain'] == domain and f['emptyOptional'] for f in fields)
        content[domain] = {locale: dict(total=len(subset), present=sum(locale in f['present'] for f in subset),
            englishFallback=sum(locale not in f['present'] and 'en' in f['present'] for f in subset),
            unavailable=sum(locale not in f['present'] and 'en' not in f['present'] for f in subset),
            emptyOptional=empty_optional) for locale in LANGUAGES}
    return dict(version=1, task='T09.01', scope='Field presence only; fallback is not translation coverage or linguistic approval. UI inventory covers implemented scaffold and reusable infrastructure, not future screens. Kana/candidate data remains authoring-only, outside T01 runtime.',
                inputHashes=hashes, languages=list(LANGUAGES), ui=ui, content=content, fields=fields,
                pendingOverlayFields={locale: sum(row['state'] == 'draft' for overlay in overlays if overlay['locale'] == locale for row in overlay['fields']) for locale in LANGUAGES})


def self_test():
    catalog = json.loads((ROOT / CATALOG).read_bytes())
    validate_catalog(catalog)
    rejected = 0
    mutations = [
        lambda c: c['strings']['nav.lessons']['localizations'].pop('en'),
        lambda c: c['strings']['results.count %lld']['localizations']['en']['variations']['plural'].pop('other'),
        lambda c: c['strings']['results.count %lld']['localizations']['en']['variations']['plural']['one']['stringUnit'].update(value='%@ result'),
        lambda c: c['strings']['nav.lessons']['localizations']['en']['stringUnit'].update(value=''),
        lambda c: c['strings']['nav.lessons']['localizations']['en']['stringUnit'].update(value='%n'),
        lambda c: c['strings']['nav.lessons']['localizations'].update(ja={'stringUnit': {'state':'translated','value':'X'}}),
        lambda c: c['strings']['results.count %lld']['localizations'].update(ar={'variations': {'plural': {'other': {'stringUnit': {'state':'translated','value':'%lld'}}}}}),
    ]
    for mutate in mutations:
        changed = copy.deepcopy(catalog)
        mutate(changed)
        try: validate_catalog(changed)
        except (ValueError, KeyError): rejected += 1
        else: raise AssertionError('Accepted invalid localization fixture')
    for locale in LANGUAGES:
        complete = copy.deepcopy(catalog)
        complete['strings']['results.count %lld']['localizations'][locale] = {'variations': {'plural': {
            category: {'stringUnit': {'state':'needs_review', 'value':'%1$lld fixture'}} for category in PLURALS[locale]}}}
        validate_catalog(complete)  # Synthetic category/type probes, never translation coverage.
    assert placeholders('%2$@ %1$lld %%') == placeholders('%lld %@')
    assert localized_text({'ar': ' ', 'en': 'E', 'vi': 'V'}, 'ar') == 'E'
    assert localized_text({'vi': 'V'}, 'he') is None
    assert text_fields({'meanings': {'en': 'E', 'vi': 'V'}}, 'ar') == ['E']
    assert text_fields({'meanings': {'en': 'E', 'ar': ' '}}, 'ar') == ['E']
    assert text_fields({'meanings': {'vi': 'V'}}, 'ar') == []
    assert text_fields({'meanings': {'en': 'E', 'ar': 'A'}}, 'ar') == ['A']
    base = {'source.json': {'id':'stable-owner', 'translation':{'en':'E','vi':'V'}, 'japanese':'日本語'}}
    row = dict(path='source.json', pointer='/translation', ownerID='stable-owner', sourceSha256=pin(base['source.json']),
               text='synthetic-ar', state='reviewed', reviewer='synthetic fixture', reviewSha256=None)
    row['reviewSha256'] = review_pin('ar', row)
    overlay = dict(version=1, locale='ar', fields=[row])
    assert apply_overlays(base, [overlay])['source.json']['translation']['ar'] == 'synthetic-ar'
    assert 'ar' not in base['source.json']['translation']
    draft = copy.deepcopy(overlay); draft['fields'][0]['state'] = 'draft'
    draft['fields'][0]['reviewSha256'] = None
    assert 'ar' not in apply_overlays(base, [draft])['source.json']['translation']
    rejected_overlays = 0
    for field, value in [('path','../escape'),('pointer','/japanese'),('ownerID','wrong'),('sourceSha256','0'*64),('text',' '),('reviewer',''),('state','approved'),('text','changed after review')]:
        invalid = copy.deepcopy(overlay); invalid['fields'][0][field] = value
        try: apply_overlays(base, [invalid])
        except ValueError: rejected_overlays += 1
        else: raise AssertionError('Accepted invalid locale sidecar')
    for invalid in [dict(overlay, locale='ja'), dict(overlay, locale='vi'), dict(overlay, fields=[row,row]), dict(overlay, version=True)]:
        try: apply_overlays(base, [invalid])
        except ValueError: rejected_overlays += 1
        else: raise AssertionError('Accepted invalid locale sidecar')
    no_english = copy.deepcopy(base); no_english['source.json']['translation']['en'] = ''
    invalid = copy.deepcopy(overlay); invalid['fields'][0]['sourceSha256'] = pin(no_english['source.json'])
    try: apply_overlays(no_english, [invalid])
    except ValueError: rejected_overlays += 1
    else: raise AssertionError('Accepted translation without English source')
    try: field_at({'rows':[{'translation':{'en':'E'}}]}, '/rows/-1/translation')
    except ValueError: rejected_overlays += 1
    else: raise AssertionError('Accepted negative array pointer')
    print(f'PASS locale sidecars: exact owner/revision; draft excluded; {rejected_overlays} invalid overlays rejected')
    print(f'PASS localization self-test: {rejected} invalid catalogs rejected; positional placeholders and exact/blank/missing/search fallback fixtures')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--self-test', action='store_true')
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument('--write', action='store_true')
    mode.add_argument('--check', action='store_true')
    args = parser.parse_args()
    if args.self_test: self_test()
    report = inventory()
    body = (json.dumps(report, ensure_ascii=False, indent=2) + '\n').encode()
    if args.write:
        REPORT.parent.mkdir(parents=True, exist_ok=True)
        REPORT.write_bytes(body)
    elif not REPORT.exists() or REPORT.read_bytes() != body:
        raise SystemExit('Stale localization inventory; review inputs and run --write')
    print(f"PASS localization inventory: {len(report['fields'])} fields / {len(LANGUAGES)} locales; {len(report['inputHashes'])} pinned inputs; UI fallback kept separate")


if __name__ == '__main__': main()
