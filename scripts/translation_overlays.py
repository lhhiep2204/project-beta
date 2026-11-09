"""Revision-bound locale sidecars. Do not mutate reviewed VI/EN authoring inputs."""
import copy
import hashlib
import json
from pathlib import Path
from localization_support import LANGUAGES, is_translation


def pin(value):
    return hashlib.sha256(json.dumps(value, ensure_ascii=False, sort_keys=True,
                                    separators=(',', ':')).encode()).hexdigest()


def review_pin(locale, row):
    """Bind a verdict to this exact translation, reviewer and source revision."""
    return pin(dict(locale=locale, field={k: v for k, v in row.items() if k != 'reviewSha256'}))


def field_at(document, pointer):
    if not isinstance(pointer, str) or not pointer.startswith('/'):
        raise ValueError('Invalid translated-field pointer')
    node = document
    owner = document
    for part in pointer[1:].split('/'):
        key = part.replace('~1', '/').replace('~0', '~')
        if isinstance(node, dict) and ('id' in node or 'key' in node): owner = node
        try:
            if isinstance(node, list):
                if not key.isascii() or not key.isdecimal() or (key != '0' and key.startswith('0')):
                    raise ValueError('Invalid array pointer')
                node = node[int(key)]
            else:
                node = node[key]
        except (KeyError, IndexError, TypeError, ValueError) as error:
            raise ValueError('Translation points to missing field') from error
    if not is_translation(node): raise ValueError('Translation target is not a localized field')
    return node, owner


def apply_overlays(documents, overlays):
    """Validate every row against immutable base data, then project reviewed rows only."""
    result = copy.deepcopy(documents)
    seen = set()
    for overlay in overlays:
        if set(overlay) != {'version', 'locale', 'fields'} or type(overlay['version']) is not int or overlay['version'] != 1:
            raise ValueError('Unsupported locale sidecar')
        locale = overlay['locale']
        if locale not in LANGUAGES or locale in ('en', 'vi'):
            raise ValueError('Sidecars target remaining locales only; VI/EN stays in canonical authoring')
        if not isinstance(overlay['fields'], list): raise ValueError('Invalid field inventory')
        for row in overlay['fields']:
            if set(row) != {'path', 'pointer', 'ownerID', 'sourceSha256', 'text', 'state', 'reviewer', 'reviewSha256'}:
                raise ValueError('Invalid translated-field record')
            if row['path'] not in documents: raise ValueError('Translation source outside the authored inventory')
            field, owner = field_at(documents[row['path']], row['pointer'])
            if not isinstance(field.get('en'), str) or not field['en'].strip():
                raise ValueError('Translation needs nonempty authored English source')
            if row['ownerID'] != owner.get('id', owner.get('key')) or row['sourceSha256'] != pin(owner):
                raise ValueError('Stale translated-field owner/revision')
            if not isinstance(row['text'], str) or not row['text'].strip(): raise ValueError('Empty translation')
            if row['state'] not in ('draft', 'reviewed') or not isinstance(row['reviewer'], str):
                raise ValueError('Invalid translation review state')
            if row['state'] == 'reviewed' and not row['reviewer'].strip(): raise ValueError('Missing translation reviewer')
            if row['state'] == 'reviewed' and row['reviewSha256'] != review_pin(locale, row):
                raise ValueError('Translation changed after recorded review')
            if row['state'] == 'draft' and row['reviewSha256'] is not None:
                raise ValueError('Draft cannot retain a review verdict')
            key = (locale, row['path'], row['pointer'])
            if key in seen: raise ValueError('Duplicate translated field')
            seen.add(key)
            if row['state'] == 'reviewed':
                projected, _ = field_at(result[row['path']], row['pointer'])
                projected[locale] = row['text']
    return result


def load_overlays(root):
    paths = sorted((root / 'docs/localization/content').glob('*.json'))
    overlays = [json.loads(path.read_bytes()) for path in paths]
    for path, overlay in zip(paths, overlays):
        if path.stem != overlay.get('locale'): raise ValueError('Locale/sidecar filename mismatch')
    return paths, overlays
