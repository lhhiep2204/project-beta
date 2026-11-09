"""Offline projection helpers; parity is exercised against the Swift runtime by T09.01."""
LANGUAGES = ('ar', 'bn', 'zh-Hans', 'nl', 'en', 'fr', 'de', 'he', 'hi', 'id', 'it', 'ko', 'pt', 'ru', 'es', 'th', 'tr', 'uk', 'vi')


def is_translation(value):
    return isinstance(value, dict) and bool(value) and set(value) <= set(LANGUAGES)


def localized_text(translations, locale):
    def available(key):
        value = translations.get(key)
        return value if isinstance(value, str) and value.strip() else None
    return available(locale) or available('en')
